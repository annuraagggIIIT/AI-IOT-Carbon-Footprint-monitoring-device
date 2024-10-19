import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import os
from dotenv import load_dotenv, set_key

load_dotenv()

alcohol_data = pd.read_csv('alcohol.csv')

alcohol_data['alcohol'].fillna(alcohol_data['alcohol'].median(), inplace=True)

threshold = alcohol_data['alcohol'].median()

alcohol_data['target'] = (alcohol_data['alcohol'] > threshold).astype(int)

X = alcohol_data[['alcohol']]  
y = alcohol_data['target'] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

logreg = LogisticRegression()

logreg.fit(X_train, y_train)

X_values = np.linspace(X_train.min(), X_train.max(), 100).reshape(-1, 1)
y_prob_values = logreg.predict_proba(X_values)[:, 1]

optimal_threshold = 0.54  

w = logreg.coef_[0][0]  
b = logreg.intercept_[0]  

ppm_at_threshold = (np.log(optimal_threshold / (1 - optimal_threshold)) - b) / w

env_file = '.env'
set_key(env_file, 'ALCOHOL_THRESHOLD', f"{ppm_at_threshold:.2f}")

plt.figure(figsize=(10, 6))
plt.plot(X_values, y_prob_values, label="Logistic Regression Curve", color='blue')

plt.axvline(x=ppm_at_threshold, color='red', linestyle='--', label=f'Optimal Threshold at {ppm_at_threshold:.2f} ppm')

plt.xlabel('Alcohol Concentration (ppm)')
plt.ylabel('Predicted Probability')
plt.title('Logistic Regression Curve with Optimal Threshold for Alcohol')
plt.legend(loc='upper left')

plt.grid(True)
plt.show()

print(f"Alcohol optimal threshold stored in .env as: {ppm_at_threshold:.2f} ppm")