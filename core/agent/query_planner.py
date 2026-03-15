class QueryPlanner:

    def __init__(self, llm):
        self.llm = llm

    def plan(self, question: str, columns: list):

        system_prompt = f"""
You are an expert SQL generator.

Convert the user question into SQL.

Table name: df

Columns available:
{columns}

Rules:
- Return ONLY SQL.
- Do not explain anything.
- SQL must start with SELECT.
- Use GROUP BY for aggregations.
- Use SUM, AVG, COUNT when required.
"""

        sql_query = self.llm.generate(system_prompt, question)

        if not sql_query:
            return {"action": "sql_query", "entities": []}

        sql_query = (
            sql_query.replace("```sql", "")
            .replace("```", "")
            .strip()
        )

        select_index = sql_query.lower().find("select")

        if select_index != -1:
            sql_query = sql_query[select_index:]

        return {
            "action": "sql_query",
            "entities": [sql_query]
        }