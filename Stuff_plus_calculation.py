import pandas as pd #Import necessary libraries
import numpy as np

def run_stuff_plus_calculation():
    data=pd.read_excel('trackmanData/Master Data File.xlsx', engine='openpyxl') # Read in data

    # Drop all rows with missing values in the 'TaggedPitchType' column and 'Warmup' in the 'PitchSession' column, as these are not relevant to the analysis
    data = data.dropna(subset=['TaggedPitchType'])
    data = data[data['PitchSession'] != 'Warmup'] # Keeps only pitches tagged as 'live'

    # We also need to drop any rows with missing values in the metric columns, as they are necessary for the calculations. This will ensure that we only have complete data for each pitch.
    data = data.dropna(subset=['RelSpeed', 'SpinRate', 'HorzBreak', 'VertBreak', 'InducedVertBreak'])

    # Pull out necessary columns for calculations (Velo, Spin, HB, VB, IVB)
    velocity=data['RelSpeed'].round(2)
    spinRate=data['SpinRate'].round(0)
    horzBreak=data['HorzBreak'].round(2)
    vertBreak=data['VertBreak'].round(2)
    inducedVertBreak=data['InducedVertBreak'].round(2)

    # Separate each series into pitch types (FB, SNK, CUT, SL, CB, SW, CH, SP)

    fbVelo=velocity[data['TaggedPitchType']=='Fastball']
    fbSpin=spinRate[data['TaggedPitchType']=='Fastball']
    fbHB=horzBreak[data['TaggedPitchType']=='Fastball']
    fbVB=vertBreak[data['TaggedPitchType']=='Fastball']
    fbIVB=inducedVertBreak[data['TaggedPitchType']=='Fastball']

    snkVelo=velocity[data['TaggedPitchType']=='Sinker']
    snkSpin=spinRate[data['TaggedPitchType']=='Sinker']
    snkHB=horzBreak[data['TaggedPitchType']=='Sinker']
    snkVB=vertBreak[data['TaggedPitchType']=='Sinker']
    snkIVB=inducedVertBreak[data['TaggedPitchType']=='Sinker']

    cutVelo=velocity[data['TaggedPitchType']=='Cutter']
    cutSpin=spinRate[data['TaggedPitchType']=='Cutter']
    cutHB=horzBreak[data['TaggedPitchType']=='Cutter']
    cutVB=vertBreak[data['TaggedPitchType']=='Cutter']
    cutIVB=inducedVertBreak[data['TaggedPitchType']=='Cutter']

    slVelo=velocity[data['TaggedPitchType']=='Slider']
    slSpin=spinRate[data['TaggedPitchType']=='Slider']
    slHB=horzBreak[data['TaggedPitchType']=='Slider']
    slVB=vertBreak[data['TaggedPitchType']=='Slider']
    slIVB=inducedVertBreak[data['TaggedPitchType']=='Slider']

    cbVelo=velocity[data['TaggedPitchType']=='Curveball']
    cbSpin=spinRate[data['TaggedPitchType']=='Curveball']
    cbHB=horzBreak[data['TaggedPitchType']=='Curveball']
    cbVB=vertBreak[data['TaggedPitchType']=='Curveball']
    cbIVB=inducedVertBreak[data['TaggedPitchType']=='Curveball']

    swVelo=velocity[data['TaggedPitchType']=='Sweeper']
    swSpin=spinRate[data['TaggedPitchType']=='Sweeper']
    swHB=horzBreak[data['TaggedPitchType']=='Sweeper']
    swVB=vertBreak[data['TaggedPitchType']=='Sweeper']
    swIVB=inducedVertBreak[data['TaggedPitchType']=='Sweeper']

    chVelo=velocity[data['TaggedPitchType']=='ChangeUp']
    chSpin=spinRate[data['TaggedPitchType']=='ChangeUp']
    chHB=horzBreak[data['TaggedPitchType']=='ChangeUp']
    chVB=vertBreak[data['TaggedPitchType']=='ChangeUp']
    chIVB=inducedVertBreak[data['TaggedPitchType']=='ChangeUp']

    spVelo=velocity[data['TaggedPitchType']=='Splitter']
    spSpin=spinRate[data['TaggedPitchType']=='Splitter']
    spHB=horzBreak[data['TaggedPitchType']=='Splitter']
    spVB=vertBreak[data['TaggedPitchType']=='Splitter']
    spIVB=inducedVertBreak[data['TaggedPitchType']=='Splitter']

    # Normalize the data by converting values to a 0-100 scale based on the min and max values for each pitch type

    fbVeloNorm=((fbVelo-fbVelo.min())/(fbVelo.max()-fbVelo.min()))*100
    fbSpinNorm=((fbSpin-fbSpin.min())/(fbSpin.max()-fbSpin.min()))*100
    fbHBNorm=((fbHB-fbHB.min())/(fbHB.max()-fbHB.min()))*100
    fbVBNorm=((fbVB-fbVB.min())/(fbVB.max()-fbVB.min()))*100
    fbIVBNorm=((fbIVB-fbIVB.min())/(fbIVB.max()-fbIVB.min()))*100

    snkVeloNorm=((snkVelo-snkVelo.min())/(snkVelo.max()-snkVelo.min()))*100
    snkSpinNorm=((snkSpin-snkSpin.min())/(snkSpin.max()-snkSpin.min()))*100
    snkHBNorm=((snkHB-snkHB.min())/(snkHB.max()-snkHB.min()))*100
    snkVBNorm=((snkVB-snkVB.min())/(snkVB.max()-snkVB.min()))*100
    snkIVBNorm=((snkIVB-snkIVB.min())/(snkIVB.max()-snkIVB.min()))*100

    cutVeloNorm=((cutVelo-cutVelo.min())/(cutVelo.max()-cutVelo.min()))*100
    cutSpinNorm=((cutSpin-cutSpin.min())/(cutSpin.max()-cutSpin.min()))*100
    cutHBNorm=((cutHB-cutHB.min())/(cutHB.max()-cutHB.min()))*100
    cutVBNorm=((cutVB-cutVB.min())/(cutVB.max()-cutVB.min()))*100
    cutIVBNorm=((cutIVB-cutIVB.min())/(cutIVB.max()-cutIVB.min()))*100

    slVeloNorm=((slVelo-slVelo.min())/(slVelo.max()-slVelo.min()))*100
    slSpinNorm=((slSpin-slSpin.min())/(slSpin.max()-slSpin.min()))*100
    slHBNorm=((slHB-slHB.min())/(slHB.max()-slHB.min()))*100
    slVBNorm=((slVB-slVB.min())/(slVB.max()-slVB.min()))*100
    slIVBNorm=((slIVB-slIVB.min())/(slIVB.max()-slIVB.min()))*100

    cbVeloNorm=((cbVelo-cbVelo.min())/(cbVelo.max()-cbVelo.min()))*100
    cbSpinNorm=((cbSpin-cbSpin.min())/(cbSpin.max()-cbSpin.min()))*100
    cbHBNorm=((cbHB-cbHB.min())/(cbHB.max()-cbHB.min()))*100
    cbVBNorm=((cbVB-cbVB.min())/(cbVB.max()-cbVB.min()))*100
    cbIVBNorm=((cbIVB-cbIVB.min())/(cbIVB.max()-cbIVB.min()))*100

    swVeloNorm=((swVelo-swVelo.min())/(swVelo.max()-swVelo.min()))*100
    swSpinNorm=((swSpin-swSpin.min())/(swSpin.max()-swSpin.min()))*100
    swHBNorm=((swHB-swHB.min())/(swHB.max()-swHB.min()))*100
    swVBNorm=((swVB-swVB.min())/(swVB.max()-swVB.min()))*100
    swIVBNorm=((swIVB-swIVB.min())/(swIVB.max()-swIVB.min()))*100

    # For the changeup, the case is special. We will normalize based on the difference between each pitcher's average fastball velocity and the average changeup velocity. The sweet spot is an 8mph difference, so we will use that as the max value for normalization. 
    # The min value will be a 0mph difference, which is the worst case scenario. Any difference higher than 8 will fall off until 12 mph, which will also be a minimum value.

    pitchers = data['Pitcher'].unique()
    chVeloNorm = {}

    for i in pitchers:
        pitcher_data = data[data['Pitcher'] == i]

        # Isolate pitch types for each pitcher
        fb_pitches = pitcher_data[pitcher_data['TaggedPitchType'].isin(['Fastball', 'Sinker', 'Cutter'])]
        ch_pitches = pitcher_data[pitcher_data['TaggedPitchType'] == 'ChangeUp']

        if ch_pitches.empty or fb_pitches.empty:
            continue

        pitcher_fbVelo = fb_pitches['RelSpeed'].mean()
        pitcher_chVelo = ch_pitches['RelSpeed'].mean()

        pitcher_diff = pitcher_fbVelo - pitcher_chVelo

        # 2. Two part normalization (0-8 mph climbing, 8-12 mph falling off)
        if pitcher_diff <= 0 or pitcher_diff >= 12:
            chVeloScore = 0.0
        elif pitcher_diff <= 8:
            # Scales from 0 mph (score 0) to 8 mph (score 100)
            chVeloScore = (pitcher_diff / 8.0) * 100
        else:
            # Falls off from 8 mph (score 100) to 12 mph (score 0)
            chVeloScore = ((12.0 - pitcher_diff) / 4.0) * 100

        chVeloNorm[i] = chVeloScore.round(2)

    # Other changeup metrics will be normalized like the other pitch types, using the min and max values for each metric across all pitchers.

    chSpinNorm=((chSpin-chSpin.min())/(chSpin.max()-chSpin.min()))*100
    chHBNorm=((chHB-chHB.min())/(chHB.max()-chHB.min()))*100
    chVBNorm=((chVB-chVB.min())/(chVB.max()-chVB.min()))*100
    chIVBNorm=((chIVB-chIVB.min())/(chIVB.max()-chIVB.min()))*100

    spVeloNorm=((spVelo-spVelo.min())/(spVelo.max()-spVelo.min()))*100
    spSpinNorm=((spSpin-spSpin.min())/(spSpin.max()-spSpin.min()))*100
    spHBNorm=((spHB-spHB.min())/(spHB.max()-spHB.min()))*100
    spVBNorm=((spVB-spVB.min())/(spVB.max()-spVB.min()))*100
    spIVBNorm=((spIVB-spIVB.min())/(spIVB.max()-spIVB.min()))*100

    # Determine different weights for each metric based on their importance to the quality of each pitch type. For example, velocity is more important for a fastball than a changeup, while spin rate is more important for a curveball than a fastball.

    fbVeloWeight=0.4
    fbSpinWeight=0.1
    fbHBWeight=0.1
    fbVBWeight=0.05
    fbIVBWeight=0.35

    snkVeloWeight=0.35
    snkSpinWeight=0.10
    snkHBWeight=0.35
    snkVBWeight=0.05
    snkIVBWeight=0.15

    cutVeloWeight=0.35
    cutSpinWeight=0.10
    cutHBWeight=0.30
    cutVBWeight=0.05
    cutIVBWeight=0.20

    slVeloWeight=0.35
    slSpinWeight=0.15
    slHBWeight=0.25
    slVBWeight=0.05
    slIVBWeight=0.20

    cbVeloWeight=0.15
    cbSpinWeight=0.25
    cbHBWeight=0.15
    cbVBWeight=0.05
    cbIVBWeight=0.40

    swVeloWeight=0.20
    swSpinWeight=0.20
    swHBWeight=0.45
    swVBWeight=0.05
    swIVBWeight=0.10

    chVeloWeight=0.30
    chSpinWeight=0.10
    chHBWeight=0.30
    chVBWeight=0.05
    chIVBWeight=0.25

    spVeloWeight=0.30
    spSpinWeight=0.10
    spHBWeight=0.15
    spVBWeight=0.05
    spIVBWeight=0.40

    # Now that we have our normalized values and weights, we can calculate the overall score for each individual pitch by multiplying the normalized value by its weight and summing them up.

    # Create a new column in the dataframe to hold the StuffScore for each pitch. The below code will also create masks to correctly map each series to the dataframe based on the pitch type.
    data['StuffScore'] = 0.0

    fb_mask = data['TaggedPitchType'] == 'Fastball'
    data.loc[fb_mask, 'StuffScore'] = (
        (fbVeloNorm * fbVeloWeight)
        + (fbSpinNorm * fbSpinWeight)
        + (fbHBNorm * fbHBWeight)
        + (fbVBNorm * fbVBWeight)
        + (fbIVBNorm * fbIVBWeight)
    )

    snk_mask = data['TaggedPitchType'] == 'Sinker'
    data.loc[snk_mask, 'StuffScore'] = (
        (snkVeloNorm * snkVeloWeight)
        + (snkSpinNorm * snkSpinWeight)
        + (snkHBNorm * snkHBWeight)
        + (snkVBNorm * snkVBWeight)
        + (snkIVBNorm * snkIVBWeight)
    )

    cut_mask = data['TaggedPitchType'] == 'Cutter'
    data.loc[cut_mask, 'StuffScore'] = (
        (cutVeloNorm * cutVeloWeight)
        + (cutSpinNorm * cutSpinWeight)
        + (cutHBNorm * cutHBWeight)
        + (cutVBNorm * cutVBWeight)
        + (cutIVBNorm * cutIVBWeight)
    )

    sl_mask = data['TaggedPitchType'] == 'Slider'
    data.loc[sl_mask, 'StuffScore'] = (
        (slVeloNorm * slVeloWeight)
        + (slSpinNorm * slSpinWeight)
        + (slHBNorm * slHBWeight)
        + (slVBNorm * slVBWeight)
        + (slIVBNorm * slIVBWeight)
    )

    cb_mask = data['TaggedPitchType'] == 'Curveball'
    data.loc[cb_mask, 'StuffScore'] = (
        (cbVeloNorm * cbVeloWeight)
        + (cbSpinNorm * cbSpinWeight)
        + (cbHBNorm * cbHBWeight)
        + (cbVBNorm * cbVBWeight)
        + (cbIVBNorm * cbIVBWeight)
    )

    sw_mask = data['TaggedPitchType'] == 'Sweeper'
    data.loc[sw_mask, 'StuffScore'] = (
        (swVeloNorm * swVeloWeight)
        + (swSpinNorm * swSpinWeight)
        + (swHBNorm * swHBWeight)
        + (swVBNorm * swVBWeight)
        + (swIVBNorm * swIVBWeight)
    )

    ch_mask = data['TaggedPitchType'] == 'ChangeUp'
    ch_velo_scores = data.loc[ch_mask, 'Pitcher'].map(chVeloNorm).fillna(0.0)
    data.loc[ch_mask, 'StuffScore'] = (
        (ch_velo_scores * chVeloWeight)
        + (chSpinNorm * chSpinWeight)
        + (chHBNorm * chHBWeight)
        + (chVBNorm * chVBWeight)
        + (chIVBNorm * chIVBWeight)
    )

    sp_mask = data['TaggedPitchType'] == 'Splitter'
    data.loc[sp_mask, 'StuffScore'] = (
        (spVeloNorm * spVeloWeight)
        + (spSpinNorm * spSpinWeight)
        + (spHBNorm * spHBWeight)
        + (spVBNorm * spVBWeight)
        + (spIVBNorm * spIVBWeight)
    )

    data['StuffScore'] = data['StuffScore'].round(2) # Round the StuffScore to 2 decimal places

    # Now that we have calculated the StuffScore for each pitch, we can create Stuff+ scores. An average pitch has a Stuff+ score of 100, so for example, a pitch with a 120 Stuff+ would be 20% better than average, while 90 Stuff+ would be 10% worse than average.

    data['Stuff+'] = round((data['StuffScore'] / data['StuffScore'].mean()) * 100,0)
    return data
