import nltk
import re
nltk.download('punkt')
from nltk.tokenize import word_tokenize

# TODO

# Remind Emily to set up conch easter egg.

# Can't do Description yet. 
# PRONUNCIATION SIDE

# Split Replacements Dictionary.

# Help Message

prof_invocations = ["Doctor", "Professor", "Dr.", "dr.", "dr", "Dr",  "Instructor"]

class_invocations = ['aero', 'agb', 'aeps', 'agc', 'aged', 'ag',
                     'asci', 'ant', 'arce', 'arch', 'art', 
                     'astr', 'bio', 'bmed', 'brae', 'bot',
                     'bus', 'chem', 'cd', 'chin', 'crp', 'ce',
                     'cla', 'coms', 'cpe', 'csc', 'cm', 'dsci',
                     'danc', 'data', 'ese', 'esm', 'ersc',
                     'econ', 'educ', 'ee', 'engr', 'enve', 'engl',
                     'edes', 'enve', 'esci', 'es', 'fpe', 'fsn',
                     'fr', 'geog', 'geol', 'ger', 'gs', 'gsa', 
                     'gsb', 'gse', 'gsp', 'grc', 'hlth', 'hist',
                     'hnrc', 'hnrs', 'ime', 'itp', 'isla', 'ital',
                     'jpns', 'jour', 'kine', 'la', 'laes', 'ls', 
                     'msci', 'mate', 'math', 'me', 'mcro', 'msl',
                     'mu', 'nr', 'phil', 'pem', 'pew', 'psc', 
                     'phys', 'pols', 'psy', 'rpta', 'rels', 'scm',
                     'soc', 'ss', 'span', 'sped', 'stat', 'sie', 
                     'th', 'univ', 'wvit', 'wgs', 'wlc'
                     ]

prof_utterances = ["Courses", "Office", "Phone", "Alias", "Email"]

class_utterances = ["Quarter", "Instructor", "Time", "Location", "Description",
                    "Sect", "Enrl", "ECap", "Spots", "Wait", "Format"]

quarters = ["F", "W", "S"]

# Synonym -> Query Utterance
replacements = {
    "instructor":"Instructor",
    "professor":"Instructor",
    "teacher":"Instructor",
    "Instructor":"Instructor",
    "teaches":"Instructor",
    "teach":"Instructor",
    "teaching":"Instructor",
    "who":"Instructor",
    "dr.":"Instructor",
    "professors":"Instructor",

    "Time":"Time",
    "time":"Time",
    "when":"Time",

    "Location":"Location",
    "room":"Location",
    "where":"Location",

    "Description":"Description",
    "description":"Description",
    "tell":"Description",

    "sections":"Sect",
    "number":"Sect",

    "enrolled":"Enrl",

    "spots":"Spots",
    "seats":"Spots",

    "enrollment":"ECap",
    "capacity":"ECap",

    "waitlist":"Wait",

    "fall":"F",
    "Fall":"F",
    "this":"F",
    "winter":"W",
    "Winter":"W",
    "next":"W",
    "spring":"S",

    "Format":"Format",
    "format":"Format",
    "virtual":"Format",
    "virtually":"Format",
    "asynchronous":"Format",
    "asynchronously":"Format",
    "person":"Format",
    "online":"Format",
    "mode":"Format",
    "Mode":"Format",
    "Instruction":"Format"
}

prof_replacements = {
    "courses":"Courses",
    "classes":"Courses",
    "teach":"Courses",
    "teaches":"Courses",

    "office":"Office",
    "phone":"Phone",
    "alias":"Alias",
    "title":"Alias",
    "email":"Email",
    "mail":"Email",
    "address":"Email"
}

subject_to_abbrev = {
    "Aerospace Engineering":"AERO",
    "Aerospace":"AERO",
    "Biomedical Engineering":"BMED",
    "Biomedical":"BMED",
    "Civil Engineering":"CE",
    "Civil":"CE",
    "Computer Science":"CSC",
    "Computer Engineering":"CPE",
    "General Engineering":"ENGR",
    "Environmental Engineering":"ENVE",
    "Industrial and Manufacturing Engineering":"IME",
    "Industrial Engineering":"IME",
    "Industrial":"IME",
    "Manufacturing Engineering":"IME",
    "Manufacturing":"IME",
    "Materials Engineering":"MATE",
    "Materials":"MATE",
    "Mechanical Engineering":"ME",
    "Mechanical":"ME",
    "Electrical Engineering":"EE",
    "Electrical":"EE"
}

