import pandas as pd
import numpy as np
import streamlit as strl

from functions import bounded_metric, colored_metric, api_btc_hist_price, api_gn_hist_data, api_fg_hist_data, plot_graphs

strl.set_page_config(layout="wide", page_title="BTC metrics - Machine Learning", page_icon = "📊")

# Title
strl.image("sentiment_strip.png", use_column_width = True)
# strl.markdown('<b style="color:darkgoldenrod ; font-size: 44px">Sentiment</b>', unsafe_allow_html=True)

# Summary
strl.markdown("""---""")

df_thresholds = pd.read_csv("thresholds.csv")
df_meta = df_thresholds[df_thresholds["type"].isin(["Sentiment"])]