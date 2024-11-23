import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import pickle
import warnings

warnings.filterwarnings("ignore")

# 1. Load and preprocess data
data = pd.read_csv("data.csv")

# Add a binary classification column for fire probability
threshold = 0.5  # Threshold for fire probability
data["BinaryFire"] = (data["ProbabilityOfFire"] >= threshold).astype(int)

# Separate features and targets
X = data.iloc[:, :-3].values  # Features: Exclude 'DangerousDegree', 'ProbabilityOfFire', and 'BinaryFire'
y_risk_level = data["DangerousDegree"].values  # Target 1: Risk level
y_fire_binary = data["BinaryFire"].values  # Target 2: Binary fire probability

# Normalize features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Split data for binary fire probability prediction
X_train_fire, X_test_fire, y_train_fire, y_test_fire = train_test_split(X_scaled, y_fire_binary, test_size=0.3, random_state=0)

# 2. Train SVM for risk level prediction
risk_model = SVC(kernel="linear", probability=True)
risk_model.fit(X_scaled, y_risk_level)

# 3. Train Logistic Regression for fire probability prediction
log_reg = LogisticRegression()
log_reg.fit(X_train_fire, y_train_fire)

# 4. Save the models and scaler
pickle.dump(risk_model, open("svm_risk_model.pkl", "wb"))
pickle.dump(log_reg, open("logistic_fire_model.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))

print("Both models and the scaler have been saved successfully.")
