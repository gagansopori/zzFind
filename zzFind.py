from bs4 import BeautifulSoup
import requests, urllib.request
import os, csv, re


class StarScraper:

	def get_models(user, header, endpoint):

		tempURIList = []
		new_endpoint = endpoint
		flag = True

		while(flag):

			modelURI = header + new_endpoint
			# Open Webpage
			try:
				main_page = urllib.request.urlopen(modelURI).read().decode('utf-8')
			except:
				print("Exception Occurred. Fix your code, or check if web-site is unavailable")
			
			# Soup-Object to store page data
			site_soup = BeautifulSoup(main_page,"lxml")
			models_container = site_soup.find("div", {"class": "model-card-container"})

			# Find Relevant Links in the object
			for link in models_container.find_all('h2'):
				tempURIList.append(link.find('a').get('href'))
			# Check for next page
			try:
				pathFinder = site_soup.find("li", {"class": "paginationui-nav next"})
			except:
				print("Done with Everything.")
			if (pathFinder):
				new_endpoint = pathFinder.find('a').get('href')
			
			# Check For the last page
			if(new_endpoint == endpoint):
				flag = False
				print("Reached the Last Page")
			else:
				new_endpoint = endpoint

			flag = False

		return tempURIList

	def get_profile(user, header, tempURIList, star_map):

		for items in tempURIList:
			stats_map = {}
			profileURI = zzHeadSecure + items
			try:
				profile_page = urllib.request.urlopen(profileURI)
			except:
				print("Can't Open Link. Check Code or URI")

			model_soup = BeautifulSoup(profile_page, "lxml")
			profile_container = model_soup.find("div", {"class": "profile-spec-list clearfix"})

			# Get Model Name
			model_name = model_soup.find("div", {"class": "model-profile-specs"}).find('h1').text.strip()

			# Get Model Details
			for details in profile_container.find_all("li",):
				stats_map[details.find('label').text] = details.find('var').text.strip().replace('                                        ,\n                                                                        \n                                        ', ', ')

			stats_map['Popularity Index'] = tempURIList.index(items)+1
			star_map[model_name] = stats_map

		return star_map




ss = StarScraper()
print("Starting")
# URIs
zzHead, zzHeadSecure = "http://www.brazzers.com", "https://www.brazzers.com"
URIList = []
female_map = {}
male_map = {}
resultMap = {}

# Endpoints
femaleEndPoint = "/pornstars/all-pornstars/female/all-categories/any/bypopularity/"
maleEndPoint = "/pornstars/all-pornstars/male/all-categories/any/bypopularity/"

# Get Female Data
URIList = ss.get_models(zzHead, femaleEndPoint)
resultMap['Females'] = ss.get_profile(zzHeadSecure, URIList, female_map)

# Get Male Data
URIList = ss.get_models(zzHead, maleEndPoint)
resultMap['Males'] = ss.get_profile(zzHeadSecure, URIList, male_map)

print(resultMap)