def replace_prof(tokens):
  replaced = []
  for token in tokens:
    if token in prof_replacements.keys():
      replaced.append(prof_replacements[token])
    elif token.split()[-1].isnumeric():
      rest = token[:len(token)-4]
      if rest in subject_to_abbrev.keys():
        replaced.append(subject_to_abbrev[rest] + token[len(token)-4:])
      else:
        replaced.append(token)
    else:
      replaced.append(token)
  return replaced

def replace(tokens):
  replaced = []
  for token in tokens:
    if token in replacements.keys():
      replaced.append(replacements[token])
    elif token.split()[-1].isnumeric():
      rest = token[:len(token)-4]
      if rest in subject_to_abbrev.keys():
        replaced.append(subject_to_abbrev[rest] + token[len(token)-4:])
      else:
        replaced.append(token)
    else:
      replaced.append(token)
  return replaced

def lower(tokens):
  return [token.lower() for token in tokens]

def detect_invocation(tokens):
  for token in tokens:
    if token == "help":
      return "help", "help"
    if token == "christmas":
      return "christmas", "santa claus"
    if token == "magic":
      return "nothing", "conch"
    if token.split()[0] in class_invocations:
      return "df_sched", token
  for token in tokens:
    if token.split()[0] in prof_invocations:
      return "df_profs", token.split()[-1]
  return ["No Invocation", "No Invocation"]

def detect_utterance(tokens, q_type, terms):
  returns = []
  if q_type == "df_sched":
    for i in range(len(tokens)):
      if (tokens[i] in class_utterances and tokens[i] not in returns and tokens[i] not in terms.keys()):
        returns.append(tokens[i])
  if q_type == "df_profs":
    for token in tokens:
      if token in prof_utterances and token not in returns:
        returns.append(token)
  return returns

def detect_quarter(tokens):
  for token in tokens:
    if token in quarters:
      return token

def detect_professor(tokens):
  for i in range(len(tokens)-1):
    if tokens[i] in prof_invocations:
      return tokens[i+1]
  return None

#  SCHEDULES
#  When: Start, End, Days
#  Who: last_name
#  How many Sections: Sect
#  Where: Location
#  Existence: []
#  Description: Description
#  Format: Format
#  Enrollment:
#  Enrolled:
#  Waitlist:

#  PROFESSOR

def convert_returns(returns):
   new = []
   for ret in returns:
      if ret == "Time":
         new.append("Start")
         new.append("End")
         new.append("Days")
      else:
         new.append(ret)
   return new

def skill(input):
  """
  Takes input as a string.
  Returns a query list to be sent to Emily's side
  """
  query = []
  terms = {}
  returns = []

  tokens = re.findall(r'\b[a-z]+ [0-9]+\b|\w+', input)
  if tokens == []:
    return None
  print(input)
  tokens[0] = tokens[0].lower()
  replaced = replace(tokens)
  print(replaced)
  invocation = detect_invocation(replaced)
  q_type = invocation[0]
  query.append(q_type)
  if q_type == "df_sched":
    terms["Course"] = invocation[1]
    name = detect_professor(replaced)
    if name is not None and name != "Instructor" and name != "is":
      terms["Instructor"] = name
      name = None
  elif q_type == "df_profs":
    replaced = replace_prof(replaced)
    name = detect_professor(replaced)
    if name is not None and name != "Instructor" and name != "is":
      terms["last_name"] = name
      name = None
  elif q_type == "christmas":
    return ["Easter Egg", 1, []]
  elif q_type == "nothing":
    return ["Easter Egg", 2, []]
  elif q_type == "help":
    return ["help", "help", []]
  quarter = detect_quarter(replaced)
  if quarter is None:
    quarter = "F"
  terms["Quarter"] = quarter   

  returns = detect_utterance(replaced, query[0], terms)
  returns = convert_returns(returns)
  
  query.append(terms)
  query.append(returns)

  return query

def test():
   fp = open("queries.txt", 'r')
   inputs = fp.readlines()
   fp.close()

   for i in range(len(inputs)):
      print("Original: < " + inputs[i].strip() + " >")
      query = skill(inputs[i].strip())
      print(query)
      #generate_response(query[0], query[1], query[2])
      print("----------------------------------")

if __name__ == "__main__":
   test()
