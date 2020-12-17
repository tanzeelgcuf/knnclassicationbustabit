import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from fake_useragent import UserAgent

options_1 = Options()
ua = UserAgent()
userAgent = ua.random
options_1.add_argument(f'user-agent={userAgent}')

chrome_path = which('chromedriver')
Players = []
Bets = []
Cashs_Out =[]
Profits = []
game_ids =[]
Busted_At = []
driver = webdriver.Chrome(executable_path=chrome_path, options= options_1)
def get():

    for a in driver.find_elements_by_xpath('//div[@class="oMRXjPQYe_IJLADVIUrdO modal-body"]/div/div[2]/table/tbody/tr/td[1]/a'):
        Players.append(a.text)
                    
    for b in driver.find_elements_by_xpath('//div[@class="oMRXjPQYe_IJLADVIUrdO modal-body"]/div/div[2]/table/tbody/tr/td[2]'):
        Bets.append(b.text)

    for c in driver.find_elements_by_xpath('//div[@class="oMRXjPQYe_IJLADVIUrdO modal-body"]/div/div[2]/table/tbody/tr/td[3]'):
        Cashs_Out.append(c.text)

    for d in driver.find_elements_by_xpath('//div[@class="oMRXjPQYe_IJLADVIUrdO modal-body"]/div/div[2]/table/tbody/tr/td[4]'):
        Profits.append(d.text)
# driver.get('https://www.bustabit.com/game/2000')
# time.sleep(5)
for id in range(3984300, 3984450):
    url = f'https://www.bustabit.com/game/{id}'
    driver.get(url)
    time.sleep(10)
    get()
    
    
   

game_1 = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//h3')))
ab = (game_1.text)

Busted = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//p[@class="_2IumaQfnOQsiJTuwTJZlvp"]/span[2]')))
bc = (Busted.text)
for game in range(len(Players)):
    game_ids.append(ab)
    Busted_At.append(bc)

    



df = pd.DataFrame(Players, columns = ['Players'])
df["Game_ID"] = game_ids
df["Bets"] = Bets
df["Cashout"] = Cashs_Out
df["Profits"] = Profits
df["Busted_At"] = Busted_At

# # Set Path for where you want to save file
df.to_csv (r'C:\Users\Amaar\Desktop\demo2.csv', index = False, header=True)
print(df)
driver.close()