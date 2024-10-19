import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter

# Define project tasks and their durations
tasks = ['IoT Development', 'Data Creation', 'Testing on ANN', 'Testing on X-AI', 'Testing on SVR', 'Testing on Logistic Regression']
start_dates = ['2024-07-25', '2024-08-15', '2024-08-30', '2024-09-10', '2024-09-20', '2024-10-01']
end_dates = ['2024-08-14', '2024-08-29', '2024-09-09', '2024-09-19', '2024-09-30', '2024-10-15']

# Convert dates to datetime objects
start_dates = pd.to_datetime(start_dates)
end_dates = pd.to_datetime(end_dates)

# Calculate durations
durations = end_dates - start_dates

# Create DataFrame
df = pd.DataFrame({'Task': tasks, 'Start': start_dates, 'End': end_dates, 'Duration': durations})

# Plot Gantt chart
fig, ax = plt.subplots(figsize=(10, 6))

for i, task in enumerate(df['Task']):
    ax.barh(task, df['Duration'][i].days, left=df['Start'][i], color='skyblue')

# Format x-axis labels
ax.xaxis.set_major_locator(plt.MaxNLocator(10))
ax.xaxis.set_minor_locator(plt.MaxNLocator(30))
ax.xaxis.set_major_formatter(DateFormatter('%d-%b'))

plt.xlabel('Date')
plt.ylabel('Task')
plt.title('Stablecoin Ecosystem Development Gantt Chart')

plt.tight_layout()
plt.grid(True)
plt.show()
