import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import os
from dotenv import load_dotenv, set_key

# Load .env file
load_dotenv()

# Load the dataset for Flammable Gas
flammable_gas_data = pd.read_csv('flammable_gas.csv')

# Handle missing values by imputing the median of the column
imputer = SimpleImputer(strategy='median')
flammable_gas_data['flammable_gas'] = imputer.fit_transform(flammable_gas_data[['flammable_gas']])

# Define a threshold to create a binary target column
threshold = flammable_gas_data['flammable_gas'].median()

# Create a binary target column (1 if 'flammable_gas' is above the median, else 0)
flammable_gas_data['target'] = (flammable_gas_data['flammable_gas'] > threshold).astype(int)

# Features (X) and Target (y)
X = flammable_gas_data[['flammable_gas']]  # Only the 'flammable_gas' column is the feature
y = flammable_gas_data['target']  # The new binary target column

# Split the dataset into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the logistic regression model
logreg = LogisticRegression()

# Train the model on the training data
logreg.fit(X_train, y_train)

# Predict the probability of the test set
X_values = np.linspace(X_train.min(), X_train.max(), 100).reshape(-1, 1)
y_prob_values = logreg.predict_proba(X_values)[:, 1]

# Optimal threshold value (using ROC or F1 method)
optimal_threshold = 0.54  # You can calculate this threshold from earlier methods

# Extract model coefficients (weights) and intercept
w = logreg.coef_[0][0]  # The coefficient for the 'flammable_gas' feature
b = logreg.intercept_[0]  # The intercept

# Use the threshold to find the corresponding gas concentration (ppm)
ppm_at_threshold = (np.log(optimal_threshold / (1 - optimal_threshold)) - b) / w

# Store the threshold value in the .env file
env_file = '.env'
set_key(env_file, 'FLAMMABLE_GAS_THRESHOLD', f"{ppm_at_threshold:.2f}")

# Plot the logistic regression curve
plt.figure(figsize=(10, 6))
plt.plot(X_values, y_prob_values, label="Logistic Regression Curve", color='blue')

# Add a vertical line for the optimal threshold
plt.axvline(x=ppm_at_threshold, color='red', linestyle='--', label=f'Optimal Threshold at {ppm_at_threshold:.2f} ppm')

# Label the axes and title
plt.xlabel('Flammable Gas Concentration (ppm)')
plt.ylabel('Predicted Probability')
plt.title('Logistic Regression Curve with Optimal Threshold for Flammable Gas')
plt.legend(loc='upper left')

# Show the plot
plt.grid(True)
plt.show()

print(f"Flammable Gas optimal threshold stored in .env as: {ppm_at_threshold:.2f} ppm")
