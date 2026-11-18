import base64
import time
from PIL import Image, ImageDraw
import pandas as pd
import requests
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

# Page display layout (optimized for iPad touch targets)
st.set_page_config(layout="wide", page_title="Session Tracker")

pitchtypes = [
    "Fastball",
    "Breaking Ball",
    "Offspeed"
]

@st.cache_data
def get_zone_image(width=360,height=450):
  img=Image.new("RGB", (width, height), color="#f8f9fa")
  draw=ImageDraw.Draw(img)

  # Outer canvas border
  draw.rectangle([0, 0, width-1, height-1], outline="#adb5bd", width=2)

  # Strike zone box (centered at x=180, y=215; width=160, height=210)
  z_left, z_right=100, 260
  z_top, z_bottom=110, 320
  draw.rectangle([z_left, z_top, z_right, z_bottom], outline="#212529", width=3)

  # 3x3 inner grid
  for i in (1, 2):
    x = z_left + i * (z_right - z_left) / 3
    y = z_top + i * (z_bottom - z_top) / 3
    draw.line([(x, z_top), (x, z_bottom)], fill="#dee2e6", width=1)
    draw.line([(z_left, y), (z_right, y)], fill="#dee2e6", width=1)

  # Home plate (catcher's perspective)
  plate = [(135, 385), (225, 385), (225, 405), (180, 425), (135, 405)]
  draw.polygon(plate, fill="#ffffff", outline="#212529", width=2)

  return img

def plot_in_zone(xloc,yloc,width=360,height=450):
  img=get_zone_image(width,height).copy()
  draw=ImageDraw.Draw(img)

  # Draw the pitch location as a red dot
  dot_radius = 5
  draw.ellipse(
      [
          (xloc - dot_radius, yloc - dot_radius),
          (xloc + dot_radius, yloc + dot_radius),
      ],
      fill="red",
      outline="black",
  )

  return img

def create_session():
  try:
    data = pd.read_csv("trackmanData/Master Data File.csv", low_memory=False)
    pitchers_list = data["Pitcher"].dropna().unique()
  except Exception:
    pitchers_list = []

  pitchers_today = st.multiselect(
      "Select pitchers throwing today", pitchers_list
  )

  if st.button("Start Session", type="primary") and pitchers_today:
    st.session_state.session_log = {
        "Date": [],
        "Pitch Number (Total)": [],
        "Pitcher": [],
        "Pitch Number (Individual)": [],
        "Outcome": [],
        "Count": [],
        "Pitch Type": [],
        "Velocity": [],
        "Location X": [],
        "Location Y": [],
        "Norm X": [],
        "Norm Y": []
    }
    st.session_state.indiv_pitchcount = {
        pitcher: 0 for pitcher in pitchers_today
    }
    st.session_state.date = pd.to_datetime("today").strftime("%m-%d-%Y")
    st.session_state.pitchers_today = pitchers_today
    return True
  return False


