import pandas as pd

# File path
csv_file = '/Users/aleg2/Desktop/KPI dataset/kpi_train_and_label_subsampled.csv'

# Output file to store all anomaly positions
output_file = 'anomalies_KPI_subsampled.txt'

# Initialize a list to store anomaly positions
anomaly_positions = []

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Assuming the anomaly column is always the third column (index 2)
anomaly_column_index = 1

try:
    # Extract the anomaly column by its position
    anomaly_column = df.iloc[:, anomaly_column_index]
    
    # Get the positions where the anomaly column is equal to 1
    anomaly_positions = anomaly_column.index[anomaly_column == 1].tolist()
    
    # Convert anomaly positions to strings and join them with a newline character
    anomaly_positions_str = "\n".join(map(str, anomaly_positions))
    
    # Write a header indicating the file name and anomaly positions to the output text file
    with open(output_file, 'w') as file:
        file.write(f"Anomalies in {csv_file.split('/')[-1]}:\n{anomaly_positions_str}\n")
    
    print("Anomaly positions have been saved to the text file.")
    
except IndexError:
    print(f"The anomaly column index {anomaly_column_index} is out of bounds.")
