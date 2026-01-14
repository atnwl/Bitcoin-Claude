"""
Market Analysis Module
Performs correlation analysis, pattern recognition, and generates insights
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from scipy import stats
from datetime import datetime, timedelta


class MarketAnalyzer:
    """Analyzes Bitcoin market conditions and correlations"""

    @staticmethod
    def calculate_correlation(btc_data: pd.Series, macro_data: pd.Series) -> float:
        """
        Calculate correlation between Bitcoin and macro indicator

        Args:
            btc_data: Bitcoin price series
            macro_data: Macro indicator series

        Returns:
            Correlation coefficient
        """
        # Align the data by index
        combined = pd.concat([btc_data, macro_data], axis=1, join='inner')
        combined.columns = ['btc', 'macro']
        combined.dropna(inplace=True)

        if len(combined) < 2:
            return 0.0

        correlation, _ = stats.pearsonr(combined['btc'], combined['macro'])
        return correlation

    @staticmethod
    def analyze_macro_correlations(btc_df: pd.DataFrame, macro_indicators: Dict[str, pd.DataFrame]) -> Dict[str, float]:
        """
        Analyze correlations between Bitcoin and macro indicators

        Args:
            btc_df: Bitcoin price DataFrame
            macro_indicators: Dictionary of macro indicator DataFrames

        Returns:
            Dictionary of correlation coefficients
        """
        correlations = {}

        for name, indicator_df in macro_indicators.items():
            if indicator_df.empty or btc_df.empty:
                continue

            try:
                correlation = MarketAnalyzer.calculate_correlation(
                    btc_df['close'],
                    indicator_df['close']
                )
                correlations[name] = correlation
            except Exception as e:
                print(f"Error calculating correlation for {name}: {e}")
                correlations[name] = 0.0

        return correlations

    @staticmethod
    def detect_market_regime(df: pd.DataFrame) -> Dict[str, str]:
        """
        Detect current market regime (Bull, Bear, Sideways)

        Args:
            df: Bitcoin price DataFrame with indicators

        Returns:
            Dictionary with regime information
        """
        if df.empty or len(df) < 50:
            return {'regime': 'Unknown', 'confidence': 'Low'}

        recent_data = df.tail(50)
        current_price = df['close'].iloc[-1]

        # Calculate price change over different periods
        change_7d = ((current_price - df['close'].iloc[-7]) / df['close'].iloc[-7]) * 100 if len(df) >= 7 else 0
        change_30d = ((current_price - df['close'].iloc[-30]) / df['close'].iloc[-30]) * 100 if len(df) >= 30 else 0

        # Check moving average alignment
        sma_20 = df['sma_20'].iloc[-1] if 'sma_20' in df.columns else current_price
        sma_50 = df['sma_50'].iloc[-1] if 'sma_50' in df.columns else current_price
        sma_200 = df['sma_200'].iloc[-1] if 'sma_200' in df.columns else current_price

        # Determine regime
        if current_price > sma_20 > sma_50 > sma_200 and change_30d > 10:
            regime = 'Strong Bull Market'
            confidence = 'High'
        elif current_price > sma_50 and change_30d > 5:
            regime = 'Bull Market'
            confidence = 'Medium'
        elif current_price < sma_20 < sma_50 < sma_200 and change_30d < -10:
            regime = 'Strong Bear Market'
            confidence = 'High'
        elif current_price < sma_50 and change_30d < -5:
            regime = 'Bear Market'
            confidence = 'Medium'
        elif abs(change_30d) < 5:
            regime = 'Sideways/Consolidation'
            confidence = 'Medium'
        else:
            regime = 'Transitional'
            confidence = 'Low'

        return {
            'regime': regime,
            'confidence': confidence,
            'change_7d': change_7d,
            'change_30d': change_30d
        }

    @staticmethod
    def identify_historical_patterns(df: pd.DataFrame) -> List[Dict]:
        """
        Identify similar historical patterns to current market conditions

        Args:
            df: Bitcoin price DataFrame

        Returns:
            List of similar historical periods
        """
        if df.empty or len(df) < 100:
            return []

        patterns = []

        # Get current conditions (last 30 days)
        current_window = 30
        current_data = df['close'].tail(current_window)
        current_returns = current_data.pct_change().dropna()

        # Calculate current pattern characteristics
        current_volatility = current_returns.std()
        current_trend = (current_data.iloc[-1] - current_data.iloc[0]) / current_data.iloc[0]

        # Search for similar patterns in history (at least 90 days ago to avoid recent data)
        search_start = len(df) - 90
        window_size = current_window

        for i in range(window_size, search_start, 5):  # Step by 5 for efficiency
            historical_data = df['close'].iloc[i-window_size:i]
            historical_returns = historical_data.pct_change().dropna()

            if len(historical_returns) < 5:
                continue

            # Calculate historical pattern characteristics
            hist_volatility = historical_returns.std()
            hist_trend = (historical_data.iloc[-1] - historical_data.iloc[0]) / historical_data.iloc[0]

            # Calculate similarity score
            vol_diff = abs(current_volatility - hist_volatility) / max(current_volatility, hist_volatility, 0.01)
            trend_diff = abs(current_trend - hist_trend)

            similarity = 1 / (1 + vol_diff + trend_diff)

            # If similarity is high, record the pattern and what happened next
            if similarity > 0.7:
                # Look at what happened in the next 30 days after the historical pattern
                if i + 30 < len(df):
                    future_price = df['close'].iloc[i + 30]
                    pattern_price = df['close'].iloc[i]
                    future_return = ((future_price - pattern_price) / pattern_price) * 100

                    patterns.append({
                        'date': df.index[i],
                        'similarity': similarity,
                        'subsequent_return_30d': future_return,
                        'pattern_start': df.index[i - window_size],
                        'pattern_end': df.index[i]
                    })

        # Sort by similarity and return top 5
        patterns.sort(key=lambda x: x['similarity'], reverse=True)
        return patterns[:5]

    @staticmethod
    def calculate_risk_metrics(df: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate various risk metrics

        Args:
            df: Bitcoin price DataFrame

        Returns:
            Dictionary of risk metrics
        """
        if df.empty:
            return {}

        returns = df['close'].pct_change().dropna()

        # Sharpe Ratio (assuming 0% risk-free rate for simplicity)
        sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(365) if returns.std() != 0 else 0

        # Maximum Drawdown
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()

        # Value at Risk (VaR) - 95% confidence
        var_95 = returns.quantile(0.05)

        # Sortino Ratio (only downside deviation)
        downside_returns = returns[returns < 0]
        sortino_ratio = (returns.mean() / downside_returns.std()) * np.sqrt(365) if len(downside_returns) > 0 and downside_returns.std() != 0 else 0

        return {
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown * 100,  # Convert to percentage
            'var_95': var_95 * 100,  # Convert to percentage
            'sortino_ratio': sortino_ratio,
            'avg_daily_return': returns.mean() * 100,
            'daily_volatility': returns.std() * 100
        }

    @staticmethod
    def generate_market_analysis(
        btc_df: pd.DataFrame,
        macro_correlations: Dict[str, float],
        fear_greed: Dict,
        on_chain: Dict
    ) -> str:
        """
        Generate comprehensive market analysis text

        Args:
            btc_df: Bitcoin price DataFrame with indicators
            macro_correlations: Dictionary of correlation coefficients
            fear_greed: Fear & Greed Index data
            on_chain: On-chain metrics data

        Returns:
            Analysis text
        """
        analysis_parts = []

        # Current Price Analysis
        if not btc_df.empty:
            current_price = btc_df['close'].iloc[-1]
            change_24h = ((btc_df['close'].iloc[-1] - btc_df['close'].iloc[-2]) / btc_df['close'].iloc[-2] * 100) if len(btc_df) > 1 else 0

            analysis_parts.append(f"**Current Bitcoin Price: ${current_price:,.2f}** ({change_24h:+.2f}% 24h)")
            analysis_parts.append("")

        # Market Regime
        regime_info = MarketAnalyzer.detect_market_regime(btc_df)
        analysis_parts.append(f"**Market Regime:** {regime_info['regime']} (Confidence: {regime_info['confidence']})")
        analysis_parts.append(f"- 7-day change: {regime_info.get('change_7d', 0):+.2f}%")
        analysis_parts.append(f"- 30-day change: {regime_info.get('change_30d', 0):+.2f}%")
        analysis_parts.append("")

        # Technical Indicators Summary
        if 'rsi' in btc_df.columns:
            rsi = btc_df['rsi'].iloc[-1]
            analysis_parts.append(f"**Technical Indicators:**")
            analysis_parts.append(f"- RSI (14): {rsi:.1f} - {'Oversold' if rsi < 30 else 'Overbought' if rsi > 70 else 'Neutral'}")

        if 'volatility' in btc_df.columns:
            vol = btc_df['volatility'].iloc[-1]
            analysis_parts.append(f"- Annualized Volatility: {vol*100:.1f}%")

        analysis_parts.append("")

        # Fear & Greed Index
        if fear_greed:
            fg_value = fear_greed.get('current_value', 50)
            fg_class = fear_greed.get('current_classification', 'Neutral')
            analysis_parts.append(f"**Fear & Greed Index:** {fg_value}/100 ({fg_class})")
            if fg_value < 25:
                analysis_parts.append("- Extreme fear often presents buying opportunities")
            elif fg_value > 75:
                analysis_parts.append("- Extreme greed may indicate overheated market")
            analysis_parts.append("")

        # Macro Correlations
        if macro_correlations:
            analysis_parts.append("**Macro Correlations:**")
            for name, corr in sorted(macro_correlations.items(), key=lambda x: abs(x[1]), reverse=True):
                display_name = name.replace('_', ' ').title()
                strength = 'Strong' if abs(corr) > 0.7 else 'Moderate' if abs(corr) > 0.4 else 'Weak'
                direction = 'positive' if corr > 0 else 'negative'
                analysis_parts.append(f"- {display_name}: {corr:.2f} ({strength} {direction})")
            analysis_parts.append("")

        # On-Chain Metrics
        if on_chain:
            analysis_parts.append("**On-Chain Activity:**")
            if 'hash_rate' in on_chain:
                hr = on_chain['hash_rate']['current']
                analysis_parts.append(f"- Hash Rate: {hr:.0f} {on_chain['hash_rate']['unit']}")
            if 'active_addresses' in on_chain:
                aa = on_chain['active_addresses']['current']
                analysis_parts.append(f"- Active Addresses: {aa:,.0f}")
            if 'transactions' in on_chain:
                tx = on_chain['transactions']['current']
                analysis_parts.append(f"- Daily Transactions: {tx:,.0f}")
            analysis_parts.append("")

        # Historical Patterns
        patterns = MarketAnalyzer.identify_historical_patterns(btc_df)
        if patterns:
            analysis_parts.append("**Similar Historical Patterns:**")
            for i, pattern in enumerate(patterns[:3], 1):
                date = pattern['date'].strftime('%Y-%m-%d') if hasattr(pattern['date'], 'strftime') else str(pattern['date'])
                ret = pattern['subsequent_return_30d']
                analysis_parts.append(
                    f"{i}. Pattern from {date}: "
                    f"Subsequent 30-day return was {ret:+.1f}%"
                )
            analysis_parts.append("")

        # Risk Metrics
        risk_metrics = MarketAnalyzer.calculate_risk_metrics(btc_df)
        if risk_metrics:
            analysis_parts.append("**Risk Metrics:**")
            analysis_parts.append(f"- Sharpe Ratio: {risk_metrics.get('sharpe_ratio', 0):.2f}")
            analysis_parts.append(f"- Maximum Drawdown: {risk_metrics.get('max_drawdown', 0):.1f}%")
            analysis_parts.append(f"- 95% VaR (Daily): {risk_metrics.get('var_95', 0):.2f}%")
            analysis_parts.append("")

        # Overall Assessment
        analysis_parts.append("**Overall Assessment:**")

        # Combine multiple factors for assessment
        bullish_signals = 0
        bearish_signals = 0

        if not btc_df.empty and 'rsi' in btc_df.columns:
            if btc_df['rsi'].iloc[-1] < 30:
                bullish_signals += 1
            elif btc_df['rsi'].iloc[-1] > 70:
                bearish_signals += 1

        if regime_info['regime'] in ['Strong Bull Market', 'Bull Market']:
            bullish_signals += 2
        elif regime_info['regime'] in ['Strong Bear Market', 'Bear Market']:
            bearish_signals += 2

        if fear_greed and fear_greed.get('current_value', 50) < 25:
            bullish_signals += 1
        elif fear_greed and fear_greed.get('current_value', 50) > 75:
            bearish_signals += 1

        if bullish_signals > bearish_signals + 1:
            analysis_parts.append("The current market conditions show bullish tendencies. "
                                 "Multiple indicators suggest potential upside opportunity, though risk management remains crucial.")
        elif bearish_signals > bullish_signals + 1:
            analysis_parts.append("The current market shows bearish tendencies. "
                                 "Caution is advised with defensive positioning potentially appropriate.")
        else:
            analysis_parts.append("The market is showing mixed signals with no clear directional bias. "
                                 "This consolidation phase may precede a significant move in either direction.")

        return "\n".join(analysis_parts)
