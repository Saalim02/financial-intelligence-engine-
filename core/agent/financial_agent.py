import json
from .memory import Memory
from .llm_interface import LLMInterface
from .tool_registry import ToolRegistry
from .agent_executor import AgentExecutor
from .tool_schema import get_tool_schemas
from .query_planner import QueryPlanner


class FinancialAgent:

    def __init__(self, engines, api_key):

        self.memory = Memory(max_history=20)
        self.llm = LLMInterface(api_key)

        self.registry = ToolRegistry(engines)
        self.executor = AgentExecutor(self.registry)

        self.tool_schemas = get_tool_schemas()

        # pass llm into planner (important)
        self.planner = QueryPlanner(self.llm)

    def ask(self, question, df, mode="Insight"):

        columns = list(df.columns)
        available_tools = self.registry.list_tools()

        # ----------------------------------
        # 1️⃣ Generate SQL plan using LLM
        # ----------------------------------

        plan = self.planner.plan(question, columns)

        if not plan or plan["action"] not in available_tools:

            return {
                "error": "Unable to generate valid query plan.",
                "available_tools": available_tools
            }

        # ----------------------------------
        # 2️⃣ Execute SQL
        # ----------------------------------

        result = self.executor.execute(plan, df)

        if isinstance(result, dict) and "error" in result:

            return {
                "error": result["error"],
                "query": result.get("query", "")
            }

        # Save conversation memory
        self.memory.add(question, str(result))

        # ----------------------------------
        # 3️⃣ SQL MODE
        # ----------------------------------

        if mode == "SQL":

            return {
                "mode": "SQL",
                "sql_query": plan["entities"][0],
                "final_answer": result
            }

        # ----------------------------------
        # 4️⃣ DASHBOARD MODE
        # ----------------------------------

        if mode == "Dashboard":

            return {
                "mode": "Dashboard",
                "dashboard_data": result,
                "sql_query": plan["entities"][0],
                "final_answer": result
            }

        # ----------------------------------
        # 5️⃣ INSIGHT MODE
        # ----------------------------------

        explanation = self.llm.generate(
            "Explain the following dataset result as a business insight.",
            str(result)
        )

        return {
            "mode": "Insight",
            "insight": explanation,
            "sql_query": plan["entities"][0],
            "final_answer": result
        }