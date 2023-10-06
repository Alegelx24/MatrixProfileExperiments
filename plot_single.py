import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_timeseries(input_file, output_image_path):
    # Read the CSV file into a DataFrame (adjust delimiter if needed)
    df = pd.read_csv(input_file)

    # Extract the value column (adjust column name if needed)
    values = df['normalized_value']

    # Create the plot
    plt.figure(figsize=(20, 10))  # Optional: Adjust the figure size
    plt.plot(values, linestyle='-', linewidth=0.5, color='red')

    # Customize the plot (title, labels, grid, etc.)
    plt.title(f'Time Series Plot for {os.path.basename(input_file)}')
    plt.xlabel('Data Point Index')
    plt.ylabel('Value')
    plt.grid(True)

    # Save the plot as an image
    plt.savefig(output_image_path)
    plt.show()

    # Close the plot to release resources (optional)
    plt.close()

    print(f"Saved plot as {output_image_path}")

def main():
    # Define input file path and output image path
    input_file = "/Users/aleg2/Desktop/ydata-labeled-time-series-anomalies-v1_0/A1_merged/merged_A1Benchmark_norm.csv"  # Replace with the path to your input file
    output_image_path = '/Users/aleg2/Desktop/ydata-labeled-time-series-anomalies-v1_0/A1_merged/merged_A1Benchmark_norm.png'  # Replace with the path to your output image file

    # Plot the time series and save the image
    plot_timeseries(input_file, output_image_path)

if __name__ == "__main__":
    main()
