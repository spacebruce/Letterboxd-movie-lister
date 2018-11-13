#!/usr/bin/python
import requests
import time
from bs4 import BeautifulSoup

class Page():
	def __init__(self, url):
		self.url = url
		self.page = None
		self.soup = None
		self.ready = False
	def Load(self):
		self.page = requests.get(self.url)
		self.soup = BeautifulSoup(self.page.text,"html.parser")
		self.ready = True

class Film():
	def __init__(self, name):
		self.name = name

UserName = input("Username? ")

firstPage = Page('https://letterboxd.com/' + UserName + '/films/page/1/')
firstPage.Load()

pageDiscovery = firstPage.soup.find(class_='paginate-pages')
pageDiscoveryList = pageDiscovery.find_all('a')

# Find page count
pageCount = 0
for pageID in pageDiscoveryList:
	pageNumber = pageID.contents[0]
	pageCount = max(pageCount, int(float(pageNumber)))

# Ready every page
print("Loading")
pageList = [ firstPage ]
for pageNum in range(2, pageCount + 1):
	pageTemp = Page('https://letterboxd.com/' + UserName + '/films/page/' + str(pageNum) + '/')
	pageList.append(pageTemp)

# Find films on pages
filmList = []

print("Reading...")
for i in range(0, len(pageList)):
	page = pageList[i]
	if page.ready == False:
		page.Load()
	print(str(i + 1) + "/" + str(len(pageList)) + " " + page.url)
	posterContainer = page.soup.find(class_='poster-list')
	posterList = posterContainer.find_all('img')
	for film in posterList:
		name = film.get('alt')
		name.encode('utf8')
		filmList.append(name)
	time.sleep(1)	# wait a bit for next request

print(filmList)

# write out
OutFile = input("Output file? ")

f = open(OutFile,'w',encoding='utf-8')
for film in filmList:
	f.write(film + '\n')
f.close()
