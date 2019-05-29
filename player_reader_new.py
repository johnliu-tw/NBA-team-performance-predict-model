import pymysql.cursors
import numpy as np
import csv

connection = pymysql.connect (host='localhost',
                             user='root',
                             password='password',
                             db='nba_analytics',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM players_advanced_statistics"
        cursor.execute(sql)
        rows = cursor.fetchall()

regre_lists = {"tspct": [3.963, -1.651],
               "efgpct": [3.469,-1.241],
               "threepar": [0.177, 0.455],
               "ftr": [0.661, 0.305],
               "trbpct": [0.035, -1.256],
               "astpct": [-0.003, 0.596],
               "stlpct": [0.004, 0.361],
               "blkpct":[0.02, 0.343],
               "tovpct":[-0.017, 0.717]}

#wiat to change
player_ref_lists = { 
        "trbpct": [-1.067, -0.282, 0.785],
        "astpct": [0.611, 0.419, -0.192],
        "stlpct": [0.340, 0.363, 0.023],
        "blkpct":[0.340, 0.542, 0.202],
        "tovpct":[0.669,0.037, 0.632]
    }

player_result_datas = []
teams = set([row['team'] for row in rows])
team_result_data = {}
team_result_data_count = {}
with open('output.csv', 'w', newline='') as csvfile:

    writer = csv.writer(csvfile)
    
    for team in teams:
        team_result_data[team] = 0
        team_result_data_count[team] = 0

    for row in rows:
        player_result_data = [row['name'], row['team']]
        for key, regre_data in regre_lists.items():
             if key in str(player_ref_lists.keys()):
                 value = (float(row[key])*regre_lists[key][0] + regre_lists[key][1] - player_ref_lists[key][0]) / player_ref_lists[key][2]
                 player_result_data.append(round(value,3))
             else:
                 player_result_data.append(round(float(row[key])*regre_lists[key][0] + regre_lists[key][1],3))
            
        player_result_data.append(round(sum(player_result_data[2:11]),3))
        player_result_datas.append(player_result_data)
        team_result_data[row['team']] += sum(player_result_data[2:11])
        team_result_data_count[row['team']] += 1

    player_result_datas = sorted(player_result_datas,key=lambda x: x[11])
    for key, team_data in team_result_data.items():
        team_result_data[key] = team_data/team_result_data_count[key]
        writer.writerow([key,team_data/team_result_data_count[key]])
with open('output2.csv', 'w', newline='') as csvfile2:
    writer2 = csv.writer(csvfile2)
    for player_data in player_result_datas:
        writer2.writerow([player_data[0],player_data[11]])

print(team_result_data)
print(player_result_datas)
    
    
