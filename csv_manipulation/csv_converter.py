import re
import csv
# Read the input text file
with open("/Users/aleg2/Desktop/RESULTS_A1.TXT", 'r') as file:
    lines = file.readlines()

# Create a CSV file for writing
with open('output.csv', 'w', newline='') as csv_file:
    # Define CSV writer
    csv_writer = csv.writer(csv_file)
    
    # Write the header row
    csv_writer.writerow(['real_#', 'SubsequenceLength', 'CurrentIndex', 'Positions'])
    
    # Initialize variables to store data
    real_number = None
    subseq_length = None
    current_index = None
    positions = []
    
    # Process each line of the input text
    for line in lines:
        line = line.strip()
        if line.startswith("---------real_"):
            # If new "real_x" section is encountered, write the previous data
            if real_number is not None:
                for subseq, index in zip(subseq_length, current_index):
                    csv_writer.writerow([real_number, subseq, index, ','.join(positions)])
            real_number = line.split('_')[1]
            subseq_length = []
            current_index = []
            positions = []  # Reset positions for the current section
        elif line.startswith("SubsequenceLength:"):
            # Extract SubsequenceLength and CurrentIndex from this section
            parts = line.split(":")
            if len(parts) >= 3:
                subseq_length.append(parts[1].strip().split(',')[0].strip())
                current_index.append(parts[2].strip())
            positions = []  # Reset positions for the current section
        elif line.isdigit():
            positions.append(line)
    
    # Write the last set of data
    if real_number is not None:
        for subseq, index in zip(subseq_length, current_index):
            csv_writer.writerow([real_number, subseq, index, ','.join(positions)])