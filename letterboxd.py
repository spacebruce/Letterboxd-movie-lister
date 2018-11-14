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
		
def getYes(prompt):
	try:
	   return {"yes":True,"no":False}[input(prompt).lower()]
# Parameters
userName = ""
outPath = ""
yearMode = False

# Argument handling
#		0				1		2		3
#python letterboxd.py username outpath year?
ArgCount = len(sys.argv)

if(ArgCount >= 2):
	userName = str(sys.argv[1])
else:
	userName = input('Please enter a Username : ')
if(ArgCount >= 3):
	outPath = sys.argv[2]
else:
	outPath = input('Please enter an output file name : ')
if(ArgCount >= 4):
	yearMode = (sys.argv[3] == 'year')

# Find needed pages
pageList = []

if(yearMode):
	startYear = 1870				# the first year EVER
	endYear = date.today().year + 1	# It's conceivable user could see a prerelease/early screening for a film from next year)

	for i in range(startYear, endYear + 1):
		pageYear = Page('https://letterboxd.com/' + userName + '/films/year/' + str(i) + '/')
		pageYear.year = i
		pageList.append(pageYear)
else:
	firstPage = Page('https://letterboxd.com/' + userName + '/films/page/1/')	#open first page and read pagination section
	firstPage.Load()
	pageList.append(firstPage)
	
	pageDiscovery = firstPage.soup.find(class_='paginate-pages')	#find links in pagination section
	pageDiscoveryList = pageDiscovery.find_all('a')
	
	#find last page number
	pageCount = 0
	for pageID in pageDiscoveryList:		
		pageNumber = pageID.contents[0]
	pageCount = max(pageCount, int(pageNumber))
	
	#add range to search list
	for pageNum in range(2, pageCount + 1):
		pageTemp = Page('https://letterboxd.com/' + userName + '/films/page/' + str(pageNum) + '/')
		pageList.append(pageTemp)

#find films on pages
filmList = []

print('Reading...')
for i in range(0, len(pageList)):
	page = pageList[i]
	if page.ready == False:
		time.sleep(1)	# wait a bit for request
		page.Load()
	
	# read posters
	posterContainer = page.soup.find(class_='poster-list')
	if posterContainer:
		ratingList = posterContainer.find_all('li')		#	<li class="poster-container" data-owner-rating="0">
		nameList = posterContainer.find_all('img')		#	<img alt="John Wick: Chapter 2" class="image" height="105" src="https://s1.ltrbxd.com/static/img/empty-poster-70.8461d4ea.png" width="70"/>
		
		for film in range(0, len(nameList)):
			nameEntry = nameList[film]
			name = nameEntry.get('alt')
			name.encode('utf8')
			
			ratingEntry = ratingList[film]
			ratingData = ratingEntry.get('data-owner-rating')
			rating = int(ratingData)
			
			year = page.year;
			
			filmList.append(Film(name, rating, year))

	print(str(i + 1) + "/" + str(len(pageList)) + " " + page.url + " (" + str(len(filmList)) + " films discovered)")
# sort list alphabetically
filmList = sorted(filmList, key=lambda film: film.name)

# write out
f = open(outPath,'w',encoding='utf-8')
for film in filmList:
	yearString = ' '
	if(yearMode):
		yearString = ' (' + str(film.year) + ') '
	
	if(film.rating != 0):
		f.write(film.name + yearString + str(film.Stars()) + '\n')
	else:
		f.write(film.name + yearString + '\n')
f.close()
