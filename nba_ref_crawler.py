import sys # system
from bs4 import BeautifulSoup # html parse (解析程式碼)
import time # for delay
from selenium import webdriver # web simulator (網頁模擬器)
from selenium.webdriver.chrome.options import Options # web simulator (網頁模擬器)
import os # operation system
import psycopg2

connection = psycopg2.connect (database = "postgres", user = "postgres", password = "will0723", 
                               host = "127.0.0.1", port = "5432")
options = Options()
options.add_argument('--headless') # hidden browser (無標頭)
options.add_argument('--disable-gpu') 
driver = webdriver.Chrome(os.getcwd() + "/python/Crawler/chromedriver") # assign chromedriver
driver2 = webdriver.Chrome(os.getcwd() + "/python/Crawler/chromedriver")

for year in range(1984, 2019):
    for month in [1, 2, 3, 4, 5, 6, 10, 11, 12]:
        for day in range(1, 32):
            time.sleep(1) # delay
            driver.get('''https://www.basketball-reference.com/boxscores/?month={}&day={}&year={}'''.format(month, day, year)) # designate website
            sourceCode = BeautifulSoup (driver.page_source, "html.parser") # initialize page source
            contents = sourceCode.find_all(id = "content")
            # print(contents)
            for content in contents:
                sourceCode2 = BeautifulSoup (str(contents), "html.parser")
                gameSummaries = sourceCode2.find_all("div", "game_summary")
                # print(gameSummaries)
                for gameSummary in gameSummaries:
                    sourceCode3 = BeautifulSoup (str(gameSummary), "html.parser")
                    boxes = sourceCode3.find_all("td", "gamelink")
                    # print(boxes)
                    for box in boxes:
                        sourceCode4 = BeautifulSoup (str(box), "html.parser")
                        link = sourceCode4.find_all("a")[0]['href']
                        # print(link)
                        driver2.get("https://www.basketball-reference.com" + link) # designate website
                        sourceCode5 = BeautifulSoup (driver2.page_source, "html.parser")
                        scores = sourceCode5.find_all("div", "score")
                        team1_score = scores[0].text
                        team2_score = scores[1].text
                        # print(team1_score + " " + team2_score)
                        if (len(sourceCode5.find_all("tfoot")) >= 4): 
                            team1_stats = sourceCode5.find_all("tfoot")[1]
                            team2_stats = sourceCode5.find_all("tfoot")[3]
                            # print(team1_stats)
                            sourceCode6_1 = BeautifulSoup (str(team1_stats), "html.parser")
                            sourceCode6_2 = BeautifulSoup (str(team2_stats), "html.parser")
                            team1_statlist = sourceCode6_1.find_all("td")
                            team2_statlist = sourceCode6_2.find_all("td")
                            # TEAM 1 STATISTICS
                            team1_tspct = float("0" + team1_statlist[1].text)
                            team1_efgpct = float("0" + team1_statlist[2].text)
                            team1_3PAr = float("0" + team1_statlist[3].text)
                            team1_FTr = float("0" + team1_statlist[4].text)
                            team1_ORBpct = float("0" + team1_statlist[5].text)
                            team1_DRBpct = float("0" + team1_statlist[6].text)
                            team1_TRBpct = float("0" + team1_statlist[7].text)
                            team1_ASTpct = float("0" + team1_statlist[8].text)
                            team1_STLpct = float("0" + team1_statlist[9].text)
                            team1_BLKpct = float("0" + team1_statlist[10].text)
                            team1_TOVpct = float("0" + team1_statlist[11].text)
                            team1_Ortg = float("0" + team1_statlist[13].text)
                            team1_Drtg = float("0" + team1_statlist[14].text)
                            # TEAM 2 STATISTICS
                            team2_tspct = float("0" + team2_statlist[1].text)
                            team2_efgpct = float("0" + team2_statlist[2].text)
                            team2_3PAr = float("0" + team2_statlist[3].text)
                            team2_FTr = float("0" + team2_statlist[4].text)
                            team2_ORBpct = float("0" + team2_statlist[5].text)
                            team2_DRBpct = float("0" + team2_statlist[6].text)
                            team2_TRBpct = float("0" + team2_statlist[7].text)
                            team2_ASTpct = float("0" + team2_statlist[8].text)
                            team2_STLpct = float("0" + team2_statlist[9].text)
                            team2_BLKpct = float("0" + team2_statlist[10].text)
                            team2_TOVpct = float("0" + team2_statlist[11].text)
                            team2_Ortg = float("0" + team2_statlist[13].text)
                            team2_Drtg = float("0" + team2_statlist[14].text)
                            # insert to elephant STL
                            cursor = connection.cursor()
                            if (int(team1_score) > int(team2_score)): result = 'W'
                            else: result = 'L'
                            cursor.execute ('''INSERT INTO nba_reference_data.team_advanced_statistics 
                                            (tspct, efgpct, threepar, ftr, orbpct, drbpct, trbpct, astpct, 
                                            stlpct, blkpct, tovpct, ortg, drtg, result) VALUES ({}, {}, 
                                            {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, '{}');'''
                                            .format(team1_tspct, team1_efgpct, team1_3PAr, team1_FTr, 
                                            team1_ORBpct, team1_DRBpct, team1_TRBpct, team1_ASTpct, 
                                            team1_STLpct, team1_BLKpct, team1_TOVpct, team1_Ortg, 
                                            team1_Drtg, result))
                            if (result == 'W'): result = 'L'
                            else: result = 'W'
                            cursor.execute ('''INSERT INTO nba_reference_data.team_advanced_statistics 
                                            (tspct, efgpct, threepar, ftr, orbpct, drbpct, trbpct, astpct, 
                                            stlpct, blkpct, tovpct, ortg, drtg, result) VALUES ({}, {}, 
                                            {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, '{}');'''
                                            .format(team2_tspct, team2_efgpct, team2_3PAr, team2_FTr, 
                                            team2_ORBpct, team2_DRBpct, team2_TRBpct, team2_STLpct, 
                                            team2_ASTpct, team2_BLKpct, team2_TOVpct, team2_Ortg, 
                                            team2_Drtg, result))
                            connection.commit()

connection.close() # end connection
driver.close() # end browser
driver2.close() # end browser
