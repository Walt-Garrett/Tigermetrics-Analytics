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
    horzBreak=abs(data['HorzBreak']).round(2) # Since horizontal break can be either positive (to the right side of the pitcher) or negative (to the left side), we need to convert it to an absolute value for fair scoring.
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

    chVeloWeight=0.35
    chSpinWeight=0.10
    chHBWeight=0.25
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

    # My coaches have also requested that I calculate stuff+ scores as if they were on an MLB scale, where 100 is the MLB average instead of Trinity Average.
    # First, define the MLB average values for each pitch type. I asked Gemini to pull these values from the Google Statcast page, which has listed averages of all my metrics from qualified MLB pitchers in 2026.

    mlb_benchmarks_df = pd.DataFrame([ # These are average mlb values for each pitch type that will be appended to the dataframe.
        {'PitchSession': 'MLB_Benchmark', 'Pitcher': 'MLB_Avg', 'TaggedPitchType': 'Fastball', 'RelSpeed': 93.8, 'SpinRate': 2280, 'HorzBreak': 7.5, 'VertBreak': 15.5, 'InducedVertBreak': 15.8},
        {'PitchSession': 'MLB_Benchmark', 'Pitcher': 'MLB_Avg', 'TaggedPitchType': 'Sinker', 'RelSpeed': 93.1, 'SpinRate': 2150, 'HorzBreak': 14.2, 'VertBreak': 8.5, 'InducedVertBreak': 8.5},
        {'PitchSession': 'MLB_Benchmark', 'Pitcher': 'MLB_Avg', 'TaggedPitchType': 'Cutter', 'RelSpeed': 89.2, 'SpinRate': 2350, 'HorzBreak': 2.5, 'VertBreak': 7.2, 'InducedVertBreak': 7.2},
        {'PitchSession': 'MLB_Benchmark', 'Pitcher': 'MLB_Avg', 'TaggedPitchType': 'Slider', 'RelSpeed': 84.8, 'SpinRate': 2420, 'HorzBreak': 4.2, 'VertBreak': 1.8, 'InducedVertBreak': 1.8},
        {'PitchSession': 'MLB_Benchmark', 'Pitcher': 'MLB_Avg', 'TaggedPitchType': 'Curveball', 'RelSpeed': 79.2, 'SpinRate': 2510, 'HorzBreak': 8.1, 'VertBreak': -9.2, 'InducedVertBreak': -9.2},
        {'PitchSession': 'MLB_Benchmark', 'Pitcher': 'MLB_Avg', 'TaggedPitchType': 'Sweeper', 'RelSpeed': 81.5, 'SpinRate': 2550, 'HorzBreak': 14.5, 'VertBreak': 1.0, 'InducedVertBreak': 1.0},
        {'PitchSession': 'MLB_Benchmark', 'Pitcher': 'MLB_Avg', 'TaggedPitchType': 'ChangeUp', 'RelSpeed': 85.1, 'SpinRate': 1750, 'HorzBreak': 13.8, 'VertBreak': 6.1, 'InducedVertBreak': 6.1},
        {'PitchSession': 'MLB_Benchmark', 'Pitcher': 'MLB_Avg', 'TaggedPitchType': 'Splitter', 'RelSpeed': 85.5, 'SpinRate': 1300, 'HorzBreak': 8.0, 'VertBreak': 4.0, 'InducedVertBreak': 4.0},
    ])

    # Append MLB rows to data so they can be used in the normalization
    data = pd.concat([data, mlb_benchmarks_df], ignore_index=True)

    # Now, we take these average pitches and normalize them on the Trinity Scale.
    # Pull out necessary columns for calculations (Velo, Spin, HB, VB, IVB)
    velocity_MLB=data['RelSpeed'].round(2)
    spinRate_MLB=data['SpinRate'].round(0)
    horzBreak_MLB=abs(data['HorzBreak']).round(2) # Since horizontal break can be either positive (to the right side of the pitcher) or negative (to the left side), we need to convert it to an absolute value for fair scoring.
    vertBreak_MLB=data['VertBreak'].round(2)
    inducedVertBreak_MLB=data['InducedVertBreak'].round(2)

    # Separate each series into pitch types (FB, SNK, CUT, SL, CB, SW, CH, SP)

    fbVelo_MLB=velocity_MLB[data['TaggedPitchType']=='Fastball']
    fbSpin_MLB=spinRate_MLB[data['TaggedPitchType']=='Fastball']
    fbHB_MLB=horzBreak_MLB[data['TaggedPitchType']=='Fastball']
    fbVB_MLB=vertBreak_MLB[data['TaggedPitchType']=='Fastball']
    fbIVB_MLB=inducedVertBreak_MLB[data['TaggedPitchType']=='Fastball']

    snkVelo_MLB=velocity_MLB[data['TaggedPitchType']=='Sinker']
    snkSpin_MLB=spinRate_MLB[data['TaggedPitchType']=='Sinker']
    snkHB_MLB=horzBreak_MLB[data['TaggedPitchType']=='Sinker']
    snkVB_MLB=vertBreak_MLB[data['TaggedPitchType']=='Sinker']
    snkIVB_MLB=inducedVertBreak_MLB[data['TaggedPitchType']=='Sinker']

    cutVelo_MLB=velocity_MLB[data['TaggedPitchType']=='Cutter']
    cutSpin_MLB=spinRate_MLB[data['TaggedPitchType']=='Cutter']
    cutHB_MLB=horzBreak_MLB[data['TaggedPitchType']=='Cutter']
    cutVB_MLB=vertBreak_MLB[data['TaggedPitchType']=='Cutter']
    cutIVB_MLB=inducedVertBreak_MLB[data['TaggedPitchType']=='Cutter']

    slVelo_MLB=velocity_MLB[data['TaggedPitchType']=='Slider']
    slSpin_MLB=spinRate_MLB[data['TaggedPitchType']=='Slider']
    slHB_MLB=horzBreak_MLB[data['TaggedPitchType']=='Slider']
    slVB_MLB=vertBreak_MLB[data['TaggedPitchType']=='Slider']
    slIVB_MLB=inducedVertBreak_MLB[data['TaggedPitchType']=='Slider']

    cbVelo_MLB=velocity_MLB[data['TaggedPitchType']=='Curveball']
    cbSpin_MLB=spinRate_MLB[data['TaggedPitchType']=='Curveball']
    cbHB_MLB=horzBreak_MLB[data['TaggedPitchType']=='Curveball']
    cbVB_MLB=vertBreak_MLB[data['TaggedPitchType']=='Curveball']
    cbIVB_MLB=inducedVertBreak_MLB[data['TaggedPitchType']=='Curveball']

    swVelo_MLB=velocity_MLB[data['TaggedPitchType']=='Sweeper']
    swSpin_MLB=spinRate_MLB[data['TaggedPitchType']=='Sweeper']
    swHB_MLB=horzBreak_MLB[data['TaggedPitchType']=='Sweeper']
    swVB_MLB=vertBreak_MLB[data['TaggedPitchType']=='Sweeper']
    swIVB_MLB=inducedVertBreak_MLB[data['TaggedPitchType']=='Sweeper']

    chVelo_MLB=velocity_MLB[data['TaggedPitchType']=='ChangeUp']
    chSpin_MLB=spinRate_MLB[data['TaggedPitchType']=='ChangeUp']
    chHB_MLB=horzBreak_MLB[data['TaggedPitchType']=='ChangeUp']
    chVB_MLB=vertBreak_MLB[data['TaggedPitchType']=='ChangeUp']
    chIVB_MLB=inducedVertBreak_MLB[data['TaggedPitchType']=='ChangeUp']

    spVelo_MLB=velocity_MLB[data['TaggedPitchType']=='Splitter']
    spSpin_MLB=spinRate_MLB[data['TaggedPitchType']=='Splitter']
    spHB_MLB=horzBreak_MLB[data['TaggedPitchType']=='Splitter']
    spVB_MLB=vertBreak_MLB[data['TaggedPitchType']=='Splitter']
    spIVB_MLB=inducedVertBreak_MLB[data['TaggedPitchType']=='Splitter']

    # Normalize the data by converting values to a 0-100 scale based on the min and max values for each pitch type

    fbVeloNorm_MLB=((fbVelo_MLB-fbVelo_MLB.min())/(fbVelo_MLB.max()-fbVelo_MLB.min()))*100
    fbSpinNorm_MLB=((fbSpin_MLB-fbSpin_MLB.min())/(fbSpin_MLB.max()-fbSpin_MLB.min()))*100
    fbHBNorm_MLB=((fbHB_MLB-fbHB_MLB.min())/(fbHB_MLB.max()-fbHB_MLB.min()))*100
    fbVBNorm_MLB=((fbVB_MLB-fbVB_MLB.min())/(fbVB_MLB.max()-fbVB_MLB.min()))*100
    fbIVBNorm_MLB=((fbIVB_MLB-fbIVB_MLB.min())/(fbIVB_MLB.max()-fbIVB_MLB.min()))*100

    snkVeloNorm_MLB=((snkVelo_MLB-snkVelo_MLB.min())/(snkVelo_MLB.max()-snkVelo_MLB.min()))*100
    snkSpinNorm_MLB=((snkSpin_MLB-snkSpin_MLB.min())/(snkSpin_MLB.max()-snkSpin_MLB.min()))*100
    snkHBNorm_MLB=((snkHB_MLB-snkHB_MLB.min())/(snkHB_MLB.max()-snkHB_MLB.min()))*100
    snkVBNorm_MLB=((snkVB_MLB-snkVB_MLB.min())/(snkVB_MLB.max()-snkVB_MLB.min()))*100
    snkIVBNorm_MLB=((snkIVB_MLB-snkIVB_MLB.min())/(snkIVB_MLB.max()-snkIVB_MLB.min()))*100

    cutVeloNorm_MLB=((cutVelo_MLB-cutVelo_MLB.min())/(cutVelo_MLB.max()-cutVelo_MLB.min()))*100
    cutSpinNorm_MLB=((cutSpin_MLB-cutSpin_MLB.min())/(cutSpin_MLB.max()-cutSpin_MLB.min()))*100
    cutHBNorm_MLB=((cutHB_MLB-cutHB_MLB.min())/(cutHB_MLB.max()-cutHB_MLB.min()))*100
    cutVBNorm_MLB=((cutVB_MLB-cutVB_MLB.min())/(cutVB_MLB.max()-cutVB_MLB.min()))*100
    cutIVBNorm_MLB=((cutIVB_MLB-cutIVB_MLB.min())/(cutIVB_MLB.max()-cutIVB_MLB.min()))*100

    slVeloNorm_MLB=((slVelo_MLB-slVelo_MLB.min())/(slVelo_MLB.max()-slVelo_MLB.min()))*100
    slSpinNorm_MLB=((slSpin_MLB-slSpin_MLB.min())/(slSpin_MLB.max()-slSpin_MLB.min()))*100
    slHBNorm_MLB=((slHB_MLB-slHB_MLB.min())/(slHB_MLB.max()-slHB_MLB.min()))*100
    slVBNorm_MLB=((slVB_MLB-slVB_MLB.min())/(slVB_MLB.max()-slVB_MLB.min()))*100
    slIVBNorm_MLB=((slIVB_MLB-slIVB_MLB.min())/(slIVB_MLB.max()-slIVB_MLB.min()))*100

    cbVeloNorm_MLB=((cbVelo_MLB-cbVelo_MLB.min())/(cbVelo_MLB.max()-cbVelo_MLB.min()))*100
    cbSpinNorm_MLB=((cbSpin_MLB-cbSpin_MLB.min())/(cbSpin_MLB.max()-cbSpin_MLB.min()))*100
    cbHBNorm_MLB=((cbHB_MLB-cbHB_MLB.min())/(cbHB_MLB.max()-cbHB_MLB.min()))*100
    cbVBNorm_MLB=((cbVB_MLB-cbVB_MLB.min())/(cbVB_MLB.max()-cbVB_MLB.min()))*100
    cbIVBNorm_MLB=((cbIVB_MLB-cbIVB_MLB.min())/(cbIVB_MLB.max()-cbIVB_MLB.min()))*100

    swVeloNorm_MLB=((swVelo_MLB-swVelo_MLB.min())/(swVelo_MLB.max()-swVelo_MLB.min()))*100
    swSpinNorm_MLB=((swSpin_MLB-swSpin_MLB.min())/(swSpin_MLB.max()-swSpin_MLB.min()))*100
    swHBNorm_MLB=((swHB_MLB-swHB_MLB.min())/(swHB_MLB.max()-swHB_MLB.min()))*100
    swVBNorm_MLB=((swVB_MLB-swVB_MLB.min())/(swVB_MLB.max()-swVB_MLB.min()))*100
    swIVBNorm_MLB=((swIVB_MLB-swIVB_MLB.min())/(swIVB_MLB.max()-swIVB_MLB.min()))*100

    # For the changeup, the case is special. We will normalize based on the difference between each pitcher's average fastball velocity and the average changeup velocity. The sweet spot is an 8mph difference, so we will use that as the max value for normalization. 
    # The min value will be a 0mph difference, which is the worst case scenario. Any difference higher than 8 will fall off until 12 mph, which will also be a minimum value.

    pitchers_MLB = data['Pitcher'].unique()
    chVeloNorm_MLB = {}

    for i in pitchers_MLB:
        pitcher_data_MLB = data[data['Pitcher'] == i]

        # Isolate pitch types for each pitcher
        fb_pitches_MLB = pitcher_data_MLB[pitcher_data_MLB['TaggedPitchType'].isin(['Fastball', 'Sinker', 'Cutter'])]
        ch_pitches_MLB = pitcher_data_MLB[pitcher_data_MLB['TaggedPitchType'] == 'ChangeUp']

        if ch_pitches_MLB.empty or fb_pitches_MLB.empty:
            continue

        pitcher_fbVelo_MLB = fb_pitches_MLB['RelSpeed'].mean()
        pitcher_chVelo_MLB = ch_pitches_MLB['RelSpeed'].mean()

        pitcher_diff_MLB = pitcher_fbVelo_MLB - pitcher_chVelo_MLB

        # 2. Two part normalization (0-8 mph climbing, 8-12 mph falling off)
        if pitcher_diff_MLB <= 0 or pitcher_diff_MLB >= 12:
            chVeloScore_MLB = 0.0
        elif pitcher_diff_MLB <= 8:
            # Scales from 0 mph (score 0) to 8 mph (score 100)
            chVeloScore_MLB = (pitcher_diff_MLB / 8.0) * 100
        else:
            # Falls off from 8 mph (score 100) to 12 mph (score 0)
            chVeloScore_MLB = ((12.0 - pitcher_diff_MLB) / 4.0) * 100

        chVeloNorm_MLB[i] = chVeloScore_MLB.round(2)

    # Other changeup metrics will be normalized like the other pitch types, using the min and max values for each metric across all pitchers.

    chSpinNorm_MLB=((chSpin_MLB-chSpin_MLB.min())/(chSpin_MLB.max()-chSpin_MLB.min()))*100
    chHBNorm_MLB=((chHB_MLB-chHB_MLB.min())/(chHB_MLB.max()-chHB_MLB.min()))*100
    chVBNorm_MLB=((chVB_MLB-chVB_MLB.min())/(chVB_MLB.max()-chVB_MLB.min()))*100
    chIVBNorm_MLB=((chIVB_MLB-chIVB_MLB.min())/(chIVB_MLB.max()-chIVB_MLB.min()))*100

    spVeloNorm_MLB=((spVelo_MLB-spVelo_MLB.min())/(spVelo_MLB.max()-spVelo_MLB.min()))*100
    spSpinNorm_MLB=((spSpin_MLB-spSpin_MLB.min())/(spSpin_MLB.max()-spSpin_MLB.min()))*100
    spHBNorm_MLB=((spHB_MLB-spHB_MLB.min())/(spHB_MLB.max()-spHB_MLB.min()))*100
    spVBNorm_MLB=((spVB_MLB-spVB_MLB.min())/(spVB_MLB.max()-spVB_MLB.min()))*100
    spIVBNorm_MLB=((spIVB_MLB-spIVB_MLB.min())/(spIVB_MLB.max()-spIVB_MLB.min()))*100

    # We will use the same weights we defined above.

    # Create a new column in the dataframe to hold the StuffScore for each pitch. The below code will also create masks to correctly map each series to the dataframe based on the pitch type.
    data['StuffScore_MLB'] = 0.0

    fb_mask_MLB = data['TaggedPitchType'] == 'Fastball'
    data.loc[fb_mask_MLB, 'StuffScore_MLB'] = (
        (fbVeloNorm_MLB * fbVeloWeight)
        + (fbSpinNorm_MLB * fbSpinWeight)
        + (fbHBNorm_MLB * fbHBWeight)
        + (fbVBNorm_MLB * fbVBWeight)
        + (fbIVBNorm_MLB * fbIVBWeight)
    )

    snk_mask_MLB = data['TaggedPitchType'] == 'Sinker'
    data.loc[snk_mask_MLB, 'StuffScore_MLB'] = (
        (snkVeloNorm_MLB * snkVeloWeight)
        + (snkSpinNorm_MLB * snkSpinWeight)
        + (snkHBNorm_MLB * snkHBWeight)
        + (snkVBNorm_MLB * snkVBWeight)
        + (snkIVBNorm_MLB * snkIVBWeight)
    )

    cut_mask_MLB = data['TaggedPitchType'] == 'Cutter'
    data.loc[cut_mask_MLB, 'StuffScore_MLB'] = (
        (cutVeloNorm_MLB * cutVeloWeight)
        + (cutSpinNorm_MLB * cutSpinWeight)
        + (cutHBNorm_MLB * cutHBWeight)
        + (cutVBNorm_MLB * cutVBWeight)
        + (cutIVBNorm_MLB * cutIVBWeight)
    )

    sl_mask_MLB = data['TaggedPitchType'] == 'Slider'
    data.loc[sl_mask_MLB, 'StuffScore_MLB'] = (
        (slVeloNorm_MLB * slVeloWeight)
        + (slSpinNorm_MLB * slSpinWeight)
        + (slHBNorm_MLB * slHBWeight)
        + (slVBNorm_MLB * slVBWeight)
        + (slIVBNorm_MLB * slIVBWeight)
    )

    cb_mask_MLB = data['TaggedPitchType'] == 'Curveball'
    data.loc[cb_mask_MLB, 'StuffScore_MLB'] = (
        (cbVeloNorm_MLB * cbVeloWeight)
        + (cbSpinNorm_MLB * cbSpinWeight)
        + (cbHBNorm_MLB * cbHBWeight)
        + (cbVBNorm_MLB * cbVBWeight)
        + (cbIVBNorm_MLB * cbIVBWeight)
    )

    sw_mask_MLB = data['TaggedPitchType'] == 'Sweeper'
    data.loc[sw_mask_MLB, 'StuffScore_MLB'] = (
        (swVeloNorm_MLB * swVeloWeight)
        + (swSpinNorm_MLB * swSpinWeight)
        + (swHBNorm_MLB * swHBWeight)
        + (swVBNorm_MLB * swVBWeight)
        + (swIVBNorm_MLB * swIVBWeight)
    )

    ch_mask_MLB = data['TaggedPitchType'] == 'ChangeUp'
    ch_velo_scores_MLB = data.loc[ch_mask_MLB, 'Pitcher'].map(chVeloNorm_MLB).fillna(0.0)
    data.loc[ch_mask_MLB, 'StuffScore_MLB'] = (
        (ch_velo_scores_MLB * chVeloWeight)
        + (chSpinNorm_MLB * chSpinWeight)
        + (chHBNorm_MLB * chHBWeight)
        + (chVBNorm_MLB * chVBWeight)
        + (chIVBNorm_MLB * chIVBWeight)
    )

    sp_mask_MLB = data['TaggedPitchType'] == 'Splitter'
    data.loc[sp_mask_MLB, 'StuffScore_MLB'] = (
        (spVeloNorm_MLB * spVeloWeight)
        + (spSpinNorm_MLB * spSpinWeight)
        + (spHBNorm_MLB * spHBWeight)
        + (spVBNorm_MLB * spVBWeight)
        + (spIVBNorm_MLB * spIVBWeight)
    )

    data['StuffScore_MLB'] = data['StuffScore_MLB'].round(2) # Round the StuffScore_MLB to 2 decimal places
    # 1. Extract MLB Benchmark StuffScore_MLB for each pitch type into a dictionary
    mlb_benchmark_map = (data[data['PitchSession'] == 'MLB_Benchmark'].set_index('TaggedPitchType')['StuffScore_MLB'].to_dict())

    # 2. Divide each pitch's StuffScore_MLB by its corresponding pitch type's benchmark score
    data['Stuff+_MLB'] = np.round((data['StuffScore_MLB'] / data['TaggedPitchType'].map(mlb_benchmark_map))* 100,0,)

    # 3. Remove MLB benchmark rows before returning the clean data
    data = data[data['PitchSession'] != 'MLB_Benchmark'].reset_index(drop=True)
    # Now that we have calculated the StuffScore for each pitch, we can create Stuff+ scores. An average pitch has a Stuff+ score of 100, so for example, a pitch with a 120 Stuff+ would be 20% better than average, while 90 Stuff+ would be 10% worse than average.

    data['Stuff+'] = round((data['StuffScore'] / data['StuffScore'].mean()) * 100,0)
    return data
