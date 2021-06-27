from selenium import webdriver
from time import sleep
import time
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

g = ""
class valorantBot():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(os.getenv('DRIVER_PATH'), options=chrome_options)

    def fTry(self, path, elementType = "xpath", debug = True, stop = 0.5):
        # Force try function

        c = 1
        sleep(stop)
        while True:
            try:
                if elementType.lower() == "xpath":
                    pathOutput = self.driver.find_element_by_xpath(path)
                elif elementType.lower() == "class":
                    pathOutput = self.driver.find_element_by_class_name(path)
                else:
                    raise Exception("elementType variable must be defined differently.")
                return pathOutput
            except Exception as e:
                if debug:
                    print(f"Waiting... {c}; Error: {e}")
                c += 1
                sleep(stop)

    def getMapsFromRank(self, numMaps = 6):
        maps_list = []
        for i in range(1, numMaps + 1):
            mapName = self.fTry(f'//*[@id="scroll-view-main"]/div[1]/div/div/div/div/div[1]/div/div[2]/div/div[2]/ul/li[{i}]/a/div/p').text
            playRate = self.fTry(f'//*[@id="scroll-view-main"]/div[1]/div/div/div/div/div[1]/div/div[2]/div/div[2]/ul/li[{i}]/a/p[2]').text
            atkWin = self.fTry(f'//*[@id="scroll-view-main"]/div[1]/div/div/div/div/div[1]/div/div[2]/div/div[2]/ul/li[{i}]/a/p[3]').text
            defWin = self.fTry(f'//*[@id="scroll-view-main"]/div[1]/div/div/div/div/div[1]/div/div[2]/div/div[2]/ul/li[{i}]/a/p[4]').text
            numMatches = self.fTry(f'//*[@id="scroll-view-main"]/div[1]/div/div/div/div/div[1]/div/div[2]/div/div[2]/ul/li[{i}]/a/p[5]').text
            maps_list.append([mapName, playRate, atkWin, defWin, numMatches])
        
        maps_df = pd.DataFrame(maps_list, columns=["Map Name", "Play Rate", "Atk Win", "Def Win", "Num Matches"])
        return maps_df

    def getMaps(self, numMaps = 6, modes = ["Competitive", "Unrated", "Spike Rush", "Custom"]):
        maps_list = []

        # Iron 1 - tier #3
        # Immortal - tier #21
        # Radiant - tier #24

        for mode in modes:
            mode = (mode.lower()).replace(' ', '')
            print(f"Completing analysis of maps for mode {mode}...")

            if mode == "competitive":
                for i in range(3, 21):
                    print(f"Completing analysis of tier {i}...")
                    self.driver.get(f'https://blitz.gg/valorant/stats/maps?map=all&act=e3act1&queue=competitive&tier={i}')
                    sleep(1)
                    maps_df = self.getMapsFromRank()
                    maps_df.to_csv(f"map_data/maps_competitive_tier={i}.csv")
            else:
                self.driver.get(f'https://blitz.gg/valorant/stats/maps?map=all&act=e3act1&queue={mode}&tier=0')
                sleep(1)
                maps_df = self.getMapsFromRank()
                maps_df.to_csv(f"map_data/maps_{mode}_tier=0.csv")

    def getAgentsFromRank(self, numAgents = 15):
        agents_list = []
        for i in range(1, numAgents + 1):
            agentName = self.fTry(f'//*[@id="scroll-view-main"]/div[1]/div/div/div/div/div[1]/div/div[2]/div/div[2]/ul/li[{i}]/a/div/p').text
            KD = self.fTry(f'//*[@id="scroll-view-main"]/div[1]/div/div/div/div/div[1]/div/div[2]/div/div[2]/ul/li[{i}]/a/p[2]').text
            KDA_text = self.fTry(f'//*[@id="scroll-view-main"]/div[1]/div/div/div/div/div[1]/div/div[2]/div/div[2]/ul/li[{i}]/a/p[3]').text
            kills = KDA_text[:KDA_text.index('/')-1]
            KDA_text = KDA_text[KDA_text.index('/')+2:]
            deaths = KDA_text[:KDA_text.index('/')-1]
            KDA_text = KDA_text[KDA_text.index('/')+2:]
            assists = KDA_text
            agents_list.append([agentName, KD, kills, deaths, assists])

        agents_df = pd.DataFrame(agents_list, columns=["Agent Name", "KD", "Kills", "Deaths", "Assists"])
        return agents_df

    def getAgents(self, modes = ["Competitive", "Unrated", "Spike Rush", "Custom"]):
        for mode in modes:
            mode = (mode.lower()).replace(' ', '')
            print(f"Completing analysis of agents for mode {mode}.")

            if mode == "competitive":
                for i in range(3, 21):
                    print(f"Completing analysis of tier {i}...")
                    self.driver.get(f'https://blitz.gg/valorant/stats/agents?map=all&act=e3act1&queue=competitive&tier={i}')
                    sleep(1)
                    agents_df = self.getAgentsFromRank()
                    agents_df.to_csv(f"agents_data/agents_competitive_tier={i}.csv")
            else:
                self.driver.get(f'https://blitz.gg/valorant/stats/agents?map=all&act=e3act1&queue={mode}&tier=0')
                sleep(1)
                agents_df = self.getAgentsFromRank()
                agents_df.to_csv(f"agents_data/agents_{mode}_tier=0.csv")

    def end(self):
        self.driver.quit()

bot = valorantBot()
#bot.getMaps()
bot.getAgents(modes=['unrated', 'spike rush', 'custom'])
#testing