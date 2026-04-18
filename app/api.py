import os
import tempfile
import sys
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

# Add src to Python path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.log_parser import get_spark_session, parse_logs
from src.spark_processing import aggregate_log_data, get_peak_traffic_hour, get_most_frequent_endpoints
from src.feature_engineering import build_features
from src.anomaly_detection import detect_anomalies, get_suspicious_ips

app = FastAPI(title="AI-Powered Big Data Log Analyzer API")

# Initialize Spark Session globally for the API
spark = get_spark_session("FastAPI_LogAnalyzer")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running"}

@app.post("/analyze")
async def analyze_logs(file: UploadFile = File(...)):
    """
    Receives a log file, processes it through the PySpark pipeline,
    and returns anomaly detection results.
    """
    try:
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".log") as tmp:
            tmp.write(await file.read())
            temp_path = tmp.name

        # 1. Parse Logs
        parsed_df = parse_logs(spark, temp_path)
        
        # Gather global stats
        total_logs = parsed_df.count()
        peak_hour, peak_count = get_peak_traffic_hour(parsed_df)
        top_endpoints = get_most_frequent_endpoints(parsed_df)
        
        # 2. PySpark Processing
        ip_stats_df = aggregate_log_data(parsed_df)
        
        # 3. Feature Engineering (Pandas)
        features_pdf = build_features(ip_stats_df)
        
        # 4. Anomaly Detection
        analyzed_pdf = detect_anomalies(features_pdf)
        suspicious_ips = get_suspicious_ips(analyzed_pdf)
        
        # Get top 10 IPs by traffic
        top_ips = analyzed_pdf.sort_values(by='total_requests', ascending=False).head(10).to_dict(orient='records')
        
        # Compute overall error rate
        total_requests = features_pdf['total_requests'].sum()
        total_errors = features_pdf['error_count'].sum()
        overall_error_rate = float(total_errors / total_requests) if total_requests > 0 else 0.0

        # Clean up temp file
        os.unlink(temp_path)

        # Prepare response
        return JSONResponse(content={
            "summary": {
                "total_logs_analyzed": total_logs,
                "total_unique_ips": len(features_pdf),
                "total_anomalies_found": len(suspicious_ips),
                "peak_traffic_hour": peak_hour,
                "overall_error_rate": round(overall_error_rate, 4)
            },
            "top_ips": top_ips,
            "suspicious_ips": suspicious_ips,
            "top_endpoints": top_endpoints
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
