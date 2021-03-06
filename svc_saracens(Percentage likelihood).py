# -*- coding: utf-8 -*-
"""svc_Saracens.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e05juuCa9zpoW4BOZhqmaFSE31FRCdtm
"""

import pandas as pd
import numpy as np
import sklearn
import plotly
from sklearn.model_selection import train_test_split
import statsmodels.api as sm 
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from numpy import mean
from numpy import std
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import cross_val_score
from numpy import mean
from numpy import std
from sklearn.model_selection import RepeatedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import matplotlib.pyplot as plt

df = pd.read_csv("FinalTestData_1.csv")

dfTraining = df.iloc[:2770,:]
df2018 = df.iloc[2770:,:]

dfTraining.tail()

y = dfTraining['Winner']
cols = ['WPT','HWPT','AWPT','APPG']
X = dfTraining[cols]

logit_model=sm.Logit(y,X)
result=logit_model.fit()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state =5)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

svc = SVC(kernel='linear')
svc.fit(X_train, y_train)
y_pred = svc.predict(X_test)
print('Accuracy of RF classifier on test set: {:.2f}'.format(svc.score(X_test , y_test)))



cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
scores3 = cross_val_score(svc, X_test, y_test, cv=cv, n_jobs=-1)
print('Score: %f (%f)' % (mean(scores3), std(scores3)))

df18 = pd.read_csv("2018.csv")

def match(df2018, team1, team2, model,random_scale=5):
    
    match = pd.DataFrame(columns=['WP1','HWP','AWP','APPG1','WP2','HWP2','AWP2','APPG2'], index=[0])
    
    WP1 = match['WP1'] = df18[df18.Home_Team == team1]['WP1'].iloc[0]
    HWP = match['HWP'] = df18[df18.Home_Team == team1]['HWP'].iloc[0]
    AWP = match['AWP'] = df18[df18.Home_Team == team1]['AWP'].iloc[0]
    APPG1 = match['APPG1'] = df18[df18.Home_Team == team1]['APPG1'].iloc[0]

    match['WP1'] = np.random.normal(WP1, scale=random_scale)
    match['HWP'] = np.random.normal(HWP, scale=random_scale)
    match['AWP'] = np.random.normal(AWP, scale=random_scale)
    match['APPG1'] = np.random.normal(APPG1, scale=random_scale)

    WP2 = match['WP2'] = df18[df18.Away_Team == team2]['WP2'].iloc[0]
    HWP2 = match['HWP2'] = df18[df18.Away_Team == team2]['HWP2'].iloc[0]
    AWP2 = match['AWP2'] = df18[df18.Away_Team == team2]['AWP2'].iloc[0]
    APPG2 = match['APPG2'] = df18[df18.Away_Team == team2]['APPG2'].iloc[0]

    match['WP2'] = np.random.normal(WP2, scale=random_scale)
    match['HWP2'] = np.random.normal(HWP2, scale=random_scale)
    match['AWP2'] = np.random.normal(AWP2, scale=random_scale)
    match['APPG2'] = np.random.normal(APPG2, scale=random_scale)
    
    match['WPT'] = match['WP1'] - match['WP2']
    match['HWPT'] = match['HWP'] - match['HWP2']
    match['AWPT'] = match['AWP'] - match['AWP2']
    match['APPG'] = match['APPG1'] - match['APPG2']
    
    match = match[['WPT', 'HWPT', 'AWPT', 'APPG']]

    
    match_array = match.values
    
    prediction = model.predict(match_array)
    
    winner = None
    
    if prediction == 0:
        winner = team1
    elif prediction == 1:
        winner = team2
    
    return winner

def simulate_matchessvc(team1, team2, n_matches=1000):
    
    match_results = []
    for i in range(n_matches):
        match_results.append(match(df2018, team1, team2, svc, random_scale=3))
        
    team1_prob = match_results.count(team1)/len(match_results)*100
    team2_prob = match_results.count(team2)/len(match_results)*100
    
    print(team1, str(round(team1_prob, 2)) + '%')
    print(team2, str(round(team2_prob,2)) + '%')
    print('-------------------------')
    print()
    
    if team1_prob > team2_prob:
        overall_winner = team1
    else:
        overall_winner = team2
    
    return {'team1': team1,
            'team2': team2,
            'team1_prob': team1_prob, 
            'team2_prob': team2_prob, 
            'overall_winner': overall_winner,
            'match_results': match_results}

semi1 = simulate_matchessvc('Saracens', 'Harlequins', n_matches=1000)
print("semi1 Winner: " + semi1['overall_winner'])


final = simulate_matchessvc('Saracens', 'Exeter Chiefs', n_matches=1000)
print("Winner of the League: " + final['overall_winner'])

svc_Saracens_prob_win = 0.999*0.952* 100 * (0.7372 ** 2)
svc_Saracens_prob_win