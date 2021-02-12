#!/usr/bin/python
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
from analytics.filter_questions_db import *


class FilterUserAnsDB:
    def __init__(self, parent_dir, user_answer_file, use_quest_id=True):
        self.parent_dir = parent_dir
        self.user_ans_file = user_answer_file
        self.user_ans_db = None
        self.use_col = 'question_id' if use_quest_id else 'question'
        self.accuracy_cols = ['ans_yes', 'ans_no', 'total_attempt', 'accuracy']
        self.user_accuracy_cols = ['u_ans_yes', 'u_ans_no', 'u_total_attempt', 'u_accuracy']
        self.added_sub_cols = FilterQuestionDB(None, None).added_cols
        pass

    def read_db(self):
        return pd.read_csv(os.path.join(self.parent_dir, self.user_ans_file))

    def get_filtered_user_answer_db(self, data):
        right_ans_skip_index = data['is_right_answer'].values == 'Skipped'
        attr = data['utterance_text'].values
        na_index = pd.isna(data)
        attr_na_indx = na_index['utterance_text'].values
        utterance_drop_index = []
        to_skip = ['atterence_text', 'SKIPPED', 'None']
        for isNa, val in zip(attr_na_indx, attr):
            if isNa:
                utterance_drop_index.append(True)
            else:
                if to_skip[0] in val or to_skip[1] in val or to_skip[2] in val:
                    utterance_drop_index.append(True)
                else:
                    utterance_drop_index.append(False)

        user_ans_skip_index = data['user_answer_text'].values == 'Skipped'

        final_drop_index = \
            np.array(right_ans_skip_index) | np.array(utterance_drop_index) | np.array(user_ans_skip_index)

        refined_df = data.iloc[np.invert(final_drop_index)]
        refined_df.reset_index(drop=True, inplace=True)
        return refined_df

    def get_counts(self, data, use_col):
        yes_index = data['is_right_answer'].values == 'yes'
        no_index = data['is_right_answer'].values == 'no'

        yes_df = data.iloc[yes_index]
        no_df = data.iloc[no_index]
        y_q_id = yes_df[use_col].values
        n_q_id = no_df[use_col].values
        #self.use_col

        un_quest_id = np.unique(np.concatenate((y_q_id, n_q_id), axis=None))
        ans_yes, ans_no, acc, total = list(), list(), list(), list()
        for q_id in un_quest_id:
            yes_cnt = y_q_id.tolist().count(q_id)
            no_cnt = n_q_id.tolist().count(q_id)
            ans_yes.append(yes_cnt)
            ans_no.append(no_cnt)
            total.append(yes_cnt + no_cnt)
            accu = yes_cnt / float(yes_cnt + no_cnt)
            acc.append(accu)
        return un_quest_id, ans_yes, ans_no, total, acc

    def get_question_accuracy(self, user_align_db):
        df_data = []
        #quest_id, quest_yes, quest_no, quest_total, quest_acc = self.get_counts(user_align_db, self.use_col)
        subject_covered = user_align_db.subject.unique()
        for subject in subject_covered:
            sub_df = user_align_db[user_align_db[self.added_sub_cols[0]] == subject]
            _, s_yes, s_no, s_total, s_acc = self.get_counts(sub_df, self.added_sub_cols[0])
            quiz_covered = sub_df.sub_subject.unique()
            for quiz in quiz_covered:
                quiz_df = sub_df[sub_df[self.added_sub_cols[1]] == quiz]
                _, q_ans_yes, q_ans_no, q_total, q_acc = self.get_counts(quiz_df, self.added_sub_cols[1])

                quest_id, quest_yes, quest_no, quest_total, quest_acc = self.get_counts(quiz_df, self.use_col)
                for qid, qy, qn, qa in zip(quest_id, quest_yes, quest_no, quest_acc):
                    data = [qid, qy, qn, qa, subject,
                            s_yes[0], s_no[0], s_acc[0], quiz, q_ans_yes[0], q_ans_no[0], q_acc[0]]

                #data = [quest_id[0], quest_yes[0], quest_no[0], quest_acc[0], subject,
                #        s_yes[0], s_no[0], s_acc[0], quiz, q_ans_yes[0], q_ans_no[0], q_acc[0]]
                    df_data.append(data)

        cols = [self.use_col, 'quest_ans_yes', 'quest_ans_no', 'quest_ans_acc', self.added_sub_cols[0],
                'subject_ans_yes', 'subject_ans_no', 'subject_acc', self.added_sub_cols[1],
                'quiz_ans_yes', 'quiz_ans_no', 'quiz_acc']

        df = pd.DataFrame(df_data, columns=cols)
        return df

    def get_user_accuracy(self, user_align_db):
        users = user_align_db['user_phone'].values
        uniq_users = np.unique(users)
        df_data = []
        for user in uniq_users:
            user_df = user_align_db[user_align_db['user_phone'] == user]
            u_quest_id, u_ans_yes, u_ans_no, u_total, u_acc = self.get_counts(user_df, 'user_phone')
            subject_covered = user_df.subject.unique()
            for subject in subject_covered:
                sub_df = user_df[user_df[self.added_sub_cols[0]] == subject]
                _, s_ans_yes, s_ans_no, s_total, s_acc = self.get_counts(sub_df, self.added_sub_cols[0])
                quiz_covered = sub_df.sub_subject.unique()
                for quiz in quiz_covered:
                    quiz_df = sub_df[sub_df[self.added_sub_cols[1]] == quiz]
                    _, q_ans_yes, q_ans_no, q_total, q_acc = self.get_counts(quiz_df, self.added_sub_cols[1])

                    data = [u_quest_id[0], u_ans_yes[0], u_ans_no[0], u_acc[0], subject,
                            s_ans_yes[0], s_ans_no[0], s_acc[0], quiz, q_ans_yes[0], q_ans_no[0], q_acc[0]]
                    df_data.append(data)

        cols = ['user_phone', 'user_ans_yes', 'user_ans_no', 'user_ans_acc', self.added_sub_cols[0],
                'user_subject_ans_yes', 'user_subject_ans_no', 'user_subject_acc', self.added_sub_cols[1],
                'user_quiz_ans_yes', 'user_quiz_ans_no', 'user_quiz_acc']

        df = pd.DataFrame(df_data, columns=cols)
        return df


if __name__ == '__main__':
    print('Done')