# core/agent/memory.py

class Memory:

    def __init__(self, max_history=20):
        self.history = []
        self.max_history = max_history

    def add(self, user, agent_response):

        self.history.append({
            "user": user,
            "agent": agent_response
        })

        # Keep memory bounded
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_recent(self, n=5):
        return self.history[-n:]

    def format_for_prompt(self, n=5):
        """
        Returns formatted conversation history
        to inject into LLM prompt.
        """

        recent = self.get_recent(n)

        formatted = ""

        for item in recent:
            formatted += f"User: {item['user']}\n"
            formatted += f"Agent: {item['agent']}\n\n"

        return formatted.strip()

    def clear(self):
        self.history = []
