#!/usr/bin/python

import os
import sys
from pathlib import Path  # path tricks so we can import wherever the module is
sys.path.append(os.path.abspath(Path(os.path.dirname(__file__))/Path("..")))
sys.path.append(os.path.abspath(Path(os.path.dirname(__file__))/Path("../..")))

import flask
from flask import request, jsonify, make_response, Flask

from nlpsim_main.similarity import *
import time

app = Flask(__name__)
app.config["DEBUG"] = False

get_similarity = None


def initialise(cwd):
    global get_similarity
    get_similarity = GetSimilarity(cwd=cwd, threshold=0.4)
    return


def get_input_sentences():
    s1, s2, s3, s4 = 'None', 'None', 'None', 'None'
    if request.method == 'GET':
        s1 = request.args.get('s1', None)
        s2 = request.args.get('s2', None)
        s3 = request.args.get('s3', None)
        s4 = request.args.get('s4', None)
    return s1, s2, s3, s4


@app.route('/similarity', methods=['GET', 'POST'])
def similarity():
    try:
        start = time.time()
        s1, s2, s3, s4 = get_input_sentences()
        match = get_similarity.process(s1=s1, s2=s2, s3=s3, s4=s4)
        end = time.time()
        response = make_response(
            jsonify(
                {"Correct_Ans": s1.replace('"', ''), "Entered_Ans": s2.replace('"', ''), "Score": match.score,
                 "Similarity": match.is_similar, "Time in seconds": (end-start),
                 "Method": match.match_method, "Match": match.match_word}), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an required format.")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise