import pandas as pd
import numpy as np
import streamlit as strl

from functions import bounded_metric, colored_metric, api_btc_hist_price, api_gn_hist_data, api_fg_hist_data, plot_graphs, api_tech_hist_data


strl.set_page_config(layout="wide", page_title="BTC metrics - Technical", page_icon = "📈")

# Title
strl.image("technical_strip.png", use_column_width = True)
# strl.markdown('<b style="color:darkgoldenrod ; font-size: 44px">Technical</b>', unsafe_allow_html=True)

# Summary
strl.markdown("""---""")


df_thresholds = pd.read_csv("thresholds.csv")
df_meta = df_thresholds[df_thresholds["type"].isin(["Technical"])]

col_bounded, col_colored= strl.columns(2)

with col_bounded:
    strl.subheader("Oscillators thresholds")
    plot_graphs(df_meta, colored = False)

with col_colored:
    strl.subheader("Colored distribution")
    plot_graphs(df_meta, colored = True)