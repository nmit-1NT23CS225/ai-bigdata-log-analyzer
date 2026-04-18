from pyspark.sql.functions import col, count, when, countDistinct, hour

def aggregate_log_data(parsed_df):
    """
    Perform Big Data processing using PySpark.
    Aggregates data by IP address.
    """
    
    # Add hour column for peak traffic analysis
    df_with_hour = parsed_df.withColumn('hour', hour(col('timestamp')))
    
    # Aggregate metrics per IP
    ip_stats = df_with_hour.groupBy('ip').agg(
        count('*').alias('total_requests'),
        count(when(col('status_code') >= 400, True)).alias('error_count'),
        countDistinct('endpoint').alias('unique_endpoints')
    )
    
    return ip_stats

def get_peak_traffic_hour(parsed_df):
    """Returns the hour with the maximum requests."""
    hourly_traffic = parsed_df.withColumn('hour', hour(col('timestamp'))) \
                              .groupBy('hour') \
                              .count() \
                              .orderBy(col('count').desc())
    
    peak_row = hourly_traffic.first()
    if peak_row:
         return peak_row['hour'], peak_row['count']
    return None, 0

def get_most_frequent_endpoints(parsed_df, limit=5):
    """Returns the most frequently accessed endpoints."""
    endpoints = parsed_df.groupBy('endpoint') \
                         .count() \
                         .orderBy(col('count').desc()) \
                         .limit(limit)
    return endpoints.toPandas().to_dict(orient='records')
