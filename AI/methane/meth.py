import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import os
from dotenv import load_dotenv, set_key

env_file = '.env'
if not os.path.exists(env_file):
    with open(env_file, 'w'): pass

load_dotenv()

methane_data = pd.read_csv('methane.csv')

plt.figure(figsize=(10, 6))
plt.hist(methane_data['methane'], bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of Methane Values')
plt.xlabel('Methane Concentration (ppm)')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

low_threshold = methane_data['methane'].quantile(0.1)  # 10th percentile
high_threshold = methane_data['methane'].quantile(0.9)  # 90th percentile

methane_data['target'] = ((methane_data['methane'] > high_threshold) | (methane_data['methane'] < low_threshold)).astype(int)

class_counts = methane_data['target'].value_counts()
print(f"Class distribution: {class_counts}")

if len(class_counts) == 1:
    print("Only one class found, consider changing the threshold further.")
else:
    X = methane_data[['methane']]  
    y = methane_data['target']  

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    logreg = LogisticRegression()

    logreg.fit(X_train, y_train)

    X_values = np.linspace(X_train.min(), X_train.max(), 100).reshape(-1, 1)
    y_prob_values = logreg.predict_proba(X_values)[:, 1]

    optimal_threshold = 0.54  

    w = logreg.coef_[0][0]  
    b = logreg.intercept_[0]  

    ppm_at_threshold = (np.log(optimal_threshold / (1 - optimal_threshold)) - b) / w

    set_key(env_file, 'METHANE_THRESHOLD', f"{ppm_at_threshold:.2f}")

    plt.figure(figsize=(10, 6))
    plt.plot(X_values, y_prob_values, label="Logistic Regression Curve", color='blue')

    plt.axvline(x=ppm_at_threshold, color='red', linestyle='--', label=f'Optimal Threshold at {ppm_at_threshold:.2f} ppm')

    plt.xlabel('Methane Concentration (ppm)')
    plt.ylabel('Predicted Probability')
    plt.title('Logistic Regression Curve with Optimal Threshold for Methane')
    plt.legend(loc='upper left')

    plt.grid(True)
    plt.show()

    print(f"Methane optimal threshold stored in .env as: {ppm_at_threshold:.2f} ppm")
