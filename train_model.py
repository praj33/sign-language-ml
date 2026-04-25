import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load dataset
df = pd.read_csv("dataset.csv")

# Features & labels
X = df[["S1", "S2", "S3", "S4", "S5"]]
y = df["label"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42,
    stratify=y
)

# Train
model = RandomForestClassifier(n_estimators=300, max_depth=12)
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
print("\nModel Performance:\n")
print(classification_report(y_test, preds))

# Save model
joblib.dump(model, "model.pkl")
print("\nModel saved as model.pkl")