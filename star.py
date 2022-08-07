from collections import deque



import pymongo

myclient = pymongo.MongoClient("mongodb+srv://dbAbhishekjha:dbPingofdeath01@abhishek-ow5k3.mongodb.net/test?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]
mycol_mapper = mydb["mapper"]
mycol_graph = mydb["graph"]

import math
import re
from collections import Counter


import requests
from bs4 import BeautifulSoup


from heapq import heapify, heappush, heappop



def scrape(url):
	try:
		return ""
		page = requests.get(url, timeout=2)

		soup = BeautifulSoup(page.content, "html.parser")
		for script in soup(["script", "style"]):
			script.extract()    # rip it out
		text = soup.get_text()
		
		lines = (line.strip() for line in text.splitlines())
		# break multi-headlines into a line each
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		  # drop blank lines
		text = ', '.join(chunk for chunk in chunks if chunk)
		text = text.replace(',', ' ')
		text = text.replace(',', '')
		punctuations = '''!()-[]{};:'"\,|<>./?@#$%^&*=_~'''

		# traverse the given string and if any punctuation
		# marks occur replace it with null
		for x in text.lower():
			if x in punctuations:
				text = text.replace(x, "")
		return text
	except:
		return ""



WORD = re.compile(r"\w+")


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)

def find_similarity(text1, text2):

	vector1 = text_to_vector(text1)
	vector2 = text_to_vector(text2)

	cosine = get_cosine(vector1, vector2)

	
	return 100-cosine







def transform_link(url):

	if url[-1] == "/":
		url = url[:-1]
	ans = ""
	for i in range(0, len(url)):
		if url[i] == "#":
			break
		ans += url[i]
	return ans

graph={}

print("Assigning ids to urls...")
mapper = {}
rev_mapper = {}
for x in mycol_mapper.find():

  name = x["name"]
  num_id = x["id"]
  mapper[name] = int(num_id)
  rev_mapper[int(num_id)] = name
 


print("creating graphs...")
for x in mycol_graph.find():
  
  s = int(x["from"])
  d = x["to"]
  for i in d:
  	i = int(i)
  	if s in graph.keys():
  		graph[s].append(i)
  	else:
  		graph[s] = [i]
  	if i in graph.keys():
  		graph[i].append(s)
  	else:
  		graph[i] = [s]




def bfs(source, destination):
	print("calculating the shortest path...")
	l = []
	heapify(l)
	
	k=0
	vis = set()
	if source not in mapper.keys() or destination not in mapper.keys():
		return "These nodes are not present"
	source = mapper[source]
	l.append((0, source))
	destination = mapper[destination]
	while(len(l) > 0):
		temp = len(l)
		for i in range(0, temp):
			curr=heappop(l)[1]
			curr_text = scrape(rev_mapper[curr])
			print(k)
			if curr == destination:
				print("...")
				return k
			if curr in graph.keys():
				for j in graph[curr]:
					if j not in vis:
						j_text = scrape(rev_mapper[j])
						vis.add(j)
						print("processing...")
						heappush(l, (find_similarity(curr_text, j_text), j))

		k+=1
	return k
source = "https://en.wikipedia.org/wiki/Tic-tac-toe"
source = transform_link(source)
print("Modified source: ", source)
destination="https://en.wikipedia.org/wiki/Coeur_d%27Alene_language"
destination = transform_link(destination)
print("Modified destination: ", destination)

print("The shortest path", bfs(source, destination))





















