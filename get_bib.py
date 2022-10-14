import requests
from bs4 import BeautifulSoup
import os
def download_bib(title,num,dirname):
    #num str
    url = 'https://dblp1.uni-trier.de/search'
    data = {
        'q': title
    }
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
    Chrome/55.0.2883.87 Safari/537.36'}
    response = requests.get(url, params=data , headers = headers)
    # print(response.text)
    bs = BeautifulSoup(response.content, "lxml")
    bib = bs.find(name ="nav",class_ = "publ")
    li = bib.find(name="li",class_="drop-down").next_sibling
    a = li.find(name="a")
    bib_url =a.get('href')
    response_bib = requests.get(bib_url , headers = headers)
    bs_bib = BeautifulSoup(response_bib.content, "lxml") 
    div_bib =bs_bib.find(name ="div",id ="main")
    a_bib = div_bib.find(name ="div",id ="breadcrumbs")
    b=a_bib.find_next_sibling()
    c=b.find(name="a")
    bib_download_url =c.get('href')
    r = requests.get(bib_download_url)
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    with open(dirname+'/'+num+".bib", "wb") as code:
        code.write(r.content)