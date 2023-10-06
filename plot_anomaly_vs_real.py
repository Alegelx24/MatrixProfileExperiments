import pandas as pd
import matplotlib.pyplot as plt

# Assuming a csv file ('data.csv') with columns: 'timestamp', 'real_anomaly', 'predicted_anomaly'
# 'timestamp' is a datetime string or timestamp
# 'real_anomaly' and 'predicted_anomaly' are integer indexes representing anomaly positions

# Load your data
data = pd.read_csv('data.csv')
# Convert 'timestamp' to datetime type if it's not
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Set the plot size
plt.figure(figsize=(10,6))

# Plotting
plt.scatter(data['timestamp'], data['real_anomaly'], color='red', label='Real Anomaly')
plt.scatter(data['timestamp'], data['predicted_anomaly'], color='blue', label='Predicted Anomaly', alpha=0.7)

# Adding labels and title
plt.xlabel('Timestamp')
plt.ylabel('Anomaly Index')
plt.title('Comparison of Real and Predicted Anomalies')
plt.legend()

# Displaying the plot
plt.xticks(rotation=45)  # rotate x-axis labels for better readability
plt.tight_layout()  # adjust layout to prevent cut-off labels
plt.show()
