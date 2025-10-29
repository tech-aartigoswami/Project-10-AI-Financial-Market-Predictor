import yfinance as yf
import pandas as pd

def get_stock_data(ticker_symbol, start_date, end_date):
    """
    Fetches historical stock data from Yahoo Finance.
    For Indian stocks, add the '.NS' suffix (e.g., 'RELIANCE.NS').
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        # Get historical market data
        hist_df = stock.history(start=start_date, end=end_date)
        if hist_df.empty:
            print(f"No data found for {ticker_symbol}. Is the ticker correct?")
            return None
        print(f"Successfully fetched data for {ticker_symbol}")
        return hist_df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# --- Example Usage ---
if __name__ == "__main__":
    # NSE Ticker for Reliance Industries Ltd.
    ticker = "RELIANCE.NS"
    data = get_stock_data(ticker, "2020-01-01", "2025-10-28")
    if data is not None:
        print("Last 5 days of data:")
        print(data.tail())
