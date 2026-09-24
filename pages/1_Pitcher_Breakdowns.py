import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from strike_zone_calculation import is_strike

# Cache the function to avoid re-running it on every interaction
@st.cache_data
def load_pitching_data():
  df=is_strike()

  # Format Date column for Streamlit date picker compatibility
  if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"]).dt.date

  return df
data=load_pitching_data()

st.title("Pitcher Breakdowns")
st.markdown("---")

# This page will be an easy way for coaches to explore metrics from individual players. 

# Remove missing values
data = data.dropna(subset=['TaggedPitchType','RelSpeed','SpinRate','HorzBreak','VertBreak','InducedVertBreak'])
data = data[data['PitchSession'] != 'Warmup'] # Keeps only pitches tagged as 'live'

st.sidebar.header("Filter Options") # This will filter by player and date.

# Date range Sidebar
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

# Pitcher Select Sidebar
pitcher_options = sorted(
    data["Pitcher"].dropna().unique().tolist()
)
selected_pitcher = st.sidebar.selectbox("Pitcher", options=pitcher_options)

# Chart options sidebar
st.sidebar.header("Chart Options") # This will allow user to choose different columns to display.

# We want to find the most important metrics for coaches to analyze. Most columns in the trackman 
# data file do not actually contain relevant information or require operations to glean meaningful 
# insight. Therefore, we will build our own list of column options.
column_options = {'Pitch Type': 'TaggedPitchType',
                  'Velocity':'RelSpeed',
                  'Spin Rate':'SpinRate',
                  'Strike/Ball':'IsStrike',
                  'Extension':'Extension',
                  'Release Height':'RelHeight',
                  'Release Side':'RelSide',
                  'Horizontal Break':'HorzBreak',
                  'Vertical Break':'VertBreak',
                  'Induced Vertical Break':'InducedVertBreak',
                  'Perceived Velocity':'EffVelocity'
                  }
selected_columns = st.sidebar.multiselect(
    "Pick Which Columns to Display", options=column_options, default=[]
)
raw_to_friendly = {v: k for k, v in column_options.items()} # This line is needed to convert display column names into the same names as in the dropdown menu.

# Filter data
filtered_data=data[data['Pitcher']==selected_pitcher].copy() # By pitcher

if date_range and isinstance(date_range, (tuple, list)) and len(date_range) == 2: # By date
  start_date, end_date = date_range
  filtered_df = filtered_data[
      (filtered_data["Date"] >= start_date) & (filtered_data["Date"] <= end_date)
  ]

# Reset index so pitch numbers start at 1 instead of taking indices from data file, which ranges into the thousands
filtered_data = filtered_data.sort_values(by="Date")
filtered_data = filtered_data.reset_index(drop=True)
filtered_data.index = filtered_data.index + 1
filtered_data.index.name = "Pitch #"

# Display columns
if filtered_data.empty:
    st.warning("No data found for the selected pitcher and date range.")
else:
    st.header(f"Performance Overview: {selected_pitcher}")

st.subheader("Pitch Log / Custom Columns Display")

raw_names=[column_options[col] for col in selected_columns]
display_columns=filtered_data[raw_names].rename(columns=raw_to_friendly)

# Round numbers
format={}
for col in display_columns.columns:
    if col=="Spin Rate":
        format[col]="{:.0f}"
    elif pd.api.types.is_numeric_dtype(display_columns[col]):
        format[col]="{:.2f}"

# Display all selected, formatted columns
st.dataframe(display_columns.style.format(format, na_rep="N/A"), use_container_width=True)
st.markdown("---")

# Display KPIs (total pitches, avg velo, max velo, strike pct for each pitch)

total_pitches=len(filtered_data)
strike_count = (filtered_data["IsStrike"] == "Strike").sum()
strike_pct = (strike_count / total_pitches * 100) if total_pitches > 0 else 0

