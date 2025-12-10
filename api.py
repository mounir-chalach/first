"""
REST API for MASI Sentiment Dashboard
Allows programmatic access to sentiment analysis via HTTP endpoints
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime, date, timedelta
import uvicorn

from sentiment_calculator import MASISentimentCalculator
from data_handler import DataHandler
from bl_client import BloombergClient
from utils.formatters import format_number, format_percentage
from config import SENTIMENT_WEIGHTS, THRESHOLDS

# Initialize FastAPI
app = FastAPI(
    title="MASI Sentiment API",
    description="REST API for Moroccan All Shares Index (MASI) sentiment analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
data_handler = DataHandler()
calculator = MASISentimentCalculator()
bloomberg_client = None  # Initialize on demand


# ==================== Request/Response Models ====================

class MarketDataInput(BaseModel):
    """Market data input for sentiment calculation"""
    close: float = Field(..., description="Closing price", example=13000.0)
    open: float = Field(..., description="Opening price", example=12950.0)
    high: float = Field(..., description="Highest price", example=13100.0)
    low: float = Field(..., description="Lowest price", example=12900.0)
    volume: float = Field(..., description="Trading volume in millions", example=2000.0)
    volume_avg_20d: Optional[float] = Field(1800.0, description="20-day average volume")
    advances: int = Field(..., description="Number of advancing stocks", example=450)
    declines: int = Field(..., description="Number of declining stocks", example=250)
    unchanged: int = Field(0, description="Number of unchanged stocks", example=50)
    total_issues: int = Field(750, description="Total number of issues")
    new_highs: int = Field(0, description="New 52-week highs", example=15)
    new_lows: int = Field(0, description="New 52-week lows", example=5)
    rsi: Optional[float] = Field(50.0, description="RSI indicator (0-100)", example=55.0)
    macd: Optional[float] = Field(0.0, description="MACD value", example=5.0)
    macd_signal: Optional[float] = Field(0.0, description="MACD signal", example=3.0)
    stochastic: Optional[float] = Field(50.0, description="Stochastic oscillator", example=60.0)
    ma_20: Optional[float] = Field(None, description="20-day moving average", example=12980.0)
    ma_50: Optional[float] = Field(None, description="50-day moving average", example=12950.0)
    ma_200: Optional[float] = Field(None, description="200-day moving average", example=12900.0)

    class Config:
        schema_extra = {
            "example": {
                "close": 13000.0,
                "open": 12950.0,
                "high": 13100.0,
                "low": 12900.0,
                "volume": 2000.0,
                "volume_avg_20d": 1800.0,
                "advances": 450,
                "declines": 250,
                "unchanged": 50,
                "total_issues": 750,
                "new_highs": 15,
                "new_lows": 5,
                "rsi": 55.0,
                "macd": 5.0,
                "macd_signal": 3.0,
                "stochastic": 60.0,
                "ma_20": 12980.0,
                "ma_50": 12950.0,
                "ma_200": 12900.0
            }
        }


class SentimentResponse(BaseModel):
    """Sentiment analysis response"""
    overall_score: float
    sentiment_label: str
    components: Dict[str, float]
    technical_levels: Dict[str, float]
    confidence: float
    timestamp: str
    analysis_date: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    bloomberg_connected: bool
    timestamp: str


class BacktestRequest(BaseModel):
    """Backtesting request"""
    start_date: str = Field(..., example="2024-10-01")
    end_date: str = Field(..., example="2024-12-10")
    entry_threshold: float = Field(30, ge=-100, le=100)
    exit_threshold: float = Field(-30, ge=-100, le=100)
    initial_capital: float = Field(100000, gt=0)
    position_size: float = Field(1.0, ge=0.1, le=1.0)


# ==================== API Endpoints ====================

@app.get("/", tags=["General"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "MASI Sentiment Analysis API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "sentiment": "/api/v1/sentiment",
            "historical": "/api/v1/historical/{date}",
            "calculate": "/api/v1/calculate",
            "config": "/api/v1/config",
            "backtest": "/api/v1/backtest"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check():
    """Health check endpoint"""
    global bloomberg_client

    bloomberg_connected = False
    if bloomberg_client is None:
        try:
            bloomberg_client = BloombergClient()
            bloomberg_connected = bloomberg_client.connected
        except:
            pass
    else:
        bloomberg_connected = bloomberg_client.connected

    return HealthResponse(
        status="healthy",
        version="1.0.0",
        bloomberg_connected=bloomberg_connected,
        timestamp=datetime.now().isoformat()
    )


@app.get("/api/v1/sentiment", response_model=SentimentResponse, tags=["Sentiment"])
async def get_current_sentiment(
    use_bloomberg: bool = Query(False, description="Use Bloomberg data instead of synthetic")
):
    """
    Get current market sentiment for today's date

    - **use_bloomberg**: Use live Bloomberg data (requires Bloomberg Terminal)
    """
    try:
        today = date.today()

        # Get market data
        if use_bloomberg:
            global bloomberg_client
            if bloomberg_client is None or not bloomberg_client.connected:
                bloomberg_client = BloombergClient()
                if not bloomberg_client.connected:
                    raise HTTPException(
                        status_code=503,
                        detail="Bloomberg Terminal not connected"
                    )

            market_data = bloomberg_client.get_masi_data(datetime.now())
            if not market_data:
                raise HTTPException(
                    status_code=404,
                    detail="No Bloomberg data available"
                )
        else:
            market_data = data_handler.get_historical_data(today)

        # Calculate sentiment
        result = calculator.calculate_sentiment(market_data, today)

        return SentimentResponse(
            overall_score=result['overall_score'],
            sentiment_label=result['sentiment_label'],
            components=result['components'],
            technical_levels=result['technical_levels'],
            confidence=result['confidence'],
            timestamp=result['timestamp'].isoformat(),
            analysis_date=result['analysis_date'].isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/historical/{analysis_date}", response_model=SentimentResponse, tags=["Sentiment"])
async def get_historical_sentiment(
    analysis_date: str = Query(..., description="Date in YYYY-MM-DD format", example="2024-12-10")
):
    """
    Get sentiment for a specific historical date

    - **analysis_date**: Date in YYYY-MM-DD format (e.g., 2024-12-10)
    """
    try:
        # Parse date
        target_date = datetime.strptime(analysis_date, "%Y-%m-%d").date()

        if target_date > date.today():
            raise HTTPException(
                status_code=400,
                detail="Cannot analyze future dates"
            )

        # Get historical data
        market_data = data_handler.get_historical_data(target_date)

        # Calculate sentiment
        result = calculator.calculate_sentiment(market_data, target_date)

        return SentimentResponse(
            overall_score=result['overall_score'],
            sentiment_label=result['sentiment_label'],
            components=result['components'],
            technical_levels=result['technical_levels'],
            confidence=result['confidence'],
            timestamp=result['timestamp'].isoformat(),
            analysis_date=result['analysis_date'].isoformat()
        )

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM-DD"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/calculate", response_model=SentimentResponse, tags=["Sentiment"])
async def calculate_sentiment(market_data: MarketDataInput):
    """
    Calculate sentiment from provided market data

    Accepts market data in JSON format and returns sentiment analysis.
    Useful for testing with custom data or integrating with external systems.
    """
    try:
        # Convert Pydantic model to dict
        data_dict = market_data.dict()

        # Calculate sentiment
        result = calculator.calculate_sentiment(data_dict, date.today())

        return SentimentResponse(
            overall_score=result['overall_score'],
            sentiment_label=result['sentiment_label'],
            components=result['components'],
            technical_levels=result['technical_levels'],
            confidence=result['confidence'],
            timestamp=result['timestamp'].isoformat(),
            analysis_date=result['analysis_date'].isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/config", tags=["Configuration"])
async def get_configuration():
    """Get current sentiment calculation configuration"""
    return {
        "sentiment_weights": SENTIMENT_WEIGHTS,
        "thresholds": THRESHOLDS,
        "version": "1.0.0"
    }


@app.get("/api/v1/range", tags=["Sentiment"])
async def get_sentiment_range(
    start_date: str = Query(..., example="2024-11-01"),
    end_date: str = Query(..., example="2024-12-10")
):
    """
    Get sentiment data for a date range

    - **start_date**: Start date (YYYY-MM-DD)
    - **end_date**: End date (YYYY-MM-DD)
    """
    try:
        # Parse dates
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start > end:
            raise HTTPException(
                status_code=400,
                detail="start_date must be before end_date"
            )

        if end > date.today():
            end = date.today()

        # Generate sentiment for date range
        results = []
        current_date = start

        while current_date <= end:
            market_data = data_handler.get_historical_data(current_date)
            sentiment = calculator.calculate_sentiment(market_data, current_date)

            results.append({
                "date": current_date.isoformat(),
                "score": sentiment['overall_score'],
                "label": sentiment['sentiment_label'],
                "components": sentiment['components']
            })

            current_date += timedelta(days=1)

        return {
            "start_date": start_date,
            "end_date": end_date,
            "count": len(results),
            "data": results
        }

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM-DD"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/backtest", tags=["Backtesting"])
async def run_backtest(request: BacktestRequest):
    """
    Run a backtesting simulation

    Simulates a trading strategy based on sentiment signals.
    """
    try:
        # Parse dates
        start = datetime.strptime(request.start_date, "%Y-%m-%d").date()
        end = datetime.strptime(request.end_date, "%Y-%m-%d").date()

        if start >= end:
            raise HTTPException(
                status_code=400,
                detail="start_date must be before end_date"
            )

        # Generate historical data
        historical_data = []
        current_date = start

        while current_date <= end:
            market_data = data_handler.get_historical_data(current_date)
            sentiment = calculator.calculate_sentiment(market_data, current_date)

            historical_data.append({
                'date': current_date,
                'sentiment': sentiment['overall_score'],
                'price': market_data['close'],
                'label': sentiment['sentiment_label']
            })

            current_date += timedelta(days=1)

        # Run simulation (simplified version)
        from pages.backtesting import simulate_strategy

        results = simulate_strategy(
            historical_data,
            request.entry_threshold,
            request.exit_threshold,
            request.initial_capital,
            request.position_size
        )

        return {
            "parameters": request.dict(),
            "results": {
                "total_return": results['total_return'],
                "final_value": results['final_value'],
                "total_trades": results['total_trades'],
                "win_rate": results['win_rate'],
                "max_drawdown": results['max_drawdown'],
                "sharpe_ratio": results['sharpe_ratio']
            },
            "trades": results['trades'][:10]  # Return first 10 trades
        }

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use YYYY-MM-DD"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Run Server ====================

if __name__ == "__main__":
    print("🚀 Starting MASI Sentiment API...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("📊 Interactive Docs: http://localhost:8000/redoc")
    print("")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
