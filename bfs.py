from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re




def get_main_link(url):
	ans = ""
	for i in range(0, len(url)):
		if url[i] == "#":
			break
		ans += url[i]
	return ans



def get_next_nodes(url):

	req = Request(url)
	links = []
	try:
	
		html_page = urlopen(req)

		soup = BeautifulSoup(html_page, "lxml")
		for link in soup.findAll('a'):
			temp = link.get('href')
			
			try:
				if ".org" not in temp:
					temp = url[:24]+temp
				elif "https:" not in temp:
					temp = "https:" + temp
				else:
					pass
				if temp[-1] == "/":
					temp = temp[:-1]
				temp = get_main_link(temp)
				
				links.append(temp)
			except:
				pass
	except:
		pass
	
	return links




def find_path(source, destination):
	queue = []
	queue.append(source)
	k = 0
	while (len(queue) > 0):
		temp = len(queue)
		for i in range(0, temp):

			curr = queue.pop(0)
			if curr == destination:
				return k
			next_nodes = get_next_nodes(curr)

			for j in next_nodes:
				try:
					
					if j[0] != 'h':
						j = "https:"+j
					
					queue.append(j)
				except:
					pass
		k+=1
	return k


source = "https://en.wikipedia.org/wiki/Tic-tac-toe"
destination = "https://en.wikipedia.org/wiki/Game_complexity"

if destination[-1] == "/":
	destination = destination[:-1]


print("shortest path: ", find_path(source, destination))