st.markdown("### Metrics by Pitch Type")
summary_df = (
    filtered_data.groupby("TaggedPitchType")
    .agg(
        Pitches=("TaggedPitchType", "count"),
        Avg_Velo=("RelSpeed", "mean"),
        Max_Velo=("RelSpeed", "max"),
        Avg_Spin=("SpinRate", "mean"),
        Avg_IVB=("InducedVertBreak", "mean"),
        Avg_HB=("HorzBreak", "mean"),
        Strike_Pct=("IsStrike", lambda x: (x == "Strike").mean() * 100),
    )
    .reset_index()
    .rename(columns={
        "TaggedPitchType": "Pitch Type",
        "Avg_Velo": "Avg Velo",
        "Max_Velo": "Max Velo",
        "Avg_Spin": "Avg Spin",
        "Avg_IVB": "Avg IVB",
        "Avg_HB": "Avg HB",
        "Strike_Pct": "Strike %"
    })
)

st.dataframe(
    summary_df.style.format({
        "Avg Velo": "{:.1f}",
        "Max Velo": "{:.1f}",
        "Avg Spin": "{:.0f}",
        "Avg IVB": "{:.1f}",
        "Avg HB": "{:.1f}",
        "Strike %": "{:.1f}%"
    }),
    use_container_width=True
)

st.markdown("Note about strikes/balls: since the provided data only includes pitch metrics and not pitch outcomes, I cannot account for strikes due to whiffs or foul balls. The strike % number reflects only pitches physically inside the zone, and therefore is lower than expected. (I plan to add a pitch outcomes tracking feature soon.)")

# Display interactive visualizations

st.subheader("Visualizations")
tab_zone,tab_break,tab_violin=st.tabs(['Strike Zone','Movement Profile','Session Distributions']) # Create tabs for each visualization

with tab_zone: # Build strike zone vis
    fig_zone = px.scatter(
        filtered_data,
        x="PlateLocSide",
        y="PlateLocHeight",
        color="TaggedPitchType",
        hover_data=["RelSpeed","SpinRate","IsStrike"],
        title="Plate Location View (Catcher's Perspective)",
        labels={
            "PlateLocSide": "Horizontal Location (ft)",
            "PlateLocHeight": "Height Location (ft)",
            "TaggedPitchType": "Pitch Type",
            "IsStrike": "Strike Call"
        }
    )

    fig_zone.add_shape(
        type="rect",
        x0=-0.7083,
        x1=0.7083,
        y0=1.4625,
        y1=3.3708,
        line=dict(color="Red", width=3),
        fillcolor="rgba(255, 0, 0, 0.05)"
    )

    fig_zone.update_traces( # This adjusts plotted points to appear roughly the same size as a baseball relative to the graph size.
        marker=dict(
            size=22,                            
            line=dict(width=1, color="black")   
        )
    )

    fig_zone.update_xaxes(range=[-2.5, 2.5], title="Plate Side (ft)")
    fig_zone.update_yaxes(
        range=[0, 5], 
        title="Plate Height (ft)",
        scaleanchor="x",    # Forces equal aspect ratio so balls remain perfectly round
        scaleratio=1
    )
    fig_zone.update_layout(height=550)

    st.plotly_chart(fig_zone, use_container_width=True)

with tab_break: # Create break vis
    fig_break = px.scatter(
        filtered_data,
        x="HorzBreak",
        y="InducedVertBreak",
        color="TaggedPitchType",
        hover_data=["RelSpeed", "SpinRate", "IsStrike"],
        title="Movement Profile (Inches)",
        labels={
            "HorzBreak": "Horizontal Break (in)",
            "InducedVertBreak": "Induced Vertical Break (in)",
            "TaggedPitchType": "Pitch Type"
        }
    )

    # Crosshair axes at (0,0) center point
    fig_break.add_vline(x=0, line_dash="dash", line_color="gray", line_width=1.5)
    fig_break.add_hline(y=0, line_dash="dash", line_color="gray", line_width=1.5)

    # Standardize scale ranges
    fig_break.update_xaxes(range=[-30, 30], title="Horizontal Break (in)")
    fig_break.update_yaxes(range=[-30, 30], title="Induced Vertical Break (in)")
    fig_break.update_layout(height=550)

    st.plotly_chart(fig_break, use_container_width=True)

