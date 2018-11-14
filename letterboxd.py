#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import time
import sys
from bs4 import BeautifulSoup

class Page():
	def __init__(self, url):
		self.url = url
		self.page = None
		self.soup = None
		self.ready = False
	def Load(self):
		self.page = requests.get(self.url)
		self.soup = BeautifulSoup(self.page.text,'html.parser')
		self.ready = True

class Film():
	def __init__(self, name, rating):
		self.name = name
		self.rating = rating
	def Stars(self):
		star = '★'
		half = '½'
		ratinghalf = int(self.rating / 2)
		returnstring = ''
		for i in range(0, ratinghalf):
			returnstring += star
		if(ratinghalf * 2 != self.rating):
			returnstring += half
		return returnstring
		

UserName = ""
OutPath = ""

ArgCount = len(sys.argv)
if(ArgCount < 2):
        UserName = input("Please enter a Username : ")
else:
        UserName = str(sys.argv[1])
        if(ArgCount == 3):
                OutPath = sys.argv[2]
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
	ratingList = posterContainer.find_all('li')
	nameList = posterContainer.find_all('img')
	for film in range(0, len(nameList)):
		nameEntry = nameList[film]
		name = nameEntry.get('alt')
		name.encode('utf8')
		
		ratingEntry = ratingList[film]
		ratingData = ratingEntry.get('data-owner-rating')
		rating = int(float(ratingData))
		
		filmList.append(Film(name,rating))
	time.sleep(1)	# wait a bit for next request

# sort list alphabetically
filmList = sorted(filmList, key=lambda film: film.name)

# write out
if(OutPath == ""):
        OutPath = input('Enter output file name : ')

f = open(OutPath,'w',encoding='utf-8')
for film in filmList:
	if(film.rating != 0):
		f.write(film.name + " " + str(film.Stars()) + '\n')
	else:
		f.write(film.name + '\n')
f.close()
