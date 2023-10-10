import pandas as pd

# Load your data
predicted_anomalies = pd.read_csv('/Users/aleg2/Downloads/positions_csv_files/Positions_SubseqLen672_Idx4032.csv', header=None)
actual_anomalies = pd.read_csv("/Users/aleg2/Desktop/ydata-labeled-time-series-anomalies-v1_0/A1_merged/all_anomalies_A1_merged_0_1.csv", header=None)  # Assuming binary flags are in column 1


# Extracting timestamps and actual anomalies as sets
predicted_timestamps = set(predicted_anomalies[0].tolist())
actual_anomaly_indices = set(actual_anomalies[actual_anomalies.iloc[:, 0] == 1].index.tolist())

# Creating a function to compute recall
def compute_recall(predicted_timestamps, actual_anomaly_indices, tolerance_window=6):
    TP = 0
    for actual_anomaly_index in actual_anomaly_indices:
        for timestamp in range(actual_anomaly_index - tolerance_window, actual_anomaly_index + tolerance_window + 1):
            if timestamp in predicted_timestamps:
                TP += 1
                break
    
    FN = len(actual_anomaly_indices) - TP
    recall = TP / (TP + FN) if TP + FN > 0 else 0
    
    return recall

# Compute and display recall
recall = compute_recall(predicted_timestamps, actual_anomaly_indices)
print(f'Recall: {recall:.2f}')