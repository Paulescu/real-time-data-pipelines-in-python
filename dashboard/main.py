import streamlit as st
# import plotly.express as px
import pandas as pd
import time
import os
import datetime
import logging

from src.utils import initialize_logger, load_env_vars
from src.backend import get_trades_from_feature_store

initialize_logger()
load_env_vars()

logger = logging.getLogger()

# Basic configuration of the Streamlit dashboard
st.set_page_config(
    page_title="Real-Time User Stats Dashboard (Quix)",
    page_icon="✅",
    layout="wide",
    menu_items={
        'About': "This dashboard shows real-time user stats the Clickstream Analysis template. More info at https://quix.io/templates"
    }
)

st.header("Real-Time User Analytics Dashboard", divider="blue")
st.markdown(
"""This dashboard vizualizes real-time agreggations and statistics from a demo clickstream. The clickstream data is being streamed from a sample log file for an online retailer and processed in a Pipeline hosted in Quix—a cloud-native solution for building event streaming applications.

* To explore the back-end services that power this Dashboard, check out the [Pipeline view](https://portal.platform.quix.io/pipeline?workspace=demo-clickstream-prod&token=pat-b88b3caf912641a1b0fa8b47b262868b) in Quix.

* To see how real-time clickstream analysis can be used to trigger events in a front end, see our accompanying [Clickstream Event Detection demo](https://template-clickstream-front-end.vercel.app/)
""")

default_height = 200

with st.container():
    # col11, col12, col13 = st.columns(3)
    col11 = st.columns(1)
    with col11:
        # Header of the first column
        st.header("Trades in the last 5 minutes")
        # A placeholder for the first chart to update it later with data
        placeholder_col11 = st.empty()

while True:

    with placeholder_col11.container():
        
        # Fetch trades from the feature store
        trades : pd.DataFrame = get_trades_from_feature_store(last_minutes=5)

        # plot it as Streamlit Dataframe
        st.dataframe(trades,
                     hide_index=True,
                     use_container_width=True,
                     height=default_height)

    # Wait for one second before asking for new data from Quix
    time.sleep(1)