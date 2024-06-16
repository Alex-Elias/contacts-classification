import os
import pickle

import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from collections import Counter
import numpy as np


FEATURES = ['s_rsa', 's_up', 's_down', 's_phi', 's_psi',  's_a1', 's_a2', 's_a3', 's_a4', 's_a5', 
         't_rsa', 't_up', 't_down', 't_phi', 't_psi',  't_a1', 't_a2', 't_a3', 't_a4', 't_a5']

INTERACTION = ['HBOND', 'VDW', 'PIPISTACK', 'IONIC', 'PICATION', 'SSBOND', 'PIHBOND']

def combine_pdb() -> pd.DataFrame:
    '''
    Combines the pbd files found in features_ring folder
    and returns a pandas DataFrame with their contents 
    '''
    dfs = []
    for filename in os.listdir('features_ring'):
        dfs.append(pd.read_csv('features_ring/' + filename, sep='\t'))
    df = pd.concat(dfs)
    return df

def convert_to_string(y_train):
    l = []
    for y in y_train:
        l.append(''.join(str(s) for s in y))
    
    return l

def convert_to_list(y_res):
    y_1 = []
    for i in y_res:
        y_1.append([int(j) for j in list(i)])

def under_oversampler(df):

    X_train = df[FEATURES]
    y_train = df['Interaction']
    l = convert_to_string(y_train)
    
    samples_under = {}
    samples_over = {}
    c = Counter(l)

    for x in c.keys():
        if c[x] > 100000:
            samples_under[x] = 100000
        else:
            samples_under[x] = c[x]
    
    for x in c.keys():
        if c[x] < 1000:
            samples_over[x] = c[x] * 15
        if c[x] < 10000:
            samples_over[x] = c[x] * 3
        else:
            samples_over[x] = c[x]
    
    rus = RandomUnderSampler(random_state=42, sampling_strategy=samples_under)

    X_res, y_res = rus.fit_resample(X_train, l)

    smot = SMOTE(sampling_strategy=samples_over)
    X_res, y_res = smot.fit_resample(X_res, y_res)

    y_1 = convert_to_list(y_res)

    X_res['Interaction'] = np.array(y_1)

    return X_res



def binarize_multi_target(df):

    grouped_df =  df.groupby(FEATURES, as_index=False).agg(lambda x: x.tolist())
    
    mlb = MultiLabelBinarizer()

    mlb.fit([INTERACTION])
    grouped_df['Interaction'] = mlb.transform(grouped_df['Interaction'])
    
    return grouped_df

def preprocess(df):

    df = under_oversampler(df)
    df = binarize_multi_target(df)

    X = df[FEATURES]
    y = df['Interaction']

    return X, y
    

if __name__ == '__main__':

    df = combine_pdb()

    X, y = preprocess(df)

    rf_classifier = RandomForestClassifier(n_estimators=100, n_jobs=7, min_samples_split=6)

    rf_classifier.fit(X, y)

    with open('model.pkl','wb') as f:
        pickle.dump(rf_classifier,f)
    