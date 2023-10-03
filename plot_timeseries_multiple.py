import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_timeseries(input_file, output_directory):
    # Read the CSV file into a DataFrame (adjust delimiter if needed)
    df = pd.read_csv(input_file)

    # Extract the value column (adjust column name if needed)
    values = df['value']

    # Create the plot
    plt.figure(figsize=(20, 10))  # Optional: Adjust the figure size
    plt.plot(values, linestyle='-', linewidth=0.5, color='red')

    # Customize the plot (title, labels, grid, etc.)
    plt.title(f'Time Series Plot for {os.path.basename(input_file)}')
    plt.xlabel('Data Point Index')
    plt.ylabel('Value')
    plt.grid(True)

    # Construct the output image path
    image_name = f"{os.path.splitext(os.path.basename(input_file))[0]}.png"
    output_image_path = os.path.join(output_directory, image_name)

    # Save the plot as an image
    plt.savefig(output_image_path)

    # Close the plot to release resources (optional)
    plt.close()

    print(f"Saved plot as {image_name}")



def main():
    # Define input and output directories
    input_directory = '/Users/aleg2/Desktop/ydata-labeled-time-series-anomalies-v1_0/A1Benchmark'  # Replace with the path to your input folder containing CSV files
    output_directory = '/Users/aleg2/Desktop/ydata-labeled-time-series-anomalies-v1_0/A1Benchmark_plot'  # Replace with the path to your output folder for saving images

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # List all CSV files in the input directory
    csv_files = [file for file in os.listdir(input_directory) if file.endswith('.csv')]

    # Loop through the CSV files and plot each one
    for csv_file in csv_files:
        # Construct the full path to the CSV file
        csv_path = os.path.join(input_directory, csv_file)

        # Plot the time series and save the image
        plot_timeseries(csv_path, output_directory)

if __name__ == "__main__":
    main()
