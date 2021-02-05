#!/usr/bin/python
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime

from src.utilities import *
from analytics.filter_questions_db import *
from analytics.filter_user_response import *


class AlignDB:
    def __init__(self, parent_dir, questions_file, user_answer_file, use_quest_id=True):
        self.parent_dir = parent_dir
        self.utils = Utilities()
        self.quest_class = FilterQuestionDB(parent_dir, questions_file)
        self.user_ans_class = FilterUserAnsDB(parent_dir, user_answer_file, use_quest_id=True)
        self.use_col_user_level = 'question_id' if use_quest_id else 'question'
        self.use_col_quest_level = 'id' if use_quest_id else 'question'
        self.added_quest_cols = self.quest_class.added_cols
        self.added_accuracy_cols = self.user_ans_class.accuracy_cols
        pass

    def generate_report(self, question_cat_data, user_ans_data, user_accuracy_df):
        user_ans_data[self.added_quest_cols[0]] = 'NA'
        user_ans_data[self.added_quest_cols[1]] = 'NA'
        user_ans_data[self.added_quest_cols[2]] = 'NA'
        user_ans_data['standard'] = 0
        user_ans_data['difficulty_level'] = 'Easy'

        user_ans_data[self.added_accuracy_cols[0]] = 0
        user_ans_data[self.added_accuracy_cols[1]] = 0
        user_ans_data[self.added_accuracy_cols[2]] = 0
        user_ans_data[self.added_accuracy_cols[3]] = 0

        unique_questions = user_accuracy_df[self.use_col_user_level].values

        for quest in unique_questions:
            user_ans_quest_index = user_ans_data[self.use_col_user_level].values == quest
            quest_db_quest_index = \
                question_cat_data.index[question_cat_data[self.use_col_quest_level] == quest].tolist()
            accuracy_sel_index = user_accuracy_df.index[user_accuracy_df[self.use_col_user_level] == quest].tolist()

            if not quest_db_quest_index:
                continue
            # print(quest_db_quest_index, '----->',quest)
            quest_sel = question_cat_data.iloc[quest_db_quest_index[0]]
            acc_sel = user_accuracy_df.iloc[accuracy_sel_index[0]]

            cat1, cat2, cat3, std, diff_level = \
                quest_sel[self.added_quest_cols[0]], quest_sel[self.added_quest_cols[1]], \
                quest_sel[self.added_quest_cols[2]], quest_sel['studying_class'], quest_sel['difficulty_level']
            print(cat1, cat2, cat3)
            user_ans_data[self.added_quest_cols[0]].iloc[user_ans_quest_index] = cat1
            user_ans_data[self.added_quest_cols[1]].iloc[user_ans_quest_index] = cat2
            user_ans_data[self.added_quest_cols[2]].iloc[user_ans_quest_index] = cat3
            user_ans_data['standard'].iloc[user_ans_quest_index] = std
            user_ans_data['difficulty_level'].iloc[user_ans_quest_index] = diff_level

            user_ans_data[self.added_accuracy_cols[0]].iloc[user_ans_quest_index] = acc_sel[self.added_accuracy_cols[0]]
            user_ans_data[self.added_accuracy_cols[1]].iloc[user_ans_quest_index] = acc_sel[self.added_accuracy_cols[1]]
            user_ans_data[self.added_accuracy_cols[2]].iloc[user_ans_quest_index] = acc_sel[self.added_accuracy_cols[2]]
            user_ans_data[self.added_accuracy_cols[3]].iloc[user_ans_quest_index] = acc_sel[self.added_accuracy_cols[3]]

        print('done')
        return user_ans_data

    def get_question_answer_aligned_db(self, question_db, user_answer_db):
        user_answer_db[self.added_quest_cols[0]] = 'NA'
        user_answer_db[self.added_quest_cols[1]] = 'NA'
        user_answer_db[self.added_quest_cols[2]] = 'NA'
        user_answer_db['standard'] = 0
        user_answer_db['difficulty_level'] = 'Easy'

        questions = question_db[self.use_col_quest_level].values.tolist()
        for quest in questions:
            user_ans_quest_index = user_answer_db[self.use_col_user_level].values == quest
            quest_db_quest_index = \
                question_db.index[question_db[self.use_col_quest_level] == quest].tolist()

            if not quest_db_quest_index:
                continue
            # print(quest_db_quest_index, '----->',quest)
            quest_sel = question_db.iloc[quest_db_quest_index[0]]

            cat1, cat2, cat3, std, diff_level = \
                quest_sel[self.added_quest_cols[0]], quest_sel[self.added_quest_cols[1]], \
                quest_sel[self.added_quest_cols[2]], quest_sel['studying_class'], quest_sel['difficulty_level']
            #print(cat1, cat2, cat3)
            user_answer_db[self.added_quest_cols[0]].iloc[user_ans_quest_index] = cat1
            user_answer_db[self.added_quest_cols[1]].iloc[user_ans_quest_index] = cat2
            user_answer_db[self.added_quest_cols[2]].iloc[user_ans_quest_index] = cat3
            user_answer_db['standard'].iloc[user_ans_quest_index] = std
            user_answer_db['difficulty_level'].iloc[user_ans_quest_index] = diff_level

        #now = datetime.now()
        #filename = os.path.join(self.parent_dir, ('quest_ans_mapped_' + now.strftime("%Y_%m_%d") + '.csv'))
        #user_answer_db.to_csv(filename, header=True, index=False, encoding="utf-8")
        return user_answer_db

    def get_accuracy_aligned_db(self, quest_ans_aligned_df):
        question_acc_df = self.user_ans_class.get_question_accuracy(quest_ans_aligned_df)
        user_acc_df = self.user_ans_class.get_user_accuracy(quest_ans_aligned_df)
        question_cols = question_acc_df.columns.tolist()
        user_cols = user_acc_df.columns.tolist()

        # question accuracy among all users
        quest_ans_aligned_df[question_cols[1:4]] = 0
        quest_ans_aligned_df[question_cols[5:8]] = 0
        quest_ans_aligned_df[question_cols[9::]] = 0

        # user accuracy among all subject/quiz/questions
        quest_ans_aligned_df[user_cols[1:4]] = 0
        quest_ans_aligned_df[user_cols[5:8]] = 0
        quest_ans_aligned_df[user_cols[9::]] = 0

        unique_questions = question_acc_df[self.use_col_user_level].values.tolist()
        for quest in unique_questions:
            quest_index = quest_ans_aligned_df[self.use_col_user_level].values == quest
            quest_acc_df_val = \
                question_acc_df[question_acc_df[self.use_col_user_level].values == quest].values.tolist()[0]
            to_add_cols = [x for x in range(1,4)] + [x for x in range(5, 8)] + [x for x in range(9, len(question_cols))]
            for x in to_add_cols:
                quest_ans_aligned_df[question_cols[x]].iloc[quest_index] = quest_acc_df_val[x]

        users = user_acc_df['user_phone'].values
        unique_users = np.unique(users)
        for user in unique_users:
            user_index = quest_ans_aligned_df['user_phone'].values == user
            user_acc_df_val = user_acc_df[user_acc_df['user_phone'].values == user].values
            for user_acc_val in user_acc_df_val:
                quiz_payed = user_acc_val[8]
                quiz_index = quest_ans_aligned_df['sub_subject'].values == quiz_payed
                quiz_user_index = np.array(user_index) & np.array(quiz_index)

                to_add_cols = [x for x in range(1, 4)] + [x for x in range(5, 8)] + \
                              [x for x in range(9, len(question_cols))]
                for x in to_add_cols:
                    quest_ans_aligned_df[user_cols[x]].iloc[quiz_user_index] = user_acc_val[x]

                '''
                # user accuracy among all subject
                quest_ans_aligned_df['u_ans_yes'].iloc[quiz_user_index] = user_acc_val[1]
                quest_ans_aligned_df['u_ans_no'].iloc[quiz_user_index] = user_acc_val[2]
                quest_ans_aligned_df['u_ans_acc'].iloc[quiz_user_index] = user_acc_val[3]
                # user accuracy subject wise
                quest_ans_aligned_df['u_s_ans_yes'].iloc[quiz_user_index] = user_acc_val[5]
                quest_ans_aligned_df['u_s_ans_no'].iloc[quiz_user_index] = user_acc_val[6]
                quest_ans_aligned_df['u_s_ans_acc'].iloc[quiz_user_index] = user_acc_val[7]
                # user accuracy quiz wise
                quest_ans_aligned_df['u_q_ans_yes'].iloc[quiz_user_index] = user_acc_val[9]
                quest_ans_aligned_df['u_q_ans_no'].iloc[quiz_user_index] = user_acc_val[10]
                quest_ans_aligned_df['u_q_ans_acc'].iloc[quiz_user_index] = user_acc_val[11]
                '''
        return quest_ans_aligned_df

    def create_report(self):
        question_database = self.quest_class.read_db()
        user_answer_database = self.user_ans_class.read_db()

        filtered_quest_df = self.quest_class.get_filtered_question_db(question_database)
        filtered_user_ans_df = self.user_ans_class.get_filtered_user_answer_db(user_answer_database)

        quest_ans_aligned_df = self.get_question_answer_aligned_db(filtered_quest_df, filtered_user_ans_df)
        user_accuracy_df = self.get_accuracy_aligned_db(quest_ans_aligned_df)

        #report = self.generate_report(filtered_quest_df, filtered_user_ans_df, user_accuracy_df)
        now = datetime.now()
        filename = os.path.join(self.parent_dir, ('quest_ans_accuracy_mapped_' + now.strftime("%Y_%m_%d") + '.csv'))
        user_accuracy_df.to_csv(filename, header=True, index=False, encoding="utf-8")
        return filename


if __name__ == '__main__':
    print('Calling Merger functions')
    user_ans_file = 'User Ans_30122020.csv'
    question_file = 'All Quiz Questions_30122020.csv'
    parent_dir = './../data/nlp_data_02012021'
    merge_db = AlignDB(parent_dir, question_file, user_ans_file)
    merge_db.create_report()
    print('Done')


