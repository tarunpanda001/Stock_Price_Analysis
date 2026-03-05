import streamlit as st
import yfinance as yf
from datetime import datetime
import plotly.graph_objects as go

st.title("Stock Price Analysis")
st.subheader("Select a stock to analyze its historical price data")
option = st.selectbox(
    "Select the stock you want to analyze",
    ("AAPL", "GOOGL", "MSFT","AMZN","TSLA","META","NVDA",)
)
col1,col2 = st.columns(2)
with col1:
    sd = st.date_input("Start Date",datetime(2020,1,1))
with col2:
    ed = st.date_input("End Date",datetime(2024,1,1))

ticker = yf.Ticker(option)

@st.cache_data
def load_data(option, sd, ed):
    ticker = yf.Ticker(option)
    data = ticker.history(start=sd, end=ed)
    return data

ticker_data = load_data(option, sd, ed)

st.subheader(f"Historical Price Data for {option}")
st.dataframe(ticker_data.head())

st.subheader("Stock Performance")
st.line_chart(ticker_data["Close"])

st.subheader("Stock Volume")
st.bar_chart(ticker_data["Volume"])


current_price = ticker_data["Close"].iloc[-1]
high_52 = ticker_data["High"].max()
low_52 = ticker_data["Low"].min()

col1,col2,col3 = st.columns(3)

with col1:
    st.metric(f"{option} Current Price", f"${round(current_price,2)}")

with col2:
    st.metric(f"{option} 52 Week High", f"${round(high_52,2)}")

with col3:
    st.metric(f"{option} 52 Week Low", f"${round(low_52,2)}")


ticker_data["MA50"] = ticker_data["Close"].rolling(window=50).mean()
ticker_data["MA200"] = ticker_data["Close"].rolling(window=200).mean()

st.subheader("Moving Averages")
st.line_chart(ticker_data[["Close", "MA50", "MA200"]])

ticker_data["Daily Returns"] = ticker_data["Close"].pct_change()
st.subheader("Daily Returns")
st.line_chart(ticker_data["Daily Returns"])

fig = go.Figure(data=[go.Candlestick(
    x=ticker_data.index,
    open=ticker_data['Open'],
    high=ticker_data['High'],
    low=ticker_data['Low'],
    close=ticker_data['Close']
)])

st.plotly_chart(fig)



st.download_button(
    label="Download Data as CSV",
    data  = ticker_data.to_csv().encode('utf-8'),
    file_name = f"{option}_data.csv",
    mime = "text/csv"
)

investment = st.number_input("Enter investment amount", value=10000)

first_price = ticker_data["Close"].iloc[0]
last_price = ticker_data["Close"].iloc[-1]

returns = (last_price - first_price) / first_price
profit = investment * returns

if profit > 0:
    st.success(f"Estimated Profit: ${round(profit,2)}")
else:
    st.error(f"Estimated Loss: ${round(profit,2)}")

st.subheader("Statistical Summary")

st.write(ticker_data.describe())

st.markdown("---")
st.markdown(
    "<center>Developed by <b>Tarun Panda</b> | Stock Price Analysis App</center>",
    unsafe_allow_html=True
)

