import pandas as pd
import numpy as np
import plotly.graph_objects as go

import requests
import os

import scipy.stats as st
from scipy.stats import norm
import matplotlib.dates as dates
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn import metrics
from datetime import date
import datetime

import streamlit as strl

def bullet_fig_metric(value_in,
                      previous_val,
                      title_text,
                      ranges,
                      color_ranges = ["greenyellow", "lemonchiffon", "sandybrown", "lightcoral"],
                      color_comments = ["green", "gold", "darkorange", "red"],
                      format_num = ".2f",
                      log_scale = False):
  
    #Data preprocessing
    
      #Adds middle range
    ranges.insert(2, (ranges[1]+ranges[2])/2)
    
     #Changes format for axis
    format_string = '{:' + format_num + '}'
    ranges_labels = [format_string.format(item) for item in ranges]
    
      #Defines input chart values
    if log_scale == False:
        bar_value = value_in
        marker_value = bar_value
        ranges_plot = ranges

    else:
        bar_value = np.log10(value_in)
        marker_value = np.log10(value_in)
        ranges_plot = np.log10(ranges).tolist() 

      #Comments generation
    if value_in <= ranges[1]:
        comment = "Bottom"
        comment_color = color_comments[0]

    elif (value_in <= ranges[2]) & (value_in > ranges[1]):
        comment = "Mid Bottom"
        comment_color = color_comments[1]

    elif (value_in <= ranges[3]) & (value_in > ranges[2]):
        comment = "Mid top"
        comment_color = color_comments[2]

    else:
        comment = "Peaking"
        comment_color = color_comments[3]

    #Plots bullet figure
    fig = go.Figure(go.Indicator(
        mode = "number+gauge+delta",
        value = value_in,
        number = {'valueformat':format_num , "font": {"size" : 15 }},
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text' :"<b>" + title_text + "</b><br><span style='color: " + comment_color + "; font-size:0.7em'>" + comment + "</span>",
                  "font": {"size" : 15 }},
        delta = {'reference': previous_val, "relative" : False, 'valueformat':format_num},
        gauge = {
            'shape': "bullet",
            'axis': {"range": [ranges_plot[0], ranges_plot[-1]],
                     "tickmode":"array",
                     "tickvals":ranges_plot,
                     "ticktext": ranges_labels,
                     "tickformat":format_num,
                     "tickangle":90},      
            'threshold': {
                'line': {'color': "mediumblue", 'width': 3},
                'thickness': 0.9,
                'value': marker_value},
            'steps': [
                {'range': [ranges_plot[0], ranges_plot[1]], 'color': color_ranges[0]},
                {'range': [ranges_plot[1], ranges_plot[2]], 'color': color_ranges[1]},
                {'range': [ranges_plot[2], ranges_plot[3]], 'color': color_ranges[2]},
                {'range': [ranges_plot[3], ranges_plot[4]], 'color': color_ranges[3]}
            ],
            'bar':{'color':'black',
                  "thickness":0}
            }))

    fig.update_layout(
        margin=dict(l=130, r=30, t=15, b=70),
        height = 120,
        width = 500
    )

    return fig
    
    
    
def api_gn_bullet_data(metric, api_ID):

    #URL required for metric
    filename_metric = metric
    url = api_ID #source of info for price

    #Parameters required for metric
    api_key = strl.secrets["API_TOKEN"]
    a = "BTC"    #token
    s = '2020-01-01' #start date - not mandatory
    u = '2021-01-01' #until date - not mandatory
    i = '24h'         #time step
    f = "CSV"        #output format 
    timestamp_format = "humanized" #time stamp format

    #Compiles parameters
    params = (("a", a),("i", i),("f", f),("timestamp_format",timestamp_format ),("api_key", api_key))

    #Generates data requests and extracts the content
    r = requests.get(url, params)
    r_content = r.content

    #Writes the CSV temporary file
    csv_file = open(filename_metric+'.csv', 'wb')
    csv_file.write(r_content)
    csv_file.close()

    #Reads dataframe from temp file
    df = pd.read_csv(filename_metric+'.csv', parse_dates = [0], dayfirst = True)
    
    #Deletes file
#     os.remove(filename_metric+'.csv')
    
    #Gets the results
    days_prev = 90
    
    val = df.value.iloc[-1]
    prev_val = df.value.iloc[-days_prev]
    min_val = df.value.min()
    max_val = df.value.max()

    return val, prev_val, min_val, max_val
    
    
def api_fg_bullet_data(metric, api_ID):
    
    #URL required for metric
    filename_metric = metric
    url = api_ID #source of info for price
    
    #Generates data requests and extracts the content
    r = requests.get(url)
    r_content = r.content

    #Writes the CSV file
    csv_file = open(filename_metric+'.csv', 'wb')
    csv_file.write(r_content)
    csv_file.close()

    #Cleans an formats database
        #Slices correct data
    df_fg = pd.read_csv(filename_metric+'.csv', header = 3)
