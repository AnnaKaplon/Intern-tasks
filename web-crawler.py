from bs4 import BeautifulSoup
import requests

def site_map(url):
	global siteMap
	global basicURL
	
	SiteMap = {}
	bassicURL = url
	
	if url in map:
		pass
	else:
		pass

def get_content(url):
	soup = get_html(url)
	title = soup.
	aTagList = soup.find_all('a', href=True)
	
	refs = []
	for a in aTagList:
		if basicURL in a['href']:
			refs.append(a['href'])
	
	return title, refs

def get_html(url):
	"""
	Function reads html code out of given url, converts it into BeautifulSoup
	obejct and returns it.
	
	Arguments:
	url - url address
	"""
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	return soup
	
	