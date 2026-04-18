# AI-Powered Big Data Log Analyzer

An end-to-end data engineering and machine learning project that processes large-scale server logs using PySpark, detects anomalies (suspicious IP activity) using Isolation Forest, and presents insights via a FastAPI backend and a Streamlit dashboard.

## 📁 Project Structure

```
ai-bigdata-log-analyzer/
├── data/
│   ├── generate_logs.py      # Script to generate synthetic logs
│   └── sample_logs.log       # Auto-generated sample dataset
├── src/
│   ├── log_parser.py         # PySpark raw log parsing
│   ├── spark_processing.py   # PySpark data aggregations
│   ├── feature_engineering.py# Pandas feature formatting
│   └── anomaly_detection.py  # Scikit-learn Isolation Forest model
├── app/
│   ├── api.py                # FastAPI backend endpoints
│   └── dashboard.py          # Streamlit frontend UI
├── requirements.txt
├── README.md
└── .gitignore
```

## ▶️ Execution Instructions

### 1. Install Dependencies

First, ensure you have Python 3.10+ installed. It is recommended to use a virtual environment.

```bash
cd ai-bigdata-log-analyzer
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 2. Generate Sample Data

To test the system, generate a sample log file containing normal and anomalous traffic.

```bash
python data/generate_logs.py
```
This will create `data/sample_logs.log` with 10,000 synthetic log entries.

### 3. Install and Run Spark Locally

PySpark will automatically run in local mode when executed via the Python scripts; you don't need to manually configure a standalone cluster. Just ensure you have Java (JDK 8 or 11) installed on your system.

### 4. Run the Backend API (FastAPI)

The backend provides the analysis engine as an API.

```bash
uvicorn app.api:app --reload
```
The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).
You can view the interactive API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 5. Run the Frontend Dashboard (Streamlit)

In a new terminal window (with the virtual environment activated), start the UI:

```bash
streamlit run app/dashboard.py
```
The dashboard will open automatically in your browser (usually at `http://localhost:8501`).
Upload `data/sample_logs.log` to view the analysis!

## ⚙️ Features

- **Big Data Processing**: Leverages Apache Spark to efficiently group, count, and aggregate IP request and error rates.
- **Machine Learning**: Utilizes Scikit-learn's Isolation Forest to pinpoint suspicious network behavior based on multi-dimensional features (requests, error ratio, endpoint spread).
- **Interactive Visualization**: Explores distributions and time-series traffic spikes using Plotly and Streamlit.
