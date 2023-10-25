import pandas as pd
from itertools import groupby
from operator import itemgetter

def group_consecutive_numbers(numbers):
    """ Group consecutive numbers into sublists. """
    return [list(map(itemgetter(1), g)) for k, g in groupby(enumerate(numbers), lambda x: x[0] - x[1])]

def evaluate_configurations_v2(top60_file_path, real_anomalies_file_path, tolerance=50, K=60):
    top60_df = pd.read_csv(top60_file_path)
    real_anomalies_df = pd.read_csv(real_anomalies_file_path)
    real_indices = real_anomalies_df['value'].tolist()
    real_sequences = group_consecutive_numbers(sorted(set(real_indices)))

    top60_df['Positions'] = top60_df['Positions'].str.strip('[]').str.split(',').apply(lambda x: [int(i) for i in x[:K]])

    unique_configs = top60_df.drop_duplicates(subset=['SubsequenceLength', 'CurrentIndex'])
    results_list = []
    ks = [1, 3, 5, 15, 30, 40, 60]

    for _, config in unique_configs.iterrows():
        subseq_len = config['SubsequenceLength']
        curr_idx = config['CurrentIndex']

        config_rows = top60_df[(top60_df['SubsequenceLength'] == subseq_len) & (top60_df['CurrentIndex'] == curr_idx)]
        all_predicted_indices = [idx for sublist in config_rows['Positions'].tolist() for idx in sublist]

        for k in ks:
            predicted_indices = all_predicted_indices[:k]
            TP, FP, FN = 0, 0, 0
            predicted_set = set(predicted_indices)

            # Update TP and FN based on new logic
            for sequence in real_sequences:
                if any(any(r_idx + i in predicted_set for i in range(-tolerance, tolerance + 1)) for r_idx in sequence):
                    TP += len(sequence)
                else:
                    FN += len(sequence)

            # Update FP
            FP = sum(1 for p_idx in predicted_indices if not any(p_idx + i in real_indices for i in range(-tolerance, tolerance + 1)))

            precision = TP / (TP + FP) if (TP + FP) > 0 else 0
            recall = TP / (TP + FN) if (TP + FN) > 0 else 0
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            results_list.append({
                "SubsequenceLength": subseq_len,
                "CurrentIndex": curr_idx,
                "k": k,
                "Precision": precision,
                "Recall": recall,
                "F1-Score": f1_score
            })

    results_df = pd.DataFrame(results_list)
    results_df.to_csv("evaluation_results_KPI_NORM_half_overK.csv", index=False)
    return results_df

if __name__ == "__main__":
    config_results_v2 = evaluate_configurations_v2("/Users/aleg2/Desktop/KPI dataset/top60_raw_kpi_subsampled.csv", "/Users/aleg2/Desktop/KPI dataset/anomalies_KPI_subsampled.csv")
