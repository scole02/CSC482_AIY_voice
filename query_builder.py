import pandas as pd

url = 'https://raw.githubusercontent.com/EmilyGavrilenko/GoogleHomeSchedules/main/'

df_profs = pd.read_csv(url + "profs.csv")
df_sched = pd.read_csv(url + "schedule.csv")

df_sched[-5:]

df_profs[:5]

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

# help_msg =

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
  day_arr = list(input.replace("TR", "R"))
  res = [day_names[d] for d in day_arr]
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
  # print(col)
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

  print(res)

# generate_response(query3, res3)
# generate_response(query4, res4)
# generate_response(query9, res9)
# generate_response(query10, res10)

import numpy as np

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
  courses = ' '.join(courses)
  if len(quarters) < 10:
    return prof + " teaches " + courses + " in the " + quarters
  else:
    return prof + " teaches " + courses + " over " + quarters 

def generate_prof_response(query, df):
  prof = "Professor " + query.get("last_name") 
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

  print(res)

# generate_prof_response(query13, res13)
# generate_prof_response(query16, res16)
# generate_prof_response(query14, res14)
generate_prof_response(query15, res15)

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

# Sample queries
query1 = {"Description": "Introduction to Mechatronics"}
res1 = query_data(df_sched, query1)
generate_response("df_sched", query1)

# Sample queries
query1 = {"Description": "Introduction to Mechatronics"}
generate_response("df_sched", query1)

query2 =  {"Description": "Engineering Statics",
            "Quarter": "F",
            "Instructor": "Castro, D"}
generate_response("df_sched", query2)

query3 = query2
generate_response("df_sched", query3, ["Course", "Sect"])

query4 = {"Course": "ME 128"}
generate_response("df_sched", query4, ["Description"])

query5 = {"Course": "CSC 482", "Quarter": "W"}
res5 = query_data(df_sched, query5)
generate_sched_response(query5, res5)
generate_response("df_sched", query2)

query7 = {"Course": "AERO 465", "Quarter": "F"}
res7 = query_data(df_sched, query7)
generate_sched_response(query7, res7)
generate_response("df_sched", query2)

query8 = {"Description": "Game Design", "Quarter": "F"}
res8 = query_data(df_sched, query8)
generate_sched_response(query8, res8)
generate_response("df_sched", query2)

query9 = {"Course": "CSC 307", "Quarter": "W"}
res9 = query_data_columns(df_sched, query9, ["Start", "End", "Days"])
generate_sched_response(query9, res9)
generate_response("df_sched", query2)

query10 = {"Course": "CSC 308", "Quarter": "W"}
res10 = query_data_columns(df_sched, query10, ["Instructor"])
generate_sched_response(query10, res10)
generate_response("df_sched", query2)

query11 = {"Course": "CSC 308", "Quarter": "W"}
res11 = query_data_columns(df_sched, query11, ["Sect", "Start", "End", "Days"])
generate_sched_response(query11, res11)
generate_response("df_sched", query2)

query12 = {"Course": "CSC 308", "Quarter": "W"}
generate_response("df_sched", query12, ["Location", "Description"])

query13 = {"last_name": "Abercromby"}
generate_response("df_profs", query13)

query14 = {"last_name": "Emily"}
generate_response("df_profs", query14)

query15 = {"last_name": "Agarwal"}
generate_response("df_profs", query15)

query16 = {"last_name": "Abercromby", "Quarter": "W"}
generate_response("df_profs", query16)

query17 = {"last_name": "Agarwal", "Quarter": "F"}
generate_response("df_profs", query17)

