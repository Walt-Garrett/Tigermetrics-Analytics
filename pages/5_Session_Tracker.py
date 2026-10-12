# This page is for tracking pitch outcomes, which allows for improved accuracy of strike/ball calls.
import streamlit as st
import pandas as pd
import requests
import base64
import time

# Page display layout (optimized for ipad, as that will be the recording device)
st.set_page_config(layout="wide", page_title="Session Tracker")


# Firstly, we will create a dictionary with the following keys: Date, Pitcher, Pitch Number (Specific to that pitcher), and outcome.
def create_session():
    data=pd.read_excel("trackmanData/Master Data File.xlsx", engine='openpyxl') # Read in pitcher names
    pitchers_today=st.multiselect('Select pitchers throwing today',data['Pitcher'].unique())
    # Display all selected pitchers to ensure they are correct
    if st.button('Start Session') and pitchers_today:
        st.session_state.session_log={
            'Date':[],
            'Pitch Number (Total)':[],
            'Pitcher':[],
            'Pitch Number (Individual)':[],
            'Outcome':[],
            'Count':[]
        }
        # separate dictionary to track individual pitch counts
        st.session_state.indiv_pitchcount={pitcher:0 for pitcher in pitchers_today}
        st.session_state.date=pd.to_datetime('today').strftime('%m-%d-%Y')
        st.session_state.pitchers_today=pitchers_today
        return True
    return False

def log_pitch(session_log,pitcher,date):
    # Initialize state variables in st.session_state so they are not rewritten on every interaction
    if 'pitchcount' not in st.session_state:
        st.session_state.pitchcount=0
    if 'atbatcount' not in st.session_state:
        st.session_state.atbatcount=[0,0]  # [balls, strikes]
    if 'step' not in st.session_state:
        st.session_state.step=1 
     # This variable tracks which "step" of logging is in process. 
     # It will determine which dropdowns are displayed. 
     # For example: Outcome is step 1, while strike type is step 2, etc.

    left_col,right_col=st.columns([1,1],gap='medium') # Sets where info will display on the screen

    # Next, we need to create options for each pitch outcome
    with left_col:
            
            if st.session_state.step==1:
                outcome=st.selectbox('Pitch Outcome',
                                     ['SELECT','Strike','Ball','In Play','Hit By Pitch'],
                                     key='outcome_selection')
                if st.button('Next') and outcome!='SELECT':
                    st.session_state.count_before_pitch=f"{st.session_state.atbatcount[0]}-{st.session_state.atbatcount[1]}"
                    st.session_state.prev_pitch_count=list(st.session_state.atbatcount) # This saves the count from the previous pitch so it can be restored if the user undoes an action.
                    st.session_state.outcome=outcome
                    st.session_state.step=2
                    st.rerun()
            elif st.session_state.step==2:
                if st.session_state.outcome=='Strike':
                    striketype=st.selectbox('Strike Type',['SELECT','Swinging Strike','Called Strike','Foul'],key='strike_selection')
                    if st.button('Next') and striketype!='SELECT':
                        if striketype=='Foul' and st.session_state.atbatcount[1]==2:
                            st.session_state.atbatcount[1]+=0
                        else:
                            st.session_state.atbatcount[1]+=1
                        if st.session_state.atbatcount[1]==3:
                            if striketype=='Swinging Strike':
                                st.session_state.pitchresult='Strikeout Swinging'
                                st.session_state.atbatcount=[0,0] # Reset at bat count since 3 strikes ends the at bat
                            elif striketype=='Called Strike':
                                st.session_state.pitchresult='Strikeout Looking'
                                st.session_state.atbatcount=[0,0] # Reset at bat count since 3 strikes ends the at bat
                        else:
                            st.session_state.pitchresult=striketype
                        st.session_state.step=4 # Skip step 3 since it is only for In Play outcomes
                        st.rerun()
                elif st.session_state.outcome=='In Play':
                    contacttype=st.selectbox('Contact Type',['SELECT','Ground Ball','Line Drive','Fly Ball','Popup'],key='contact_selection')
                    if st.button('Next') and contacttype!='SELECT':
                        st.session_state.contacttype=contacttype
                        st.session_state.step=3
                        st.rerun()
                elif st.session_state.outcome=='Ball':
                    st.session_state.atbatcount[0]+=1
                    if st.session_state.atbatcount[0]==4:
                        st.session_state.pitchresult='Base on Balls'
                        st.session_state.atbatcount=[0,0] # Reset at bat count since 4 balls ends the at bat
                    else:
                        st.session_state.pitchresult='Ball'
                    st.session_state.step=4 # Skip step 3 since it is only for In Play outcomes
                    st.rerun()
                elif st.session_state.outcome=='Hit By Pitch':
                    st.session_state.atbatcount=[0,0] # Reset at bat count since HBP ends the at bat
                    st.session_state.step=4
                    st.session_state.pitchresult='Hit By Pitch'
                    st.rerun()
            elif st.session_state.step==3:
                playresult=st.selectbox('Result',['SELECT','Single','Double','Triple','Home Run','Error',"Fielder's Choice",'Out'],key='result_selection')
                if st.button('Next') and playresult!='SELECT':
                    st.session_state.atbatcount=[0,0] # Reset at bat count since In Play ends the at bat
                    if playresult=='Out':
                        if st.session_state.contacttype=='Ground Ball':
                            st.session_state.pitchresult='Groundout'
                        elif st.session_state.contacttype=='Line Drive':
                            st.session_state.pitchresult='Lineout'
                        elif st.session_state.contacttype=='Fly Ball':
                            st.session_state.pitchresult='Flyout'
                        elif st.session_state.contacttype=='Popup':
                            st.session_state.pitchresult='Popout'
                    else:
                        st.session_state.pitchresult=playresult
                    st.session_state.step=4
                    st.rerun()
            else:
                # Final step: Display pitch summary and add confirm/undo buttons. Once it is confirmed, the pitch will be logged into the dictionary and the state variables will be reset for the next pitch.
                next_indiv_count=st.session_state.indiv_pitchcount.get(pitcher, 0) + 1
                
                st.write("### Confirm Pitch")
                st.write(f"**Pitcher:** {pitcher}")
                st.write(f"**Pitch # ({pitcher}):** {next_indiv_count}")
                st.write(f"**Count Before Pitch:** {st.session_state.count_before_pitch}")
                st.write(f"**Outcome:** {st.session_state.pitchresult}")
        
                b_col1,b_col2=st.columns(2)
                with b_col1:
                    if st.button('Confirm'):
                        st.session_state.pitchcount += 1
                        st.session_state.indiv_pitchcount[pitcher]+=1
                        st.session_state.session_log['Date'].append(date)
                        st.session_state.session_log['Pitch Number (Total)'].append(st.session_state.pitchcount)
                        st.session_state.session_log['Pitcher'].append(pitcher)
                        st.session_state.session_log['Pitch Number (Individual)'].append(st.session_state.indiv_pitchcount[pitcher])
                        st.session_state.session_log['Count'].append(st.session_state.count_before_pitch)
                        st.session_state.session_log['Outcome'].append(st.session_state.pitchresult)
                        st.session_state.step=1
                        st.rerun()
                with b_col2:
                    if st.button('Undo'):
                        # Reset state variables for next pitch without logging
                        st.session_state.step=1
                        st.session_state.atbatcount=list(st.session_state.prev_pitch_count)
                        st.rerun()
    with right_col:
        st.markdown("### Last 5 Pitches Thrown")
        df_log = pd.DataFrame(st.session_state.session_log)
        
        if not df_log.empty:
            # Display last 5 pitches in reverse order so latest pitch is on top
            recent_df = df_log.tail(5).iloc[::1]
            st.dataframe(recent_df, use_container_width=True, hide_index=True)
        else:
            st.info("No pitches logged yet in this session.")
    return st.session_state.session_log

