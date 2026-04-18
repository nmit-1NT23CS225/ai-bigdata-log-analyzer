from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract, col, to_timestamp

def get_spark_session(app_name="LogAnalyzer"):
    """Initialize and return a Spark session."""
    spark = SparkSession.builder \
        .appName(app_name) \
        .master("local[*]") \
        .getOrCreate()
    # Reduce logging verbosity
    spark.sparkContext.setLogLevel("WARN")
    return spark

def parse_logs(spark, file_path):
    """
    Read raw log file and parse into structured PySpark DataFrame.
    Format expected: 192.168.1.1 - - [18/Apr/2026:10:00:00 +0000] "GET /api/v1/data HTTP/1.1" 200 1024
    """
    raw_df = spark.read.text(file_path)
    
    # Regex patterns for Apache/Nginx combined log format
    ip_pattern = r'^(\S+)'
    timestamp_pattern = r'\[([^\]]+)\]'
    request_pattern = r'\"(\S+)\s+(\S+)\s+([^\"]+)\"'
    status_pattern = r'\"\s+(\d{3})'
    
    parsed_df = raw_df.select(
        regexp_extract('value', ip_pattern, 1).alias('ip'),
        regexp_extract('value', timestamp_pattern, 1).alias('timestamp_str'),
        regexp_extract('value', request_pattern, 1).alias('method'),
        regexp_extract('value', request_pattern, 2).alias('endpoint'),
        regexp_extract('value', status_pattern, 1).cast('integer').alias('status_code')
    )
    
    # Filter out invalid rows (if any didn't parse correctly)
    parsed_df = parsed_df.filter(col('ip') != '')
    
    # Parse timestamp
    parsed_df = parsed_df.withColumn(
        'timestamp', 
        to_timestamp(col('timestamp_str'), 'dd/MMM/yyyy:HH:mm:ss Z')
    )
    
    return parsed_df

if __name__ == "__main__":
    # Test parsing
    spark = get_spark_session()
    df = parse_logs(spark, "../data/sample_logs.log")
    df.show(5, truncate=False)
    spark.stop()
