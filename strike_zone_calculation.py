import pandas as pd # Import necessary libraries
import numpy as np

def is_strike(): 
    # This function's purpose is to take coordinate data from a trackman in order to determine 
    # whether a tracked pitch is a strike.
    
    # Load the data from the Master Data File
    data = pd.read_excel("trackmanData/Master Data File.xlsx", engine='openpyxl')
    data = data.dropna(subset=['TaggedPitchType','PlateLocHeight','PlateLocSide'])
    data = data[data['PitchSession'] != 'Warmup'] # Keeps only pitches tagged as 'live'

    # Define the strike zone boundaries
    # The dimensions of a strike zone are 17 inches wide (width of the plate) and roughly 20
    # inches high depending on the knee/waist height of the batter. For the sake of simplicity, 
    # and since we don't have data on batter heights, we will use 20 inches.
    # Additionally, a baseball is about 1.45 inches in radius. Trackman tracks locations from
    # The exact center point of the ball, meaning that we need to add a buffer equal to one ball
    # radius to our strike zone boundaries.

    upper_bound=40.45 # Inches off the ground
    lower_bound=17.55 # Inches off the ground
    left_bound=-9.95 # Inches from plate centerline
    right_bound=9.95 # Inches from plate centerline

    # Now, we can get the location data from trackman when the ball crosses the plate. 
    ballHeight_in=data['PlateLocHeight']*12 # Both converted from ft to in
    ballSide_in=data['PlateLocSide']*12

    zone_mask=( # Create a mask for the zone.
        (ballHeight_in>=lower_bound)
        &(ballHeight_in<=upper_bound)
        &(ballSide_in>=left_bound)
        &(ballSide_in<=right_bound)
    )

    # Apply mask
    data['IsStrike']=np.where(zone_mask,'Yes','No')
    return data