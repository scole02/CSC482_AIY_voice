import pandas as pd
import numpy as np

url = 'https://raw.githubusercontent.com/scole02/CSC482_AIY_voice/master/data/'

df_profs = pd.read_csv(url + "profs.csv")
df_sched = pd.read_csv(url + "schedule.csv")

def clean_instructor(prof):
  if str(prof) != "nan":
    input = prof.split(", ")
    return input[0]
  else:
    return prof

df_sched['Course'] = df_sched['Course'].str.lower()
df_sched['Description'] = df_sched['Description'].str.lower()
df_sched['Instructor'] = df_sched['Instructor'].apply(clean_instructor)

df_profs['first_name'] = df_profs['first_name'].str.lower()
df_profs['last_name'] = df_profs['last_name'].str.lower()

df_sched = df_sched.drop(columns=['Unnamed: 0'])
df_sched = df_sched.drop_duplicates(keep='last')

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

def get_quarters(query):
  if query.get("Quarter"):
    quarters = [query.get("Quarter")]
  else:
    quarters = ["F", "W", "S"]
  return quarters

def no_matches(course, quarter):
  quarter_names = {"F": "Fall", "W": "Winter", "S": "Spring"}
  if quarter:
    return "No matching sections of " + course + " are offered " + quarter_names[quarter] 
  else:
    return "No matching sections of " + course + " are offered"

def many_matches(course, query, df):
  quarter_names = {"F": "Fall", "W": "Winter", "S": "Spring"}
  quarters = get_quarters(query)
  quarter_info = ""
  res = ""
  if len(quarters) == 1:
    quarter_info = " are offered during " + quarter_names[quarters[0]]
  elif len(quarters) == 2:
    quarter_info = " are offered during " + quarter_names[quarters[0]] + " and " + quarter_names[quarters[1]]
  elif len(quarters) == 3:
    quarter_info = " are offered throughout Fall, Winter, and Spring" 
  num_sections = len(df)
  return str(num_sections) + " sections of " + course + quarter_info + ". Please check schedules.calpoly.edu for more info"

def get_days(input):
  if str(input) == "nan":
    return None
  day_names = {"M": "Monday", "T": "Tuesday", "W": "Wednesday", "R": "Thursday", "F": "Friday"}
  res = [day_names[d] for d in input]
  return ' '.join(res)

def get_time(start, end):
  if str(start) == "nan":
    return None
  return " from " + start + " to " + end

def get_format(location, time):
  if time == None:
    return "asynchronously"
  if location == '999':
    return "virtually"
  return "in-person"

def get_prof(prof):
  if str(prof) == "nan":
    return "an unknown professor"
  else:
    return "Professor " + prof

def general_course_info(course, df):
  res = course + " is taught by "
  for i in range(len(df)):
    if (i > 0 and i == len(df) - 1):
      res += "and "
    row = df.iloc[i]
    prof = get_prof(row["Instructor"])
    days = get_days(row["Days"])
    time = get_time(row["Start"], row["End"])
    format = get_format(row["Location"], time)
    if format == "asynchronously":
      res += prof + " asynchronously. "
    else:
      res += prof + time + " " + format + " on " + days + ". "
  return res

def specific_course_info(course, df):
  col = df.columns.tolist()
  res = course + " is "
  for i in range(len(df)):
    if (i > 0 and i == len(df) - 1):
      res += "and "
    row = df.iloc[i]
    if "Course" in col:
      res += row["Course"]
    if "Description" in col:
      res += row["Description"]
    if "Sect" in col:
      res += " Section " + str(row["Sect"])

    if "Days" in col:
      res += " on " + get_days(row["Days"])
    
    if "Start" in col:
      res += get_time(row["Start"], row["End"])

    if "Instructor" in col:
      res += " taught by " + get_prof(row["Instructor"])

    if "Location" in col:
      if str(row["Location"]) == "nan":
        res += " virtual "
      else:
        res += " in " + row["Location"]

    if "Format" in col:
      if res[-3:] == "is ":
        res += "taught " 
      res += " " + row["Format"]

    res += ". "

  return res

def some_matches(course, df):
  num_col = len(df.columns)
  # All columns are returned
  if num_col > 5:
    return general_course_info(course, df)

  # Queried by column, not all returned
  else:
    return specific_course_info(course, df)

def generate_sched_response(query, df):
  print(df)
  course = query.get("Course", query.get("Description", "Requested course"))
  quarter = query.get("Quarter", None)
  res = ""
  # No matches to the search
  if len(df) == 0:
    res = no_matches(course, quarter)
    
  # Lots of matches to the search 
  elif len(df) > 4:
    res = many_matches(course, query, df)

  # 4 or less matches to the search
  else:
    res = some_matches(course, df)

  # print(res)
  return res

def no_prof_matches(prof, quarters):
  return prof + " is not teaching in the " + quarters


def prof_matches(prof, quarters, df):
  courses = []
  for i in range(len(df)):
    res = df.Courses.tolist()[i][2:-2].split("', '")
    for c in res:
      if not c in courses:
        courses.append(c)
  if courses == ["on"]:
    return no_prof_matches(prof, quarters)
  if len(courses) > 1:
    courses.insert(-1, "and")
  # Cap at 20 courses
  courses = ' '.join(courses[:20])
  if len(quarters) < 10:
    return prof + " teaches " + courses + " in the " + quarters
  else:
    return prof + " teaches " + courses + " over " + quarters 

def generate_prof_response(query, df):
  # print(df)
  prof = "Professor " + query.get("last_name", query.get("Name", "requested professor")) 
  if prof == "Professor requested professor":
    return "Not understood"
  quarter_names = {"F": "Fall", "W": "Winter", "S": "Spring"}
  quarters = [quarter_names[q] for q in get_quarters(query)]
  if len(quarters) > 1:
    quarters.insert(2, "and")
  quarters = ' '.join(quarters)
  res = ""

  # No matches to the search
  if len(df) == 0:
    res = no_prof_matches(prof, quarters)

  # Found match(s)
  else:
    res = prof_matches(prof, quarters, df)

  # print(res)
  return res


def generate_response(df_name, query, col=[]):
  res = None
  if df_name == "df_sched":
    if len(col) == 0:
      res = query_data(df_sched, query)
    else:
      res = query_data_columns(df_sched, query, col)
    return generate_sched_response(query, res)

  else:
    if len(col) == 0:
      res = query_data(df_profs, query)
    else:
      res = query_data_columns(df_profs, query, col)
    return generate_prof_response(query, res)


