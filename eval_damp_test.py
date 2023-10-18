import pandas as pd


def evaluate_predictions(predicted_file_path, real_file_path, tolerance=7):
    predicted_anomalies = pd.read_csv(predicted_file_path, header=None)
    real_anomalies = pd.read_csv(real_file_path)
    
    # Extract the anomaly indices
    predicted_indices = predicted_anomalies.iloc[:, 0].tolist()
    real_indices = real_anomalies['value'].tolist()
    
    TP = 0
    FP = 0
    FN = 0

    predicted_set = set(predicted_indices)

    # For each real anomaly index, check if a predicted anomaly index within the tolerance window
    for r_idx in real_indices:
        found = False
        for i in range(-tolerance, tolerance + 1):
            if r_idx + i in predicted_set:
                found = True
                break
        if found:
            TP += 1
        else:
            FN += 1

    # For each predicted anomaly index, check if it doesn't correspond to any real anomaly within the tolerance window
    for p_idx in predicted_indices:
        found = False
        for i in range(-tolerance, tolerance + 1):
            if p_idx + i in real_indices:
                found = True
                break
        if not found:
            FP += 1

    # Compute the metrics
    precision = TP / (TP + FP) if (TP + FP) != 0 else 0
    recall = TP / (TP + FN) if (TP + FN) != 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0
    
    return precision, recall, f1_score



if __name__ == "__main__":
    results= evaluate_predictions("/Users/aleg2/Downloads/top_60_prediction_a1/Positions_SubseqLen672_Idx4032.csv", "/Users/aleg2/Desktop/ydata-labeled-time-series-anomalies-v1_0/A1_merged/all_anomalies_A1_merged.csv")
    print("precision: " + str(results[0]) + "\nrecall: " + str(results[1]) + "\nf1_score: " + str(results[2]))
