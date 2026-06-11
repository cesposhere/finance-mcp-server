import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from functools import lru_cache
from fastmcp import FastMCP

# Initialize the server
mcp = FastMCP("AdvancedFinanceServer")

# ==========================================
# Caching & Error Handling
# ==========================================
# @lru_cache prevents spamming Yahoo Finance if the AI asks for the same data twice.
@lru_cache(maxsize=32)
def fetch_stock_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """Helper function to fetch and cache stock data safely."""
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    
    if data.empty:
        # Clean error handling to prevent server crashes
        raise ValueError(f"Ticker '{ticker}' not found on major exchanges.")
    return data

@mcp.tool()
def compare_multiple_stocks(tickers: list[str]) -> dict:
    """Fetches the latest closing prices for a list of multiple stock tickers."""
    results = {}
    for ticker in tickers:
        try:
            data = fetch_stock_data(ticker, period="5d")
            results[ticker] = float(data['Close'].iloc[-1])
        except ValueError as e:
            results[ticker] = str(e)
    return results

# ==========================================
# Advanced Indicators
# ==========================================
@mcp.tool()
def calculate_rsi(ticker: str, days: int = 14) -> float:
    """Calculates the Relative Strength Index (RSI) to determine if a stock is overbought or oversold."""
    data = fetch_stock_data(ticker, period="6mo")
    
    # Calculate daily price changes
    delta = data['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    
    # Calculate rolling averages
    avg_gain = gain.rolling(window=days).mean()
    avg_loss = loss.rolling(window=days).mean()
    
    # Calculate RSI formula
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return float(rsi.iloc[-1])

@mcp.tool()
def calculate_sharpe_ratio(ticker: str, risk_free_rate: float = 0.04) -> float:
    """Calculates the annualized Sharpe Ratio to measure risk-adjusted return."""
    data = fetch_stock_data(ticker, period="1y")
    
    # Calculate daily percentage returns
    daily_returns = data['Close'].pct_change().dropna()
    
    # Annualize the returns and volatility (assuming 252 trading days in a year)
    annual_return = daily_returns.mean() * 252
    annual_volatility = daily_returns.std() * np.sqrt(252)
    
    # Sharpe Ratio formula
    sharpe = (annual_return - risk_free_rate) / annual_volatility
    return float(sharpe)

# ==========================================
# Matplotlib to Claude
# ==========================================
@mcp.tool()
def generate_stock_chart(ticker: str, days: int = 90) -> str:
    """Generates a visual line chart of a stock's price history and returns it as a Base64 markdown image."""
    data = fetch_stock_data(ticker, period="1y")
    
    # Slice to the requested days
    df = data.tail(days)
    
    # Create the Matplotlib figure
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['Close'], color='blue', linewidth=2, label=f"{ticker} Close")
    plt.title(f"{ticker} Price History - Last {days} Days", fontsize=14, fontweight='bold')
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    
    # Save the plot to a temporary memory buffer instead of a file
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    
    # Encode the image to a Base64 string that Claude's UI can render
    base64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f"![{ticker} Chart](data:image/png;base64,{base64_img})"

if __name__ == "__main__":
    mcp.run()