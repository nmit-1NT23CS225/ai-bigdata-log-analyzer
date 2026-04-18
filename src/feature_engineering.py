import pandas as pd

def build_features(ip_stats_df):
    """
    Converts PySpark aggregated DataFrame to Pandas and engineers features
    for machine learning.
    """
    # Convert PySpark DataFrame to Pandas
    pdf = ip_stats_df.toPandas()
    
    # Feature Engineering
    # Calculate error ratio (error_count / total_requests)
    pdf['error_ratio'] = pdf['error_count'] / pdf['total_requests']
    
    # Fill NaN values just in case
    pdf.fillna(0, inplace=True)
    
    return pdf
