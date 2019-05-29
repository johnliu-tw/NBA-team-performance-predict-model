import sys # system
import os # operation system
import pymysql.cursors
import numpy as np
from sympy import *
from bokeh.io import output_notebook, push_notebook, show
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Spectral6
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.models import GMapPlot, GMapOptions, Circle, Range1d
from bokeh.models import BoxZoomTool, ResetTool, HoverTool
from bokeh.models import CustomJS, Slider
from bokeh.models import TextInput
from bokeh.layouts import row, column, gridplot
from random import random

connection = pymysql.connect (host='localhost',
                             user='root',
                             password='password',
                             db='nba_analytics',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
rows={}
with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM team_advanced_statistics where id > 50000"
        cursor.execute(sql)
        rows = cursor.fetchall()
tspct = [row['tspct'] for row in rows]
efgpct = [row['efgpct'] for row in rows]
threepar = [row['threepar'] for row in rows]
ftr = [row['ftr'] for row in rows]
orbpct = [row['orbpct'] for row in rows]
drbpct = [row['drbpct'] for row in rows]
trbpct = [row['trbpct'] for row in rows]
astpct = [row['astpct'] for row in rows]
stlpct = [row['stlpct'] for row in rows]
blkpct = [row['blkpct'] for row in rows]
tovpct = [row['tovpct'] for row in rows]
result = [1 if row['result'] == "W" else 0 for row in rows]

# # PRINT



########################################
X = np.linspace(0, 10)
f = lambda x: x #y=x
F = np.vectorize(f)
Y = F(X)

#random data by F(X) + random residual(upper bound=2)
num = 15 #number of data
random_sign = np.vectorize(lambda x: x if np.random.sample() > 0.5 else -x)
data_X = {
    "tspct": tspct,
    "efgpct": efgpct,
    "threepar": threepar,
    "ftr": ftr,
    "orbpct": orbpct,
    "drbpct": drbpct, 
    "trbpct": trbpct,
    "astpct": astpct, 
    "stlpct": stlpct,
    "blkpct": blkpct,
    "tovpct": tovpct
}
data_Y = result


LR_X = [[0,0.5,1],[10,30,50]]
LR_Y = []



plots = []

for key, subDataX in data_X.items():
    x=0
    xx=0
    yy=0
    xy=0
    for idx, data in enumerate(subDataX):
        x += data
        xx += data*data
        yy += data_Y[idx]*data_Y[idx]
        xy += data*data_Y[idx]
    xmean = x/len(subDataX)
    slope = (xy-len(subDataX)*xmean*0.5)/(xx-len(subDataX)*xmean*xmean)
    a = 0.5-slope*xmean
    slope=round(slope, 3)
    a=round(a, 3)
    print(key)

    if key in str(["tspct","efgpct","threepar","ftr"]):
        x_idx = 0
    else:
        x_idx = 1
    
    source_data_y = []
    for i in range(3):
        source_data_y.append(round(LR_X[x_idx][i]*slope+a, 3))
    LR_Y.append(source_data_y)
    print(slope)
    print(a)

    if abs(slope) > 1:
        y_range = [-2,2]
    else:
        y_range = [0,1]
       
    title = key+" y= "+str(slope)+" x+ "+str(a)
    p = figure(plot_width = 400, y_range=y_range, plot_height = 400, title=title)
    p.line (LR_X[x_idx], source_data_y, line_width = 4)
    plots.append(p)


grid = gridplot([[plots[0],plots[1],plots[2]],[plots[3],plots[4],plots[5]],[plots[6],plots[7],plots[8]],[plots[9],plots[10]]]) 
show(grid)
output_file("figure.html")


# TODO
# MILESTONES
# mergeList (+)
# + with +, - with -
# totalX, totalY

# HOW TO PUSH
# git add .
# git commit -m ".."
# git push
