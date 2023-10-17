import pandas as pd
import numpy as np

# Load your time series data
# Assume 'value' is the column that contains your time series data
df = pd.read_csv("/Users/aleg2/Desktop/KPI dataset/kpi_train_and_label_subsampled.csv")

# Function to perform Z-score normalization
def zscore_normalize(series):
    mean = np.mean(series)
    std = np.std(series)
    return (series - mean) / std

# Apply Z-score normalization
df['normalized_value'] = zscore_normalize(df['value'])

# Save the normalized data back to CSV if needed
df.to_csv('normalized_A1_merged.csv', index=False)
