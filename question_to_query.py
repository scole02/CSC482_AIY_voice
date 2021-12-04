import nltk
import re
nltk.download('punkt')
from nltk.tokenize import word_tokenize


#@title Conversions { form-width: "10%" }

prof_invocations = ["Doctor", "Professor", "Dr."]

class_invocations = ['AERO', 'BMED', 'CE', 'CPE', 'CSC', 
                    'EE', 'ENGR', 'ENVE', 'IME', 'MATE', 
                    'ME', 'AEPS', 'AG', 'AGB', 'AGC', 'AGED',
                     'ASCI', 'BRAE', 'DSCI', 'ERSC', 'ESCI',
                     'FSN', 'MSL', 'NR', 'RPTA', 'SS', 'WVIT',
                     ]

prof_utterances = ["Course"]

class_utterances = ["Quarter", "Instructor", "Time", "Location", "Description",
                    "Sect", "Enrl_x", "ECap_x", "Wait", "Format"]

quarters = ["F", "W", "Sp", "Su"]


# Synonym -> Query Utterance
replacements = {
    # Class Query
    "instructor":"Instructor",
    "professor":"Instructor",
    "teacher":"Instructor",
    "Instructor":"Instructor",
    "teaches":"Instructor",
    "teaching":"Instructor",
    "who":"Instructor",
    "dr.":"Instructor",

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
    "many":"Sect",
    "number":"Sect",

    "enrolled":"Enrl_x",

    "enrollment":"ECap_x",
    "enrolled":"ECap_x",
    "capacity":"ECap_x",

    "waitlist":"Wait",

    "fall":"F",
    "Fall":"F",
    "this":"F",
    "winter":"W",
    "Winter":"W",
    "next":"W",
    "spring":"S",
    "Spring":"S",

    "Format":"Format",
    "Mode":"Format",
    "Instruction":"Format",

    # Prof Query
    "courses":"Course",
    "which":"Course",
}

subject_to_abbrev = {
    "Computer Science":"CSC",
    "Computer Engineering":"CPE",
    "Aerospace Engineering":"AERO",
    "Aerospace":"AERO",
    "Biomedical Engineering":"BMED",
    "Biomedical":"BMED",
    "Civil Engineering":"CE",
    "Civil":"CE",
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
    if token.split()[0] in class_invocations:
      return "df_sched", token
  for token in tokens:
    if token.split()[0] in prof_invocations:
      return "df_profs", token.split()[-1]
  return "No Invocation"

def detect_utterance(tokens, q_type):
  returns = []
  if q_type == "df_sched":
    for token in tokens:
      if token in class_utterances and token not in returns:
        returns.append(token)
  if q_type == "df_profs":
    for token in tokens:
      if token in prof_utterances and token not in returns:
        returns.append(token)
  return returns

def detect_quarter(tokens):
  for token in tokens:
    if token in quarters:
      return token

def skill(input):
  # The parts of a skill:
  # [Wake word] [Launch] [Invocation Name] [Utterance]
  # EX: [Alexa], [Ask] [Daily Horoscopes] about [Taurus]
  # Launch Word - The first word after the Wake Word.
  # Invocation Name - Name of the skill.
  # Utterance - Determines what we do with the skill.

  # Our Questions will follow this rough structure, with the Invocation being
  # either class or professor, and the utterance being the arguments for the query.

  # The complexity will come in determining what combination of utterances create
  # what query results.
  query = []
  terms = {}
  returns = []

  tokens = re.findall(r'\bProfessor [A-Z][a-z]+\b|\bDr. [A-Z][a-z]+\b|\b[A-Z]+ [0-9]+\b|\b[a-zA-Z][a-z]+ [a-zA-Z][a-z]+ [0-9]+\b|\w+', input)
  tokens[0] = tokens[0].lower()
  replaced = replace(tokens)
  print(replaced)
  invocation = detect_invocation(replaced)
  q_type = invocation[0]
  query.append(q_type)
  if q_type == "df_sched":
    terms["Course"] = invocation[1]
  elif q_type == "df_profs":
    terms["Name"] = invocation[1]

  quarter = detect_quarter(replaced)
  if quarter is None:
    quarter = "F"
  terms["quarter"] = quarter

  returns = detect_utterance(replaced, query[0])

  print(returns)
  query.append(terms)
  return query

