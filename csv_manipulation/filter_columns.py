import os
import csv

def create_csv_with_second_column(input_file, output_file):
    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the first row (header) if present

        data_to_write = []
        for row in reader:
                data_to_write.append([row[2]])  # Add only the data from the second column

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data_to_write)

def process_files_in_directory(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all files in the input folder
    files = os.listdir(input_folder)

    for filename in files:
        if filename.endswith(".csv"):  # Process only CSV files
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename)
            create_csv_with_second_column(input_file, output_file)

if __name__ == "__main__":
    input_folder = "/Users/aleg2/Desktop/MatrixProfileExperiments/"  # Specify the input folder path
    output_folder = "/Users/aleg2/Desktop/"  # Specify the output folder path

    process_files_in_directory(input_folder, output_folder)
