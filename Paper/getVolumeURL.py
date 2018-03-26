import os
import shelve
import requests
import bs4

shelveFile = shelve.open('urls')

urls = shelveFile['urls']

print(urls)

n = 0
volsUrl={}

for url in urls:
    if url.startswith('http://www'): 
        continue
    res = requests.get(url)
    soup1 = bs4.BeautifulSoup(res.text, 'lxml')
    elems = soup1.select('div[id="main"] > p')
    if len(elems) == 2:
        title = elems[1].getText()
    else:
        title = elems[0].getText()
    volumeUrls = soup1.select('div[id="main"] > ul > li')
    vurls = []
    for vurlElement in volumeUrls:
        if n > 3:
            n = 0
            break
        if len(vurlElement.select('a')) > 0:
            vurl = vurlElement.select('a')[0].get('href')
            vurls.append(vurl)
        n = n + 1
    volsUrl[title] = vurls

print(volsUrl)

shelveFile['volUrl'] = volsUrl

shelveFile.close()
