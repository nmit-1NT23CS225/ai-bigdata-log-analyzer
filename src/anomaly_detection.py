import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(features_pdf):
    """
    Trains an Isolation Forest model to detect anomalous IP addresses based on features.
    """
    if features_pdf.empty:
        return features_pdf
        
    # Select features for training
    feature_cols = ['total_requests', 'error_count', 'error_ratio', 'unique_endpoints']
    X = features_pdf[feature_cols]
    
    # Initialize Isolation Forest
    # contamination is the expected proportion of outliers. We set a small arbitrary value.
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    
    # Fit and Predict (-1 for outliers, 1 for inliers)
    preds = model.fit_predict(X)
    
    # Add anomaly column: True if prediction is -1
    features_pdf['is_anomaly'] = preds == -1
    
    return features_pdf

def get_suspicious_ips(analyzed_pdf):
    """Returns a list of IP addresses flagged as anomalies."""
    if 'is_anomaly' not in analyzed_pdf.columns:
        return []
    
    anomalies = analyzed_pdf[analyzed_pdf['is_anomaly'] == True]
    # Sort by total requests descending
    anomalies = anomalies.sort_values(by='total_requests', ascending=False)
    
    # Return as list of dictionaries
    return anomalies[['ip', 'total_requests', 'error_count', 'error_ratio', 'unique_endpoints']].to_dict(orient='records')
