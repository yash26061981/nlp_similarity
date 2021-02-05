#!/usr/bin/python
import os
import sys
import pandas as pd
import numpy as np
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.cluster import KMeans
from datetime import datetime
from matplotlib import pyplot as plt
import json

import src
from src.utilities import *
from analytics.filter_questions_db import *
from analytics.filter_user_response import *


class Stats:
    def __init__(self):
        self.stats = dict.fromkeys(['min', 'max', 'mean', 'user_acc', 'user_rank',
                                    'total_users', 'values', 'subject', 'quiz'])
        pass


class Result:
    def __init__(self):
        self.result = dict.fromkeys(['user_accuracy', 'subject_accuracy',
                                     'quiz_accuracy', 'quiz_played', 'subject_covered', 'user', 'grade'])
        pass


class Insight:
    def __init__(self, parent_dir=None, aligned_db_file=None):
        self.parent_dir = parent_dir
        self.aligned_db_file = aligned_db_file
        self.utils = Utilities()
        self.quest_user_ans_db = None
        self.subjects = FilterQuestionDB(None, None).subjects
        self.subject_categories = FilterQuestionDB(None, None).added_cols
        self.accuracy_cols = FilterUserAnsDB(None, None).accuracy_cols

        self.users_parent_dir = None
        self.subject_parent_dir = None

        self.save_fig = True
        self.save_ranks_result = True
        pass

    def initialise(self):
        self.users_parent_dir = self.utils.create_dir_if_not_exists(parent_dir=self.parent_dir, dir='User')
        self.subject_parent_dir = self.utils.create_dir_if_not_exists(parent_dir=self.parent_dir, dir='Subjects')

    def read_db(self):
        return pd.read_csv(os.path.join(self.parent_dir, self.aligned_db_file))

    def create_user_dir(self, user_number, flush=False):
        return self.utils.create_dir_if_not_exists(parent_dir=self.users_parent_dir, dir=str(user_number), flush=flush)

    def create_user_standard_dir(self, user_number, standard, flush=False):
        return self.utils.create_dir_if_not_exists(
            parent_dir=self.create_user_dir(user_number, flush=flush), dir=str(standard), flush=flush)

    def create_subject_dir(self, subject, flush=False):
        return self.utils.create_dir_if_not_exists(parent_dir=self.subject_parent_dir, dir=subject, flush=flush)

    @staticmethod
    def get_data_label_count_for_plot(unique_cat, selected_cat, right_ans_cat):
        data, label = [], []
        total_count = 0
        for un in unique_cat:
            acc = [right_ans_cat[idx] for idx, sub in enumerate(selected_cat) if sub == un]
            if len(acc) ==0:
                continue
            un_cnt = selected_cat.count(un)
            acc_val = float(acc.count('yes'))/len(acc) if len(acc) > 0 else 0
            val = un + '({0}) - (Accuracy {1:.2f}%)'.format(un_cnt, acc_val)
            label.append(val)
            data.append(un_cnt)
            total_count += un_cnt
        return data, label, total_count

    @staticmethod
    def draw_figure(num_id, all_data, all_label, all_count, all_sub, path):
        for d, l, cnt, sub in zip(all_data, all_label, all_count, all_sub):
            fig = plt.figure(figsize=(12, 4))
            plt.pie(d, labels=l)
            plt.xlabel('Total Questions Attempted {}'.format(cnt))
            if sub == 'All':
                if num_id:
                    title = 'User {} Attempts \n(Subject Level Chart)'.format(num_id)
                else:
                    title = 'All User Attempts \n(Subject Level Chart)'
            else:
                if num_id:
                    title = 'User {} Attempts \n({}) (Count, Accuracy %)'.format(num_id, sub)
                else:
                    title = 'All User Attempts \n({}) (Count, Accuracy %)'.format(sub)
            plt.title(title)
            file_name = os.path.join(path, 'chart_{}.png'.format(sub))
            plt.savefig(file_name, bbox_inches='tight', dpi=100)
        return

    def get_standard(self, df, num_id):
        user_df = df[df['user_phone'] == num_id]
        standard = user_df.standard.unique().tolist()
        return standard

    def get_insight_user_level(self, input_df, num_id):
        results = []
        input_df = input_df.fillna(0)
        standard = self.get_standard(input_df, num_id)
        print('User {} has entries in standard {}'.format(num_id, standard))
        for std in standard:
            path = self.create_user_standard_dir(num_id, std, flush=False)
            all_data, all_label, all_count, all_sub = [], [], [], []

            std_df = input_df[input_df['standard'] == std]
            user_df = std_df[std_df['user_phone'] == num_id]
            user_df = user_df.reset_index(drop=True)

            cat1_data, cat1_label, cat1_total_count = \
                self.get_counts_for_plot(user_df, self.subject_categories[0], 'user_subject_acc', 'user_ans_acc')

            all_data.append(cat1_data)
            all_label.append(cat1_label)
            all_count.append(cat1_total_count)
            all_sub.append('All')
            for sub in self.subjects:
                sub_df = user_df[user_df[self.subject_categories[0]] == sub]
                sub_df = sub_df.reset_index(drop=True)
                cat2_data, cat2_label, cat2_total_count = \
                    self.get_counts_for_plot(sub_df, self.subject_categories[1], 'user_quiz_acc', 'user_subject_acc')
                all_data.append(cat2_data)
                all_label.append(cat2_label)
                all_count.append(cat2_total_count)
                all_sub.append(sub)

            if self.save_fig:
                self.draw_figure(num_id, all_data, all_label, all_count, all_sub, path)

            rank_result = insight.get_user_rank_among_peers(std_df, num_id)
            rank_result['grade'] = std
            if self.save_ranks_result:
                filename = os.path.join(path, 'rank_statistics.json')
                with open(filename, 'w') as fp:
                    json.dump(rank_result, fp)

            results.append(rank_result)
        return results

    def get_insight_user_level_old(self, input_df, num_id):
        standard = self.get_standard(input_df, num_id)
        for std in standard:
            path = self.create_user_standard_dir(num_id, std, flush=True)
            all_data, all_label, all_count, all_sub = [], [], [], []

            df = input_df[input_df['standard'] == std]
            user_df = df[df['user_phone'] == num_id]

            cat1 = df[self.subject_categories[0]].values
            cat2 = df[self.subject_categories[1]].values
            is_right_ans = df['is_right_answer'].values
            num_id_index = df.index[df['user_phone'] == num_id].tolist()

            sel_cat1 = [cat1[id] for id in num_id_index]
            sel_cat2 = [cat2[id] for id in num_id_index]
            right_ans_cat = [is_right_ans[id] for id in num_id_index]

            un_cat1 = np.unique(sel_cat1)
            cat1_data, cat1_label, cat1_total_count = self.get_data_label_count_for_plot(un_cat1, sel_cat1, right_ans_cat)
            all_data.append(cat1_data)
            all_label.append(cat1_label)
            all_count.append(cat1_total_count)
            all_sub.append('All')
            for c1 in un_cat1:
                sc1 = [sel_cat2[idx] for idx, sub in enumerate(sel_cat1) if sub == c1]
                uc1 = np.unique(sc1)
                c1_d, c1_l, c1_tc = self.get_data_label_count_for_plot(uc1, sc1, right_ans_cat)
                all_data.append(c1_d)
                all_label.append(c1_l)
                all_count.append(c1_tc)
                all_sub.append(c1)

            if self.save_fig:
                self.draw_figure(num_id, all_data, all_label, all_count, all_sub, path)

            rank_result = 0 #insight.get_user_rank_among_peers(df, num_id)
            if self.save_ranks_result:
                filename = os.path.join(path, 'rank_statistics.json')
                with open(filename, 'w') as fp:
                    json.dump(rank_result, fp)
            return rank_result

    def get_counts_for_plot(self, df, index, acc_index, u_index=None):
        sub = df[index].values.tolist()
        acc = df[acc_index].values.tolist()
        unique_cat = np.unique(sub)
        data, label = [], []
        total_count = 0
        for un in unique_cat:
            un_cnt = sub.count(un)
            sub_index = df.index[df[index] == un].tolist()
            sel_acc = np.unique([acc[id] for id in sub_index])
            if sel_acc.size < 1:
                continue
            val = un + '({0}) - (Accuracy {1:.2f}%)'.format(un_cnt, sel_acc[0])
            label.append(val)
            data.append(un_cnt)
            total_count += un_cnt
        return data, label, total_count

    def get_insight_subject_level(self, df):
        df = df.fillna(0)
        all_data, all_label, all_count, all_sub = [], [], [], []
        cat1_data, cat1_label, cat1_total_count = \
            self.get_counts_for_plot(df, self.subject_categories[0], 'subject_acc')
        all_data.append(cat1_data)
        all_label.append(cat1_label)
        all_count.append(cat1_total_count)
        all_sub.append('All')

        for sub in self.subjects:
            sub_df = df[df[self.subject_categories[0]] == sub]
            sub_df = sub_df.reset_index(drop=True)
            cat2_data, cat2_label, cat2_total_count = \
                self.get_counts_for_plot(sub_df, self.subject_categories[1], 'quiz_acc')
            all_data.append(cat2_data)
            all_label.append(cat2_label)
            all_count.append(cat2_total_count)
            all_sub.append(sub)

        path = self.subject_parent_dir
        self.draw_figure(None, all_data, all_label, all_count, all_sub, path)
        return

    def get_all_user_unique_subject_quiz_acc_df(self, df):
        user_align_db = df #df.set_index(['updated_date_time'])
        users = user_align_db['user_phone'].values
        uniq_users = np.unique(users)
        data = []
        cols = ['user_phone', 'user_acc', 'subject', 'subject_acc', 'quiz', 'quiz_acc']
        # User phone number level
        for user in uniq_users:
            user_df = user_align_db[user_align_db['user_phone'] == user]
            sel_sub_cat1 = user_df[self.subject_categories[0]].values.tolist()
            sel_sub_cat2 = user_df[self.subject_categories[1]].values.tolist()
            sel_accuracy = user_df[self.accuracy_cols[-1]].values.tolist()

            user_level_accuracy = np.average(sel_accuracy)
            uniq_sub_cat1 = np.unique(sel_sub_cat1)
            # Subject Level
            for uniq_sub in uniq_sub_cat1:
                index1 = [index for index, val in enumerate(sel_sub_cat1) if val == uniq_sub]
                accuracy_sub_level = [sel_accuracy[id] for id in index1]
                sub_cat2_level = [sel_sub_cat2[id] for id in index1]
                sub_level_accuracy = np.average(accuracy_sub_level)
                # Subject at quiz level
                for uniq_sub1 in np.unique(sub_cat2_level):
                    index2 = [index for index, val in enumerate(sub_cat2_level) if val == uniq_sub1]
                    accuracy_sub_level2 = [accuracy_sub_level[id] for id in index2]
                    sub_sub_level_accuracy = np.average(accuracy_sub_level2)

                    to_insert = [user, user_level_accuracy, uniq_sub, sub_level_accuracy,
                                 uniq_sub1, sub_sub_level_accuracy]
                    data.append(to_insert)
        df = pd.DataFrame(data, columns=cols)
        #filename = os.path.join(self.parent_dir, 'temp.csv')
        #df.to_csv(filename, header=True, index=False, encoding="utf-8")
        return df

    def get_statistics(self, df, index, num_id, ret_val=False):
        stats = Stats()
        if index == 'user_subject_acc':
            subject = df.subject.unique()[0]
            quiz = 'All'
        elif index == 'user_quiz_acc':
            subject = df.subject.unique()[0]
            quiz = df.sub_subject.unique()[0]
        else:
            subject = 'All'
            quiz = 'All'

        values = df[index].values.tolist() if ret_val else []
        user_index = df.index[df['user_phone'] == num_id].tolist()
        user_rank = user_index[0] + 1
        total_users = df.shape[0]
        user_acc = df.iloc[user_index[0]][index]

        data = [df[index].min(), df[index].max(), df[index].mean(), user_acc, user_rank, total_users, values,
                subject, quiz]
        res = dict(zip(stats.stats, data))
        return res

    def get_selected_df(self, user_level_accuracy_df, acc):
        df = user_level_accuracy_df
        if acc == 'user_ans_acc':
            df = user_level_accuracy_df[['user_phone', 'user_ans_acc']]
            df = df.drop_duplicates()
        elif acc == 'user_subject_acc':
            df = user_level_accuracy_df[['user_phone', 'subject', 'user_subject_acc']]
            df = df.drop_duplicates()
        elif acc == 'user_quiz_acc':
            df = user_level_accuracy_df[['user_phone', 'subject', 'sub_subject', 'user_quiz_acc']]
            df = df.drop_duplicates()
        return df

    def get_leading_lagging_user_stats(self, selected_df, acc, num_id):
        sorted_df = selected_df.sort_values(by=[acc], ascending=False)
        sorted_df.reset_index(drop=True, inplace=True)
        stats = self.get_statistics(sorted_df, acc, num_id)
        return stats

    def get_leading_lagging_user_subject_stats(self, selected_df, acc, num_id):
        user_df = selected_df[selected_df['user_phone'] == num_id]
        col = 'subject' if acc == 'user_subject_acc' else 'sub_subject'
        col_acc = user_df.subject.unique() if acc == 'user_subject_acc' else user_df.sub_subject.unique()

        subject_stats = []
        for sub in col_acc:
            sub_df = selected_df[selected_df[col] == sub]
            sorted_df = sub_df.sort_values(by=[acc], ascending=False)
            sorted_df.reset_index(drop=True, inplace=True)
            stats = self.get_statistics(sorted_df, acc, num_id)
            subject_stats.append(stats)
        return subject_stats

    def get_rank_details(self, user_level_accuracy_df, num_id):
        result = Result().result
        acc = 'user_ans_acc'
        u_df = self.get_selected_df(user_level_accuracy_df, acc)
        user_rank = self.get_leading_lagging_user_stats(u_df, acc, num_id)
        result['user_accuracy'] = user_rank

        acc = 'user_subject_acc'
        s_df = self.get_selected_df(user_level_accuracy_df, acc)
        subject_rank = self.get_leading_lagging_user_subject_stats(s_df, acc, num_id)
        result['subject_accuracy'] = subject_rank

        acc = 'user_quiz_acc'
        q_df = self.get_selected_df(user_level_accuracy_df, acc)
        quiz_rank = self.get_leading_lagging_user_subject_stats(q_df, acc, num_id)
        result['quiz_accuracy'] = quiz_rank

        return result

    def get_user_rank_among_peers(self, df, num_id):
        user_level_accuracy_df = df  # df.set_index(['updated_date_time'])
        #user_level_accuracy_df = self.get_all_user_unique_subject_quiz_acc_df(user_align_db)
        user_df = user_level_accuracy_df[user_level_accuracy_df['user_phone'] == num_id]
        result = self.get_rank_details(user_level_accuracy_df, num_id)

        subject_covered = user_df.subject.unique()
        result['subject_covered'] = len(subject_covered)
        quiz_covered = user_df.sub_subject.unique()
        result['quiz_played'] = len(quiz_covered)
        result['user'] = num_id
        return result



if __name__ == '__main__':
    print('Calling Insights functions')
    parent_dir = './../data/nlp_data_02012021'
    #user_ans_quest_db = 'detailed_user_answers_2021_01_09.csv'
    user_ans_quest_db = 'quest_ans_accuracy_mapped_2021_01_20.csv'
    insight = Insight(parent_dir, user_ans_quest_db)
    user_ans_quest_db = insight.read_db()
    insight.initialise()

    user = True
    if user:
        user_phone_number = 9818375351  # 8800774404 #9818375351
        insight.get_insight_user_level(user_ans_quest_db, user_phone_number)
    else:
        insight.get_insight_subject_level(user_ans_quest_db)
    print('Done')


