import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(logs):
    df = pd.DataFrame(logs)
    model = IsolationForest(random_state=42)
    df["anomaly_score"] = model.fit_predict(df[["length"]])
    return df