import pandas as pd
import numpy as np
from datetime import datetime

data = pd.read_excel('user_submit.xls')

index1 = data['is_right_answer'].values == 'Skipped'
attr = data['atterence_text'].values
index2 = []
to_skip = ['atterence_text', 'SKIPPED', 'None']
for val in attr:
    if to_skip[0] in val or to_skip[1] in val or to_skip[2] in val:
        index2.append(True)
    else:
        index2.append(False)

index3 = data['user_answer_text'].values == 'Skipped'
#index3_2 = data['user_answer_text'].values == 'None'
#index3 = np.array(index3_1) | np.array(index3_2)

f_index = np.array(index1) | np.array(index2) | np.array(index3)


refined_df = data.iloc[np.invert(f_index)]
refined_df.reset_index(drop=True, inplace=True)

actual_answer = refined_df['actual_answer_text'].values
attrence_text = refined_df['atterence_text'].values
#questions = refined_df['question'].values
#is_answered = refined_df['is_right_answer'].values

yes_index = refined_df['is_right_answer'].values == 'yes'
no_index = refined_df['is_right_answer'].values == 'no'

yes_df = refined_df.iloc[yes_index]
no_df = refined_df.iloc[no_index]

y_q = yes_df['question'].values
n_q = no_df['question'].values

un_quest = np.unique(np.concatenate((y_q, n_q), axis=None))
ans_yes, ans_no, acc = list(), list(), list()
for q in un_quest:
    yes_cnt = y_q.tolist().count(q)
    no_cnt = n_q.tolist().count(q)
    ans_yes.append(yes_cnt)
    ans_no.append(no_cnt)
    accu = yes_cnt / float( yes_cnt + no_cnt)
    acc.append(accu)

list_of_tuples = list(zip(un_quest, ans_yes, ans_no, acc))
df = pd.DataFrame(list_of_tuples,
                  columns = ['Questions', 'Ans_YES', 'Ans_NO', 'YES_Accuracy'])

now = datetime.now()
filename = 'question_answered_classification_' + now.strftime("%Y_%m_%d_%H_%M_%S") + '.csv'
df.to_csv(filename, header=True, index=False,  encoding="utf-8")