def log_pitch(session_log, pitcher, date):
  if "pitchcount" not in st.session_state:
    st.session_state.pitchcount = 0
  if "atbatcount" not in st.session_state:
    st.session_state.atbatcount = [0, 0]  # [balls, strikes]
  if "step" not in st.session_state:
    st.session_state.step = 1

  left_col, right_col = st.columns([1, 1], gap="medium")

  with left_col:
    if st.session_state.step == 1:
      st.session_state.count_before_pitch = (
          f"{st.session_state.atbatcount[0]}-{st.session_state.atbatcount[1]}"
      )
      st.session_state.prev_pitch_count = list(st.session_state.atbatcount)

      st.markdown("### Step 1: Enter Velocity")

      velo = st.number_input(
          "Pitch Velocity (mph)",
          min_value=0.0,
          max_value=115.0,
          value=None,
          step=0.1,
          format="%.1f",
          placeholder="Tap to enter velocity",
          key="velo_input",
      )

      v_col1, v_col2 = st.columns(2, gap="small")
      with v_col1:
        if st.button("Next", use_container_width=True, type="primary"):
          st.session_state.velocity = (
              round(velo, 1) if velo is not None else None
          )
          st.session_state.step = 2
          st.rerun()
      with v_col2:
        if st.button("Skip Velocity", use_container_width=True):
          st.session_state.velocity = None
          st.session_state.step = 2
          st.rerun()

    elif st.session_state.step == 2:
      if st.button("Back to Velocity", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

      st.markdown("### Step 2: Select Pitch Type")
      if st.session_state.velocity is not None:
        st.caption(f"Velocity: **{st.session_state.velocity} mph**")

      pt_col1, pt_col2 = st.columns(2, gap="small")
      selected_pitch_type = None

      for idx, pt in enumerate(pitchtypes):
        target_col = pt_col1 if idx % 2 == 0 else pt_col2
        with target_col:
          if st.button(pt, use_container_width=True, key=f"pt_{pt}"):
            selected_pitch_type = pt

      if selected_pitch_type:
        st.session_state.pitch_type = selected_pitch_type
        st.session_state.step = 3
        st.rerun()

    elif st.session_state.step == 3:
      nav1, nav2 = st.columns(2)
      with nav1:
        if st.button("Back to Pitch Type", use_container_width=True):
          st.session_state.step = 2
          st.rerun()
      with nav2:
        if st.button("Skip Location", use_container_width=True):
          st.session_state.loc_x = None
          st.session_state.loc_y = None
          st.session_state.norm_x = None
          st.session_state.norm_y = None
          st.session_state.step = 4
          st.rerun()

      st.markdown("### Step 3: Tap Pitch Location")
      st.caption(
          f"**{st.session_state.pitch_type}**"
          + (
              f" ({st.session_state.velocity} mph)"
              if st.session_state.velocity is not None
              else ""
          )
      )

      coords = streamlit_image_coordinates(
          get_zone_image(), key="strike_zone_tap"
      )

      if coords is not None and coords != st.session_state.last_click:
        st.session_state.last_click = coords
        st.session_state.loc_x = coords["x"]
        st.session_state.loc_y = coords["y"]
        # Normalized to strike zone box center (180, 215) & half-dimensions (80, 105)
        st.session_state.norm_x = round((coords["x"] - 180) / 80, 3)
        st.session_state.norm_y = round((215 - coords["y"]) / 105, 3)
        st.session_state.step = 4
        st.rerun()

    elif st.session_state.step == 4:
      if st.button("Back to Location", use_container_width=True):
        st.session_state.step = 3
        st.rerun()

      st.markdown("### Step 4: Select Pitch Outcome")

      col1, col2 = st.columns(2, gap="small")
      with col1:
        if st.button(
            "Strike", use_container_width=True, type="primary", key="btn_str"
        ):
          st.session_state.outcome = "Strike"
          st.session_state.step = "4_type"
          st.rerun()

        if st.button("Ball", use_container_width=True, key="btn_ball"):
          st.session_state.outcome = "Ball"
          st.session_state.atbatcount[0] += 1
          if st.session_state.atbatcount[0] == 4:
            st.session_state.pitchresult = "Base on Balls"
            st.session_state.atbatcount = [0, 0]
          else:
            st.session_state.pitchresult = "Ball"
          st.session_state.step = 5
          st.rerun()

      with col2:
        if st.button(
            "In Play", use_container_width=True, type="primary", key="btn_play"
        ):
          st.session_state.outcome = "In Play"
          st.session_state.step = "4_type"
          st.rerun()

        if st.button("Hit By Pitch", use_container_width=True, key="btn_hbp"):
          st.session_state.outcome = "Hit By Pitch"
          st.session_state.pitchresult = "Hit By Pitch"
          st.session_state.atbatcount = [0, 0]
          st.session_state.step = 5
          st.rerun()

    elif st.session_state.step == "4_type":
      if st.button("Back to Outcome", use_container_width=True):
        st.session_state.atbatcount = list(st.session_state.prev_pitch_count)
        st.session_state.step = 4
        st.rerun()

      if st.session_state.outcome == "Strike":
        st.markdown("### Step 4: Select Strike Type")
        s_col1, s_col2, s_col3 = st.columns(3)
        striketype = None

        with s_col1:
          if st.button("Swinging Strike", use_container_width=True):
            striketype = "Swinging Strike"
        with s_col2:
          if st.button("Called Strike", use_container_width=True):
            striketype = "Called Strike"
        with s_col3:
          if st.button("Foul", use_container_width=True):
            striketype = "Foul"

        if striketype:
          if striketype == "Foul" and st.session_state.atbatcount[1] == 2:
            pass  # Foul with 2 strikes keeps 2 strikes
          else:
            st.session_state.atbatcount[1] += 1

          if st.session_state.atbatcount[1] == 3:
            if striketype == "Swinging Strike":
              st.session_state.pitchresult = "Strikeout Swinging"
            elif striketype == "Called Strike":
              st.session_state.pitchresult = "Strikeout Looking"
            st.session_state.atbatcount = [0, 0]
          else:
            st.session_state.pitchresult = striketype

          st.session_state.step = 5
          st.rerun()

      elif st.session_state.outcome == "In Play":
        st.markdown("### Step 4: Select Contact Type")
        c1, c2 = st.columns(2)
        contacttype = None

        with c1:
          if st.button("Ground Ball", use_container_width=True):
            contacttype = "Ground Ball"
          if st.button("Fly Ball", use_container_width=True):
            contacttype = "Fly Ball"
        with c2:
          if st.button("Line Drive", use_container_width=True):
            contacttype = "Line Drive"
          if st.button("Popup", use_container_width=True):
            contacttype = "Popup"

        if contacttype:
          st.session_state.contacttype = contacttype
          st.session_state.step = "4_result"
          st.rerun()

    elif st.session_state.step == "4_result":
      if st.button("Back to Contact Type", use_container_width=True):
        st.session_state.step = "4_type"
        st.rerun()

      st.markdown("### Step 4: Select Play Result")
      r1, r2 = st.columns(2)
      playresult = None

      with r1:
        if st.button("Single", use_container_width=True):
          playresult = "Single"
        if st.button("Double", use_container_width=True):
          playresult = "Double"
        if st.button("Triple", use_container_width=True):
          playresult = "Triple"
        if st.button("Home Run", use_container_width=True):
          playresult = "Home Run"
      with r2:
        if st.button("Out", use_container_width=True, type="primary"):
          playresult = "Out"
        if st.button("Error", use_container_width=True):
          playresult = "Error"
        if st.button("Fielder's Choice", use_container_width=True):
          playresult = "Fielder's Choice"

      if playresult:
        st.session_state.atbatcount = [0, 0]
        if playresult == "Out":
          out_map = {
              "Ground Ball": "Groundout",
              "Line Drive": "Lineout",
              "Fly Ball": "Flyout",
              "Popup": "Popout",
          }
          st.session_state.pitchresult = out_map.get(
              st.session_state.contacttype, "Out"
          )
        else:
          st.session_state.pitchresult = playresult
        st.session_state.step = 5
        st.rerun()

    elif st.session_state.step == 5:
      next_indiv_count = (
          st.session_state.indiv_pitchcount.get(pitcher, 0) + 1
      )
      velo_display = (
          f"{st.session_state.velocity} mph"
          if st.session_state.velocity is not None
          else "N/A"
      )
      loc_display = (
          f"({st.session_state.norm_x}, {st.session_state.norm_y})"
          if st.session_state.norm_x is not None
          else "Skipped"
      )

      st.markdown("### Step 5: Confirm Pitch")

      info_col, preview_col = st.columns([1, 1], gap="small")
      with info_col:
        st.write(f"**Pitcher:** {pitcher}")
        st.write(f"**Pitch # ({pitcher}):** {next_indiv_count}")
        st.write(
            f"**Count Before Pitch:** {st.session_state.count_before_pitch}"
        )
        st.write(f"**Velocity:** {velo_display}")
        st.write(f"**Pitch Type:** {st.session_state.pitch_type}")
        st.write(f"**Zone Coords:** {loc_display}")
        st.write(f"**Outcome:** {st.session_state.pitchresult}")

      with preview_col:
        if (
            st.session_state.loc_x is not None
            and st.session_state.loc_y is not None
        ):
          preview_img = plot_in_zone(
              st.session_state.loc_x, st.session_state.loc_y
          )
          st.image(
              preview_img,
              caption="Selected Location",
              use_container_width=True,
          )
        else:
          st.info("Location skipped.")

      b_col1, b_col2, b_col3 = st.columns(3)
      with b_col1:
        if st.button("Confirm", use_container_width=True, type="primary"):
          st.session_state.pitchcount += 1
          st.session_state.indiv_pitchcount[pitcher] += 1
          st.session_state.session_log["Date"].append(date)
          st.session_state.session_log["Pitch Number (Total)"].append(
              st.session_state.pitchcount
          )
          st.session_state.session_log["Pitcher"].append(pitcher)
          st.session_state.session_log["Pitch Number (Individual)"].append(
              st.session_state.indiv_pitchcount[pitcher]
          )
          st.session_state.session_log["Count"].append(
              st.session_state.count_before_pitch
          )
          st.session_state.session_log["Outcome"].append(
              st.session_state.pitchresult
          )
          st.session_state.session_log["Pitch Type"].append(
              st.session_state.pitch_type
          )
          st.session_state.session_log["Velocity"].append(
              st.session_state.velocity
          )
          st.session_state.session_log["Location X"].append(
              st.session_state.loc_x
          )
          st.session_state.session_log["Location Y"].append(
              st.session_state.loc_y
          )
          st.session_state.session_log["Norm X"].append(
              st.session_state.norm_x
          )
          st.session_state.session_log["Norm Y"].append(
              st.session_state.norm_y
          )
          st.session_state.step = 1
          st.rerun()
      with b_col2:
        if st.button("Re-tap Location", use_container_width=True):
          st.session_state.atbatcount = list(st.session_state.prev_pitch_count)
          st.session_state.step = 3
          st.rerun()
      with b_col3:
        if st.button("Undo / Reset", use_container_width=True):
          st.session_state.atbatcount = list(st.session_state.prev_pitch_count)
          st.session_state.step = 1
          st.rerun()

  with right_col:
    st.markdown("### Last 5 Pitches Thrown")
    df_log = pd.DataFrame(st.session_state.session_log)

    if not df_log.empty:
      display_cols = [
          "Pitch Number (Individual)",
          "Pitcher",
          "Velocity",
          "Pitch Type",
          "Count",
          "Outcome",
          "Norm X",
          "Norm Y",
      ]
      recent_df = df_log[display_cols].tail(5).iloc[::-1]
      st.dataframe(recent_df, use_container_width=True, hide_index=True)
    else:
      st.info("No pitches logged yet in this session.")

  return st.session_state.session_log


if "session_log" not in st.session_state:
  create_session()
else:
  pitcher = st.selectbox(
      "Select Active Pitcher", st.session_state.pitchers_today
  )
  date = st.session_state.date
  log_pitch(st.session_state.session_log, pitcher, date)


def upload_to_github(csv_string, filename):
  try:
    token = st.secrets["GITHUB_TOKEN"]
    repo = st.secrets["GITHUB_REPO"]

    path = f"Tracked Sessions/{filename}"
    url = f"https://api.github.com/repos/{repo}/contents/{path}"

    content_b64 = base64.b64encode(csv_string.encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    payload = {
        "message": f"Add tracked pitch session CSV: {filename}",
        "content": content_b64,
    }

    response = requests.put(url, headers=headers, json=payload)
    return response.status_code in [200, 201]
  except Exception as e:
    st.error(f"GitHub Upload Error: {e}")
    return False


@st.dialog("Confirm End Session")
def confirm_end_session_dialog():
  st.write(
      "Are you sure you want to end this session? This will save your"
      " session log and upload it to GitHub."
  )

  col_yes, col_no = st.columns(2)
  with col_yes:
    if st.button("Yes, Save & End", use_container_width=True, type="primary"):
      timestamp = int(time.time())
      filename = f"session_{st.session_state.date}_{timestamp}.csv"

      df = pd.DataFrame(st.session_state.session_log)
      csv_data = df.to_csv(index=False)

      with st.spinner("Uploading session CSV to GitHub..."):
        success = upload_to_github(csv_data, filename)

      if success:
        st.success(f"Session saved to GitHub as `{filename}`!")
        for key in [
            "session_log",
            "step",
            "pitchcount",
            "atbatcount",
            "last_click",
        ]:
          if key in st.session_state:
            del st.session_state[key]
        st.rerun()
      else:
        st.error(
            "Failed to upload to GitHub. Please verify your secrets"
            " configuration."
        )

  with col_no:
    if st.button("Cancel", use_container_width=True):
      st.rerun()


st.divider()
if st.button("End Session", type="secondary", use_container_width=True):
  confirm_end_session_dialog()