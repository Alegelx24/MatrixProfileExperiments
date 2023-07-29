import os
import pandas as pd

def merge_all_csv_files_in_folder(folder_path, output_file):
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    
    # Sort the CSV files in alphabetical order (you can modify the sorting criteria as needed)
    csv_files.sort()

    # Initialize an empty DataFrame to store the merged data
    merged_df = pd.DataFrame()

    # Iterate through each CSV file and merge its contents into the final DataFrame
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(file_path)
        merged_df = pd.concat([merged_df, df], ignore_index=True)

    # Write the merged DataFrame to a new CSV file
    merged_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    folder_path = "path/to/your/folder"  # Replace with the path to your folder containing CSV files
    output_csv_file = "merged_file.csv"  # Replace with the desired output file name

    merge_all_csv_files_in_folder(folder_path, output_csv_file)
