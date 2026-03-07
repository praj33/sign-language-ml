import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

DATASET_PATH = "sign_glove_synthetic_dataset.csv"
MODEL_PATH = "sign_language_rf_model.pkl"
FEATURE_COLS = ["thumb", "index", "middle", "ring", "little"]


def main():
    df = pd.read_csv(DATASET_PATH)

    X = df[FEATURE_COLS]
    y = df["letter"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=14,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Accuracy: {acc:.4f}")

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved: {MODEL_PATH}")


if __name__ == "__main__":
    main()
