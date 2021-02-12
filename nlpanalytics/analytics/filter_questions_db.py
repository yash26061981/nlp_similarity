#!/usr/bin/python
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime


class FilterQuestionDB:
    def __init__(self, parent_dir, questions_file):
        self.parent_dir = parent_dir
        self.questions_file = questions_file
        self.question_db = None
        self.spare = ['Mock Test', '&']
        self.subjects = ['GK', 'English', 'Math', 'Science', 'Others']
        self.tot_subjects = len(self.subjects)
        self.use_user_defined_category = True
        self.user_defined_category = 'Olympiad'
        self.added_cols = ['subject', 'sub_subject', 'specialised_sub']
        pass

    def read_db(self):
        return pd.read_csv(os.path.join(self.parent_dir, self.questions_file))

    def find_subject(self, val):
        for sub in self.subjects[0:self.tot_subjects]:
            if sub.lower() in val.lower():
                return sub
        return self.subjects[self.tot_subjects-1]

    def get_filtered_question_db(self, data):
        cat1, cat2, cat3 = [], [], []
        cat_table = data['category_table'].values
        for count, val in enumerate(cat_table):
            cat1.append(self.find_subject(val.strip()))
            split_data = val.split('>')
            new_data = '{} [{}]'.format(split_data[0], split_data[1])
            cat2.append(new_data)
            cat3.append(True if self.user_defined_category.lower() in val.lower() else False)

        data[self.added_cols[0]], data[self.added_cols[1]], data[self.added_cols[2]] = cat1, cat2, cat3
        return data


if __name__ == '__main__':
    print('Done')