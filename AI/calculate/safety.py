import os
from dotenv import load_dotenv

# Load the .env file to get gas thresholds
load_dotenv()

# Define the gas thresholds (from .env file)
thresholds = {
    'CO': float(os.getenv('CO_THRESHOLD')),
    'SMOKE': float(os.getenv('SMOKE_THRESHOLD')),
    'ALCOHOL': float(os.getenv('ALCOHOL_THRESHOLD')),
    'FLAMMABLE_GAS': float(os.getenv('FLAMMABLE_GAS_THRESHOLD')),
    'LPG': float(os.getenv('LPG_THRESHOLD')),
    'METHANE': float(os.getenv('METHANE_THRESHOLD')),
}

# Example concentrations (these should be replaced with actual gas concentration values)
concentrations = {
    'CO': 60,  # Example concentration for CO
    'SMOKE': 64000,  # Example concentration for SMOKE
    'ALCOHOL': 370,  # Example concentration for ALCOHOL
    'FLAMMABLE_GAS': 30,  
    'LPG': 2800, 
    'METHANE': 4,  
}

weights = {
    'CO': 0.5,         
    'SMOKE': 0.00,       
    'ALCOHOL': 0.05,     
    'METHANE': 0.30,     
    'LPG': 0.10,         
    'FLAMMABLE_GAS': 0.25, 
}

def calculate_safety_score(concentration, threshold):
    score =1- (concentration / threshold)
    return max(0, score)  

def calculate_safety_index(concentrations, thresholds, weights):
    safety_scores = []
    for gas, concentration in concentrations.items():
        threshold = thresholds[gas]
        weight = weights[gas]
        score = calculate_safety_score(concentration, threshold)
        weighted_score = score * weight
        safety_scores.append(weighted_score)

    return sum(safety_scores)

safety_index = calculate_safety_index(concentrations, thresholds, weights)

MAX_SAFE_INDEX = 0.85  

if safety_index >= MAX_SAFE_INDEX:
    safety_status = "Healthy (Safe)"
else:
    safety_status = "Dangerous (Pollution)"

print(f"Overall Safety Index: {safety_index:.2f}")
print(f"Safety Status: {safety_status}")
