import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which
import time
import pandas as pd
import numpy as np
import joblib
from numpy import savetxt
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


chrome_path = 'chromedriver.exe'
Players = []
Bets = []
Cashs_Out =[]
Profits = []
game_ids =[]
Busted_At = []
driver = webdriver.Chrome(executable_path=chrome_path)

# driver.get('https://www.bustabit.com/game/2000')
# time.sleep(5)
i=3973010       #starting id
idd=[]
pred=[]
m=1
while (m<21):
    j=i+1
    m=m+1
    for id in range(i,j):
        Players = []
        Bets = []
        Cashs_Out = []
        Profits = []
        game_ids = []
        Busted_At = []
        #i=i+1
        url = f'https://www.bustabit.com/game/{id}'
        driver.get(url)
        time.sleep(8)
        for a in driver.find_elements_by_xpath('//div[@class="oMRXjPQYe_IJLADVIUrdO modal-body"]/div/div[2]/table/tbody/tr/td[1]/a'):
            Players.append(a.text)
            #print(Players)
        for b in driver.find_elements_by_xpath('//div[@class="oMRXjPQYe_IJLADVIUrdO modal-body"]/div/div[2]/table/tbody/tr/td[2]'):
            Bets.append(b.text)

        for c in driver.find_elements_by_xpath('//div[@class="oMRXjPQYe_IJLADVIUrdO modal-body"]/div/div[2]/table/tbody/tr/td[3]'):
            Cashs_Out.append(c.text)

        for d in driver.find_elements_by_xpath('//div[@class="oMRXjPQYe_IJLADVIUrdO modal-body"]/div/div[2]/table/tbody/tr/td[4]'):
            Profits.append(d.text)


    
    
   

    game_1 = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//h3')))
    ab = (game_1.text)

    Busted = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//p[@class="_2IumaQfnOQsiJTuwTJZlvp"]/span[2]')))
    bc = (Busted.text)
  
    for game in range(len(Players)):
        game_ids.append(ab)
        Busted_At.append(bc)

    



    df = pd.DataFrame(game_ids, columns = ['Game_ID'])
    df["Players"] = Players
    df["Bets"] = Bets
    df["Cashout"] = Cashs_Out
    df["Profits"] = Profits
    df["Busted_At"] = Busted_At
    df.drop(["Players"], axis=1, inplace=True)
    df['Cashout'] = df['Cashout'].str.replace('-','0')
    df['Cashout'] = df['Cashout'].str.replace('x','0')
    df['Cashout'] = df['Cashout'].str.replace('Cashout','0')
    df['Busted_At'] = df['Busted_At'].str.replace('z','0')
    df['Busted_At'] = df['Busted_At'].str.replace('x','')
    df['Game_ID'] = df['Game_ID'].str.replace('Game #','')
    df['Bets'] = df['Bets'].str.replace(',','')
    df['Profits'] = df['Profits'].str.replace(',','')
    df['Cashout'] = df['Cashout'].str.replace(',','')
    x = df.iloc[:,[1,2,3]].values
    print(x)
    id1=[]
    id1=df['Game_ID']

    model = joblib.load('train_LR')
    res= model.predict(x)
    #pred.append(list(model.predict(x)))
    show=[id1,res]
    show=np.transpose(show)
    print(show)
    i=i+1
    for k in range(len(id1)):
        idd.append(id1[k])
    for l in range(len(res)):
        pred.append(res[l])
    #savetxt('predicted_data.csv', data,'%s',delimiter=',')
# # Set Path for where you want to save file
#df.to_csv ('test.csv', index = False, header=True)
    data=[idd,pred]
    data=np.transpose(data)

    #df=pd.DataFrame(data,columns=['Game_id','Price'])
    savetxt('predicted_data.csv', data, '%s', delimiter=',')
    #print(data)
    #print(data)
    #savetxt("nxx", data.reshape((3,-1)), fmt="%s", header=str(data.shape))
driver.close()