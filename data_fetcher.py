"""
Data Fetcher Module
Handles all API calls for Bitcoin price, macro indicators, and on-chain metrics
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import time

# Try to import yfinance, but make it optional
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("Warning: yfinance not available. Macro indicators will be disabled.")

# Import demo data generator
from demo_data import DemoDataGenerator


class DataFetcher:
    """Fetches cryptocurrency and macro economic data from various sources"""

    def __init__(self, demo_mode: bool = False):
        self.coingecko_base = "https://api.coingecko.com/api/v3"
        self.fear_greed_api = "https://api.alternative.me/fng/"
        self.demo_mode = demo_mode
        self.api_failed = False  # Track if APIs are failing

    def get_bitcoin_price_data(self, days: int = 365) -> pd.DataFrame:
        """
        Fetch Bitcoin price data from CoinGecko

        Args:
            days: Number of days of historical data (max 365 for free tier)

        Returns:
            DataFrame with OHLCV data
        """
        # Use demo data if in demo mode or if APIs have failed
        if self.demo_mode or self.api_failed:
            print(f"📊 Using demo data (demo_mode={self.demo_mode}, api_failed={self.api_failed})")
            return DemoDataGenerator.generate_bitcoin_price_data(days)

        try:
            url = f"{self.coingecko_base}/coins/bitcoin/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'daily' if days > 90 else 'hourly'
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Create DataFrame
            df = pd.DataFrame({
                'timestamp': [x[0] for x in data['prices']],
                'price': [x[1] for x in data['prices']],
                'volume': [x[1] for x in data['total_volumes']],
                'market_cap': [x[1] for x in data['market_caps']]
            })

            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)

            # For OHLC, we'll approximate using the price data
            df['open'] = df['price']
            df['high'] = df['price'] * 1.02  # Approximate
            df['low'] = df['price'] * 0.98   # Approximate
            df['close'] = df['price']

            return df

        except Exception as e:
            print(f"⚠️  Error fetching Bitcoin data from API: {e}")
            print("🔄 Switching to demo mode...")
            self.api_failed = True  # Switch to demo mode for subsequent calls
            return DemoDataGenerator.generate_bitcoin_price_data(days)

    def get_current_bitcoin_price(self) -> Dict:
        """
        Get current Bitcoin price and 24h statistics

        Returns:
            Dictionary with current price data
        """
        if self.demo_mode or self.api_failed:
            return DemoDataGenerator.generate_current_bitcoin_price()

        try:
            url = f"{self.coingecko_base}/simple/price"
            params = {
                'ids': 'bitcoin',
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_24hr_vol': 'true',
                'include_market_cap': 'true'
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()['bitcoin']

            return {
                'price': data['usd'],
                'change_24h': data.get('usd_24h_change', 0),
                'volume_24h': data.get('usd_24h_vol', 0),
                'market_cap': data.get('usd_market_cap', 0)
            }

        except Exception as e:
            print(f"⚠️  Error fetching current Bitcoin price: {e}")
            self.api_failed = True
            return DemoDataGenerator.generate_current_bitcoin_price()

    def get_fear_greed_index(self) -> Dict:
        """
        Fetch Fear & Greed Index from Alternative.me

        Returns:
            Dictionary with Fear & Greed data
        """
        if self.demo_mode or self.api_failed:
            return DemoDataGenerator.generate_fear_greed_index()

        try:
            response = requests.get(self.fear_greed_api, params={'limit': 30}, timeout=10)
            response.raise_for_status()
            data = response.json()

            current = data['data'][0]
            historical = data['data']

            return {
                'current_value': int(current['value']),
                'current_classification': current['value_classification'],
                'timestamp': datetime.fromtimestamp(int(current['timestamp'])),
                'historical': pd.DataFrame([{
                    'timestamp': datetime.fromtimestamp(int(d['timestamp'])),
                    'value': int(d['value']),
                    'classification': d['value_classification']
                } for d in historical])
            }

        except Exception as e:
            print(f"⚠️  Error fetching Fear & Greed Index: {e}")
            self.api_failed = True
            return DemoDataGenerator.generate_fear_greed_index()

    def get_on_chain_metrics(self) -> Dict:
        """
        Fetch on-chain metrics from blockchain.com API

        Returns:
            Dictionary with on-chain metrics
        """
        if self.demo_mode or self.api_failed:
            return DemoDataGenerator.generate_on_chain_metrics()

        metrics = {}

        try:
            # Hash rate
            url = "https://api.blockchain.info/charts/hash-rate"
            params = {'timespan': '30days', 'format': 'json'}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            hash_data = response.json()

            if hash_data['values']:
                metrics['hash_rate'] = {
                    'current': hash_data['values'][-1]['y'],
                    'unit': hash_data['unit'],
                    'historical': pd.DataFrame(hash_data['values'])
                }

            time.sleep(0.5)  # Rate limiting

            # Active addresses
            url = "https://api.blockchain.info/charts/n-unique-addresses"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            addr_data = response.json()

            if addr_data['values']:
                metrics['active_addresses'] = {
                    'current': addr_data['values'][-1]['y'],
                    'historical': pd.DataFrame(addr_data['values'])
                }

            time.sleep(0.5)

            # Transaction count
            url = "https://api.blockchain.info/charts/n-transactions"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            tx_data = response.json()

            if tx_data['values']:
                metrics['transactions'] = {
                    'current': tx_data['values'][-1]['y'],
                    'historical': pd.DataFrame(tx_data['values'])
                }

        except Exception as e:
            print(f"⚠️  Error fetching on-chain metrics: {e}")
            self.api_failed = True
            return DemoDataGenerator.generate_on_chain_metrics()

        return metrics if metrics else DemoDataGenerator.generate_on_chain_metrics()

    def get_macro_indicators(self, days: int = 365) -> Dict[str, pd.DataFrame]:
        """
        Fetch macro economic indicators using yfinance

        Args:
            days: Number of days of historical data

        Returns:
            Dictionary of DataFrames for each indicator
        """
        if self.demo_mode or self.api_failed:
            return DemoDataGenerator.generate_macro_indicators(days)

        if not YFINANCE_AVAILABLE:
            return DemoDataGenerator.generate_macro_indicators(days)

        indicators = {}
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Tickers to fetch
        tickers = {
            'DX-Y.NYB': 'dollar_index',  # US Dollar Index
            'GC=F': 'gold',                # Gold Futures
            '^GSPC': 'sp500',              # S&P 500
            '^VIX': 'vix',                 # Volatility Index
            '^TNX': 'treasury_10y'         # 10-Year Treasury
        }

        for ticker, name in tickers.items():
            try:
                data = yf.download(
                    ticker,
                    start=start_date,
                    end=end_date,
                    progress=False
                )

                if not data.empty:
                    indicators[name] = data['Close'].to_frame('close')

                time.sleep(0.3)  # Rate limiting

            except Exception as e:
                print(f"Error fetching {name}: {e}")
                continue

        return indicators

    def _get_fallback_btc_data(self, days: int) -> pd.DataFrame:
        """
        Fallback method using yfinance if CoinGecko fails

        Args:
            days: Number of days of historical data

        Returns:
            DataFrame with OHLCV data
        """
        if not YFINANCE_AVAILABLE:
            print("yfinance not available for fallback")
            return pd.DataFrame(columns=['open', 'high', 'low', 'close', 'price', 'volume'])

        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            data = yf.download(
                'BTC-USD',
                start=start_date,
                end=end_date,
                progress=False
            )

            if not data.empty:
                df = pd.DataFrame({
                    'open': data['Open'],
                    'high': data['High'],
                    'low': data['Low'],
                    'close': data['Close'],
                    'price': data['Close'],
                    'volume': data['Volume']
                })
                return df

        except Exception as e:
            print(f"Fallback data fetch also failed: {e}")

        # Return empty DataFrame with correct structure
        return pd.DataFrame(columns=['open', 'high', 'low', 'close', 'price', 'volume'])
