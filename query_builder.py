import pandas as pd

def complex_query_builder(input):
  """
  Create a complex pandas query from a combination of query parameters
  :param dict input: A dictionary of input parameters with the structure column_name: value
  :return: a pandas query 
  :rtype: str
  """
  query = ""
  for key, value in input.items():
    query_str = key + " == '" + value + "' & "
    query += query_str
  return query[:-3]

def query_data(df, input, print_str=False):
  """
  Query the given pandas dataframe by the given input parameters
  :param df: The dataframe to query
  :param dict input: A dictionary of input parameters with the structure column_name: value
  :param bool print_str: Whether or not to print the query string
  :return: All dataframe entries that match the query params 
  :rtype: pandas dataframe
  """
  query_str = complex_query_builder(input)
  if print_str:
    print(query_str)
  return df.query(query_str)

def query_data_columns(df, input, columns, print_str=False):
  """
  Query the given pandas dataframe by the given input parameters and return only the provided columns
  :param df: The dataframe to query
  :param dict input: A dictionary of input parameters with the structure column_name: value
  :param list columns: The columns to return
  :param bool print_str: Whether or not to print the query string
  :return: Specified columns for all dataframe entries that match the query params 
  :rtype: pandas dataframe
  """
  data_df = query_data(df, input, print_str)
  if (print_str):
    print(columns)
    print(data_df)
  return data_df[columns].drop_duplicates()