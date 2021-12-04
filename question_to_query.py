import nltk
import re
nltk.download('punkt')
from nltk.tokenize import word_tokenize

# TODO
# Time -> Time, Days Query 
# AND OTHER Multidimensional queries.

# Problems: 
# Can't do Description yet. 

# "Is Professor Khosmood teaching CSC 482 next quarter?"
# should be a professor query. Still Broken.

# Convert common misunderstandings of Acronyms.

# In Person or Virtual queries.

# Named Entity Recognition
# "Is Eckhardt teaching next quarter?"
# "How many Sections of Game Design are offered in the Fall?"

# Enrollment

# Easter Egg
# Happy Holidays: "Ho Ho Ho! Merry Christmas!"
# Open the Pod Bay Doors.

#---------------------------------------------------------------------
# NOTES

# If no other query details are specified, read out existence.

prof_invocations = ["Doctor", "Professor", "Dr.", "dr.", "dr", "Dr",  "Instructor"]

class_invocations = ['AERO', 'AGB', 'AEPS', 'AGC', 'AGED', 'AG',
                     'ASCI', 'ANT', 'ARCE', 'ARCH', 'ART', 
                     'ASTR', 'BIO', 'BMED', 'BRAE', 'BOT',
                     'BUS', 'CHEM', 'CD', 'CHIN', 'CRP', 'CE',
                     'CLA', 'COMS', 'CPE', 'CSC', 'CM', 'DSCI',
                     'DANC', 'DATA', 'ESE', 'ESM', 'ERSC',
                     'ECON', 'EDUC', 'EE', 'ENGR', 'ENVE', 'ENGL',
                     'EDES', 'ENVE', 'ESCI', 'ES', 'FPE', 'FSN',
                     'FR', 'GEOG', 'GEOL', 'GER', 'GS', 'GSA', 
                     'GSB', 'GSE', 'GSP', 'GRC', 'HLTH', 'HIST',
                     'HNRC', 'HNRS', 'IME', 'ITP', 'ISLA', 'ITAL',
                     'JPNS', 'JOUR', 'KINE', 'LA', 'LAES', 'LS', 
                     'MSCI', 'MATE', 'MATH', 'ME', 'MCRO', 'MSL',
                     'MU', 'NR', 'PHIL', 'PEM', 'PEW', 'PSC', 
                     'PHYS', 'POLS', 'PSY', 'RPTA', 'RELS', 'SCM',
                     'SOC', 'SS', 'SPAN', 'SPED', 'STAT', 'SIE', 
                     'TH', 'UNIV', 'WVIT', 'WGS', 'WLC'
                     ]

for i in range(len(class_invocations)):
   class_invocations[i] = class_invocations[i].lower()

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
    for i in range(len(tokens)):
      if tokens[i] in class_utterances and tokens[i] not in returns:
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
  # The parts of a skill:
  # [Invocation Name] [Utterance]
  # Invocation Name - Name of the skill.
  # Utterance - Determines what we do with the skill.

  # Our Questions will follow this rough structure, with the Invocation being
  # either class or professor, and the utterance being the arguments for the query.

  query = []
  terms = {}
  returns = []

  tokens = re.findall(r'\bProfessor [A-Z][a-z]+\b|\bDr. [A-Z][a-z]+\b|\b[a-z]+ [0-9]+\b|\w+', input)
  tokens[0] = tokens[0].lower()
  replaced = replace(tokens)
  print(replaced)
  invocation = detect_invocation(replaced)
  q_type = invocation[0]
  query.append(q_type)
  if q_type == "df_sched":
    terms["Course"] = invocation[1]
    name = detect_professor(replaced)
    print(name)
    if name is not None and name != "Instructor":
      terms["last_name"] = name
      name = None
  elif q_type == "df_profs":
    name = detect_professor(replaced)
    if name is not None and name != "Instructor":
      terms["last_name"] = name
      name = None
  quarter = detect_quarter(replaced)
  if quarter is None:
    quarter = "F"
  terms["Quarter"] = quarter

   

  returns = detect_utterance(replaced, query[0])
  returns = convert_returns(returns)
  
  query.append(terms)
  query.append(returns)

  return query


inputs = ["When is cpe 357 offered next quarter?", # Class, Time
   "Who teaches csc 471 winter quarter?", # Class, Professor
   "How many sections are offered of cpe 101?", # Class, Sections
   "Which courses does dr. khosmood teach next quarter?", # Prof, Courses
   "Is professor wood teaching next quarter?", # Prof, Existence
   #"Who teaches computer science 307 in the fall?", # Class, Professor
   "Is professor khosmood teaching csc 482 next quarter?"
]

for i in range(len(inputs)):
    print("Original: < " + inputs[i] + " >")
    query = skill(inputs[i])
    print(query)
    #generate_response(query[0], query[1], query[2])
    print("----------------------------------")
