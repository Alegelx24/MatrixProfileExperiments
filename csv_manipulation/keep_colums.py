import pandas as pd

def extract_columns(input_file, output_file, column_indexes):
    df = pd.read_csv(input_file)
    columns_to_keep = df.columns[column_indexes]
    df = df[columns_to_keep]
    df.to_csv(output_file, index=False)

# Example usage
input_file = "/Users/aleg2/Desktop/MGAB_all.csv"
output_file = '/Users/aleg2/Desktop/MGAB_all_cleaned.csv'
column_indexes_to_keep = [1]  # Replace with the desired column indexes
extract_columns(input_file, output_file, column_indexes_to_keep)
