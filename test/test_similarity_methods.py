#!/usr/bin/python
import os
import sys
import requests
import pandas as pd
from nlpsim.nlpsim_main import *

if __name__ == '__main__':
    threshold = 0.4
    get_similarity = GetSimilarity(threshold=threshold)
    # test data for testing
    s1 = 'worse'
    s2 = '[was, worst, vs, vas, verse, worse, vaaste, watch, bus]'
    s3 = None
    s4 = '[Badest, Worst, Badder]'

    match = get_similarity.process(s1=s1, s2=s2, s3=s3, s4=s4, th=threshold)
    print('s1 = {}'.format(match.actual_answer))
    print('s2 = {}'.format(match.entered_ans))
    print('s3 = {}'.format(match.true_alternatives))
    print('s4 = {}'.format(match.other_options))

    print("Similar = {0} , with Score = {1:.3f}%, Match Word : '{2}', From Method : '{3}'\n".format(
        match.is_similar, match.score, match.match_word, match.match_method))