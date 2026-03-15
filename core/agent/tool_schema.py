# core/agent/tool_schema.py

def get_tool_schemas():

    return {
        "aggregation": {
            "description": "Calculate grouped totals and category performance for a numeric KPI column.",
            "required_entities": True,
            "min_entities": 1,
            "max_entities": 1,
            "entity_type": "numeric_column"
        },
        "trend": {
            "description": "Analyze time-based trends for a numeric column using a date column.",
            "required_entities": True,
            "min_entities": 1,
            "max_entities": 1,
            "entity_type": "numeric_column"
        },
        "anomaly": {
            "description": "Detect statistical anomalies in numeric columns using IQR.",
            "required_entities": True,
            "min_entities": 1,
            "max_entities": 5,
            "entity_type": "numeric_column"
        },
        "correlation": {
            "description": "Find strongest correlations between numeric columns.",
            "required_entities": False,
            "min_entities": 0,
            "max_entities": 0,
            "entity_type": None
        },
        "financial_health": {
            "description": "Analyze financial performance including revenue, profit, and margin.",
            "required_entities": False,
            "min_entities": 0,
            "max_entities": 0,
            "entity_type": None
        },
        "metric": {
            "description": "Detect financial metric columns like revenue, profit, cost.",
            "required_entities": False,
            "min_entities": 0,
            "max_entities": 0,
            "entity_type": None
        },
        "groupby": {
            "description": "Find entities with highest or lowest frequency using groupby counts",
            "required_entities": True,
            "min_entities": 1,
            "max_entities": 1,
            "entity_type": "categorical_column"
        },
        
        "sql_query": {
            "description": "Execute SQL queries on the dataset using table name 'df'",
            "required_entities": True,
            "min_entities": 1,
            "max_entities": 1,
            "entity_type": "sql_query"
        }
    }
