#!/usr/bin/python
import os
import sys
import requests
import pandas as pd
from nlpsim.nlpsim_api import *


if __name__ == '__main__':
    input_file = 'test_data.csv'
    ip_df = pd.read_csv(input_file)
    ip_df = ip_df.fillna('None')
    s1val, s2val, s3val,s4val = ip_df['s1'].tolist(), ip_df['s2'].tolist() , ip_df['s3'].tolist() ,ip_df['s4'].tolist()
    index = 1
    for s1, s2, s3, s4 in zip(s1val, s2val, s3val,s4val):
        reqs = 'http://localhost:5000/similarity?s1={}&s2=[{}]&s3=[{}]&s4=[{}]'.format(s1,s2,s3,s4)
        response = requests.get(reqs)
        print('index : {} : {}'.format(index, response.text))
        index += 1