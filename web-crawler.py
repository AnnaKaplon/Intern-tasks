from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import re

def site_map(url, siteMap={}, basicURL=''):
	"""
	Creates map of site as dictionary with urls (given url and its subpages) as keys 
	and another dictionaries containing data about particular url as values.
	Nested dictionary contains 'title' and 'links' keys which correspons to
	title of page and accessible links within given domain.
	
	url - url address of site to map
	siteMap (optional) - dictionary with part of map; if passed, function doesn't 
		create new map but expands this one
	basicURL (optional) - url in reference to which function search subpages;
		if not passed, url is basicURL
	"""
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
	"""
	Returns title of page and set of references from this page which are 
	subpages of given main url.
	
	Arguments:
	url - page url address
	basicURL - main url in relation to which we check if reference is a subpage
	"""
	soup = get_html(url)
	title = soup.title.string
	return title, set(get_a_refs(soup, url, basicURL) + (get_area_refs(soup, url, basicURL)))
	
def get_a_refs(soup, url, basicURL):
	"""
	Returns list of references from a tags from given page which are subpages
	of given main url.
	
	Arguments:
	soup - BeautifulSoup object representing url
	url - page url address
	basicURL - main url in relation to which we check if reference is a subpage
	"""
	aTagList = soup.find_all('a', href=True)
	
	refs = []
	for a in aTagList:
		ref = a['href']
		if check_correctness(basicURL, ref):
			refs.append(urljoin(basicURL, delete_bookmark(ref)))
	return refs

def get_area_refs(soup, url, basicURL):
	"""
	Returns list of references from area tags from given page which are subpages
	of given main url.
	
	Arguments:
	soup - BeautifulSoup object representing url
	url - page url address
	basicURL - main url in relation to which we check if reference is a subpage
	"""
	areaTagList = soup.find_all('area', href=True)
	
	refs = []
	for area in areaTagList:
		ref = area['href']
		if len(soup.find_all('img', usemap='#'+area.parent['name'])) > 0:
			if check_correctness(basicURL, ref):
				refs.append(urljoin(basicURL, delete_bookmark(ref)))
	return refs

def check_correctness(basicURL, ref):
	"""
	Returns True when given url is subpage of main url and False
	otherwise.
	
	Arguments:
	basicURL - main url in relation to which we check if ref is a subpage
	ref - checked url
	"""
	if ref.startswith(basicURL):
		return True
	elif not ref.startswith('http'):
		return True
	return False

def delete_bookmark(url):
	"""
	Checks if given url ends with bookmark, removes it if necessary and 
	returns url without bookmark.
	
	Arguments:
	url - url address
	"""
	match = re.search('#.+$', url)
	if match:
		return url[:match.start()]
	return url

def get_html(url):
	"""
	Reads html code out of given url, converts it into BeautifulSoup
	obejct and returns it.
	
	Arguments:
	url - url address
	"""
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')