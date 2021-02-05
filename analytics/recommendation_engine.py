#!/usr/bin/python
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
import json

import src
from src.utilities import *
from analytics.filter_questions_db import *
from analytics.filter_user_response import *
from analytics.insight import *


class REngine:
    def __init__(self, parent_dir, aligned_db_file):
        self.parent_dir = parent_dir
        self.aligned_db_file = aligned_db_file
        self.utils = Utilities()
        self.quest_user_ans_db = None
        self.subjects = FilterQuestionDB(None, None).subjects
        self.subject_categories = FilterQuestionDB(None, None).added_cols
        self.accuracy_cols = FilterUserAnsDB(None, None).accuracy_cols
        self.insight = Insight(parent_dir, aligned_db_file)
        pass

    def read_db(self):
        return pd.read_csv(os.path.join(self.parent_dir, self.aligned_db_file))

    def retrieve_last_quizzes(self, input_df, num_id, n_last_played):
        standards = self.insight.get_standard(input_df, num_id)
        for std in standards:
            cumulative_dfs = []
            df = input_df[input_df['standard'] == std]
            user_df = df[df['user_phone'] == num_id]
            sorted_df = user_df.sort_values(by=['updated_date_time'], ascending=False)
            sorted_df['date'] = pd.to_datetime(sorted_df['updated_date_time']).dt.date
            sorted_df['time'] = pd.to_datetime(sorted_df['updated_date_time']).dt.time

            sorted_df['date'] = pd.to_datetime(sorted_df['date'], dayfirst=True)
            day_wise_all_subject = sorted_df['date'].dt.date.value_counts().sort_index().reset_index()
            cumulative_dfs.append(['all_subject', day_wise_all_subject])
            subject_covered = sorted_df.subject.unique().tolist()
            for sub in subject_covered:
                sub_df = sorted_df[sorted_df['subject'] == sub]
                day_wise_subject = sub_df['date'].dt.date.value_counts().sort_index().reset_index()
                cumulative_dfs.append([sub, day_wise_subject])
            dfp = cumulative_dfs[0][1]
            dfp.plot.bar(x='index', y='date')
            print('done')




if __name__ == '__main__':
    print('Calling Insights functions')
    parent_dir = './../data/nlp_data_02012021'
    # user_ans_quest_db = 'detailed_user_answers_2021_01_09.csv'
    user_ans_quest_db = 'report_2021_01_15.csv'
    engine = REngine(parent_dir, user_ans_quest_db)
    user_ans_quest_db = engine.read_db()
    engine.retrieve_last_quizzes(user_ans_quest_db, 9818375351, 24)

    print('Done')
