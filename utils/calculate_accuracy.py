import pandas as pd
import numpy as np

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

#user_answers = refined_df['is_right_answer'].values

method1_df = pd.read_csv('file1.csv')
method2_df = pd.read_csv('file2.csv')

method1_ans = method1_df['Similar'].values
method2_ans = method2_df['Similar'].values
user_answers = method1_df['is_right_answer'].values

user_answer_yes = np.count_nonzero(user_answers == 'yes')
user_answer_accuracy = user_answer_yes/ float(len(user_answers))

method1_ans_yes = np.count_nonzero(method1_ans == True)
method1_ans_accuracy = method1_ans_yes/ float(len(method1_ans))

method2_ans_yes = np.count_nonzero(method2_ans == True)
method2_ans_accuracy = method2_ans_yes/ float(len(method2_ans))

print('Accuracy------------>')
print('Without Rules: {0:.3f}, Method 1: {1:.3f}, Method 2: {2:.3f}'.format(
    user_answer_accuracy, method1_ans_accuracy, method2_ans_accuracy))