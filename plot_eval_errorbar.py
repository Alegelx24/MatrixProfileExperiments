import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = "/Users/aleg2/Desktop/MatrixProfileExperiments/eval_as_ts2vec_kpi_complete_raw.csv"  # Replace with your file path
data = pd.read_csv(file_path)

# Convert 'Precision', 'Recall', and 'MRR' to floats
data['Precision'] = data['Precision'].astype(float)
data['Recall'] = data['Recall'].astype(float)
data['MRR'] = data['MRR'].astype(float)

# Group by 'K' and calculate mean and standard deviation
grouped = data.groupby('K').agg({'Precision': ['mean', 'std'], 'Recall': ['mean', 'std'], 'MRR': ['mean', 'std']})

# Plot for Precision
plt.figure(figsize=(10, 6), dpi=300)
plt.plot(grouped.index, grouped['Precision']['mean'], color="blue", label='Precision', marker='o')
plt.fill_between(grouped.index, grouped['Precision']['mean'] - grouped['Precision']['std'], grouped['Precision']['mean'] + grouped['Precision']['std'], color="blue", alpha=0.2)
plt.title('Precision@K')
plt.xlabel('K')
plt.ylabel('Precision')
plt.legend()
plt.grid(True)
plt.savefig('precision_plot.png')
plt.close()

# Plot for Recall
plt.figure(figsize=(10, 6), dpi=300)
plt.plot(grouped.index, grouped['Recall']['mean'], color="red", label='Recall', marker='x')
plt.fill_between(grouped.index, grouped['Recall']['mean'] - grouped['Recall']['std'], grouped['Recall']['mean'] + grouped['Recall']['std'], color="red", alpha=0.2)
plt.title('Recall@K')
plt.xlabel('K')
plt.ylabel('Recall')
plt.legend()
plt.grid(True)
plt.savefig('recall_plot.png')
plt.close()

# Plot for MRR
plt.figure(figsize=(10, 6), dpi=300)
plt.plot(grouped.index, grouped['MRR']['mean'], color="green", label='MRR', marker='^')
plt.fill_between(grouped.index, grouped['MRR']['mean'] - grouped['MRR']['std'], grouped['MRR']['mean'] + grouped['MRR']['std'], color="green", alpha=0.2)
plt.title('MRR')
plt.xlabel('K')
plt.ylabel('MRR')
plt.legend()
plt.grid(True)
plt.savefig('mrr_plot.png')
plt.close()
