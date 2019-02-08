from bs4 import BeautifulSoup
import requests

def site_map(url):
	global siteMap
	global basicURL
	
	def create_site_map(url):
		if url in siteMap:
			pass
		else:
			title, refs = get_content(url)
			add_to_map(url, title, refs)
			for ref in refs:
				create_site_map(ref)
	
	siteMap = {}
	bassicURL = url
	create_site_map(url)
	return siteMap

def get_content(url):
	soup = get_html(url)
	title = soup.title.string
	aTagList = soup.find_all('a', href=True)
	
	refs = set()
	for a in aTagList:
		ref = a['href']
		if basicURL in ref:
			refs.add(ref)
		elif 'http' not in ref:
			refs.add(url + ref)
	
	return title, refs

def add_to_map(url, title, refs):
	siteMap[url] = {}
	siteMap[url]['title'] = title
	siteMap[url]['links'] = refs

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
	print(site_map('http://0.0.0.0:8000/'))
	