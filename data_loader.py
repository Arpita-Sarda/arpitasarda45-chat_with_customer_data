"""
This file handles Excel data loading
"""

import pandas as pd


def load_excel_data(file):

    """
    Read Excel file and return dataframe
    """

    dataframe = pd.read_excel(file)

    # Removing extra spaces from column names
    dataframe.columns = dataframe.columns.str.strip()

    return dataframe


def get_schema_description(dataframe):

    """
    Create dataset information for Gemini
    """

    schema_text = f"""
Dataset Information

Total Rows: {len(dataframe)}

Columns:
{', '.join(dataframe.columns.tolist())}

Column Details:
"""

    for column in dataframe.columns:

        data_type = dataframe[column].dtype

        if data_type == 'object':

            unique_count = dataframe[column].nunique()

            sample_values = dataframe[column].dropna().head(3).tolist()

            schema_text += f"""
- {column}
  Type: Text
  Unique Values: {unique_count}
  Sample Values: {sample_values}
"""

        elif data_type in ['int64', 'float64']:

            schema_text += f"""
- {column}
  Type: Number
  Minimum: {dataframe[column].min()}
  Maximum: {dataframe[column].max()}
  Average: {dataframe[column].mean():.2f}
"""

        else:

            schema_text += f"""
- {column}
  Type: {data_type}
"""

    return schema_text