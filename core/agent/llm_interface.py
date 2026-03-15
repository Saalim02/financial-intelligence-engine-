# core/agent/llm_interface.py

from openai import OpenAI


class LLMInterface:

    def __init__(self, api_key, model="gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, system_prompt, user_prompt):

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0
            )

            if not response.choices:
                return ""

            message = response.choices[0].message

            if not message or not message.content:
                return ""

            return message.content

        except Exception as e:
            return f'{{"error": "LLM call failed", "details": "{str(e)}"}}'
