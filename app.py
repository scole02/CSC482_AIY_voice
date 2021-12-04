from flask import Flask, request
import query_builder as qb
import question_to_query as q2q
import pandas as pd
from pronounce import wordbreak, known_phonemes

app = Flask(__name__)

# df = pd.read_csv("schedule.csv") 

@app.route('/query')
def query():
    args = request.args
    print(args.keys())
    if 'query' not in args.keys():
        return "Please include ?query in url"
    query_str = args['query']
    
    query = q2q.skill(query_str)
    print(query)
    res = qb.generate_response(query[0], query[1], query[2])

    #print(q2q.skill(query_str))
    print("\n" + query_str + "\n")
    query_words = query_str.split()
    for w in query_words:
        print(w)
        if str(wordbreak(w)) in known_phonemes:
            print(known_phonemes[str(wordbreak(w))])
        print(wordbreak(w))
        print("\n")
    return res, 200



def decode_str(query_str):
    return 

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")