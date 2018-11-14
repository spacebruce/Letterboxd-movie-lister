#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import time
from datetime import date
import sys
import re
from bs4 import BeautifulSoup

class Page():
	def __init__(self, url):
		self.url = url
		self.page = None
		self.soup = None
		self.year = 0
		self.ready = False
	def Load(self):
		self.page = requests.get(self.url)
		self.soup = BeautifulSoup(self.page.text,'html.parser')
		self.ready = True

class Film():
	def __init__(self, name, rating, year):
		self.name = name
		self.rating = rating
		self.year = year
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
        UserName = input('Please enter a Username : ')
else:
        UserName = str(sys.argv[1])
        if(ArgCount == 3):
                OutPath = sys.argv[2]
firstPage = Page('https://letterboxd.com/' + UserName + '/films/page/1/')
firstPage.Load()
startYear = 1870				# the first year EVER
endYear = date.today().year + 1	# It's conceivable user could see a prerelease/early screening for a film from next year)

# Find page count
pageCount = 0

pageDiscovery = firstPage.soup.find(class_='paginate-pages')
pageDiscoveryList = pageDiscovery.find_all('a')

for pageID in pageDiscoveryList:
	pageNumber = pageID.contents[0]
	pageCount = max(pageCount, int(pageNumber))

# Ready every page
pageList = [ firstPage ]

for pageNum in range(2, pageCount + 1):
	pageTemp = Page('https://letterboxd.com/' + UserName + '/films/page/' + str(pageNum) + '/')
	pageList.append(pageTemp)

# Find films on pages
filmList = []

print('Reading...')
for i in range(0, len(pageList)):
	page = pageList[i]
	if page.ready == False:
		time.sleep(1)	# wait a bit for request
		page.Load()
	print(str(i + 1) + "/" + str(len(pageList)) + " " + page.url)
	
	# read posters
	posterContainer = page.soup.find(class_='poster-list')
	ratingList = posterContainer.find_all('li')		#	<li class="poster-container" data-owner-rating="0">
	nameList = posterContainer.find_all('img')		#	<img alt="John Wick: Chapter 2" class="image" height="105" src="https://s1.ltrbxd.com/static/img/empty-poster-70.8461d4ea.png" width="70"/>
	
	for film in range(0, len(nameList)):
		nameEntry = nameList[film]
		name = nameEntry.get('alt')
		name.encode('utf8')
		
		ratingEntry = ratingList[film]
		ratingData = ratingEntry.get('data-owner-rating')
		rating = int(ratingData)
		
		year = 0
		#yearEntry = ratingEntry.find_all('div')
		#print(yearEntry[0])
		#yearData = ratingEntry.get('data-film-release-year')
		
		filmList.append(Film(name, rating, year))

# sort list alphabetically
filmList = sorted(filmList, key=lambda film: film.name)

# write out
if(OutPath == ''):
        OutPath = input('Enter output file name : ')

f = open(OutPath,'w',encoding='utf-8')
for film in filmList:
	if(film.rating != 0):
		f.write(film.name + " " + str(film.Stars()) + '\n')
	else:
		f.write(film.name + '\n')
f.close()
