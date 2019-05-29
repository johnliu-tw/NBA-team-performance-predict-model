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

for i in range(ord("a"), ord("z")+1):
    time.sleep(1)
    driver.get('''https://www.basketball-reference.com/players/{}/'''.format(chr(i))) # designate website
    sourceCode = BeautifulSoup (driver.page_source, "html.parser") # initialize page source
    contents = sourceCode.find_all(id = "players")
    for content in contents:
        sourceCode2 = BeautifulSoup (str(contents), "html.parser")
        playersData = sourceCode2.find_all("tr")
        for idx, playerData in enumerate(playersData):
            # print(idx)
            if (idx != 0): 
                sourceCode3 = BeautifulSoup (str(playerData), "html.parser")
                playersYear = sourceCode3.find_all("td")
                # print(playersYear)
                if (int(playersYear[0].text) != 2018 and int(playersYear[1].text) >= 2018):
                    link = sourceCode3.find_all("a")[0]['href']
                    # print(link)
                    driver2.get('''https://www.basketball-reference.com''' + link)
                    sourceCode4 = BeautifulSoup (driver2.page_source, "html.parser")
                    total_data_source = sourceCode4.find_all(id="totals.2018")
                    total_data = BeautifulSoup(str(total_data_source), "html.parser")
                    row_data_source = sourceCode4.find_all(id = "advanced.2018")[0]
                    row_data = BeautifulSoup (str(row_data_source), "html.parser")
                    player_statlist = row_data.find_all("td")
                    # PLAYER STATISTICS
                    player_name = sourceCode4.find_all("h1")[0].text
                    player_team = player_statlist[1].text
                    player_tspct = float("0" + player_statlist[7].text)
                    player_efgpct = float("0" + total_data.find_all("td")[16].text)
                    player_3PAr = float("0" + player_statlist[8].text)
                    player_FTr = float("0" + player_statlist[9].text)
                    player_ORBpct = float("0" + player_statlist[10].text)
                    player_DRBpct = float("0" + player_statlist[11].text)
                    player_TRBpct = float("0" + player_statlist[12].text)
                    player_ASTpct = float("0" + player_statlist[13].text)
                    player_STLpct = float("0" + player_statlist[14].text)
                    player_BLKpct = float("0" + player_statlist[15].text)
                    player_TOVpct = float("0" + player_statlist[16].text)
                    player_USGpct = float("0" + player_statlist[17].text)
                    # player_Ortg = float("0" + player_statlist[].text)
                    # player_Drtg = float("0" + player_statlist[].text)
                    # print (player_name + " " + str(player_tspct) + " " + str(player_efgpct))
                    cursor = connection.cursor()
                    cursor.execute ('''INSERT INTO nba_reference_data.players_advanced_statistics 
                                        (name, team, tspct, efgpct, threepar, ftr, orbpct, drbpct, 
                                        trbpct, astpct, stlpct, blkpct, tovpct) VALUES ('{}', '{}', 
                                        {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});'''.format
                                        (player_name, player_team, player_tspct, player_efgpct, 
                                        player_3PAr, player_FTr, player_ORBpct, player_DRBpct, 
                                        player_TRBpct, player_ASTpct, player_STLpct, player_BLKpct, 
                                        player_TOVpct))
                    connection.commit()
                    
                    


connection.close() # end connection
driver.close() # end browser
driver2.close() # end browser
