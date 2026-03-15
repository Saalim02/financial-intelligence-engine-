class GroupByAnalyzer:

    def run(self, df, entities=None):

        if not entities or len(entities) < 1:
            return {"error": "Group column not provided"}

        group_col = entities[0]

        if group_col not in df.columns:
            return {"error": f"{group_col} not found"}

        counts = df[group_col].value_counts()

        if counts.empty:
            return {"error": "No records"}

        least_customer = counts.idxmin()
        least_orders = counts.min()

        most_customer = counts.idxmax()
        most_orders = counts.max()

        return {
            "least_frequent": {
                "customer": least_customer,
                "orders": int(least_orders)
            },
            "most_frequent": {
                "customer": most_customer,
                "orders": int(most_orders)
            }
        }