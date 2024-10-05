import neurokit2 as nk
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# This code will generate RMSSD from each PPG types for each participants
# What sampling rates to use? 
# Are there futher processing needed before we pass to NeuroKit?
# What method to choose (currently hrv_time() - elgendi) 

typetags = ['PI', 'PR', 'PG']
DATA_FOLDER = 'C:/Users/nancy/Documents/MInfoTech/EmotiBitParsedData/'
participants = ['Lucia', 'Steven', 'Nick', 'LindsayDuring', 'LindsayAfter']
for typetag in typetags:
    print(f"using PPG type: {typetag}")
    for participant in participants: 
        folder_path = f"{DATA_FOLDER}{participant}"
        ppg = []
        all_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                all_files.append(os.path.join(root, file))

        for filename in all_files:
            if filename.endswith(f"_{typetag}.csv"):
                file_path = os.path.join(folder_path, filename)
                data = pd.read_csv(file_path, sep=',')
                ppg.append(data[typetag].to_numpy())
        combined_ppg = np.concatenate(ppg)
        
        try:
            peaks, info = nk.ppg_peaks(nk.ppg_clean(combined_ppg, method='elgendi'), sampling_rate=1000, method="elgendi", show=True)
            bio_df, bio_info = nk.bio_process(ppg=peaks, sampling_rate=1000)
            bio_df.head()
            hrv = nk.hrv_time(bio_df, sampling_rate=1000, show=True)
            print(f"{participant}'s RMSSD is: {hrv['HRV_RMSSD'].iloc[0]}")
        except Exception as e:
            print(f"{participant}'s data processing fail")
    print()
    # close plot possibly opened by neurokit to avoid memory issue
    plt.close('all')
    