from bs4 import BeautifulSoup as bsp
import requests,os,datetime

##--Colecting URLs from Kijiji for grand Montreal Area. The URLs will be saved in a Text file for future data collection

##---creating folder to save cellected files
tday=datetime.date.today()
folder="URLs_"+str(tday)
mkdr="mkdir "+os.getcwd()+"\\"+folder
os.system(mkdr)

###--creating txt file with urls
textpath=os.getcwd()+"\\"+folder+"\\"+folder+".txt"
urltext = open(textpath, 'w')
urltext.writelines('URLS\n')

urlsarray=[] ###--urls array

appttype=["appartement","duplex+triplex","condo","sous+sol+appartement","maison","maison+en+rangee"] ###--unit type

response=requests
###---collecting urls for each apptype
pageend=0
for type in appttype:

    url="https://www.kijiji.ca/b-appartement-condo/grand-montreal/"+type+"/c37l80002a29276001"

    ##--the initial searching page for each apptype will tested 1000 times, if any page restulte in a error, the page will be printed for the future check.
    ##--The initial target is to get the number of page searched returned for each apptype
    for n in range(10002):
        try:
            requests.session().close()
            response = requests.get(url)
            soup=bsp(response.text,"html.parser")
            pages=soup.select_one("span[class=resultsShowingCount-2351335546]").text
            break
        except:
            if n>10000:
                print("error: "+ url)

    number=pages.split(" ") ##--number of pages.
    pages=int(int(number[6]*1)/40)+2
    if pages>100: ##-- I have noticide that the maximum number of pages that Kijiji returned with data is 100 (40 advertising for page, maximum of 4000 advertising), even if the result shows that are more retults.
        pages=101

    advUrls=soup.findAll('div',attrs={'class':'search-item'})

    ##--colecting data for the first page
    for i in advUrls:
        urlpth="https://www.kijiji.ca"+i.find('a')['href']
        urlsarray.append(urlpth)
        urltext.writelines(urlpth+ '\n')


    ##getting data for the other pages
    for link in range(2,pages):
        k = 0
        while k<1:###--the loop will persist until gets a return. It maybe results in a deadlock, but it has worked so far.
            url="https://www.kijiji.ca/b-appartement-condo/grand-montreal/"+type+"/page-"+str(link)+"/c37l80002a29276001"
            try:
                response=requests.get(url)
                soup = bsp(response.text, "html.parser")
                advUrls = soup.findAll('div', attrs={'class': 'search-item'})

                for i in advUrls:
                    k=k+1
                    urlpth = "https://www.kijiji.ca" + i.find('a')['href']
                    urlsarray.append(urlpth)
                    urltext.writelines(urlpth + '\n')
            except:
                pass

        print(k)


urltext.close()


