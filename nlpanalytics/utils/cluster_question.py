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
questions = refined_df['question'].values

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(questions)

true_k = 10
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)
clust = list()
for q in questions:
    Y = vectorizer.transform([q])
    prediction = model.predict(Y)
    clust.append(prediction)
print("\n")

refined_df['Cluster'] = clust
print('done')
filename = 'question_cluster_' + str(true_k) + '.csv'
refined_df.to_csv(filename, header=True, index=False,  encoding="utf-8")





