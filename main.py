# main.py

import os
from dotenv import load_dotenv
import pandas as pd

from core.engines.aggregation import AggregationEngine
from core.engines.time_analyzer import TimeAnalyzer
from core.engines.anomaly_detector import AnomalyDetector
from core.engines.correlation import CorrelationEngine
from core.engines.financial_analyzer import FinancialAnalyzer
from core.engines.metric_engine import MetricEngine
from core.engines.sql_engine import SQLEngine

from core.agent.financial_agent import FinancialAgent


# ----------------------------------------
# Robust File Loader
# ----------------------------------------

def load_data(path):
    """
    Load CSV or Excel file automatically.
    Supports: .csv, .xls, .xlsx
    """

    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    extension = path.split(".")[-1].lower()

    if extension == "csv":
        try:
            return pd.read_csv(path, encoding="utf-8")
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding="latin-1")

    elif extension in ["xls", "xlsx"]:
        return pd.read_excel(path)

    else:
        raise ValueError("Unsupported file format. Use CSV or Excel.")


# ----------------------------------------
# Engine Initialization
# ----------------------------------------

def initialize_engines():
    return {
        "aggregation": AggregationEngine(),
        "time": TimeAnalyzer(),
        "anomaly": AnomalyDetector(),
        "correlation": CorrelationEngine(),
        "financial": FinancialAnalyzer(),
        "metric": MetricEngine(),
        "sql": SQLEngine()
    }


# ----------------------------------------
# MAIN ENTRY
# ----------------------------------------

if __name__ == "__main__":

    # Load environment variables
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("ERROR: OPENAI_API_KEY not found in .env file")
        exit()

    # Ask user for dataset path
    file_path = input("Enter dataset file path (CSV/XLS/XLSX): ").strip()

    try:
        df = load_data(file_path)
        print(f"\nLoaded dataset successfully: {df.shape[0]} rows, {df.shape[1]} columns\n")
    except Exception as e:
        print(f"Failed to load dataset: {e}")
        exit()

    # Initialize engines
    engines = initialize_engines()

    # Initialize Agent
    agent = FinancialAgent(
        engines=engines,
        api_key=api_key
    )

    print("Autonomous Financial AI Agent is ready.")
    print("Type 'exit' to quit.\n")

    # Chat Loop
    while True:

        question = input("Ask your financial question: ").strip()

        if question.lower() == "exit":
            print("Exiting agent.")
            break

        try:
            response = agent.ask(question, df)

            print("\nAgent Response:")
            print(response)
            print("\n" + "-" * 60 + "\n")

        except Exception as e:
            print(f"Error during processing: {e}")
