import streamlit as st # Import streamlit, pandas, and the function from the calculation file
import pandas as pd
from Stuff_plus_calculation import run_stuff_plus_calculation

# Cache the function to avoid re-running it on every interaction
@st.cache_data
def load_pitching_data():
    return run_stuff_plus_calculation()

data=load_pitching_data()

st.title("TrackMan Stuff+ Analytics")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Filter Options")

# 1. Pitcher Handedness Filter
throws_options = ["All"] + sorted(
    data["PitcherThrows"].dropna().unique().tolist()
)
selected_hand = st.sidebar.selectbox("Pitcher Handedness", options=throws_options)

# 2. Pitch Type Filter
pitch_options = sorted(data["TaggedPitchType"].dropna().unique().tolist())
selected_pitches = st.sidebar.multiselect(
    "Pitch Types", options=pitch_options, default=pitch_options
)

# 3. Pitcher Select Filter
pitcher_options = ["All Pitchers"] + sorted(
    data["Pitcher"].dropna().unique().tolist()
)
selected_pitcher = st.sidebar.selectbox("Pitcher", options=pitcher_options)

# 4. Minimum Pitches Filter
min_pitches = st.sidebar.slider(
    "Minimum Pitches Thrown", min_value=1, max_value=100, value=10, step=1
)

# --- FILTER DATA ---
filtered_df = data.copy()

if selected_hand != "All":
  filtered_df = filtered_df[filtered_df["PitcherThrows"] == selected_hand]

if selected_pitches:
  filtered_df = filtered_df[
      filtered_df["TaggedPitchType"].isin(selected_pitches)
  ]

if selected_pitcher != "All Pitchers":
  filtered_df = filtered_df[filtered_df["Pitcher"] == selected_pitcher]

# --- SECTION 1: PITCHER & PITCH TYPE LEADERBOARD ---
st.subheader("Average Stuff+ Leaderboard (by Pitcher & Pitch Type)")

leaderboard = (
    filtered_df.groupby(["Pitcher", "PitcherThrows", "TaggedPitchType"])
    .agg(
        Pitches=("Stuff+", "count"),
        AvgVelo=("RelSpeed", "mean"),
        StuffPlus=("Stuff+", "mean"),
    )
    .reset_index()
)

# Apply sample size threshold and sort by highest StuffPlus
leaderboard = leaderboard[leaderboard["Pitches"] >= min_pitches]
leaderboard = leaderboard.sort_values(by="StuffPlus", ascending=False)

# Format display columns
leaderboard["AvgVelo"] = leaderboard["AvgVelo"].round(1)
leaderboard["StuffPlus"] = leaderboard["StuffPlus"].round(0).astype(int)

st.dataframe(
    leaderboard,
    column_config={
        "Pitcher": "Pitcher",
        "PitcherThrows": "Hand",
        "TaggedPitchType": "Pitch Type",
        "Pitches": "Pitches Thrown",
        "AvgVelo": st.column_config.NumberColumn("Avg Velo", format="%.1f mph"),
        "StuffPlus": st.column_config.NumberColumn(
            "StuffPlus", help="100 is League Average", format="%d"
        ),
    },
    use_container_width=True,
    hide_index=True,
)

# --- SECTION 2: TOP INDIVIDUAL PITCH THROWS ---
st.subheader("🔥 Top Individual Pitches Tracked")

top_n = st.slider("Number of top pitches to show", 5, 50, 10)

top_pitches = (
    filtered_df.sort_values(by="Stuff+", ascending=False)
    .head(top_n)[
        [
            "Pitcher",
            "PitcherThrows",
            "TaggedPitchType",
            "RelSpeed",
            "SpinRate",
            "Stuff+",
        ]
    ]
    .copy()
)

top_pitches["RelSpeed"] = top_pitches["RelSpeed"].round(1)
top_pitches["SpinRate"] = top_pitches["SpinRate"].round(0)
top_pitches["Stuff+"] = top_pitches["Stuff+"].round(0).astype(int)

st.dataframe(
    top_pitches,
    column_config={
        "PitcherThrows": "Hand",
        "TaggedPitchType": "Pitch Type",
        "RelSpeed": st.column_config.NumberColumn("Velo", format="%.1f mph"),
        "SpinRate": st.column_config.NumberColumn("Spin Rate", format="%d rpm"),
        "Stuff+": st.column_config.NumberColumn("Stuff+", format="%d"),
    },
    use_container_width=True,
    hide_index=True,
)