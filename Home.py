import pandas as pd
import numpy as np
import plotly.graph_objects as go

import requests
# import os

import scipy.stats as st
from scipy.stats import norm
import matplotlib.dates as dates
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn import metrics
from datetime import date
import datetime

import streamlit as st


# from functions import api_gn_bullet_data, api_tech_bullet_data, api_fg_bullet_data, bullet_fig_metric

st.write("first point")

# df_thresholds = pd.read_csv("thresholds.csv")

# df = df_thresholds[df_thresholds["type"].isin(["Onchain", "Sentiment", "Technical"])]

    
# # Runs functions in loops
# for i, metric in enumerate(df["metric_name"]):
    
#     # Defines the source of data to be used
#     if df.iloc[i]["type"] == "Onchain":
#         val, prev_val, min_val, max_val = api_gn_bullet_data(metric, df.iloc[i]["api_id"])
#     elif df.iloc[i]["type"] == "Technical":
#         val, prev_val, min_val, max_val = api_tech_bullet_data(metric, df.iloc[i]["api_id"])
#     else:
#         val, prev_val, min_val, max_val = api_fg_bullet_data(metric, df.iloc[i]["api_id"])
    
#     # Defines ranges to be used
#     if df.iloc[i]["custom_limit"] == True:
#         range_vals = [df.iloc[i]["min"], df.iloc[i]["low"], df.iloc[i]["high"], df.iloc[i]["max"]]
        
#     else:
#         range_vals = [min_val, df.iloc[i]["low"], df.iloc[i]["high"], max_val]

#     # Plots data
#     fig = bullet_fig_metric(value_in = val,
#                   previous_val = prev_val,
#                   title_text = metric,
#                   ranges = range_vals,
#                   format_num = df.iloc[i]["format"],
#                   log_scale = df.iloc[i]["log_scale"]
#                   )
    
#     st.plotly_chart(fig, use_container_width=True)

    
    
    
st.write("second point")
