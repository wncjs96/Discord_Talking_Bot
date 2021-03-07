import urllib
import requests
from bs4 import BeautifulSoup
import os

def create_folder(dir_name):
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)
	return dir_name

# Given keyword, download images
def google_image_search(keyword):
	# create dir named after keyword
	dir_name = create_folder(keyword)

	keyword = urllib.parse.quote(keyword)
	print('url encoded keyword: ' + keyword)
	query = 'https://www.google.com/search?q=' + keyword + '&newwindow=1&rlz=1C1CHBF_enUS744US744&sxsrf=ALeKk03k7eEOKl_UVfwDw41fo7C5m6U1ng:1615046997912&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjlmez0hpzvAhVaTTABHR4ODuMQ_AUoAXoECBYQAw&biw=1920&bih=937'
	reply = requests.get(query)
	soup = BeautifulSoup(reply.content)
	results = soup.findAll('img')
	
	count = 1
	for result in results:
		file_name = dir_name + '/' + str(count) + '.png'
		try:
			urllib.request.urlretrieve(results[count]['src'], file_name)
			count = count + 1
			print('Downloaded file: ' + file_name)
		except:
			print('Download Failed')
	return count

def main():
	keyword = input("Write down the keyword for google image search:- ")
	# google_image_search to download
	google_image_search(keyword)
	return
	

if __name__ == '__main__':
	main()
	