if 'session_log' not in st.session_state:
    create_session()
else:
    pitcher=st.selectbox("Select Active Pitcher", st.session_state.pitchers_today)
    date=st.session_state.date

    # Call log_pitch with session state variables
    log_pitch(st.session_state.session_log, pitcher, date)

# Function to upload CSV directly to GitHub repository (I asked gemini to help me with this)
def upload_to_github(csv_string, filename):
    try:
        token=st.secrets["GITHUB_TOKEN"]
        repo=st.secrets["GITHUB_REPO"]  # Format: "Username/Repository"
        
        path=f"Tracked Sessions/{filename}"
        url=f"https://api.github.com/repos/{repo}/contents/{path}"
        
        # Base64 encode the CSV text for the GitHub REST API
        content_b64=base64.b64encode(csv_string.encode('utf-8')).decode('utf-8')
        
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        payload={
            "message": f"Add tracked pitch session CSV: {filename}",
            "content": content_b64
        }
        
        response=requests.put(url, headers=headers, json=payload)
        return response.status_code in [200, 201]
    except Exception as e:
        st.error(f"GitHub Upload Error: {e}")
        return False

# End session confirmation modal
@st.dialog("Confirm End Session")
def confirm_end_session_dialog():
    st.write("Are you sure you want to end this session? This will save your session log and upload it to GitHub.")
    
    col_yes, col_no=st.columns(2)
    with col_yes:
        if st.button("Yes, Save & End", use_container_width=True, type="primary"):
            timestamp=int(time.time())
            filename=f"session_{st.session_state.date}_{timestamp}.csv"
            
            # Convert session log dictionary directly to CSV string
            df=pd.DataFrame(st.session_state.session_log)
            csv_data=df.to_csv(index=False)
            
            with st.spinner("Uploading session CSV to GitHub..."):
                success=upload_to_github(csv_data, filename)
            
            if success:
                st.success(f"Session saved to GitHub as `{filename}`!")
                # Reset session state variables
                del st.session_state.session_log
                if 'step' in st.session_state:
                    del st.session_state.step
                st.rerun()
            else:
                st.error("Failed to upload to GitHub. Please verify your secrets configuration.")

    with col_no:
        if st.button("Cancel", use_container_width=True):
            st.rerun()

st.divider()
if st.button("End Session", type="secondary", use_container_width=True):
    confirm_end_session_dialog()



        
