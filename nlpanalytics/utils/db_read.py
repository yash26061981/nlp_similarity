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

actual_answer = refined_df['actual_answer_text'].values
attrence_text = refined_df['atterence_text'].values
score = list()
similar = list()
match_word = list()
method = list()
from nlp.similarity import GetSimilarity
get_similarity = GetSimilarity(threshold=0.4)
for ac_val, at_val in zip(actual_answer, attrence_text):
    sim, sc, match, mt = get_similarity.process(actual_ans=ac_val, utterance_ans=at_val)
    print(ac_val, at_val, sim, sc, match, mt)
    similar.append(sim)
    score.append(sc)
    match_word.append(match)
    method.append(mt)

refined_df['Similar'] = similar
refined_df['Score'] = score
refined_df['MatchWord'] = match_word
refined_df['Method'] = method
print('done')
refined_df.to_csv('file5.csv', header=True, index=False,  encoding="utf-8")





