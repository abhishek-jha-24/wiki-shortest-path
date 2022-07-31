from collections import deque
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
edges = open('myfile.txt', 'r')
Lines = edges.readlines()
print("creating graphs...")
for i in Lines:
	temp = i.split()
	temp = [int(x) for x in temp]
	if temp[0] in graph.keys():
		graph[temp[0]].append(temp[1])
	else:
		graph[temp[0]] = [temp[1]]
	if temp[1] in graph.keys():
		graph[temp[1]].append(temp[0])
	else:
		graph[temp[1]] = [temp[0]]

mapper = {}
maps = open('mapper.txt', 'r', encoding="utf-16")
Lines = maps.readlines()
count=0
print("preprocessing nodes...")
for i in Lines:
	temp = i.split()
	count+=1
	mapper[temp[0]] = int(temp[-1])


def bfs(source, destination):
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
source = "https://en.wikipedia.org/wiki/IETF_language_tag"
source = transform_link(source)
print("Modified source: ", source)
destination="https://en.wikipedia.org/wiki/Acad%C3%A9mie_des_Beaux-Arts"
destination = transform_link(destination)
print("Modified destination: ", destination)

print("The shortest path", bfs(source, destination))

