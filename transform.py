import neurokit2 as nk
import pandas as pd
import numpy as np
import os

# This code will get all csv under the specified folder and generate HRV related data
# Instructions: put csv you want under data folder and update folder_path
#TBC: sampling rate? method?

# configs to print all colummns of result
pd.set_option('display.max_rows', None) 
pd.set_option('display.max_columns', None)  

folder_path = os.path.join(os.path.dirname(__file__), 'data/nick') 
print("Processing all csv in " + folder_path)
ppg = []
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        print(f"Processing file: {filename}")
        data = pd.read_csv(file_path, sep=',')
        ppg.append(data['PI'].to_numpy())
combined_ppg = np.concatenate(ppg)

peaks, info = nk.ppg_peaks(nk.ppg_clean(combined_ppg, method='elgendi'), sampling_rate=1000, method="elgendi", show=True)

bio_df, bio_info = nk.bio_process(ppg=peaks, sampling_rate=1000)
bio_df.head()
hrv = nk.hrv_time(bio_df, sampling_rate=250, show=True)
print(hrv)