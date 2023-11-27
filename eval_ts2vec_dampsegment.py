import pandas as pd
from itertools import groupby
from operator import itemgetter

def group_consecutive_numbers(numbers):
    """ Group consecutive numbers into sublists. """
    return [list(map(itemgetter(1), g)) for k, g in groupby(enumerate(numbers), lambda x: x[0] - x[1])]

def evaluate_configurations_v2(top60_file_path, real_anomalies_file_path, K=60):
    top60_df = pd.read_csv(top60_file_path)
    real_anomalies_df = pd.read_csv(real_anomalies_file_path)
    real_indices = real_anomalies_df['value'].tolist()
    real_sequences = group_consecutive_numbers(sorted(set(real_indices)))

    top60_df['Positions'] = top60_df['Positions'].str.strip('[]').str.split(';').apply(lambda x: [int(i) for i in x[:K]])

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
            reciprocal_ranks = []

            # Adjusted logic for True Positives (TP)
            for sequence in real_sequences:
                sequence_end = sequence[0] + subseq_len
                found_sequence = any(p_idx >= sequence[0] and p_idx < sequence_end for p_idx in predicted_indices)
                TP += len(sequence) if found_sequence else 0
                FN += len(sequence) if not found_sequence else 0

                # Check for the earliest occurrence within subsequence length for MRR
                for rank, p_idx in enumerate(predicted_indices, start=1):
                    if p_idx >= sequence[0] and p_idx < sequence_end:
                        reciprocal_ranks.append(1 / rank)
                        break

            FP = sum(1 for p_idx in predicted_indices if not any(p_idx >= r_idx and p_idx < r_idx + subseq_len for r_idx in real_indices))

            precision = TP / (TP + FP) if (TP + FP) > 0 else 0
            recall = TP / (TP + FN) if (TP + FN) > 0 else 0
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            mrr = sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0

            results_list.append({
                "SubsequenceLength": subseq_len,
                "CurrentIndex": curr_idx,
                "k": k,
                "Precision": precision,
                "Recall": recall,
                "MRR": mrr 
            })

    results_df = pd.DataFrame(results_list)
    results_df.to_csv("eval_as_ts2vec_KPI_with segment.csv", index=False)
    return results_df

if __name__ == "__main__":
    #config_results_v2 = evaluate_configurations_v2("/Users/aleg2/Desktop/ydata-labeled-time-series-anomalies-v1_0/A1_merged/A1_merged_raw_top60.csv", "/Users/aleg2/Desktop/ydata-labeled-time-series-anomalies-v1_0/A1_merged/all_anomalies_a1_merged.csv")
    config_results_v2 = evaluate_configurations_v2("/Users/aleg2/Desktop/KPI dataset/TopK_kpi_complete.csv", "/Users/aleg2/Desktop/KPI dataset/all_anomalies_kpi_complete.csv")
