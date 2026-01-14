# Quick Start Guide

## Fastest Way to Run the Dashboard

### Option 1: Minimal Installation (Recommended for Quick Start)

If you're having dependency issues, you can run the dashboard with just the core features:

```bash
pip install streamlit plotly pandas numpy requests scipy python-dateutil

streamlit run dashboard.py
```

**What you'll get:**
- Live Bitcoin price data
- Historical price charts
- All technical indicators (RSI, MACD, Moving Averages, Bollinger Bands)
- Fear & Greed Index
- On-chain metrics (Hash Rate, Active Addresses)
- Market analysis and pattern recognition

**What won't work:**
- Macro indicator correlations (Dollar Index, Gold, S&P500, etc.)

### Option 2: Full Installation (All Features)

For the complete experience including macro correlations:

```bash
# Install core packages first
pip install streamlit plotly pandas numpy requests scipy python-dateutil

# Then try to install yfinance with all its dependencies
pip install yfinance beautifulsoup4 html5lib lxml frozendict peewee platformdirs

# If multitasking fails to install, try:
pip install --no-build-isolation multitasking

# Or install an older version:
pip install 'yfinance==0.2.40'
```

### Option 3: Using Virtual Environment (Best Practice)

```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows

# Install packages
pip install -r requirements.txt

# Run the dashboard
streamlit run dashboard.py
```

## Running the Dashboard

Once packages are installed, run:

```bash
streamlit run dashboard.py
```

Or use the provided script:

```bash
./run.sh
```

The dashboard will open in your browser at `http://localhost:8501`

## Troubleshooting

### "Module not found" errors

If you get module not found errors, install them individually:

```bash
pip install <module-name>
```

### yfinance won't install

The dashboard will work without yfinance - you'll just miss macro correlations. The error handling will gracefully skip that section.

### Streamlit won't start

Make sure Python 3.8+ is installed:

```bash
python3 --version
```

### Port already in use

If port 8501 is busy, specify a different port:

```bash
streamlit run dashboard.py --server.port 8502
```

## First Run

When you first load the dashboard:

1. **Be patient** - Initial data loading takes 10-30 seconds
2. **Check your internet** - The dashboard needs to fetch data from APIs
3. **Try refreshing** - If data doesn't load, click the "Refresh Data" button
4. **Adjust the time period** - Start with "7 Days" for faster loading

## Performance Tips

- Use shorter time periods for faster loading
- Disable "Auto Refresh" unless you need real-time updates
- On-chain metrics take the longest to load - they update once daily anyway

## Still Having Issues?

Run the test script to diagnose:

```bash
python3 test_setup.py
```

This will tell you exactly which packages are missing or broken.

---

**Happy trading! 🚀**
