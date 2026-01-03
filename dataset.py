import pandas as pd

df = pd.read_csv('mental_health_dataset.csv')
print(df.head())
print("\nUnique mental_health_risk values:")
print(df['mental_health_risk'].unique())