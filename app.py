import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

st.title("FMCG Comparable Company Analysis")

TICKERS = ["HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS", "MARICO.NS", "COLPAL.NS", "EMAMILTD.NS"]

@st.cache_data(ttl=3600)
def fetch_data(tickers):
    rows = []
    for t in tickers:
        info = yf.Ticker(t).info
        rows.append({
            "Ticker": t,
            "Name": info.get("shortName"),
            "PE": info.get("trailingPE"),
            "PB": info.get("priceToBook"),
            "EV_EBITDA": info.get("enterpriseToEbitda"),
        })
    return pd.DataFrame(rows)

df = fetch_data(TICKERS)
st.dataframe(df)

avg_pe = df["PE"].mean()

st.subheader("P/E Comparison")
fig, ax = plt.subplots()
ax.barh(df["Name"], df["PE"])
ax.axvline(avg_pe, color="red", linestyle="--", label=f"Peer avg: {avg_pe:.1f}x")
ax.set_xlabel("P/E")
ax.legend()
st.pyplot(fig)

st.subheader("Valuation Quadrant: P/E vs P/B")
avg_pb = df["PB"].mean()

fig2, ax2 = plt.subplots()
ax2.scatter(df["PE"], df["PB"])
for _, row in df.iterrows():
    ax2.annotate(row["Name"], (row["PE"], row["PB"]))
ax2.axvline(avg_pe, color="gray", linestyle="--")
ax2.axhline(avg_pb, color="gray", linestyle="--")
ax2.set_xlabel("P/E")
ax2.set_ylabel("P/B")
st.pyplot(fig2)