import sys 
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import pymysql
import traceback 

connection = pymysql.connect (db = "nba", user = "root", password = "password", 
                               host = "localhost")
options = Options()
options.add_argument('--headless') # hidden browser (無標頭)
options.add_argument('--disable-gpu') 
driver = webdriver.Chrome(os.getcwd() + "/chromedriver") # assign chromedriver
driver2 = webdriver.Chrome(os.getcwd() + "/chromedriver")

try:
    for i in range(ord("a"), ord("z")+1):
        driver.get('''https://www.basketball-reference.com/players/{}/'''.format(chr(i))) # designate website
        sourceCode = BeautifulSoup (driver.page_source, "html.parser") # initialize page source
        contents = sourceCode.find_all(id = "players")
        for content in contents:
            sourceCode2 = BeautifulSoup (str(contents), "html.parser")
            playersData = sourceCode2.find_all("tr")
            for idx, playerData in enumerate(playersData):
                # print(idx)
                if (idx != 0 and "thead" not in str(playerData)): 
                    sourceCode3 = BeautifulSoup (str(playerData), "html.parser")
                    playersYear = sourceCode3.find_all("td")
                    # print(playersYear)
                    if (int(playersYear[1].text) == 2019):
                        link = sourceCode3.find_all("a")[0]['href']
                        # print(link)
                        time.sleep(1)
                        driver2.get('''https://www.basketball-reference.com''' + link)
                        print(link)
                        sourceCode4 = BeautifulSoup (driver2.page_source, "html.parser")
                        total_data_source = sourceCode4.find_all(id="totals.2019")
                        total_data = BeautifulSoup(str(total_data_source), "html.parser")
                        row_data_source = sourceCode4.find_all(id = "advanced.2019")
                        for row_data_source_item in row_data_source:
                            row_data = BeautifulSoup (str(row_data_source_item), "html.parser")
                            player_statlist = row_data.find_all("td")
                            # PLAYER STATISTICS
                            player_name = sourceCode4.find_all("h1")[0].text
                            player_team = player_statlist[1].text
                            player_pos = player_statlist[3].text
                            player_game = int(player_statlist[4].text.strip().replace(" ",""))
                            print(player_statlist[4].text)
                            print(player_game)
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
                            if "-" in player_statlist[22].text:
                                player_WS48 = float( player_statlist[22].text)
                            else:
                                player_WS48 = float("0" + player_statlist[22].text)
                            cursor = connection.cursor()
                            sql = '''INSERT INTO nba.players_advanced_statistics 
                                    (name, team, pos, game, tspct, efgpct, threepar, ftr, orbpct, drbpct, 
                                    trbpct, astpct, stlpct, blkpct, tovpct, ws_rate) VALUES ("{}", "{}","{}",
                                    {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});'''.format(player_name, player_team, player_pos, 
                                    player_game, player_tspct, player_efgpct, 
                                    player_3PAr, player_FTr, player_ORBpct, player_DRBpct, 
                                    player_TRBpct, player_ASTpct, player_STLpct, player_BLKpct, 
                                    player_TOVpct, player_WS48)
                            print(sql)
                            cursor.execute (sql)
                            connection.commit()
    connection.close() # end connection
    driver.close() # end browser
    driver2.close() # end browser


except Exception as e:
    driver.quit()
    driver2.quit()
    connection.close()
    traceback.print_exc()                
                    