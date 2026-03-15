# core/agent/tool_registry.py

class ToolRegistry:

    def __init__(self, engines):
        """
        Registry that maps tool names used by the agent
        to the actual engine implementations.
        """

        required_tools = {
            "aggregation": "aggregation",
            "trend": "time",
            "anomaly": "anomaly",
            "correlation": "correlation",
            "financial_health": "financial",
            "metric": "metric",
            "sql_query": "sql"
        }

        self.tools = {}

        for public_name, engine_key in required_tools.items():

            engine = engines.get(engine_key)

            if engine is None:
                raise ValueError(
                    f"Engine '{engine_key}' not provided for tool '{public_name}'."
                )

            self.tools[public_name] = engine

    def list_tools(self):
        """
        Returns all available tool names.
        """
        return list(self.tools.keys())

    def get_tool(self, tool_name):
        """
        Retrieve the engine corresponding to a tool.
        """
        if tool_name not in self.tools:
            return None

        return self.tools[tool_name]