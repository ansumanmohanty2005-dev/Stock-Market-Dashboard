import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Market Dashboard")
st.markdown("Analyze stocks using live market data.")

st.sidebar.header("Stock Selection")

ticker = st.sidebar.text_input(
    "Stock Symbol",
    value="AAPL"
).upper()

start_date = st.sidebar.date_input(
    "Start Date",
    value=pd.to_datetime("2020-01-01")
)

end_date = st.sidebar.date_input(
    "End Date",
    value=pd.to_datetime("today")
)

df = yf.download(
    ticker,
    start=start_date,
    end=end_date,
    auto_adjust=False,
    progress=False
)

if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

if df.empty:
    st.error("No data found. Please enter a valid stock symbol.")
    st.stop()

df["MA20"] = df["Close"].rolling(20).mean()
df["MA50"] = df["Close"].rolling(50).mean()
df["MA200"] = df["Close"].rolling(200).mean()

df["Daily Return"] = df["Close"].pct_change()

df["Volatility"] = df["Daily Return"].rolling(20).std()

current_price = df["Close"].iloc[-1]
highest = df["High"].max()
lowest = df["Low"].min()
volume = df["Volume"].iloc[-1]

c1, c2, c3, c4 = st.columns(4)

c1.metric("Current Price", f"${current_price:.2f}")
c2.metric("Highest Price", f"${highest:.2f}")
c3.metric("Lowest Price", f"${lowest:.2f}")
c4.metric("Volume", f"{volume:,.0f}")

st.subheader("📊 Candlestick Chart")

fig = go.Figure()

fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"]
    )
)

fig.update_layout(
    xaxis_rangeslider_visible=False,
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📈 Moving Averages")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["Close"],
        name="Close"
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["MA20"],
        name="MA20"
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["MA50"],
        name="MA50"
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["MA200"],
        name="MA200"
    )
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📦 Trading Volume")

fig = px.bar(
    df,
    x=df.index,
    y="Volume"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📉 Daily Returns")

fig = px.line(
    df,
    x=df.index,
    y="Daily Return"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("⚠️ Rolling Volatility")

fig = px.line(
    df,
    x=df.index,
    y="Volatility"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📄 Stock Data")

st.dataframe(df)

csv = df.to_csv().encode("utf-8")

st.download_button(
    "📥 Download Data",
    csv,
    file_name=f"{ticker}.csv",
    mime="text/csv"
)

st.markdown("---")

st.caption(
    "Created by Ansuman Mohanty | Stock Market Dashboard | Python • Pandas • Plotly • Streamlit"
)

# -----------------------------
# RSI (Relative Strength Index)
# -----------------------------

delta = df["Close"].diff()

gain = delta.where(delta > 0, 0)

loss = -delta.where(delta < 0, 0)

avg_gain = gain.rolling(14).mean()

avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss

df["RSI"] = 100 - (100 / (1 + rs))

st.subheader("📈 Relative Strength Index (RSI)")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["RSI"],
        name="RSI"
    )
)

fig.add_hline(y=70, line_dash="dash", line_color="red")

fig.add_hline(y=30, line_dash="dash", line_color="green")

fig.update_layout(height=400)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# MACD
# -----------------------------

ema12 = df["Close"].ewm(span=12, adjust=False).mean()

ema26 = df["Close"].ewm(span=26, adjust=False).mean()

df["MACD"] = ema12 - ema26

df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

# -----------------------------
# MACD
# -----------------------------

ema12 = df["Close"].ewm(span=12, adjust=False).mean()

ema26 = df["Close"].ewm(span=26, adjust=False).mean()

df["MACD"] = ema12 - ema26

df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

# -----------------------------
# Bollinger Bands
# -----------------------------

df["STD"] = df["Close"].rolling(20).std()

df["Upper Band"] = df["MA20"] + (2 * df["STD"])

df["Lower Band"] = df["MA20"] - (2 * df["STD"])

st.subheader("📊 Bollinger Bands")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["Close"],
        name="Close"
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["Upper Band"],
        name="Upper Band"
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["MA20"],
        name="20-Day MA"
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["Lower Band"],
        name="Lower Band"
    )
)

st.plotly_chart(fig, use_container_width=True)

high_52 = df["High"].rolling(252).max().iloc[-1]

low_52 = df["Low"].rolling(252).min().iloc[-1]

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Current Price",
    f"${current_price:.2f}"
)

c2.metric(
    "52 Week High",
    f"${high_52:.2f}"
)

c3.metric(
    "52 Week Low",
    f"${low_52:.2f}"
)

c4.metric(
    "Volume",
    f"{volume:,.0f}"
)

golden_cross = (
    df["MA50"].iloc[-2] < df["MA200"].iloc[-2]
    and
    df["MA50"].iloc[-1] > df["MA200"].iloc[-1]
)

death_cross = (
    df["MA50"].iloc[-2] > df["MA200"].iloc[-2]
    and
    df["MA50"].iloc[-1] < df["MA200"].iloc[-1]
)

if golden_cross:
    st.success("🟢 Golden Cross Detected (Bullish Signal)")

elif death_cross:
    st.error("🔴 Death Cross Detected (Bearish Signal)")

else:
    st.info("ℹ️ No recent Golden Cross or Death Cross detected.")

ticker_obj = yf.Ticker(ticker)

info = ticker_obj.info

st.subheader("🏢 Company Information")

st.write("**Company:**", info.get("longName", "N/A"))
st.write("**Sector:**", info.get("sector", "N/A"))
st.write("**Industry:**", info.get("industry", "N/A"))
st.write("**Market Cap:**", f"${info.get('marketCap', 0):,}")
st.write("**Employees:**", info.get("fullTimeEmployees", "N/A"))