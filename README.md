# 📊 MASI Market Sentiment Dashboard

A comprehensive real-time market sentiment analysis dashboard for the Moroccan All Shares Index (MASI), powered by Bloomberg Terminal data and advanced technical analysis.

## 🚀 Features

- **Real-time Bloomberg Integration**: Connect directly to Bloomberg Terminal for live market data
- **Multi-Component Sentiment Analysis**:
  - 📊 Market Breadth (Advances/Declines)
  - 🚀 Price Momentum (New Highs/Lows)
  - 📈 Trend Analysis (Moving Averages, RSI)
  - 💧 Volume Analysis
- **Interactive Visualizations**: Professional charts using Plotly
- **Historical Data Analysis**: View and export historical sentiment trends
- **Backtesting Engine**: Test sentiment-based trading strategies
- **Configurable Parameters**: Customize weights, thresholds, and indicators
- **Data Caching**: Intelligent caching system for optimal performance
- **Synthetic Data Mode**: Test without Bloomberg connection

## 📁 Project Structure

\`\`\`
first/
├── Main.py                 # Main Streamlit application
├── bl_client.py           # Bloomberg API client
├── sentiment_calculator.py # Sentiment calculation engine
├── data_handler.py        # Data management and caching
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── run.sh                # Startup script
│
├── components/           # UI components
│   ├── __init__.py
│   ├── cards.py         # Metric and component cards
│   ├── charts.py        # Plotly chart components
│   ├── header.py        # Header components
│   └── sidebar.py       # Sidebar navigation
│
├── utils/               # Utility functions
│   ├── __init__.py
│   ├── cache.py         # Caching utilities
│   └── formatters.py    # Number and text formatting
│
├── pages/               # Dashboard pages
│   ├── __init__.py
│   ├── historical_data.py   # Historical data viewer
│   ├── configuration.py     # Settings page
│   └── backtesting.py       # Strategy backtesting
│
├── assets/              # Static assets
│   ├── styling.css      # Custom CSS styles
│   └── logo.png         # Dashboard logo (optional)
│
└── data/                # Data storage
    ├── cache/          # Cached data files
    ├── historical/     # Historical market data
    ├── exports/        # Exported reports
    └── config/         # User configuration files
\`\`\`

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- Bloomberg Terminal (for live data)
- Bloomberg API (blpapi) installed and configured

### Setup

1. **Clone the repository**
\`\`\`bash
git clone <repository-url>
cd first
\`\`\`

2. **Create virtual environment**
\`\`\`bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

3. **Install dependencies**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. **Configure Bloomberg** (if using live data)
   - Ensure Bloomberg Terminal is running
   - Verify Bloomberg API is installed: \`pip show blpapi\`
   - Default connection: localhost:8194

5. **Run the dashboard**
\`\`\`bash
# Quick start with the provided script
./run.sh

# Or manually
streamlit run Main.py
\`\`\`

The dashboard will open in your browser at \`http://localhost:8501\`

## 🎯 Usage

### 1. Dashboard Page
- View real-time market sentiment score
- See component breakdown (Breadth, Momentum, Trend, Volume)
- Monitor technical levels and support/resistance

### 2. Market Analysis
- Deep dive into price action
- Breadth analysis (Advances/Declines)
- Technical indicators (RSI, MACD, Stochastic)

### 3. Historical Data
- Load and visualize historical sentiment trends
- Export data to CSV, Excel, or JSON
- Analyze sentiment patterns over time

### 4. Configuration
- Customize sentiment weights
- Adjust classification thresholds
- Configure technical indicator periods
- Manage cache settings

### 5. Backtesting
- Test sentiment-based trading strategies
- Define entry/exit thresholds
- View performance metrics and equity curves
- Analyze trade logs

## 📊 Sentiment Calculation

The sentiment score ranges from -100 (Very Bearish) to +100 (Very Bullish) and is calculated using:

**Overall Score = (Breadth × 30%) + (Momentum × 25%) + (Trend × 25%) + (Volume × 20%)**

### Component Scores

1. **Breadth Score**: Based on advance/decline ratio
2. **Momentum Score**: Price change and new highs/lows
3. **Trend Score**: Moving averages and RSI
4. **Volume Score**: Volume relative to average

### Sentiment Labels

- 🚀 **Very Bullish**: Score ≥ 60
- ↗️ **Bullish**: Score 30-60
- ➡️ **Neutral**: Score -30 to 30
- ↘️ **Bearish**: Score -60 to -30
- 📉 **Very Bearish**: Score ≤ -60

## 🔌 Data Sources

### Bloomberg Terminal (Live Mode)
- Real-time MASI index data
- Breadth indicators (advances, declines, unchanged)
- Technical indicators (RSI, MACD, Stochastic)
- Volume and moving averages
- Sector indices (Banks, Insurance)

### Synthetic Mode (Testing)
- Algorithmically generated realistic market data
- Reproducible based on date seed
- Useful for development and backtesting

## 🛠️ Configuration

Configuration files are stored in \`data/config/\` and can be managed through the Configuration page:

- \`sentiment_weights.json\`: Component weights
- \`thresholds.json\`: Sentiment classification thresholds
- \`technical_config.json\`: Technical indicator parameters
- \`cache_config.json\`: Cache TTL settings

## 📈 Performance

- **Caching**: Intelligent caching reduces Bloomberg API calls
- **Lazy Loading**: Components load only when needed
- **Optimized Queries**: Efficient data fetching strategies
- **Session State**: Maintains state across page navigation

## ⚠️ Disclaimer

This dashboard is for informational purposes only. It does not constitute financial advice. Trading and investment decisions should not be based solely on sentiment indicators.

---

**Built with ❤️ for the Moroccan financial markets**
