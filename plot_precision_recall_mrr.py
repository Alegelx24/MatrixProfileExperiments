import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = "/Users/aleg2/Downloads/sorted_A1_NORM_evaluation_results.csv"  # Replace with your file path
data = pd.read_csv(file_path)

# Convert 'Precision', 'Recall', and 'MRR' to floats
data['Precision'] = data['Precision'].str.replace(',', '.').astype(float)
data['Recall'] = data['Recall'].str.replace(',', '.').astype(float)
data['MRR'] = data['MRR'].str.replace(',', '.').astype(float)

# Group by 'SubsequenceLength' and 'CurrentIndex'
grouped = data.groupby(['SubsequenceLength', 'CurrentIndex'])

# Plot for each group
for (subseq_length, current_index), group in grouped:
    plt.figure(figsize=(10, 6))

    # Plotting
    plt.plot(group['K'], group['Precision'], label='Precision', marker='o')
    plt.plot(group['K'], group['Recall'], label='Recall', marker='x')
    plt.plot(group['K'], group['MRR'], label='MRR', marker='^')

    # Labeling the plot
    plt.title(f'Subsequence Length: {subseq_length}, Current Index: {current_index}')
    plt.xlabel('K')
    plt.ylabel('Metrics')
    plt.legend()
    plt.grid(True)
    
    plot_filename = f'plots_evaluation/A1_NORM_Subseq_{subseq_length}_Index_{current_index}.png'
    plt.savefig(plot_filename)
