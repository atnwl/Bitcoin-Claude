"""
Technical Indicators Module
Calculates RSI, moving averages, volatility, and other technical indicators
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict


class TechnicalIndicators:
    """Calculate various technical indicators for cryptocurrency analysis"""

    @staticmethod
    def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI)

        Args:
            data: Price series
            period: RSI period (default 14)

        Returns:
            RSI series
        """
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    @staticmethod
    def calculate_moving_averages(data: pd.Series) -> Dict[str, pd.Series]:
        """
        Calculate multiple moving averages

        Args:
            data: Price series

        Returns:
            Dictionary of moving averages
        """
        return {
            'sma_20': data.rolling(window=20).mean(),
            'sma_50': data.rolling(window=50).mean(),
            'sma_200': data.rolling(window=200).mean(),
            'ema_12': data.ewm(span=12, adjust=False).mean(),
            'ema_26': data.ewm(span=26, adjust=False).mean(),
            'ema_50': data.ewm(span=50, adjust=False).mean()
        }

    @staticmethod
    def calculate_macd(data: pd.Series) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate MACD (Moving Average Convergence Divergence)

        Args:
            data: Price series

        Returns:
            Tuple of (MACD line, Signal line, Histogram)
        """
        ema_12 = data.ewm(span=12, adjust=False).mean()
        ema_26 = data.ewm(span=26, adjust=False).mean()

        macd_line = ema_12 - ema_26
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        histogram = macd_line - signal_line

        return macd_line, signal_line, histogram

    @staticmethod
    def calculate_bollinger_bands(data: pd.Series, period: int = 20, std_dev: int = 2) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate Bollinger Bands

        Args:
            data: Price series
            period: Moving average period (default 20)
            std_dev: Standard deviation multiplier (default 2)

        Returns:
            Tuple of (Upper band, Middle band, Lower band)
        """
        middle_band = data.rolling(window=period).mean()
        std = data.rolling(window=period).std()

        upper_band = middle_band + (std * std_dev)
        lower_band = middle_band - (std * std_dev)

        return upper_band, middle_band, lower_band

    @staticmethod
    def calculate_volatility(data: pd.Series, period: int = 30) -> pd.Series:
        """
        Calculate historical volatility (annualized)

        Args:
            data: Price series
            period: Rolling window period

        Returns:
            Volatility series
        """
        returns = data.pct_change()
        volatility = returns.rolling(window=period).std() * np.sqrt(365)

        return volatility

    @staticmethod
    def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Average True Range (ATR)

        Args:
            high: High price series
            low: Low price series
            close: Close price series
            period: ATR period

        Returns:
            ATR series
        """
        high_low = high - low
        high_close = np.abs(high - close.shift())
        low_close = np.abs(low - close.shift())

        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)

        atr = true_range.rolling(window=period).mean()

        return atr

    @staticmethod
    def calculate_support_resistance(data: pd.Series, window: int = 20) -> Tuple[float, float]:
        """
        Calculate support and resistance levels

        Args:
            data: Price series
            window: Lookback window

        Returns:
            Tuple of (support level, resistance level)
        """
        recent_data = data.tail(window)

        support = recent_data.min()
        resistance = recent_data.max()

        return support, resistance

    @staticmethod
    def detect_golden_death_cross(data: pd.Series) -> Dict[str, bool]:
        """
        Detect Golden Cross and Death Cross patterns

        Args:
            data: Price series

        Returns:
            Dictionary with cross detection results
        """
        sma_50 = data.rolling(window=50).mean()
        sma_200 = data.rolling(window=200).mean()

        # Check last 5 days for crosses
        if len(sma_50) < 5 or len(sma_200) < 5:
            return {'golden_cross': False, 'death_cross': False}

        # Golden Cross: 50 SMA crosses above 200 SMA
        golden_cross = (
            sma_50.iloc[-1] > sma_200.iloc[-1] and
            sma_50.iloc[-2] <= sma_200.iloc[-2]
        )

        # Death Cross: 50 SMA crosses below 200 SMA
        death_cross = (
            sma_50.iloc[-1] < sma_200.iloc[-1] and
            sma_50.iloc[-2] >= sma_200.iloc[-2]
        )

        return {
            'golden_cross': golden_cross,
            'death_cross': death_cross,
            'sma_50_above_200': sma_50.iloc[-1] > sma_200.iloc[-1]
        }

    @staticmethod
    def calculate_momentum(data: pd.Series, period: int = 10) -> pd.Series:
        """
        Calculate price momentum

        Args:
            data: Price series
            period: Momentum period

        Returns:
            Momentum series
        """
        return data.diff(period)

    @staticmethod
    def calculate_rate_of_change(data: pd.Series, period: int = 9) -> pd.Series:
        """
        Calculate Rate of Change (ROC)

        Args:
            data: Price series
            period: ROC period

        Returns:
            ROC series
        """
        roc = ((data - data.shift(period)) / data.shift(period)) * 100
        return roc

    @staticmethod
    def get_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate all technical indicators for a dataframe

        Args:
            df: DataFrame with OHLCV data

        Returns:
            DataFrame with all indicators added
        """
        result = df.copy()

        # RSI
        result['rsi'] = TechnicalIndicators.calculate_rsi(result['close'])

        # Moving Averages
        mas = TechnicalIndicators.calculate_moving_averages(result['close'])
        for name, values in mas.items():
            result[name] = values

        # MACD
        macd, signal, hist = TechnicalIndicators.calculate_macd(result['close'])
        result['macd'] = macd
        result['macd_signal'] = signal
        result['macd_histogram'] = hist

        # Bollinger Bands
        bb_upper, bb_middle, bb_lower = TechnicalIndicators.calculate_bollinger_bands(result['close'])
        result['bb_upper'] = bb_upper
        result['bb_middle'] = bb_middle
        result['bb_lower'] = bb_lower

        # Volatility
        result['volatility'] = TechnicalIndicators.calculate_volatility(result['close'])

        # ATR (if we have high/low data)
        if 'high' in result.columns and 'low' in result.columns:
            result['atr'] = TechnicalIndicators.calculate_atr(
                result['high'], result['low'], result['close']
            )

        # Momentum indicators
        result['momentum'] = TechnicalIndicators.calculate_momentum(result['close'])
        result['roc'] = TechnicalIndicators.calculate_rate_of_change(result['close'])

        return result

    @staticmethod
    def get_current_signal(df: pd.DataFrame) -> Dict[str, str]:
        """
        Get current trading signals based on indicators

        Args:
            df: DataFrame with indicators

        Returns:
            Dictionary of signals
        """
        signals = {}

        if df.empty or len(df) < 2:
            return signals

        latest = df.iloc[-1]

        # RSI Signal
        if 'rsi' in df.columns and pd.notna(latest['rsi']):
            if latest['rsi'] < 30:
                signals['rsi'] = 'Oversold (Bullish)'
            elif latest['rsi'] > 70:
                signals['rsi'] = 'Overbought (Bearish)'
            else:
                signals['rsi'] = 'Neutral'

        # Moving Average Signal
        if 'sma_50' in df.columns and 'sma_200' in df.columns:
            if pd.notna(latest['sma_50']) and pd.notna(latest['sma_200']):
                if latest['sma_50'] > latest['sma_200']:
                    signals['ma_trend'] = 'Bullish (Golden Zone)'
                else:
                    signals['ma_trend'] = 'Bearish (Death Zone)'

        # MACD Signal
        if 'macd' in df.columns and 'macd_signal' in df.columns:
            if pd.notna(latest['macd']) and pd.notna(latest['macd_signal']):
                if latest['macd'] > latest['macd_signal']:
                    signals['macd'] = 'Bullish'
                else:
                    signals['macd'] = 'Bearish'

        # Bollinger Bands Signal
        if all(col in df.columns for col in ['bb_upper', 'bb_lower', 'close']):
            if pd.notna(latest['bb_upper']) and pd.notna(latest['bb_lower']):
                if latest['close'] > latest['bb_upper']:
                    signals['bollinger'] = 'Overbought'
                elif latest['close'] < latest['bb_lower']:
                    signals['bollinger'] = 'Oversold'
                else:
                    signals['bollinger'] = 'Normal'

        # Volatility Signal
        if 'volatility' in df.columns and pd.notna(latest['volatility']):
            if latest['volatility'] > 1.0:
                signals['volatility'] = 'High'
            elif latest['volatility'] > 0.5:
                signals['volatility'] = 'Moderate'
            else:
                signals['volatility'] = 'Low'

        return signals
