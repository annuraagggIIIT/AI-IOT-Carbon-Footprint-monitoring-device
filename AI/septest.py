import pandas as pd
import json

# Load the JSON file
with open('sensor_data_12000.json') as json_file:
    data = json.load(json_file)

# Convert the loaded JSON data into a DataFrame
df = pd.DataFrame(data)

# List of gases (columns)
gases = ['lpg', 'smoke', 'alcohol', 'methane', 'co', 'flammable_gas']

# Iterate over each gas and save it to its own CSV file without timestamp
for gas in gases:
    # Select the column for the current gas (without timestamp)
    gas_df = df[[gas]]
    
    # Save it to a CSV file
    gas_df.to_csv(f'{gas}.csv', index=False)
