import nltk
from nltk import ngrams
from functools import lru_cache
from itertools import product as iterprod

try:
    arpabet = nltk.corpus.cmudict.dict()
except LookupError:
    nltk.download('cmudict')
    arpabet = nltk.corpus.cmudict.dict()

    
@lru_cache()
def wordbreak(s):
    s = s.lower()
    if s in arpabet:
        return arpabet[s]
    middle = len(s)/2
    partition = sorted(list(range(len(s))), key=lambda x: (x-middle)**2-x)
    for i in partition:
        pre, suf = (s[:i], s[i:])
        if pre in arpabet and wordbreak(suf) is not None:
            return [x+y for x,y in iterprod(arpabet[pre], wordbreak(suf))]
    return None

def wordbreak_wrapper(s):
    # to handle tuples of ngrams
    phonemes = []
    for sub in s:
        temp = wordbreak(sub)
        if temp:
            phonemes += temp[0]
        else: return None
    return phonemes

def gen_phoneme_dict(phoneme_pairs):
    """
        creates dictionary and populates it with input
        phoneme pairs.
        
        args: 
            phoneme_pairs(list) [(google_home_pronounciation, program_recognized key)...]
                ex: [("c s c", "CSC"), ("en vee", )] 
                
        returns: 
            (dict) {key : value, str(phoneme_list) : "ACRONYM"...}
                ex: { "[['S', 'IY1', 'EH1', 'S', 'S', 'IY1']]" : "CSC", ...}
    """
    phoneme_dict = {}
    for pair in phoneme_pairs:
        pronounciation = pair[0]
        phoneme_ls = []
        for substring in pronounciation.split():
            phoneme_ls += wordbreak(substring)[0]
        if str(phoneme_ls) not in phoneme_dict:
            phoneme_dict[str(phoneme_ls)] = pair[1]
        
    return phoneme_dict    

def replace_homophones(text, known_phonemes, num_grams=5):
    """
        parses a string and checks if the pronounciation of each word
        appears in the dictionary, if so replace it with its value in the dictionary.
        
        "when is cee 440" --> "when is CE 440"
        
        args: 
            text(str) string to be modified
            known_phonemes(dict) { "[['S', 'IY1', 'EH1', 'S', 'S', 'IY1']]" : "CSC", ...}
            num_grams(int) number of ngrams to process as a single pronounciation
        
        returns:
            (string) modified (or not) string
    """
    
    res = text.split()
    for n in range(num_grams, 0, -1):
        grams = ngrams(res, n)
        skip = 0
        for i, g in enumerate(grams):
            if skip:
                skip -= 1
                continue
            p = wordbreak_wrapper(g)
            if not p: # does the input have a valid pronounciation?
                continue
            else: # make it a string so we can hash it 
                p = str(p)
            if p in known_phonemes:
                res[i] = known_phonemes[p].lower()
                for j in range(1, n):
                    res[i+j] = '_' 
                skip = num_grams - 1
                    #HMMMMM
                print(f'\nProcessed query --> {" ".join(res)}\n')
    return " ".join(res)

import re
s = "when is csc4 82"
def seperate_chars_nums(s):
    s_l = s.split()
    print(s_l)
    s_new = []
    for tok in s_l:
        if not tok.isalpha() and tok.islower():
            s_new += (re.split('(\d+)', tok))
        else:
            s_new.append(tok)
    return " ".join(s_new)
pairs = [
    ("c s c", "csc"),
    ("tcsc", "225"),
    ("CSE", "csc"),
    ("VSC", "csc"),
    ("cee", "ce"),
    ("cp e", "cpe"),
    ("aero", "aero"),
    ("arrow", "aero"),
    ("b med", "bmed"),
    ("e e", "ee"),
    ("en vee", "enve"),
    ("envy", "enve"),
    ("i m e", "ime"),
    ("m e", "ME"),
    ("fill", "phil"),
    ("full", "phil"),
    ("philosophy", "phil"),
    # full dept names
    ("aerospace engineering", "aero"),
    ("biomedical engineering", "bmed"),
    ("botany", "bot"),
    ("civil engineering", "ce"),
    ("computer science", "csc"),
    ("computer engineering", "cpe"),
    ("general engineering", "engr"),
    ("environmental engineering", "enve"),
    ("industrial and manufacturing engineering", "ime"),
    ("industrial engineering", "ime"),
    ("materials engineering", "mate"),
    ("mechanical engineering", "me"),
    ("electrical engineering", "ee"),
    # professors
    ("niecy", "nishi"),
    ("DC", "nishi"),
    ("eck hart", "eckhardt"),
    ("eckhart", "eckhardt"),
    ("cash mode", "khosmood"),
    ("cost mood", "khosmood"),
    ("cause mood", "khosmood"),
    ("called mood", "khosmood"),
    ("kutchma", "khosmood"),
    ("chaos modes", "khosmood"),
    ("kashmir", "khosmood"),
    ("crush mood", "khosmood"),
    ("crush made", "khosmood"),
    ("cosmo", "khosmood"),
    ("kosmin", "khosmood"),
    ("cosmic", "khosmood"),
    ("cool guy", "khosmood"),
    ("Hans", "haungs"),
    ("plank", "planck"),
    ("sing", "seng"),
    ("sang", "seng"),
    ("Sue", "siu"),
    ("Seuss", "siu"),
    ("Apes", "aeps"),
    ("niggler", "migler"),
    
    # descrips
    ("systems programming", "cpe 357"),
    
]

with open('conversions.txt') as f:
    lines = f.readlines()

conversions = []
for line in lines:
    res = line[2:-3].split("', '")
    conversions.append(res)

   
known_phonemes = gen_phoneme_dict(conversions + pairs)
#print(conversions + pairs)