# ₿ Bitcoin Market Analysis Dashboard

A comprehensive, interactive Bitcoin market analysis dashboard built with Python, Streamlit, and Plotly. This dashboard provides real-time price data, technical indicators, macro correlations, on-chain metrics, and AI-powered market analysis.

![Bitcoin Dashboard](https://img.shields.io/badge/Bitcoin-Dashboard-orange?style=for-the-badge&logo=bitcoin)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red?style=for-the-badge&logo=streamlit)

## Features

### 📊 Live Data & Price Charts
- Real-time Bitcoin price from CoinGecko API
- Historical price data (7 days to 1 year)
- Interactive candlestick charts with zoom and pan
- 24-hour price change and volume statistics

### 📈 Technical Indicators
- **RSI (Relative Strength Index)** - Momentum oscillator
- **Moving Averages** - SMA 20/50/200, EMA 12/26/50
- **MACD** - Moving Average Convergence Divergence
- **Bollinger Bands** - Volatility and price envelope
- **Volatility Analysis** - Annualized volatility metrics
- **ATR** - Average True Range for volatility measurement

### 🌍 Macro Economic Correlations
- US Dollar Index (DXY)
- Gold Futures (GC=F)
- S&P 500 Index (^GSPC)
- VIX (Volatility Index)
- 10-Year Treasury Yield (^TNX)
- Real-time correlation coefficients

### 😱 Sentiment Analysis
- Fear & Greed Index from Alternative.me
- Historical sentiment trends
- Visual gauge with color-coded zones

### ⛓️ On-Chain Metrics
- Network Hash Rate
- Active Addresses
- Daily Transaction Count
- 30-day historical trends

### 🔍 Market Analysis
- Automated market regime detection (Bull/Bear/Sideways)
- Historical pattern recognition
- Risk metrics (Sharpe Ratio, Max Drawdown, VaR)
- AI-generated market insights
- Similar pattern identification with outcome analysis

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone or download this repository**
   ```bash
   cd Bitcoin-Claude
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install streamlit plotly pandas numpy requests yfinance ta scipy python-dateutil
   ```

## Usage

### Running the Dashboard

**Option 1: Using the run script**
```bash
chmod +x run.sh
./run.sh
```

**Option 2: Direct command**
```bash
streamlit run dashboard.py
```

The dashboard will automatically open in your default web browser at `http://localhost:8501`

### Dashboard Controls

- **Time Period Selector**: Choose from 7 days to 1 year of historical data
- **Auto Refresh**: Enable automatic data refresh every minute
- **Refresh Button**: Manually refresh all data
- **Interactive Charts**:
  - Zoom in/out with scroll or box selection
  - Pan by clicking and dragging
  - Toggle indicators on/off by clicking legend items
  - Hover for detailed information

## Project Structure

```
Bitcoin-Claude/
│
├── dashboard.py          # Main Streamlit application
├── data_fetcher.py       # API data retrieval module
├── indicators.py         # Technical indicator calculations
├── analysis.py           # Market analysis and pattern recognition
├── requirements.txt      # Python dependencies
├── run.sh               # Launch script
└── README.md            # This file
```

## Data Sources

This dashboard uses **100% free, no-API-key-required** data sources:

- **CoinGecko API** - Bitcoin price and market data
- **Alternative.me API** - Fear & Greed Index
- **Blockchain.com API** - On-chain metrics
- **Yahoo Finance** - Macro economic indicators (via yfinance)

### Rate Limits & Caching

- Data is cached for 1-10 minutes depending on the metric
- API calls include rate limiting to respect free tier limits
- **Automatic Demo Mode** - If APIs are unreachable (network restrictions, rate limits), the dashboard automatically switches to realistic demo data
- All features remain functional in demo mode for testing and demonstration

### Demo Mode

If you see a warning banner stating "Demo Mode Active", the dashboard is displaying realistic simulated data because:
- External APIs are unreachable (firewall, proxy, or network restrictions)
- API rate limits have been exceeded
- Internet connection is unavailable

**Demo mode provides:**
- Realistic Bitcoin price patterns based on historical trends
- Fully functional technical indicators
- Simulated Fear & Greed Index
- Mock on-chain metrics
- Generated macro economic data

This ensures the dashboard can be tested and demonstrated even without internet access!

## Features Explained

### Technical Indicators

**RSI (Relative Strength Index)**
- Measures momentum on a scale of 0-100
- Below 30: Oversold (potential buy signal)
- Above 70: Overbought (potential sell signal)

**Moving Averages**
- SMA 20: Short-term trend
- SMA 50: Medium-term trend
- SMA 200: Long-term trend
- Golden Cross: 50 SMA crosses above 200 SMA (bullish)
- Death Cross: 50 SMA crosses below 200 SMA (bearish)

**MACD**
- Trend-following momentum indicator
- Bullish: MACD line above signal line
- Bearish: MACD line below signal line

**Bollinger Bands**
- Price touching upper band: potentially overbought
- Price touching lower band: potentially oversold
- Band width indicates volatility

### Market Regime Detection

The dashboard automatically classifies the market into:
- **Strong Bull Market**: Price above all MAs, +10% in 30 days
- **Bull Market**: Price above 50 SMA, +5% in 30 days
- **Strong Bear Market**: Price below all MAs, -10% in 30 days
- **Bear Market**: Price below 50 SMA, -5% in 30 days
- **Sideways/Consolidation**: Less than ±5% in 30 days
- **Transitional**: Mixed signals

### Historical Pattern Recognition

The analysis engine:
1. Analyzes current 30-day price pattern
2. Searches historical data for similar patterns
3. Identifies what happened after those patterns
4. Displays top 5 most similar patterns with outcomes

### Risk Metrics

- **Sharpe Ratio**: Risk-adjusted returns (higher is better)
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Value at Risk (95%)**: Expected maximum loss at 95% confidence
- **Sortino Ratio**: Returns relative to downside risk only

## Customization

### Changing Time Periods

Edit the `days_options` dictionary in `dashboard.py`:

```python
days_options = {
    '7 Days': 7,
    '30 Days': 30,
    '90 Days': 90,
    # Add custom periods here
}
```

### Adding New Technical Indicators

Add methods to `TechnicalIndicators` class in `indicators.py`:

```python
@staticmethod
def your_indicator(data: pd.Series) -> pd.Series:
    # Your calculation here
    return result
```

### Modifying Analysis Logic

Update the `MarketAnalyzer` class in `analysis.py` to customize:
- Correlation calculations
- Pattern recognition algorithms
- Risk metric calculations
- Market regime definitions

## Troubleshooting

### Dashboard won't load
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (must be 3.8+)

### No data showing
- Check internet connection
- APIs may have rate limits - wait a few minutes and refresh
- Try a different time period

### Charts not displaying
- Ensure Plotly is installed: `pip install plotly`
- Try clearing browser cache
- Refresh the page (F5)

### Module import errors
- Ensure you're in the correct directory
- Run: `pip install -r requirements.txt --upgrade`

## Performance Tips

- Use shorter time periods (7-30 days) for faster loading
- Disable auto-refresh when not needed
- Charts with fewer indicators render faster
- Cache is automatic - subsequent loads are much faster

## Limitations

### Free API Limitations
- CoinGecko free tier: ~10-50 calls/minute
- Some macro data may have slight delays
- On-chain metrics update once daily

### Data Accuracy
- Historical data is approximate for intraday periods
- OHLC data approximated from price points for some periods
- Correlations are statistical, not causal

## Future Enhancements

Potential additions:
- [ ] Multiple cryptocurrency support
- [ ] Custom alert system
- [ ] Export analysis to PDF
- [ ] Machine learning price predictions
- [ ] Social sentiment analysis
- [ ] Portfolio tracking
- [ ] Backtesting capabilities

## Contributing

This is a personal project, but suggestions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Improve documentation
- Optimize code

## License

This project is provided as-is for educational and personal use.

## Disclaimer

**This dashboard is for informational purposes only. It is NOT financial advice.**

- Cryptocurrency trading carries significant risk
- Past performance does not guarantee future results
- Always do your own research (DYOR)
- Never invest more than you can afford to lose
- Consult with a qualified financial advisor before making investment decisions

## Acknowledgments

- **CoinGecko** for comprehensive cryptocurrency data
- **Alternative.me** for Fear & Greed Index
- **Blockchain.com** for on-chain metrics
- **Streamlit** for the amazing web framework
- **Plotly** for interactive visualizations

---

**Built with ❤️ and Python**

For questions or issues, please check the troubleshooting section or review the code comments for detailed explanations.

Happy analyzing! 🚀📈
