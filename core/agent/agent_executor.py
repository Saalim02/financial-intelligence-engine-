# core/agent/agent_executor.py

class AgentExecutor:

    def __init__(self, registry):
        self.registry = registry

    def execute(self, plan, df):

        tool_name = plan.get("action")
        entities = plan.get("entities", [])

        if not tool_name:
            return {"error": "No tool action specified."}

        tool = self.registry.get_tool(tool_name)

        if not tool:
            return {"error": f"Tool '{tool_name}' not found."}

        try:
            # Standardized interface
            return tool.run(df, entities)

        except Exception as e:
            return {
                "error": f"Tool execution failed for '{tool_name}'.",
                "details": str(e)
            }
