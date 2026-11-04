import pandas as pd
import numpy as np

def effective_velocity_calculation():
    # This function is an improvement on Trackman's method of calculating effective velocity.
    # Trackman calculates eff. velo by taking only the release speed and the extension, when there
    # are a number of other factors that can affect the perceived velocity of a pitch.
    # I will be using release speed, extension, movement (IVB and HB), location, and batter handedness to more accurately depict perceived velocity.
    df=pd.read_csv("trackmanData/Master Data File.csv")
    fastball_df=df[df['TaggedPitchType']=='Fastball'] # Split fastballs out
    fastball_df=fastball_df[fastball_df['PitchSession']!='Warmup']
        # Drop all rows with missing values in the columns we care about
    fastball_df=fastball_df.dropna(subset=['ReleaseSpeed','ZoneSpeed','Extension','HorzBreak','InducedVertBreak','PlateLocHeight','PlateLocSide'])
    fastball_df['HorzBreak']=fastball_df['HorzBreak'].abs() # Take abs. val of HB so handedness does not skew the average
    fastball_df['TotalBreak']=np.sqrt(fastball_df['HorzBreak']**2+fastball_df['InducedVertBreak']**2) # Finds total break of each pitch
    fastball_df['VeloLoss']=fastball_df['ReleaseSpeed']-fastball_df['ZoneSpeed'] # Finds the difference between release speed and speed at the plate
    # Take the team average values of each column, not including location
    team_avg_release_speed=fastball_df['ReleaseSpeed'].mean()
    team_avg_zone_speed=fastball_df['ZoneSpeed'].mean()
    team_avg_velo_loss=fastball_df['VeloLoss'].mean()
    team_avg_extension=fastball_df['Extension'].mean()
    team_avg_horz_break=fastball_df['HorzBreak'].mean()
    team_avg_vert_break=fastball_df['InducedVertBreak'].mean()

    # I asked Gemini to find the extension value where the trackman effective velocity calculation 
    # resulted in 0 change from release speed. After a regression, it found 6.38 ft
    extension_component=(fastball_df['Extension']-6.38)*1.5 # roughly 1.5 mph added for every foot of extension above this baseline
    break_component=fastball_df['TotalBreak']*0.1 # 1 mph added for every 10 in total break
    drag_component=team_avg_velo_loss-fastball_df['VeloLoss'] # If a pitch loses less velo than the team average, it is perceived as faster
    effective_velocity=fastball_df['ReleaseSpeed']+extension_component+break_component+drag_component