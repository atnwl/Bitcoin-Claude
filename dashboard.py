"""
Bitcoin Market Analysis Dashboard
Interactive web application for comprehensive Bitcoin market analysis
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime
import time

from data_fetcher import DataFetcher
from indicators import TechnicalIndicators
from analysis import MarketAnalyzer


# Page configuration
st.set_page_config(
    page_title="Bitcoin Market Analysis Dashboard",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #f7931a 0%, #ffa500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #0e1117;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #262730;
    }
    .positive {
        color: #00ff00;
    }
    .negative {
        color: #ff4444;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_bitcoin_data(days):
    """Load and cache Bitcoin data"""
    fetcher = DataFetcher()
    return fetcher.get_bitcoin_price_data(days)


@st.cache_data(ttl=60)  # Cache for 1 minute
def load_current_price():
    """Load current Bitcoin price"""
    fetcher = DataFetcher()
    return fetcher.get_current_bitcoin_price()


@st.cache_data(ttl=300)
def load_fear_greed():
    """Load Fear & Greed Index"""
    fetcher = DataFetcher()
    return fetcher.get_fear_greed_index()


@st.cache_data(ttl=600)  # Cache for 10 minutes
def load_on_chain_metrics():
    """Load on-chain metrics"""
    fetcher = DataFetcher()
    return fetcher.get_on_chain_metrics()


@st.cache_data(ttl=300)
def load_macro_indicators(days):
    """Load macro indicators"""
    fetcher = DataFetcher()
    return fetcher.get_macro_indicators(days)


def create_price_chart(df):
    """Create interactive price chart with indicators"""
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.5, 0.15, 0.15, 0.2],
        subplot_titles=('Bitcoin Price & Indicators', 'RSI', 'MACD', 'Volume')
    )

    # Main price chart with candlesticks
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['close'],
            name='BTC Price',
            line=dict(color='#f7931a', width=2)
        ),
        row=1, col=1
    )

    # Bollinger Bands
    if 'bb_upper' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['bb_upper'],
                name='BB Upper',
                line=dict(color='rgba(255, 255, 255, 0.2)', dash='dash'),
                showlegend=False
            ),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['bb_lower'],
                name='BB Lower',
                line=dict(color='rgba(255, 255, 255, 0.2)', dash='dash'),
                fill='tonexty',
                fillcolor='rgba(255, 255, 255, 0.05)',
                showlegend=False
            ),
            row=1, col=1
        )

    # Moving averages
    if 'sma_20' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['sma_20'],
                name='SMA 20',
                line=dict(color='cyan', width=1)
            ),
            row=1, col=1
        )

    if 'sma_50' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['sma_50'],
                name='SMA 50',
                line=dict(color='magenta', width=1)
            ),
            row=1, col=1
        )

    if 'sma_200' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['sma_200'],
                name='SMA 200',
                line=dict(color='orange', width=1.5)
            ),
            row=1, col=1
        )

    # RSI
    if 'rsi' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['rsi'],
                name='RSI',
                line=dict(color='purple', width=2)
            ),
            row=2, col=1
        )
        # RSI levels
        fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=2, col=1)

    # MACD
    if 'macd' in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['macd'],
                name='MACD',
                line=dict(color='blue', width=1)
            ),
            row=3, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df['macd_signal'],
                name='Signal',
                line=dict(color='red', width=1)
            ),
            row=3, col=1
        )
        if 'macd_histogram' in df.columns:
            colors = ['green' if val >= 0 else 'red' for val in df['macd_histogram']]
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df['macd_histogram'],
                    name='MACD Hist',
                    marker_color=colors,
                    opacity=0.5
                ),
                row=3, col=1
            )

    # Volume
    if 'volume' in df.columns:
        fig.add_trace(
            go.Bar(
                x=df.index,
                y=df['volume'],
                name='Volume',
                marker_color='rgba(100, 150, 200, 0.5)'
            ),
            row=4, col=1
        )

    # Update layout
    fig.update_layout(
        title='Bitcoin Price Analysis',
        height=900,
        showlegend=True,
        hovermode='x unified',
        template='plotly_dark',
        xaxis_rangeslider_visible=False
    )

    fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig.update_yaxes(title_text="RSI", row=2, col=1, range=[0, 100])
    fig.update_yaxes(title_text="MACD", row=3, col=1)
    fig.update_yaxes(title_text="Volume", row=4, col=1)

    return fig


def create_correlation_chart(correlations):
    """Create correlation chart with macro indicators"""
    if not correlations:
        return None

    names = list(correlations.keys())
    values = list(correlations.values())
    colors = ['green' if v > 0 else 'red' for v in values]

    fig = go.Figure(data=[
        go.Bar(
            x=values,
            y=[name.replace('_', ' ').title() for name in names],
            orientation='h',
            marker_color=colors,
            text=[f'{v:.2f}' for v in values],
            textposition='auto',
        )
    ])

    fig.update_layout(
        title='Bitcoin Correlation with Macro Indicators',
        xaxis_title='Correlation Coefficient',
        height=300,
        template='plotly_dark',
        xaxis=dict(range=[-1, 1])
    )

    return fig


def create_fear_greed_gauge(fear_greed_data):
    """Create Fear & Greed Index gauge"""
    value = fear_greed_data.get('current_value', 50)

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': "Fear & Greed Index"},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "orange"},
            'steps': [
                {'range': [0, 25], 'color': "darkred"},
                {'range': [25, 45], 'color': "red"},
                {'range': [45, 55], 'color': "gray"},
                {'range': [55, 75], 'color': "lightgreen"},
                {'range': [75, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))

    fig.update_layout(
        height=300,
        template='plotly_dark'
    )

    return fig


def create_on_chain_chart(on_chain_data):
    """Create on-chain metrics chart"""
    if not on_chain_data or 'hash_rate' not in on_chain_data:
        return None

    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Network Hash Rate', 'Active Addresses'),
        vertical_spacing=0.15
    )

    # Hash rate
    if 'hash_rate' in on_chain_data and not on_chain_data['hash_rate']['historical'].empty:
        hr_df = on_chain_data['hash_rate']['historical']
        if 'x' in hr_df.columns and 'y' in hr_df.columns:
            hr_df['x'] = pd.to_datetime(hr_df['x'], unit='s')
            fig.add_trace(
                go.Scatter(
                    x=hr_df['x'],
                    y=hr_df['y'],
                    name='Hash Rate',
                    line=dict(color='cyan', width=2),
                    fill='tozeroy'
                ),
                row=1, col=1
            )

    # Active addresses
    if 'active_addresses' in on_chain_data and not on_chain_data['active_addresses']['historical'].empty:
        aa_df = on_chain_data['active_addresses']['historical']
        if 'x' in aa_df.columns and 'y' in aa_df.columns:
            aa_df['x'] = pd.to_datetime(aa_df['x'], unit='s')
            fig.add_trace(
                go.Scatter(
                    x=aa_df['x'],
                    y=aa_df['y'],
                    name='Active Addresses',
                    line=dict(color='magenta', width=2),
                    fill='tozeroy'
                ),
                row=2, col=1
            )

    fig.update_layout(
        height=500,
        showlegend=False,
        template='plotly_dark'
    )

    fig.update_yaxes(title_text="Hash Rate", row=1, col=1)
    fig.update_yaxes(title_text="Addresses", row=2, col=1)

    return fig


def main():
    """Main dashboard application"""

    # Header
    st.markdown('<h1 class="main-header">₿ Bitcoin Market Analysis Dashboard</h1>', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.header("⚙️ Settings")

    days_options = {
        '7 Days': 7,
        '30 Days': 30,
        '90 Days': 90,
        '180 Days': 180,
        '1 Year': 365
    }

    selected_period = st.sidebar.selectbox(
        'Select Time Period',
        list(days_options.keys()),
        index=4  # Default to 1 year
    )

    days = days_options[selected_period]

    auto_refresh = st.sidebar.checkbox('Auto Refresh (1 min)', value=False)

    if st.sidebar.button('🔄 Refresh Data'):
        st.cache_data.clear()
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "This dashboard provides comprehensive Bitcoin market analysis including:\n\n"
        "- Live price data & technical indicators\n"
        "- Fear & Greed Index\n"
        "- On-chain metrics\n"
        "- Macro correlations\n"
        "- Historical pattern analysis"
    )

    # Load data with progress indication
    with st.spinner('Loading data...'):
        current_price = load_current_price()
        btc_df = load_bitcoin_data(days)

        if not btc_df.empty:
            btc_df = TechnicalIndicators.get_all_indicators(btc_df)

        fear_greed = load_fear_greed()
        on_chain = load_on_chain_metrics()
        macro_indicators = load_macro_indicators(days)

    # Current Price Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        price = current_price.get('price', 0)
        st.metric(
            "Current Price",
            f"${price:,.2f}",
            f"{current_price.get('change_24h', 0):.2f}%"
        )

    with col2:
        st.metric(
            "24h Volume",
            f"${current_price.get('volume_24h', 0):,.0f}"
        )

    with col3:
        st.metric(
            "Market Cap",
            f"${current_price.get('market_cap', 0):,.0f}"
        )

    with col4:
        fg_value = fear_greed.get('current_value', 50)
        fg_class = fear_greed.get('current_classification', 'Neutral')
        st.metric(
            "Fear & Greed",
            fg_value,
            fg_class
        )

    st.markdown("---")

    # Main price chart
    if not btc_df.empty:
        st.plotly_chart(create_price_chart(btc_df), use_container_width=True)
    else:
        st.warning("Unable to load price data. Please try refreshing.")

    st.markdown("---")

    # Two column layout for additional charts
    col1, col2 = st.columns(2)

    with col1:
        # Fear & Greed Gauge
        st.subheader("😱 Fear & Greed Index")
        if fear_greed:
            st.plotly_chart(create_fear_greed_gauge(fear_greed), use_container_width=True)
        else:
            st.info("Fear & Greed data unavailable")

    with col2:
        # Correlation chart
        st.subheader("📊 Macro Correlations")
        if not btc_df.empty and macro_indicators:
            correlations = MarketAnalyzer.analyze_macro_correlations(btc_df, macro_indicators)
            if correlations:
                st.plotly_chart(create_correlation_chart(correlations), use_container_width=True)
            else:
                st.info("Correlation data unavailable")
        else:
            st.info("Loading macro indicators...")

    st.markdown("---")

    # On-chain metrics
    st.subheader("⛓️ On-Chain Metrics")
    if on_chain:
        on_chain_chart = create_on_chain_chart(on_chain)
        if on_chain_chart:
            st.plotly_chart(on_chain_chart, use_container_width=True)

        # Display current values
        col1, col2, col3 = st.columns(3)
        if 'hash_rate' in on_chain:
            with col1:
                st.metric(
                    "Current Hash Rate",
                    f"{on_chain['hash_rate']['current']:,.0f} {on_chain['hash_rate']['unit']}"
                )
        if 'active_addresses' in on_chain:
            with col2:
                st.metric(
                    "Active Addresses",
                    f"{on_chain['active_addresses']['current']:,.0f}"
                )
        if 'transactions' in on_chain:
            with col3:
                st.metric(
                    "Daily Transactions",
                    f"{on_chain['transactions']['current']:,.0f}"
                )
    else:
        st.info("On-chain metrics are loading... This may take a moment.")

    st.markdown("---")

    # Market Analysis
    st.subheader("📈 Market Analysis")

    if not btc_df.empty:
        correlations = MarketAnalyzer.analyze_macro_correlations(btc_df, macro_indicators) if macro_indicators else {}

        analysis_text = MarketAnalyzer.generate_market_analysis(
            btc_df,
            correlations,
            fear_greed,
            on_chain
        )

        st.markdown(analysis_text)

        # Technical signals
        st.markdown("---")
        st.subheader("📡 Current Technical Signals")

        signals = TechnicalIndicators.get_current_signal(btc_df)

        if signals:
            signal_cols = st.columns(len(signals))
            for idx, (name, signal) in enumerate(signals.items()):
                with signal_cols[idx]:
                    # Determine color
                    if 'Bullish' in signal or 'Oversold' in signal:
                        color = '🟢'
                    elif 'Bearish' in signal or 'Overbought' in signal:
                        color = '🔴'
                    else:
                        color = '🟡'

                    st.metric(
                        name.upper(),
                        f"{color} {signal}"
                    )

    # Footer with timestamp
    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Data sources: CoinGecko, Blockchain.com, Alternative.me, Yahoo Finance")

    # Auto-refresh logic
    if auto_refresh:
        time.sleep(60)
        st.rerun()


if __name__ == "__main__":
    main()
