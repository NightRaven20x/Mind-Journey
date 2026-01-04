import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import pickle

print("Loading dataset...")
df = pd.read_csv('mental_health_dataset.csv')
print(f"Dataset loaded: {len(df)} rows\n")

# Encode categorical variables to numbers
print("Encoding categorical data...")
label_encoders = {}

# Gender
le_gender = LabelEncoder()
df['gender_encoded'] = le_gender.fit_transform(df['gender'])
label_encoders['gender'] = le_gender

# Employment Status
le_employment = LabelEncoder()
df['employment_encoded'] = le_employment.fit_transform(df['employment_status'])
label_encoders['employment_status'] = le_employment

# Work Environment
le_work = LabelEncoder()
df['work_environment_encoded'] = le_work.fit_transform(df['work_environment'])
label_encoders['work_environment'] = le_work

# Mental Health History
le_history = LabelEncoder()
df['mental_health_history_encoded'] = le_history.fit_transform(df['mental_health_history'])
label_encoders['mental_health_history'] = le_history

# Seeks Treatment
le_treatment = LabelEncoder()
df['seeks_treatment_encoded'] = le_treatment.fit_transform(df['seeks_treatment'])
label_encoders['seeks_treatment'] = le_treatment

# Target variable (what we predict)
le_target = LabelEncoder()
df['risk_encoded'] = le_target.fit_transform(df['mental_health_risk'])
label_encoders['mental_health_risk'] = le_target

print(f"Risk levels: {le_target.classes_}\n")

# Prepare features (X) and target (y)
feature_columns = [
    'age',
    'gender_encoded',
    'employment_encoded',
    'work_environment_encoded',
    'mental_health_history_encoded',
    'seeks_treatment_encoded',
    'stress_level',
    'sleep_hours',
    'physical_activity_days',
    'depression_score',
    'anxiety_score',
    'social_support_score',
    'productivity_score'
]

X = df[feature_columns]
y = df['risk_encoded']

# Split data: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training samples: {len(X_train)}")
print(f"Testing samples: {len(X_test)}\n")

# Train the model
print("Training model...")
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Calculate accuracy (THIS MUST COME FIRST!)
train_accuracy = model.score(X_train, y_train) * 100
test_accuracy = model.score(X_test, y_test) * 100

# Save model and encoders
print("\nSaving model...")
with open('mental_health_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)

print("Done! Model saved successfully.")
