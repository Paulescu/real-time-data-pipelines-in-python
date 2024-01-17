import streamlit as st
# import plotly.express as px
import pandas as pd
import time
import os
import datetime
import logging

from src.utils import initialize_logger, load_env_vars
from src.backend import get_features

initialize_logger()
load_env_vars()

logger = logging.getLogger()

# Basic configuration of the Streamlit dashboard
st.set_page_config(
    page_title="Real-Time OHLC data for crypto products",
    page_icon="✅",
    layout="wide",
    menu_items={
        'About': "This dashboard shows real-time OHLC data computed from Kraken API using Quix Streams"
    }
)

st.header("Real-Time OHLC data", divider="blue")
st.markdown(
"""This dashboard vizualizes real-time OHLC data computed from Kraken API using [Quix Streams](https://github.com/quixio/quix-streams).

* To explore the back-end services that power this Dashboard, check out [this repository](https://github.com/Paulescu/real-time-data-pipelines-in-python)

""")

default_height = 2000

with st.container():
    col11, col12 = st.columns(2)
    # col11 = st.columns(1)
    with col11:
        # Header of the first column
        st.header("Trades in the last 5 minutes")
        # A placeholder for the first chart to update it later with data
        placeholder_col11 = st.empty()

    with col12:
        # Header of the second column
        st.header("User stats in the last 5 minutes")
        # A placeholder for the second chart to update it later with data
        placeholder_col12 = st.empty()

while True:

    # Fetch ohlc data from the feature store
    features : pd.DataFrame = get_features(last_minutes=5)

    with placeholder_col11.container():    
        # plot it as Streamlit Dataframe
        st.dataframe(features,
                     hide_index=True,
                     use_container_width=True,
                     height=default_height)

    with placeholder_col12.container():    
        # plot it as Candle chart
        from src.plot import get_candlestick_plot
        p = get_candlestick_plot(features, window_seconds=10)
        st.bokeh_chart(p, use_container_width=True)
        
        # st.dataframe(features,
        #              hide_index=True,
        #              use_container_width=True,
        #              height=default_height)
        
    # Wait for one second before asking for new data from Quix
    time.sleep(1)