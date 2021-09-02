from bs4 import BeautifulSoup as bsp
import pandas as pd
import requests

###-- which colect the walk score for each Montreal postal code.
path = "Montreal_ZIP_Code.csv" ###--input file with each montreal postal code.

address = pd.read_csv(path)

response = requests

dataexit=[]

for i in range(len(address)):

    postal=address.iloc[i][1] + "+" + address.iloc[i][2]

    url="https://www.walkscore.com/score/"+postal
    k=0
    while k<1:
        try:
            response = requests.get(url)
            soup = bsp(response.text, "html.parser")
            walsco=soup.find('div',{"class": "block-header-badge score-info-link"}).img
            walsco=str(walsco).split('=')
            walsco=walsco[1].split('"')
            walkscore=walsco=walsco[1].split(" ")
            dataexit.append([address.iloc[i][1], walkscore[0]])
            print("Score "+str(walkscore[0]))
            k=2
        except:
            k=k+1
            if k>99:
                dataexit.append([address.iloc[i][1], ""])
                print("Score erro")

    print(i)

dataexit=pd.DataFrame(dataexit)
dataexit.to_csv("WalkscoreZipcode.csv")
