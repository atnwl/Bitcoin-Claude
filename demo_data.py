"""
Demo Data Generator
Generates realistic mock data when APIs are unavailable
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict


class DemoDataGenerator:
    """Generates realistic demo data for testing without API access"""

    @staticmethod
    def generate_bitcoin_price_data(days: int = 365) -> pd.DataFrame:
        """
        Generate realistic Bitcoin price data

        Args:
            days: Number of days of historical data

        Returns:
            DataFrame with OHLCV data
        """
        # Start with a base price
        base_price = 45000

        # Generate dates
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')

        # Generate realistic price movement using random walk with drift
        np.random.seed(42)  # For reproducible demo data

        # Create price series with trend and volatility
        returns = np.random.normal(0.001, 0.02, len(dates))  # Daily returns
        prices = base_price * np.exp(np.cumsum(returns))

        # Add some realistic patterns
        # Add a bull run in the middle
        if days > 100:
            bull_start = len(prices) // 3
            bull_end = 2 * len(prices) // 3
            prices[bull_start:bull_end] *= np.linspace(1, 1.4, bull_end - bull_start)

        # Create OHLCV data
        df = pd.DataFrame({
            'timestamp': dates,
            'close': prices,
            'open': prices * (1 + np.random.uniform(-0.01, 0.01, len(prices))),
        })

        df['high'] = df[['open', 'close']].max(axis=1) * (1 + np.random.uniform(0, 0.02, len(df)))
        df['low'] = df[['open', 'close']].min(axis=1) * (1 - np.random.uniform(0, 0.02, len(df)))
        df['price'] = df['close']
        df['volume'] = np.random.uniform(20000000000, 40000000000, len(df))
        df['market_cap'] = df['price'] * 19500000  # Approximate BTC supply

        df.set_index('timestamp', inplace=True)

        return df

    @staticmethod
    def generate_current_bitcoin_price(df: pd.DataFrame = None) -> Dict:
        """
        Generate current Bitcoin price data

        Args:
            df: Optional DataFrame to extract current price from

        Returns:
            Dictionary with current price data
        """
        if df is not None and not df.empty:
            current_price = df['close'].iloc[-1]
            prev_price = df['close'].iloc[-2] if len(df) > 1 else current_price
            change_24h = ((current_price - prev_price) / prev_price) * 100

            return {
                'price': current_price,
                'change_24h': change_24h,
                'volume_24h': df['volume'].iloc[-1],
                'market_cap': df['market_cap'].iloc[-1]
            }

        return {
            'price': 47500.00,
            'change_24h': 2.34,
            'volume_24h': 28500000000,
            'market_cap': 925000000000
        }

    @staticmethod
    def generate_fear_greed_index() -> Dict:
        """
        Generate Fear & Greed Index data

        Returns:
            Dictionary with Fear & Greed data
        """
        # Generate realistic current value
        value = np.random.randint(30, 70)

        if value < 25:
            classification = 'Extreme Fear'
        elif value < 45:
            classification = 'Fear'
        elif value < 55:
            classification = 'Neutral'
        elif value < 75:
            classification = 'Greed'
        else:
            classification = 'Extreme Greed'

        # Generate historical data
        historical_dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        historical_values = np.random.randint(20, 80, 30)

        historical_df = pd.DataFrame({
            'timestamp': historical_dates,
            'value': historical_values,
            'classification': ['Neutral'] * 30  # Simplified
        })

        return {
            'current_value': value,
            'current_classification': classification,
            'timestamp': datetime.now(),
            'historical': historical_df
        }

    @staticmethod
    def generate_on_chain_metrics() -> Dict:
        """
        Generate on-chain metrics data

        Returns:
            Dictionary with on-chain metrics
        """
        metrics = {}

        # Hash rate data
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        timestamps = [int(d.timestamp()) for d in dates]
        hash_rates = np.random.uniform(600, 700, 30)  # EH/s

        metrics['hash_rate'] = {
            'current': hash_rates[-1],
            'unit': 'EH/s',
            'historical': pd.DataFrame({
                'x': timestamps,
                'y': hash_rates
            })
        }

        # Active addresses
        active_addrs = np.random.randint(800000, 1200000, 30)

        metrics['active_addresses'] = {
            'current': active_addrs[-1],
            'historical': pd.DataFrame({
                'x': timestamps,
                'y': active_addrs
            })
        }

        # Transactions
        transactions = np.random.randint(250000, 400000, 30)

        metrics['transactions'] = {
            'current': transactions[-1],
            'historical': pd.DataFrame({
                'x': timestamps,
                'y': transactions
            })
        }

        return metrics

    @staticmethod
    def generate_macro_indicators(days: int = 365) -> Dict[str, pd.DataFrame]:
        """
        Generate macro economic indicator data

        Args:
            days: Number of days of historical data

        Returns:
            Dictionary of DataFrames for each indicator
        """
        indicators = {}

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')

        # Dollar Index (typically 100-110)
        dxy = 105 + np.cumsum(np.random.normal(0, 0.3, len(dates)))
        indicators['dollar_index'] = pd.DataFrame({
            'close': dxy
        }, index=dates)

        # Gold (typically 1800-2100)
        gold = 1950 + np.cumsum(np.random.normal(0, 15, len(dates)))
        indicators['gold'] = pd.DataFrame({
            'close': gold
        }, index=dates)

        # S&P 500 (typically 4000-5000)
        sp500 = 4500 + np.cumsum(np.random.normal(2, 25, len(dates)))
        indicators['sp500'] = pd.DataFrame({
            'close': sp500
        }, index=dates)

        # VIX (typically 12-30)
        vix = 20 + np.cumsum(np.random.normal(0, 1, len(dates)))
        vix = np.clip(vix, 10, 40)
        indicators['vix'] = pd.DataFrame({
            'close': vix
        }, index=dates)

        # 10-Year Treasury (typically 3-5%)
        treasury = 4 + np.cumsum(np.random.normal(0, 0.05, len(dates)))
        indicators['treasury_10y'] = pd.DataFrame({
            'close': treasury
        }, index=dates)

        return indicators
