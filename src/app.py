import streamlit as st
import pandas as pd
import plotly.express as px
import time

from data_ingestion import fetch_news, fetch_alpha_vantage_news, fetch_gdelt_news, fetch_csv_tweets
from nlp_engine import NLPRiskEngine
from portfolio_rebalancer import TacticalRebalancer
from stress_testing import StrategicStressTester

st.set_page_config(page_title="AI/NLP Risk Engine", layout="wide")

@st.cache_resource
def load_nlp_engine():
    return NLPRiskEngine()

@st.cache_resource
def load_rebalancer():
    return TacticalRebalancer()

@st.cache_resource
def load_stress_tester():
    return StrategicStressTester()

nlp_engine = load_nlp_engine()
rebalancer = load_rebalancer()
stress_tester = load_stress_tester()

st.title("📈 AI/NLP Risk Engine & Portfolio Dashboard")
st.markdown("This dashboard ingests unstructured text, extracts financial risk signals, and demonstrates downstream applications.")

# --- Sidebar Controls ---
st.sidebar.header("Controls")
ticker_query = st.sidebar.selectbox("Select Target Asset/Theme", ["Apple", "Tesla", "Microsoft", "JPMorgan", "Finance"])

# Module Selection
selected_module = st.sidebar.radio("Select Downstream Module", ["Module A: Tactical Rebalancing", "Module B: Stress Testing"])

# Register Modules as Subscribers
if selected_module == "Module A: Tactical Rebalancing":
    nlp_engine.subscribe(rebalancer)
elif selected_module == "Module B: Stress Testing":
    nlp_engine.subscribe(stress_tester)

if st.sidebar.button("Run Pipeline"):
    with st.spinner("Fetching data and running NLP models..."):
        # Map ticker query to an actual ticker for Rebalancer and APIs
        ticker_map = {"Apple": "AAPL", "Tesla": "TSLA", "Microsoft": "MSFT", "JPMorgan": "JPM", "Finance": "FINANCE"}
        target_ticker = ticker_map.get(ticker_query, "AAPL")

        # 1. Ingest Data from all sources
        news1 = fetch_news(ticker_query, limit=2)
        news2 = fetch_alpha_vantage_news(target_ticker, limit=2)
        news3 = fetch_gdelt_news(target_ticker, limit=2)
        tweets = fetch_csv_tweets(target_ticker)
        
        # We will process a mix of news and tweets
        raw_data = news1 + news2 + news3 + tweets[:2]
        
        # 2. Process NLP Signals & Trigger Subscribers Automatically
        st.subheader("1. Ingested Data & Extracted Signals")
        results = []
        for item in raw_data:
            # The nlp_engine will automatically call `.update()` on subscribed modules
            signal = nlp_engine.process_text(
                item['text'], 
                metadata={"source": item['source'], "target_ticker": target_ticker}
            )
            results.append(signal)

        # Display NLP Results
        results_df = pd.DataFrame(results)
        st.dataframe(results_df, width="stretch")

    st.divider()

    # --- Downstream Application Visualization ---
    if selected_module == "Module A: Tactical Rebalancing":
        st.subheader("Module A: Tactical Index Rebalancing")
        st.write("Dynamic rebalancing of a mock index based on real-time sentiment signals.")
        
        col1, col2 = st.columns([1, 2])
        
        df_portfolio = rebalancer.get_portfolio_summary()
        
        with col1:
            st.dataframe(df_portfolio, width="stretch")
            
        with col2:
            fig = px.pie(df_portfolio, values='Weight (%)', names='Ticker', title="Portfolio Weights")
            st.plotly_chart(fig, width="stretch")
            
    elif selected_module == "Module B: Stress Testing":
        st.subheader("Module B: Strategic Portfolio Stress Testing")
        st.write("Simulates the impact of detected high-impact events on a synthetic banking portfolio.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Portfolio Value", f"${stress_tester.total_value:,.2f}")
            st.write("Current Asset Allocation:")
            st.json(stress_tester.portfolio)
            
        with col2:
            # Simple bar chart of assets
            assets = list(stress_tester.portfolio.keys())
            values = list(stress_tester.portfolio.values())
            fig = px.bar(x=assets, y=values, labels={'x': 'Asset Class', 'y': 'Value ($)'}, title="Asset Exposure")
            st.plotly_chart(fig, width="stretch")

else:
    st.info("👈 Select a target and click 'Run Pipeline' in the sidebar to begin.")
