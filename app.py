import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# --- Placeholder for model prediction logic ---
# In a real app, you would load your trained model here.
def predict_next_day_price(ticker):
    # This is a placeholder. Replace with your actual model's prediction.
    # For now, let's just return a random-ish value for demonstration.
    last_price = yf.Ticker(ticker).history(period='1d')['Close'][0]
    prediction = last_price * (1 + (np.random.rand() - 0.5) * 0.05) # Predict a small change
    return prediction

st.set_page_config(layout="wide", page_title="AI Stock Predictor")

st.title("📈 AI Stock Prediction Agent")
st.write("This app displays the live stock chart and a *demo* AI prediction for the next day's closing price.")

# --- Sidebar for user input ---
st.sidebar.header("User Input")
ticker_symbol = st.sidebar.text_input("Enter NSE Ticker Symbol (e.g., RELIANCE.NS)", "RELIANCE.NS").upper()
predict_button = st.sidebar.button("Predict & Show Chart")

if predict_button:
    # --- Fetching Data ---
    today = datetime.now()
    start_date = today - timedelta(days=365*2) # 2 years of data
    
    try:
        data = yf.download(ticker_symbol, start=start_date.strftime('%Y-%m-%d'), end=today.strftime('%Y-%m-%d'))
        
        if data.empty:
            st.error(f"No data found for ticker '{ticker_symbol}'. Please check the symbol and try again.")
        else:
            # --- Display Chart ---
            st.subheader(f"Live Stock Chart for {ticker_symbol}")
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=data.index,
                            open=data['Open'],
                            high=data['High'],
                            low=data['Low'],
                            close=data['Close'], name='Market Data'))
            fig.update_layout(title=f'{ticker_symbol} Share Price', yaxis_title='Stock Price (INR)')
            st.plotly_chart(fig, use_container_width=True)

            # --- Display Prediction ---
            st.subheader("🤖 AI Prediction")
            with st.spinner('Calculating prediction...'):
                # In a real app, you'd feed the latest data to your loaded LSTM model
                predicted_price = predict_next_day_price(ticker_symbol)
                last_close = data['Close'][-1]
                
                delta = predicted_price - last_close
                delta_percent = (delta / last_close) * 100
                
                st.metric(
                    label=f"Predicted Next Day Close for {ticker_symbol}",
                    value=f"₹{predicted_price:.2f}",
                    delta=f"{delta:.2f} ({delta_percent:.2f}%)"
                )

            # --- Guidance Section ---
            st.subheader("💡 Simple Guidance")
            if delta > 0:
                st.success("The model predicts a **potential upward** movement. This could be a positive signal.")
            else:
                st.warning("The model predicts a **potential downward** movement. This could be a cautionary signal.")
            
            st.info("**Disclaimer:** This is a simplified, educational AI prediction and not financial advice.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
