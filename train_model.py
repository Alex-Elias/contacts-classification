import os
import pickle
import joblib

import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from collections import Counter
import numpy as np
from time import sleep


FEATURES = [ 's_up', 's_down', 's_phi', 's_psi',  's_a1', 's_a2', 's_a3', 's_a4', 's_a5', 
          't_up', 't_down', 't_phi', 't_psi',  't_a1', 't_a2', 't_a3', 't_a4', 't_a5']

INTERACTION = ['HBOND', 'VDW', 'PIPISTACK', 'IONIC', 'PICATION', 'SSBOND', 'PIHBOND']

def combine_pdb() -> pd.DataFrame:
    '''
    Combines the pbd files found in features_ring folder
    and returns a pandas DataFrame with their contents 
    '''
    dfs = []
    for filename in os.listdir('../features_ring'):
        dfs.append(pd.read_csv('../features_ring/' + filename, sep='\t'))
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
    return y_1

def under_oversampler(X_train, y_train):

    l = convert_to_string(y_train)
    
    samples_under = {}
    samples_over = {}
    c = Counter(l)

    max_samples = 100000  
    
    for x in c.keys():
        if c[x] > max_samples:
            samples_under[x] = max_samples
        else:
            samples_under[x] = c[x]
    
    for x in c.keys():
        if c[x] < 1000:
            samples_over[x] = min(c[x] * 10, max_samples)
        else:
            samples_over[x] = c[x]
    
    # Ensure oversampling does not exceed max_samples
    for key in samples_over.keys():
        if samples_over[key] > max_samples:
            samples_over[key] = max_samples
    
    rus = RandomUnderSampler(random_state=42, sampling_strategy=samples_under)

    X_res, y_res = rus.fit_resample(X_train, l)

    smot = SMOTE(sampling_strategy=samples_over)
    X_res, y_res = smot.fit_resample(X_res, y_res)

    y_1 = convert_to_list(y_res)

    return X_res, np.array(y_1)



def binarize_multi_target(df):

    grouped_df =  df.groupby(FEATURES, as_index=False).agg(lambda x: x.tolist())
    
    mlb = MultiLabelBinarizer()

    mlb.fit([INTERACTION])
    y = mlb.transform(grouped_df['Interaction'])
    
    return grouped_df[FEATURES], y

def preprocess(df):
    df.dropna(inplace=True)
    X, y = binarize_multi_target(df)
    X, y = under_oversampler(X, y)
    
    return X, y
    

if __name__ == '__main__':

    df = combine_pdb()

    X, y = preprocess(df)

    clf = OneVsRestClassifier(RandomForestClassifier(class_weight='balanced_subsample', 
                                                         min_samples_split=6, n_estimators=200, 
                                                         criterion='log_loss', n_jobs=-1))

    clf.fit(X, y)

    sleep(60)
    joblib.dump(clf, 'loblib_model.sav')
    #with open('model.pkl','wb') as f:
    #    pickle.dump(clf,f)
    