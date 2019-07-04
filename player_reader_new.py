import pymysql.cursors
import pandas as pd
import numpy as np
import csv
from sklearn.externals import joblib 

connection = pymysql.connect (host='localhost',
                             user='root',
                             password='password',
                             db='nba',
                             cursorclass=pymysql.cursors.DictCursor)
with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM players_advanced_statistics where game > 5 and team != 'TOT'"
        df = pd.read_sql(sql, con=connection)
        sql2 = "SELECT * FROM team_advanced_statistics"
        df2 = pd.read_sql(sql2, con=connection)

TEAMS_RANK = {
    'MIL': 1, 'TOR': 2, 'GSW': 3, 'DEN': 4, 'HOU': 5,
    'POR': 6, 'PHI': 7, 'UTA': 8, 'BOS': 9, 'OKC': 10,
    'IND': 11, 'SAS': 12, 'LAC': 13, 'ORL': 14, 'BRK': 15,
    'DET': 16, 'CHO': 17, 'SAC': 18, 'MIA': 19, 'LAL': 20,
    'MIN': 21, 'MEM': 22, 'NOP': 23, 'DAL': 24, 'WAS': 25,
    'ATL': 26, 'CHI': 27, 'CLE': 28, 'PHO': 29,'NYK': 30
}

accumulation_columns = ['orbpct','drbpct','trbpct', 'astpct', 'stlpct','blkpct', 'tovpct']
team_margin_data = []
player_margin_data = []
for column in accumulation_columns:
    team_max = df2[column].max()
    team_min = df2[column].min()
    team_diff = team_max - team_min
    team_margin_data.append([team_min, team_diff])
    player_max = df[column].max()
    player_min = df[column].min()
    player_diff = player_max - player_min
    player_margin_data.append([player_min, player_diff])

for idx, column in enumerate(accumulation_columns):
    df[column] = (df[column] - player_margin_data[idx][0]) / player_margin_data[idx][1]
    df[column] = (team_margin_data[idx][1]*df[column]) + team_margin_data[idx][0]

player_result_datas = []
model_names = [['tspct','efgpct','ftr'], ['orbpct','drbpct','trbpct', 'astpct'], ['stlpct','blkpct', 'tovpct']]
model_names = ["models/{}.pkl".format('_'.join(model_name)) for model_name in model_names]
models = [ joblib.load(model_name) for model_name in model_names]

teams = [team for team in df['team'].unique().tolist()]

x1 = df[['tspct','efgpct','ftr']]
x2 = df[['orbpct','drbpct','trbpct', 'astpct']]
x3 = df[['stlpct','blkpct', 'tovpct']]
players = df[['name', 'team', 'pos', 'game', 'usg_rate', 'ws_rate']]

# Cauculate game and usg rate according to team quantity
players['team_game'] = df.groupby('team')['game'].transform('sum')
players['team_usg_rate'] = df.groupby('team')['usg_rate'].transform('sum')
players['game'] = players['game'] / players['team_game'] 
players['usg_rate'] = players['usg_rate'] / players['team_usg_rate']  

# For persent data
y_pred = models[0].predict(x1)
y_pred2 = models[1].predict(x2)
y_pred3 = models[2].predict(x3)
y_pred_result = y_pred + y_pred2 + y_pred3
y_pred_result = y_pred_result.astype('float64')
for idx, pred in enumerate(y_pred_result):
    y_pred_result[idx] = y_pred_result[idx] * (players['game'].iloc[idx] + players['usg_rate'].iloc[idx]) + float(players['ws_rate'].iloc[idx])
    
players['win_rate'] = y_pred_result
print(players.sort_values(by=['team']))
teams = players.groupby('team').sum()
print(teams.sort_values(by=['win_rate']))
# For data should be regularize



# team_result_data = {}
# team_result_data_count = {}
# with open('output.csv', 'w', newline='') as csvfile:

#     writer = csv.writer(csvfile)
    
#     for team in teams:
#         team_result_data[team] = 0
#         team_result_data_count[team] = 0


#     for row in rows:
#         player_result_data = [row['name'], row['team']]
#         for key, regre_data in regre_lists.items():
#              if key in str(player_ref_lists.keys()):
#                  value = (float(row[key])*regre_lists[key][0] + regre_lists[key][1] - player_ref_lists[key][0]) / player_ref_lists[key][2]
#                  if key == "trbpct":
#                      player_result_data.append(round(value/3, 3))
#                  else:
#                      player_result_data.append(round(value,3))
#              else:
#                  player_result_data.append(round(float(row[key])*regre_lists[key][0] + regre_lists[key][1],3))
            
#         player_result_data.append(round(sum(player_result_data[2:11]),3))
#         player_result_datas.append(player_result_data)
#         team_result_data[row['team']] += sum(player_result_data[2:11])
#         team_result_data_count[row['team']] += 1

#     player_result_datas = sorted(player_result_datas,key=lambda x: x[11])
#     for key, team_data in team_result_data.items():
#         team_result_data[key] = team_data/team_result_data_count[key]
#         writer.writerow([key,team_data/team_result_data_count[key]])
# with open('output2.csv', 'w', newline='') as csvfile2:
#     writer2 = csv.writer(csvfile2)
#     for player_data in player_result_datas:
#         writer2.writerow([player_data[0],player_data[11]])

# print(team_result_data)
# print(player_result_datas)
    
    
