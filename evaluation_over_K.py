import pandas as pd

def evaluate_configurations_v2(top60_file_path, real_anomalies_file_path, tolerance=50, K_values=[1, 3, 5, 15, 20, 30, 40, 50, 60]):
    real_anomalies_df = pd.read_csv(real_anomalies_file_path)
    real_indices = real_anomalies_df['value'].tolist()

    all_results_list = []  # List to store results for all K values

    for K in K_values:
        top60_df = pd.read_csv(top60_file_path)  # Re-read the CSV for each K
        # Convert Positions column to list of integers based on K value
        top60_df['Positions'] = top60_df['Positions'].str.strip('[]').str.split(',').apply(lambda x: [int(i) for i in x[:K]])

        unique_configs = top60_df.drop_duplicates(subset=['SubsequenceLength', 'CurrentIndex'])

        for _, config in unique_configs.iterrows():
            subseq_len = config['SubsequenceLength']
            curr_idx = config['CurrentIndex']
            
            # Filter rows with the current configuration and extract predicted positions
            config_rows = top60_df[(top60_df['SubsequenceLength'] == subseq_len) & (top60_df['CurrentIndex'] == curr_idx)]
            predicted_indices = [idx for sublist in config_rows['Positions'].tolist() for idx in sublist]  # Flatten the lists

            TP, FP, FN = 0, 0, 0
            predicted_set = set(predicted_indices)
            
            for r_idx in real_indices:
                found = False
                for i in range(-tolerance, tolerance + 1):
                    if r_idx + i in predicted_set:
                        found = True
                        break
                TP += found
                FN += not found

            for p_idx in predicted_indices:
                found = any(p_idx + i in real_indices for i in range(-tolerance, tolerance + 1))
                FP += not found

            # Compute metrics
            precision = TP / (TP + FP) if TP + FP else 0
            recall = TP / (TP + FN) if TP + FN else 0

            mrr_values = []
            for r_idx in real_indices:
                for rank, p_idx in enumerate(predicted_indices, start=1):
                    if abs(p_idx - r_idx) <= tolerance:
                        mrr_values.append(1 / rank)
                        break

            mrr = sum(mrr_values) / len(real_indices) if mrr_values else 0

            all_results_list.append({
                "SubsequenceLength": subseq_len,
                "CurrentIndex": curr_idx,
                "K": K,
                "Precision": precision,
                "Recall": recall,
                "MRR": mrr
            })

    # Convert the all_results_list to DataFrame and save as CSV
    all_results_df = pd.DataFrame(all_results_list)
    all_results_df.to_csv("evaluation_results_KPI_NORM_over_K_values.csv", index=False)

    return all_results_df

if __name__ == "__main__":
    config_results_v2 = evaluate_configurations_v2(
        "/Users/aleg2/Desktop/KPI dataset/top60_raw_kpi_subsampled.csv", 
        "/Users/aleg2/Desktop/KPI dataset/anomalies_KPI_subsampled.csv"
    )
