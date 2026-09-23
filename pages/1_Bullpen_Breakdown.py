import streamlit as st
import pandas as pd
st.title("Bullpen Breakdown")

# This page will be an easy way for coaches to explore metrics from individual players. 
# First, import data
data=pd.read_excel("trackmanData/Master Data File.xlsx", engine='openpyxl')

# Remove duplicate rows and missing values
data = data.dropna(subset=['TaggedPitchType'])
data = data[data['PitchSession'] != 'Warmup'] # Keeps only pitches tagged as 'live'

st.sidebar.header("Filter Options") # This will filter by player and date.

# Date range filter
date_range = None
if "Date" in data.columns:
  min_date = data["Date"].min()
  max_date = data["Date"].max()
  date_range = st.sidebar.date_input(
      "Date Range",
      value=(min_date, max_date),
      min_value=min_date,
      max_value=max_date
  )

# Pitcher Select Filter
pitcher_options = sorted(
    data["Pitcher"].dropna().unique().tolist()
)
selected_pitcher = st.sidebar.selectbox("Pitcher", options=pitcher_options)

st.sidebar.header("Chart Options") # This will allow user to choose different columns to display.

# We want to find the most important metrics for coaches to analyze. Most columns in the trackman 
# data file do not actually contain relevant information or require operations to glean meaningful 
# insight. Therefore, we will build our own list of column options.
column_options = {'Pitch Type': 'TaggedPitchType',
                  'Velocity':'RelSpeed',
                  'Spin Rate':'SpinRate',
                  'Strike':'IsStrike',
                  
                  }
selected_columns = st.sidebar.multiselect(
    "Pick Which Columns to Display", options=column_options, default=[]
)

