from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re

def site_map(url, siteMap={}, basicURL=''):
	url = delete_bookmark(url)
	if basicURL == '':
		basicURL = url
		
	title, refs = get_content(url,basicURL)
	if url not in siteMap:
		siteMap[url] = {}
		siteMap[url]['title'] = title
		siteMap[url]['links'] = refs
		
		for ref in refs:
			siteMap = site_map(ref, siteMap, basicURL)
			
	return siteMap

def get_content(url, basicURL):
	soup = get_html(url)
	title = soup.title.string
	return title, set(get_a_refs(soup, url, basicURL) + (get_area_refs(soup, url, basicURL)))
	
def get_a_refs(soup, url, basicURL):
	aTagList = soup.find_all('a', href=True)
	
	refs = []
	for a in aTagList:
		ref = a['href']
		if check_correctness(basicURL, ref):
			refs.append(urljoin(basicURL, delete_bookmark(ref)))
	return refs

def get_area_refs(soup, url, basicURL):
	areaTagList = soup.find_all('area', href=True)
	
	refs = []
	for area in areaTagList:
		ref = area['href']
		if len(soup.find_all('img', usemap='#'+area.parent['name'])) > 0:
			if check_correctness(basicURL, ref):
				refs.append(urljoin(basicURL, delete_bookmark(ref)))
	return refs

def check_correctness(basicURL, ref):
	if ref.startswith(basicURL):
		return True
	elif not ref.startswith('http'):
		return True
	return False

def delete_bookmark(url):
	match = re.search('#.+$', url)
	if match:
		return url[:match.start()]
	return url

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
	
if __name__ == '__main__':
	print(site_map('http://0.0.0.0:8000'))
	