#     os.remove(filename_metric+'.csv')
    df_fg = df_fg.iloc[:-5]

        #Renames data
    df_fg = df_fg.rename(columns={"fng_value": "Date", "fng_classification": "fg", "date":"fg_cat"})

        #Sets Date as index
    df_fg['Date']= pd.to_datetime(df_fg['Date'], utc = True, dayfirst = True)
    df_fg = df_fg.set_index("Date").sort_index()

    #Removes blank data
    df_fg = df_fg.fillna(method='ffill')
    
    #Makes fear index between 0-1
    df_fg["fg"] = df_fg["fg"]/100

    #Creates a moving averae of F&G for cleaning extremes
    fg_roll = 90
    df_fg["fg_MA"] = df_fg["fg"].rolling(fg_roll).mean()

    #Gets the results
    days_prev = 90
    
    if filename_metric == "Fear and Greed":
        val = df_fg.fg.iloc[-1]
        prev_val = df_fg.fg.iloc[-days_prev]
        min_val = df_fg.fg.min()
        max_val =df_fg.fg.max()

    else:
        val = df_fg.fg_MA.iloc[-1]
        prev_val = df_fg.fg_MA.iloc[-days_prev]
        min_val = df_fg.fg.min()
        max_val =df_fg.fg.max()

    return val, prev_val, min_val, max_val
    
    
    
def api_tech_bullet_data (metric, api_ID):
    
    filename_metric = metric
    url = api_ID #source of info for price

    #Parameters required for metric
    api_key = strl.secrets["API_TOKEN"]
    a = "BTC"    #token
    s = '2020-01-01' #start date - not mandatory
    u = '2021-01-01' #until date - not mandatory
    i = '24h'         #time step
    f = "CSV"        #output format 
    timestamp_format = "humanized" #time stamp format

    #Compiles parameters
    params = (("a", a),("i", i),("f", f),("timestamp_format",timestamp_format ),("api_key", api_key))

    #Generates data requests and extracts the content
    r = requests.get(url, params)
    r_content = r.content

    #Writes the CSV temporary file
    csv_file = open(filename_metric+'.csv', 'wb')
    csv_file.write(r_content)
    csv_file.close()

    #Reads dataframe from temp file
    dfp = pd.read_csv(filename_metric+'.csv', parse_dates = [0], dayfirst = True)
    os.remove(filename_metric+'.csv')

    #Renames colums
    dfp = dfp.rename(columns={"timestamp": "Date", "c": "close", "h":"high", "l":"low", "o":"open" })

    #Removes blank data
    dfp = dfp.fillna(method='ffill')

    #Estimates number of days since inception "X"
    df = dfp
    df["DSI"] = df.index + 1
    df['Date']= pd.to_datetime(df['Date'], utc = True)
    df = df.set_index("Date")

    # 4.Fitting Polynomial Regression to the price
    X = np.log(df["DSI"].values).reshape(-1,1)
    Y = np.log(df["close"].values).reshape(-1,1)
    poly_reg = PolynomialFeatures(degree=3) #Defines the polinomial degree
    X_poly = poly_reg.fit_transform(X)
    pol_reg = LinearRegression()
    pol_reg.fit(X_poly, Y)

    #Estimates the regressed price
    df["price_reg"] = np.exp(pol_reg.predict(poly_reg.fit_transform(np.log(df["DSI"].values.reshape(-1,1)))))

    #Summary statistics
    SE_reg = np.sqrt(metrics.mean_squared_error(np.log(df.close), np.log(df.price_reg)))
    R2_reg = metrics.r2_score(np.log(df.close), np.log(df.price_reg))

    #5. Creates a normalization variable
    df["norm_dist"] = df.apply(lambda x: norm.cdf(np.log(x['close']), np.log(x['price_reg']), SE_reg),axis = 1)

    #6. Defines time (day) parameters for risk. Roll_long cannot be more than 326 as it will exclude the peak
    roll_short = 7
    roll_long = 350 #interesting 140

    #Moving average and risk index generated
    df["MA_short"] = df["close"].rolling(roll_short).mean()
    df["MA_long"] = df["close"].rolling(roll_long).mean()

    #Risk according to moving averages
    df["risk_MA"] = np.log(df["MA_short"]/df["MA_long"])

    SE_risk_MA = df["risk_MA"].std()
    mean_risk_MA = df["risk_MA"].mean()

    #Creates a normalization variable
    df["risk_MA_norm"] = df.apply(lambda x: norm.cdf(x['risk_MA'], mean_risk_MA, SE_risk_MA),axis = 1)

    #Gets the results
    days_prev = 90

    if metric == "MA log rat":
        var_select = "risk_MA_norm"
        val = df[var_select].iloc[-1]
        prev_val = df[var_select].iloc[-days_prev]
        min_val = df[var_select].min()
        max_val = df[var_select].max()

    else:
        var_select = "norm_dist"
        val = df[var_select].iloc[-1]
        prev_val = df[var_select].iloc[-days_prev]
        min_val = df[var_select].min()
        max_val =df[var_select].max()

    return val, prev_val, min_val, max_val
