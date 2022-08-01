from collections import deque



import pymongo

myclient = pymongo.MongoClient("mongodb+srv://dbAbhishekjha:dbPingofdeath01@abhishek-ow5k3.mongodb.net/test?retryWrites=true&w=majority")
mydb = myclient["mydatabase"]
mycol_mapper = mydb["mapper"]
mycol_graph = mydb["graph"]


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
for x in mycol_mapper.find():

  name = x["name"]
  num_id = x["id"]
  mapper[name] = int(num_id)
 


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
	l = deque([])
	
	k=0
	vis = set()
	if source not in mapper.keys() or destination not in mapper.keys():
		return "These nodes are not present"
	source = mapper[source]
	l.append(source)
	destination = mapper[destination]
	while(len(l) > 0):
		temp = len(l)
		for i in range(0, temp):
			curr=l.popleft()

			if curr == destination:
				print("...")
				return k
			if curr in graph.keys():
				for j in graph[curr]:
					if j not in vis:
						vis.add(j)
						l.append(j)

		k+=1
	return k
source = "https://en.wikipedia.org/wiki/Tic-tac-toe"
source = transform_link(source)
print("Modified source: ", source)
destination="https://en.wikipedia.org/wiki/Coeur_d%27Alene_language"
destination = transform_link(destination)
print("Modified destination: ", destination)

print("The shortest path", bfs(source, destination))

