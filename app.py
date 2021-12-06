from flask import Flask, request
import query_builder as qb
import question_to_query as q2q
import pandas as pd
import pronounce as pron
import sys
import traceback

app = Flask(__name__)

df = pd.read_csv("schedule.csv") 

@app.route('/query')
def query():
    args = request.args
    if 'query' not in args.keys():
        return "Please include ?query in url"
    query_str = args['query']
    
    
    try:
        query_str = preprocess_query(query_str, pron.known_phonemes)
        print(f'query string after processing: {query_str}')
        query = q2q.skill(query_str)
        print(query)
        res = qb.generate_response(query[0], query[1], query[2])
    except Exception as e:
        print(f'An exception occurred: {e}')
        traceback.print_exc()
        return "None", 500
    
    return res, 200

def seperate_chars_nums(s):
    s_l = s.split()
    s_new = []
    for tok in s_l:
        if not tok.isalpha() and tok.islower():
            s_new.append(tok[0])
            s_new.append(tok[1:])
        else:
            s_new.append(tok)
    return " ".join(s_new)

def preprocess_query(text, known_phonemes):
    res = seperate_chars_nums(text)
    print(res)
    res = pron.replace_homophones(res, known_phonemes)
    print(res)
    res = res.replace(" _", "")
    res = res.replace(":", "")
    return res


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")