with tab_violin: # Create violin vis
    pitcher_pitch_types = sorted(filtered_data["TaggedPitchType"].dropna().unique().tolist()) # Create a filter for pitch type
    selected_violin_pitch = st.selectbox(
            "Select Pitch Type to Display:",
            options=pitcher_pitch_types,
            key="violin_pitch_type_filter"
        )
    violin_data = filtered_data.copy()

    # Converts dates to strings and sorts chronologically
    violin_data["Date"] = violin_data["Date"].astype(str)
    violin_data = violin_data.sort_values(by="Date")

    violin_data = violin_data[violin_data["TaggedPitchType"] == selected_violin_pitch] # Filters by pitch type

    # Calculate max, min, and mean velocity for each pitch type per session/date
    session_stats = (
        violin_data.groupby(["Date", "TaggedPitchType"])
        .agg(
            Min_Velo=("RelSpeed", "min"),
            Max_Velo=("RelSpeed", "max"),
            Mean_Velo=("RelSpeed", "mean"),
        )
        .reset_index()
    )
    violin_data = violin_data.merge(
        session_stats[["Date", "TaggedPitchType", "Min_Velo", "Max_Velo"]],
        on=["Date", "TaggedPitchType"],
    )
    # Assign distinct colors to each pitch type for consistency across violins and mean lines
    pitch_types = violin_data["TaggedPitchType"].unique()
    palette = px.colors.qualitative.Plotly
    color_map = {pt: palette[i % len(palette)] for i, pt in enumerate(pitch_types)}

    # 1. Base Violin Plot (Distribution of Velocity per Session)
    fig_violin = px.violin(
        violin_data,
        x="Date",
        y="RelSpeed",
        color="TaggedPitchType",
        color_discrete_map=color_map,
        custom_data=["Min_Velo", "Max_Velo"], # This is needed to format the tooltips that are displayed when hovering over a violin. Otherwise, they display a lot of unnecessary information.
        box=True, 
        points="all",
        title="Pitch Velocity Distribution & Mean Trend Over Time",
        labels={
            "Date": "Date",
            "RelSpeed": "Velocity (MPH)",
            "TaggedPitchType": "Pitch Type",
        },
    )

    # This removes displaying unneeded info such as quartiles when hovering over the violin. I asked AI how to do this. Also adjusts violin scale for readability
    fig_violin.update_traces(hoverinfo="skip", hovertemplate=None, scalemode="width")

    # 2. Overlay Mean Lines Connecting Session Averages
    for pt in pitch_types:
        pt_stats = session_stats[session_stats["TaggedPitchType"] == pt]
        fig_violin.add_trace(
            go.Scatter(
                x=pt_stats["Date"],
                y=pt_stats["Mean_Velo"],
                mode="lines+markers",
                name=f"{pt} Mean",
                line=dict(color=color_map[pt], width=3, dash="dash"),
                marker=dict(size=8, symbol="diamond", color=color_map[pt]),
                legendgroup=pt,  # Groups with corresponding pitch type in legend
                customdata=pt_stats[["Min_Velo","Max_Velo"]],
                hovertemplate=f"<b>{pt} Mean</b><br>Session: %{{x}}<br>Avg Velocity: %{{y:.1f}} MPH<extra></extra>",
            )
        )

    # 3. Layout Formatting
    fig_violin.update_layout(
        hovermode="closest",
        violinmode="group",
        violingap=0,
        violingroupgap=0,
        height=550,
        xaxis_title="Date",
        yaxis_title="Velocity (MPH)",
    )

    st.plotly_chart(fig_violin, use_container_width=True)