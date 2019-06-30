import sys
import os
import pymysql.cursors
import pymysql
import pandas as pd
import numpy as np
from sklearn.externals import joblib 
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

connection = pymysql.connect (host='localhost',
                             user='root',
                             password='password',
                             db='nba',
                            cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT tspct, efgpct, ftr, orbpct, drbpct, trbpct, astpct, stlpct, blkpct, tovpct, result FROM team_advanced_statistics"
        df = pd.read_sql(sql, con=connection)

        x = df[['tspct','efgpct','ftr']]
        x2 = df[['orbpct','drbpct','trbpct', 'astpct']]
        x3 = df[['stlpct','blkpct', 'tovpct']]
        y = df['result']
        X = [x, x2, x3]
        for sub_x in X:
            X_train, X_test, y_train, y_test = train_test_split(sub_x, y, test_size = 0.20)
            file_name = '_'.join(str(x) for x in sub_x.columns.values)
            model_name = "models/{}.pkl".format(file_name)
            print(model_name)
            if os.path.isfile(model_name):
                svclassifier = joblib.load(model_name)
            else:
                print("train start")
                svclassifier = SVC(kernel='linear')
                svclassifier.fit(X_train, y_train)
                joblib.dump(svclassifier, model_name)
                print("train end")
                y_pred = svclassifier.predict(X_test)
                print(classification_report(y_test,y_pred))

