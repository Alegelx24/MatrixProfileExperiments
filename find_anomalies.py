import os
import pandas as pd

# Directory containing CSV files
csv_directory = '/Users/aleg2/Desktop/ydata-labeled-time-series-anomalies-v1_0/A1_merged'

# Output file to store all anomaly positions
output_file = 'all_anomalies_a1_merged.txt'

# Initialize a list to store anomaly positions and file names
all_anomaly_positions = []

# Loop through all CSV files in the directory
for filename in os.listdir(csv_directory):
    if filename.endswith('.csv'):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(os.path.join(csv_directory, filename))

        # Assuming the anomaly column is always the third column (index 2)
        anomaly_column_index = 2
        
        try:
            # Extract the anomaly column by its position
            anomaly_column = df.iloc[:, anomaly_column_index]
            
            # Get the positions where the anomaly column is equal to 1
            anomaly_positions = anomaly_column.index[anomaly_column == 1].tolist()
            
            # Append a header indicating the file name
            all_anomaly_positions.append(f"Anomalies in {filename}:\n")
            
            # Append the anomaly positions to the list
            all_anomaly_positions.extend(map(str, anomaly_positions))
            all_anomaly_positions.append('\n')  # Add a separator between files
        except IndexError:
            print(f"Skipping file {filename} as the anomaly column index is out of bounds.")

# Write all anomaly positions to the output text file
with open(output_file, 'w') as file:
    file.write('\n'.join(all_anomaly_positions))

print("All anomaly positions have been saved to a text file with sections for each file.")
