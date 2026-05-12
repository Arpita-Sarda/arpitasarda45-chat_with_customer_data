"""
This file converts user questions into Pandas queries
using Gemini API
"""

from google import genai
import pandas as pd
import re
from data_loader import get_schema_description


class QueryEngine:

    def __init__(self, api_key, dataframe):

        self.client = genai.Client(api_key=api_key)

        self.model_name = 'gemini-2.5-flash-lite'

        self.dataframe = dataframe

        self.schema_info = get_schema_description(dataframe)

    def generate_pandas_code(self, question):

        prompt = f"""
You are a Pandas expert.

{self.schema_info}

Rules:
1. DataFrame name is dataframe
2. Return only Python code
3. Save final output in variable called result
4. No explanations
5. No markdown
6. No print statements

Question:
{question}

Python Code:
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )

        generated_code = response.text.strip()

        # Removing markdown if Gemini returns it
        generated_code = re.sub(r'^```python\\s*', '', generated_code)
        generated_code = re.sub(r'^```\\s*', '', generated_code)
        generated_code = re.sub(r'\\s*```$', '', generated_code)

        return generated_code

    def execute_code(self, code):

        try:

            local_variables = {
                'pd': pd,
                'dataframe': self.dataframe.copy()
            }

            exec(code, local_variables)

            return True, local_variables.get('result', 'No result found'), ""

        except Exception as error:

            return False, None, str(error)

    def format_result(self, result):

        if isinstance(result, pd.DataFrame):

            if len(result) == 0:
                return "No matching records found."

            elif len(result) <= 20:
                return result.to_string(index=False)

            else:
                return result.head(20).to_string(index=False)

        elif isinstance(result, pd.Series):

            return result.to_string()

        elif isinstance(result, (int, float)):

            if isinstance(result, int):
                return f"{result:,}"

            return f"{result:,.2f}"

        else:
            return str(result)

    def generate_summary(self, result, question):

        try:

            prompt = f"""
Question: {question}

Result:
{str(result)[:1000]}

Give a short summary in 1 sentence.
"""

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )

            return response.text.strip()

        except:
            return ""

    def query(self, question):

        code = self.generate_pandas_code(question)

        success, result, error = self.execute_code(code)

        if not success:

            # Trying one more time if error comes
            code = self.generate_pandas_code(
                f"{question} (Previous error: {error})"
            )

            success, result, error = self.execute_code(code)

        if success:

            return {
                'success': True,
                'answer': self.format_result(result),
                'summary': self.generate_summary(result, question),
                'code': code
            }

        else:

            return {
                'success': False,
                'answer': f"Error: {error}",
                'summary': "",
                'code': code
            }


def create_query_engine(api_key, dataframe):

    return QueryEngine(api_key, dataframe)