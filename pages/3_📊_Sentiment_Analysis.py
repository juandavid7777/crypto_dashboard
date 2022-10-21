import pandas as pd
import numpy as np
import streamlit as strl

from functions import bounded_metric, colored_metric, api_btc_hist_price, api_gn_hist_data, api_fg_hist_data, plot_graphs

strl.set_page_config(layout="wide", page_title="BTC metrics - Sentiment", page_icon = "📊")

df_thresholds = pd.read_csv("thresholds.csv")
df_meta = df_thresholds[df_thresholds["type"].isin(["Sentiment"])]

col_bounded, col_colored= strl.columns(2)

with col_bounded:
    plot_graphs(df_meta, colored = False)

with col_colored:
    plot_graphs(df_meta, colored = True)