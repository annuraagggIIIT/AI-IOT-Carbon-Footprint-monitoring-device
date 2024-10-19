import pandas as pd
import numpy as np

data = pd.read_json('sensor_data.json')  

initial_size = data.shape[0]

target_size = 12000
replication_factor = target_size // initial_size

data_replicated = pd.concat([data] * replication_factor, ignore_index=True)

numeric_columns = data.select_dtypes(include=np.number).columns

for col in numeric_columns:
    data_replicated[col] = data_replicated[col] * (1 + np.random.uniform(-0.02, 0.02, data_replicated[col].shape[0]))

data_final = data_replicated.iloc[:target_size]

data_final.to_json('sensor_data_12000.json', orient='records')

