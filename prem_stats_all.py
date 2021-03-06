# -*- coding: utf-8 -*-
"""Prem_stats_all.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10jnnXb-0s2tleG1FcySJEJ9HPSmyl_q4
"""

import pandas as pd 
import csv

#remove new line charachters
df = pd.read_csv("Prem_scores_1.csv")
df = df.replace(r'\n','', regex=True) 
df.head()

#remove any spaces before or after what I want
df['Home_Team'] = df['Home_Team'].str.strip()
df['Away_Team'] = df['Away_Team'].str.strip()
df['Winner'] = df['Winner'].str.strip()
df['Loser'] = df['Loser'].str.strip()
df.head()

#set up columns for new file
output_file = csv.writer(open('Prem_stats_All.csv','w', newline = ''))
output_file.writerow(['Team','Played','WinPercent','Total_Points_Scored','average_points_per_game','Home_win_pc','Away_win_pc'])


#import columns from prem_scores_1
teamsWin = df['Winner'].values.tolist()
winScore = df['Winning_score'].values.tolist()
teamsLose = df['Loser'].values.tolist()
loseScore = df['Losing_score'].values.tolist()
draws = df['Draw'].values.tolist()
Home_Team = df['Home_Team'].values.tolist()
Away_Team = df['Away_Team'].values.tolist()
teamList = []

#sort 
teams = teamsWin + teamsLose 
teams = list(dict.fromkeys(teams))
for team in teams:
    teamList.append(team.strip())

teamList = list(dict.fromkeys(teamList))
teamList.remove("Draw")

for team in teams:

    #set all values to 0
    played = 0
    wins = 0
    matchScore = []
    points = 0
    totalpoints = 0
    homewin = 0
    homeplayed = 0 
    awaywin = 0
    awayplayed = 0 
    j=0
   
    for t in list(teamsWin):
        #looking at the winning team add wins played and points 
        if (team == t ):
            played = played+1
            matchScore = winScore[j]
            points = points + int(matchScore)
            if draws[j] !=1:
                wins = wins+1
            if  t == Home_Team[j]:
              homewin = homewin+1
              homeplayed = homeplayed+1 

            if t == Away_Team[j]:
              awaywin = awaywin+1
              awayplayed = awayplayed+1
            
        j=j+1
    j=0  
                    
    for t in list(teamsLose):
      #do the same with the losing team
        if (team == t ):
            played = played+1
            matchScore = loseScore[j]
            points = points + int(matchScore)

            if t == Home_Team[j]:
              homeplayed = homeplayed+1

            if t == Away_Team[j]:
              awayplayed = awayplayed+1
        j=j+1
    j=0  
    
    #calculate all features needed
    if played != 0:
        winpercent = (wins/played)*100
        average_ppg = (points/played)
        try:
          homewinpercent = (homewin/(homeplayed))*100
          awaywinpercent = (awaywin/(awayplayed))*100
        except ZeroDivisionError:

          homewinpercent  = 0
          awaywinpercent = 0
    else:
        winpercent = 0
        average_ppg = 0
        homewinpercent = 0 
        awaywinpercent = 0 
    points
    #put correct figures in correct columns
    output_file.writerow([team,played,round(winpercent,3),points,round(average_ppg,3),round(homewinpercent,3),round(awaywinpercent,3)])

#get rid of 'Draw' out of team column
df = pd.read_csv("Prem_stats_All.csv")
df = df.drop([12], axis =0)
df

df.to_csv('Prem_Stats_All.csv')
#convert to csv file