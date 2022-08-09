# Pip install waitress

from flask import Flask, render_template, request, make_response
#from waitress import serve
# from flask_mysqldb import MySQL


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'Students'

# mysql = MySQL(app)

import networkx as nx

from difflib import SequenceMatcher
from w3lib.url import canonicalize_url
from urllib.parse import urlparse
from pyvis.network import Network
import pandas as pd
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

graph={}

print("Assigning ids to urls...")
mapper = {}
rev_mapper = {}
vertices = 0
for x in mycol_mapper.find():

  name = x["name"]
  num_id = x["id"]
  mapper[name] = int(num_id)
  vertices = max(vertices, int(num_id))
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
  

def transform_link(url):

    if url[-1] == "/":
        url = url[:-1]
    ans = ""
    for i in range(0, len(url)):
        if url[i] == "#":
            break
        ans += url[i]
    return ans

got_net = Network(height='750px', width='100%', directed=True, bgcolor='#00ff1e', font_color='white')

# set the physics layout of the network
got_net.barnes_hut()


def compare_urls(url1, url2):
    url1 = canonicalize_url(url1)
    url2 = canonicalize_url(url2)
    url1_parsed = urlparse(url1)
    url2_parsed = urlparse(url2)
    domain = SequenceMatcher(None, url1_parsed.netloc, url2_parsed.netloc).ratio()
    path = SequenceMatcher(None, url1_parsed.path, url2_parsed.path).ratio()
    query = SequenceMatcher(None, url1_parsed.query, url2_parsed.query).ratio()
    print(domain+path+query)
    return 3-(domain+path+query)




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
    path = [-1 for i in range(vertices+1)]

    while(len(l) > 0):
        temp = len(l)
        flag=False
        for i in range(0, temp):
            curr=heappop(l)[1]
            
            print(k)
            if curr == destination:
                flag=True
            if curr in graph.keys():
                for j in graph[curr]:
                    if j not in vis:
                        path[j]=curr
                        vis.add(j)
                        heappush(l, (3*k+compare_urls(rev_mapper[curr], rev_mapper[j]), j))

        if flag:
            break
        k+=1
    route = set()
    while path[destination] != -1:
        print(destination)
        route.add(destination)
        if destination == 0:
            break 
        destination=path[destination]
    if path[destination] == -1:
        return [-1, route]
    else:
        return [k, route]





def do(path_find):
    vis = set()

    for k,v in graph.items():
        if k in vis:
            pass
        else:
            if k in path_find:
                
                got_net.add_node(rev_mapper[k], rev_mapper[k], title=rev_mapper[k], color="#162347")
            else:
                got_net.add_node(rev_mapper[k], rev_mapper[k], title=rev_mapper[k], color="#dd4b39")
            vis.add(k)
        for j in v:
            if j in vis:
                pass
            else:
                if j in path_find:
                    got_net.add_node(rev_mapper[j], rev_mapper[j], title=rev_mapper[j], color="#162347")
                else:
                    got_net.add_node(rev_mapper[j], rev_mapper[j], title=rev_mapper[j], color="#dd4b39")
                vis.add(j)
            if k in path_find and j in path_find:
                print("yes something happened")
                got_net.add_edge(rev_mapper[k], rev_mapper[j], value=1000,color="#162347")
            else:
                got_net.add_edge(rev_mapper[k], rev_mapper[j], value=400,color="#dd4b39")



    neighbor_map = got_net.get_adj_list()

    # add neighbor data to node hover data
    for node in got_net.nodes:
        node['title'] += ' Neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
        node['value'] = len(neighbor_map[node['id']])

    return got_net.show("./templates/gameofthrones.html")



@app.route("/")
@app.route('/home', methods=['GET', 'POST'])
def home():
    title = 'Home'
    return render_template('index.html', title=title)

@app.route('/graph', methods=['GET', 'POST'])
def okk():
    source = "https://en.wikipedia.org/wiki/Tic-tac-toe"
    source = transform_link(source)
    print("Modified source: ", source)
    destination="https://en.wikipedia.org/wiki/Knots_and_Crosses"
    destination = transform_link(destination)
    print("Modified destination: ", destination)
    # Put inputs to dataframe
    okk = bfs(source, destination)
    
    # Get prediction
    prediction = okk[0]
    print(okk)
    path_find = okk[1]
    do(path_find)

    return render_template("gameofthrones.html")



@app.route('/projects')
def projects():
    title = 'Projects'

    return render_template('projects.html',title=title)

@app.route('/blogs', methods=['GET', 'POST'])
def second():
    title = "Blogs"
    return render_template('blogs.html', title=title)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        userdetails = request.form
        fname = userdetails['fname']
        # cur = mysql.connection.cursor()
        # cur.execute("INSERT INTO student(idnum,name) VALUES(%i,%s)",(54252,'Testing1'))
        # mysql.connection.commit()
        # cur.close()
        # return "{name}"
    return render_template('contact.html')


if __name__ == '__main__':
    #serve(app, host="0.0.0.0", port=8080)
    app.run(debug=True)
