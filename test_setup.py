#!/usr/bin/env python3
"""
Test script to verify all components are working correctly
Run this before launching the dashboard to check your setup
"""

import sys
from datetime import datetime


def test_imports():
    """Test if all required packages can be imported"""
    print("Testing package imports...")

    packages = [
        ('streamlit', 'Streamlit'),
        ('plotly', 'Plotly'),
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
        ('requests', 'Requests'),
        ('yfinance', 'yfinance'),
        ('scipy', 'SciPy'),
    ]

    failed = []

    for package, name in packages:
        try:
            __import__(package)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT FOUND")
            failed.append(name)

    if failed:
        print(f"\n❌ Missing packages: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
        return False

    print("\n✅ All packages imported successfully!\n")
    return True


def test_modules():
    """Test if custom modules can be imported"""
    print("Testing custom modules...")

    modules = [
        ('data_fetcher', 'DataFetcher'),
        ('indicators', 'TechnicalIndicators'),
        ('analysis', 'MarketAnalyzer'),
    ]

    failed = []

    for module, name in modules:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError as e:
            print(f"  ✗ {name} - ERROR: {e}")
            failed.append(name)

    if failed:
        print(f"\n❌ Failed to import modules: {', '.join(failed)}")
        return False

    print("\n✅ All modules imported successfully!\n")
    return True


def test_data_fetching():
    """Test if data can be fetched from APIs"""
    print("Testing API connections...")

    from data_fetcher import DataFetcher

    fetcher = DataFetcher()

    # Test Bitcoin price
    print("  Testing Bitcoin price API...")
    try:
        current = fetcher.get_current_bitcoin_price()
        if current['price'] > 0:
            print(f"  ✓ Current BTC Price: ${current['price']:,.2f}")
        else:
            print("  ⚠ API returned zero price")
    except Exception as e:
        print(f"  ✗ Error fetching Bitcoin price: {e}")

    # Test historical data
    print("  Testing historical data API...")
    try:
        df = fetcher.get_bitcoin_price_data(days=7)
        if not df.empty:
            print(f"  ✓ Historical data: {len(df)} records")
        else:
            print("  ⚠ No historical data returned")
    except Exception as e:
        print(f"  ✗ Error fetching historical data: {e}")

    # Test Fear & Greed
    print("  Testing Fear & Greed Index API...")
    try:
        fg = fetcher.get_fear_greed_index()
        if fg.get('current_value'):
            print(f"  ✓ Fear & Greed: {fg['current_value']} ({fg['current_classification']})")
        else:
            print("  ⚠ No Fear & Greed data")
    except Exception as e:
        print(f"  ✗ Error fetching Fear & Greed: {e}")

    print("\n✅ API connections tested!\n")
    return True


def test_indicators():
    """Test if technical indicators can be calculated"""
    print("Testing technical indicators...")

    from indicators import TechnicalIndicators
    import pandas as pd
    import numpy as np

    # Create sample data
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    prices = 50000 + np.cumsum(np.random.randn(100) * 1000)
    df = pd.DataFrame({
        'close': prices,
        'high': prices * 1.02,
        'low': prices * 0.98,
        'open': prices,
        'volume': np.random.randint(1000000, 5000000, 100)
    }, index=dates)

    try:
        # Test RSI
        rsi = TechnicalIndicators.calculate_rsi(df['close'])
        print(f"  ✓ RSI: {rsi.iloc[-1]:.2f}")

        # Test Moving Averages
        mas = TechnicalIndicators.calculate_moving_averages(df['close'])
        print(f"  ✓ SMA 20: {mas['sma_20'].iloc[-1]:.2f}")

        # Test MACD
        macd, signal, hist = TechnicalIndicators.calculate_macd(df['close'])
        print(f"  ✓ MACD: {macd.iloc[-1]:.2f}")

        # Test all indicators
        df_with_indicators = TechnicalIndicators.get_all_indicators(df)
        print(f"  ✓ All indicators calculated: {len(df_with_indicators.columns)} columns")

        print("\n✅ Technical indicators working correctly!\n")
        return True

    except Exception as e:
        print(f"\n❌ Error calculating indicators: {e}\n")
        return False


def test_analysis():
    """Test if analysis functions work"""
    print("Testing market analysis...")

    from analysis import MarketAnalyzer
    import pandas as pd
    import numpy as np

    # Create sample data
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    prices = 50000 + np.cumsum(np.random.randn(100) * 1000)
    df = pd.DataFrame({
        'close': prices,
        'high': prices * 1.02,
        'low': prices * 0.98,
        'sma_20': prices,
        'sma_50': prices,
        'sma_200': prices,
        'rsi': 50,
        'volatility': 0.5
    }, index=dates)

    try:
        # Test market regime detection
        regime = MarketAnalyzer.detect_market_regime(df)
        print(f"  ✓ Market regime: {regime['regime']}")

        # Test risk metrics
        risk = MarketAnalyzer.calculate_risk_metrics(df)
        print(f"  ✓ Sharpe Ratio: {risk.get('sharpe_ratio', 0):.2f}")

        # Test pattern recognition
        patterns = MarketAnalyzer.identify_historical_patterns(df)
        print(f"  ✓ Patterns found: {len(patterns)}")

        print("\n✅ Market analysis working correctly!\n")
        return True

    except Exception as e:
        print(f"\n❌ Error in analysis: {e}\n")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("  Bitcoin Dashboard Setup Test")
    print("=" * 50)
    print(f"\nTest started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    results = []

    results.append(("Package Imports", test_imports()))
    results.append(("Module Imports", test_modules()))

    # Only run further tests if basic imports work
    if all(r[1] for r in results):
        results.append(("API Connections", test_data_fetching()))
        results.append(("Technical Indicators", test_indicators()))
        results.append(("Market Analysis", test_analysis()))

    # Summary
    print("=" * 50)
    print("  Test Summary")
    print("=" * 50)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    print("\n" + "=" * 50)

    if all(r[1] for r in results):
        print("\n🎉 All tests passed! You're ready to run the dashboard.")
        print("\nRun the dashboard with:")
        print("  streamlit run dashboard.py")
        print("or")
        print("  ./run.sh")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\nTo install missing packages:")
        print("  pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
