import ast
import pandas as pd

def evaluate_configurations_v2(top60_file_path, real_anomalies_file_path, tolerance=50):

    top60_df = pd.read_csv(top60_file_path)
    real_anomalies_df = pd.read_csv(real_anomalies_file_path)
    
    real_indices = real_anomalies_df['value'].tolist()
    
    #top60_df['Positions'] = top60_df['Positions'].apply(lambda x: ast.literal_eval(x))
    #top60_df['Positions'] = top60_df['Positions'].str.split(',').apply(lambda x: [int(i) for i in x])
    top60_df['Positions'] = top60_df['Positions'].str.strip('[]')
    top60_df['Positions'] = top60_df['Positions'].str.split(',').apply(lambda x: [int(i) for i in x])

    unique_configs = top60_df.drop_duplicates(subset=['SubsequenceLength', 'CurrentIndex'])
    
    results_list = []
    
    for _, config in unique_configs.iterrows():
        subseq_len = config['SubsequenceLength']
        curr_idx = config['CurrentIndex']
        
        # Filter rows with the current configuration and extract predicted positions
        config_rows = top60_df[(top60_df['SubsequenceLength'] == subseq_len) & (top60_df['CurrentIndex'] == curr_idx)]
        predicted_indices = [idx for sublist in config_rows['Positions'].tolist() for idx in sublist]  # Flatten the lists
        
        TP = 0
        FP = 0
        FN = 0

        # Using a set for efficient look-up
        predicted_set = set(predicted_indices)

        # Check each real anomaly index against predicted indices within the tolerance window
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

        # Check each predicted index against real anomalies within the tolerance window
        for p_idx in predicted_indices:
            found = False
            for i in range(-tolerance, tolerance + 1):
                if p_idx + i in real_indices:
                    found = True
                    break
            if not found:
                FP += 1

        # Compute metrics
        precision = TP / (TP + FP) if (TP + FP) != 0 else 0
        recall = TP / (TP + FN) if (TP + FN) != 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0
        
        # Store results
        results_list.append({
            "SubsequenceLength": subseq_len,
            "CurrentIndex": curr_idx,
            "Precision": precision,
            "Recall": recall,
            "F1-Score": f1_score
        })
    
    # Convert the results list to DataFrame and save as CSV
    results_df = pd.DataFrame(results_list)
    results_df.to_csv("evaluation_results_KPI_NORM_half.csv", index=False)
    
    return results_df



if __name__ == "__main__":
    config_results_v2 = evaluate_configurations_v2("/Users/aleg2/Desktop/KPI dataset/Top60_half_KPI_NORM.csv", "/Users/aleg2/Desktop/KPI dataset/anomalies_KPI_subsampled.csv")
