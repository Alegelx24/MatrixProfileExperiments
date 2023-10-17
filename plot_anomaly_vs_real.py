import pandas as pd
import matplotlib.pyplot as plt
import ast  # To convert stringified lists to actual lists

csv_path = "/Users/aleg2/Downloads/Top60_a1_merged_raw_halftraining.csv"
data = pd.read_csv(csv_path)

#csv_path_real = "/Users/aleg2/Downloads/anomalies_KPI_subsampled.csv"
csv_path_real = "/Users/aleg2/Desktop/ydata-labeled-time-series-anomalies-v1_0/A1_merged/all_anomalies_a1_merged.csv"

data_real = pd.read_csv(csv_path_real)

#data['Positions'] = data['Positions'].apply(ast.literal_eval)
data['Positions'] = data['Positions'].str.split(';').apply(lambda x: [int(i) for i in x])

#data['Scores'] = data['Scores'].apply(ast.literal_eval)

data['Scores'] = data['Scores'].str.split(';').apply(lambda x: [float(i) for i in x])


for index, row in data.iterrows():
    plt.figure(figsize=(15, 9))
    plt.scatter(row['Positions'], row['Scores'], marker='.', color="red" ,alpha=0.5)
    
    plt.title(f"Scatter Plot for SubsequenceLength={row['SubsequenceLength']}, CurrentIndex={row['CurrentIndex']}(Points are predicted anomalies, vertical line real ones)")
    plt.xlabel('Timestamp positions')
    plt.ylabel('Predicted discord scores')
    plt.xlim([0, 100000])
    
    for val in data_real['value']:
        plt.axvline(x=val, color='green', linestyle='-', linewidth=0.5)
    
    plt.savefig(f"A1_raw_scatter_plot_L={row['SubsequenceLength']}_start={row['CurrentIndex']}.png" )
    
    #plt.show()
