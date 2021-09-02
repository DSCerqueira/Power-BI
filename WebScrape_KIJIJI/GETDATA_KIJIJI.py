from bs4 import BeautifulSoup as bsp
import pandas as pd
import requests,time

path = "URLs_collection.txt" ##--The file shoud be in the same directory than the file python code
buildings = pd.read_csv(path)
###--- buldings array collection ----###
columnsArray = ['type', 'bedroom', 'bathroom', 'size(sqft)', 'address', 'price','lat','long','url']
response = requests

def coldata(data,bld): ##--function created to collect the data for each url
    counter=0
    error=[]
    buildingArrayFunc=bld

    for i in range(len(data)):
        counter=counter+1
        try:
            collectionArray = []
            requests.session().close()

            if counter>100: ##--it will sleep 1s for each 100 urls searched.
                time.sleep(1)
                counter=0

            url = data.iloc[i][0]
            response = requests.get(url)
            soup = bsp(response.text, "html.parser")
            advDesc = soup.findAll('span', attrs={'class': 'noLabelValue-3861810455'})

            for i in range(3):
                col = advDesc[i].text
                col = col.split(':')
                collectionArray.append(col[-1])

            advDesc = soup.findAll('dd', attrs={'class': 'twoLinesValue-2815147826'})
            collectionArray.append(advDesc[4].text)
            advDesc = soup.findAll('span', attrs={'class': 'address-3617944557'})
            collectionArray.append(advDesc[0].text)
            advDesc = soup.findAll('div', attrs={'class': 'priceWrapper-1165431705'})
            price = advDesc[0].text
            price = price.split(' ')
            collectionArray.append(price[0])
            lat = soup.find('meta', {"property": "og:latitude"}).attrs['content']
            lon = soup.find('meta', {"property": "og:longitude"}).attrs['content']
            collectionArray.append(lat)
            collectionArray.append(lon)
            collectionArray.append(url)
            buildingArrayFunc.append(collectionArray)

        except: ###-- the list of urls havent found in this cycle serching will be saved
            error.append(url)

    return(buildingArrayFunc,error) ##--the function returns two arrays, The first one is with the data of URLs found and the second one is the urls havent found.


bldinput=buildings
errorout=buildings
bldout=[]
countert=0
while len(errorout)>0: ###---this loop will be used to try to clean up the list of URLs not found. If the loop exceed more tha 10 times for the same error array, the loop will be interrupted and URLs with error will be saved.
    a = len(errorout)
    callfunc = coldata(bldinput, bldout)
    errorout = callfunc[1]
    bldout = callfunc[0]
    if a==len(errorout):
        countert=countert+1
    elif a>len(errorout):
        countert=0
    bldinput=pd.DataFrame(errorout,columns=['URLS'])

    if countert>10:
        print("More than 10 loops!")
        errorout=pd.DataFrame(errorout)
        errorout.to_csv("URLsError.csv")
        break


datacollection=pd.DataFrame(bldout,columns=columnsArray)
    
datacollection.to_csv("URLs_found.csv")

