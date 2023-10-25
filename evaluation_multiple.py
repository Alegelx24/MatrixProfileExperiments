import ast
import pandas as pd

def evaluate_configurations_v2(top60_file_path, real_anomalies_file_path, tolerance=50, K=15):

    top60_df = pd.read_csv(top60_file_path)
    real_anomalies_df = pd.read_csv(real_anomalies_file_path)
    
    real_indices = real_anomalies_df['value'].tolist()
    
    #top60_df['Positions'] = top60_df['Positions'].apply(lambda x: ast.literal_eval(x))
    #top60_df['Positions'] = top60_df['Positions'].str.split(',').apply(lambda x: [int(i) for i in x])
    top60_df['Positions'] = top60_df['Positions'].str.strip('[]')
    #top60_df['Positions'] = top60_df['Positions'].str.split(',').apply(lambda x: [int(i) for i in x])
    top60_df['Positions'] = top60_df['Positions'].str.split(',').apply(lambda x: [int(i) for i in x[:K]])


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

        #tolerance=subseq_len

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
        reciprocal_ranks = []
        
        # Calculate Reciprocal Rank for each real anomaly
        for r_idx in real_indices:
            nearest_rank = None
            for rank, p_idx in enumerate(predicted_indices, start=1):
                if abs(p_idx - r_idx) <= tolerance:  # Check if within tolerance window
                    nearest_rank = rank
                    break
            if nearest_rank is not None:
                reciprocal_ranks.append(1 / nearest_rank)

        # Calculate Mean Reciprocal Rank
        mrr = sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0

        # Store results with MRR instead of F1-Score
        results_list.append({
            "SubsequenceLength": subseq_len,
            "CurrentIndex": curr_idx,
            "Precision": precision,
            "Recall": recall,
            "MRR": mrr  # Replacing F1-Score with MRR
        })
    # Convert the results list to DataFrame and save as CSV
    results_df = pd.DataFrame(results_list)
    results_df.to_csv("evaluation_results_KPI_NORM_half.csv", index=False)
    
    return results_df



if __name__ == "__main__":
    
    config_results_v2 = evaluate_configurations_v2("/Users/aleg2/Desktop/KPI dataset/top60_raw_kpi_subsampled.csv", "/Users/aleg2/Desktop/KPI dataset/anomalies_KPI_subsampled.csv")



    #config_results_v2 = evaluate_configurations_v2("/Users/aleg2/Desktop/KPI dataset/Top60_half_KPI_NORM.csv", "/Users/aleg2/Desktop/KPI dataset/anomalies_KPI_subsampled.csv")
