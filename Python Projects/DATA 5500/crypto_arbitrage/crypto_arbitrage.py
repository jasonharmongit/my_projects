import requests
import json
import time
from datetime import datetime, timedelta
from itertools import permutations
import networkx as nx
from networkx.classes.function import path_weight
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# start timer (for fun :))
start_time = time.time()

# piece together url with all the names and ids of desired coins
ids = 'bitcoin,ethereum,eos,ripple,bitcoin-cash,litecoin,cardano'
vs_currencies = 'btc,eth,eos,xrp,bch,ltc,ada'
url1 = "https://api.coingecko.com/api/v3/simple/price?ids="
url2 = "&vs_currencies="
url = url1 + ids + url2 + vs_currencies

# load json into a dictionary
request = requests.get(url)
dct1 = json.loads(request.text)

# put coin names and tickers into respective lists for iteration, initialize edges list
coins = ids.split(",")
tickers = vs_currencies.split(",")
edges = []

# for each coin, create edges to every ticker
for coin in coins:
    for ticker in tickers:
        try: # in case any of the coins or tickers don't exist in json
            edges.append((tickers[coins.index(coin)], ticker, dct1[coin][ticker]))
        except:
            print(coin, "to", ticker, "returned an error.")

# create graph object (g) and add weighted edges using a directive graph class from nx
g = nx.DiGraph()
g.add_weighted_edges_from(edges) 

# add nodes
for e in edges:
    g.add_edge(e[0], e[1], weight=e[2])

# define the layout of the graph
pos = nx.circular_layout(g)

# draw the nodes and edges of the graph
nx.draw_networkx_nodes(g, pos)
nx.draw_networkx_edges(g, pos)
nx.draw_networkx_edge_labels(g, pos, edge_labels={(u, v): d['weight'] for u, v, d in g.edges(data=True)})
nx.draw_networkx_labels(g, pos)

# show the plot
plt.savefig("/Users/jasonharmon/Documents/DATA 5500/covid/crypto_graph.png")

# initialize storage variables
greatest_weight = -99999999
greatest_path = []
lowest_weight = 99999999
lowest_path = []

for n1, n2 in permutations(g.nodes,2): # for each node pair:
    try: # if errors occur due to missing info
    
        print("---------------- paths from", n1, "to", n2, "----------------------")
        
        for path in nx.all_simple_paths(g, source=n1, target=n2): # for each possible path between the node pair:
            
            # factor in the weight of every edge in each path from n1 TO n2
            path_weight_to = 1
            for i in range(len(path)-1):
                # print("edge from",path[i],"to",path[i+1],": ",g[path[i]][path[i+1]]["weight"]) # un-comment to see each edge and its weight in the path
                path_weight_to *= g[path[i]][path[i+1]]["weight"]
            print("path to:", path, path_weight_to)
            
            # reverse the path direction
            path.reverse()
            
            # factor in the weight of every edge in each path FROM n2 to n1
            path_weight_from = 1
            for i in range(len(path)-1):
                # print("edge from",path[i],"to",path[i+1],": ",g[path[i]][path[i+1]]["weight"]) # un-comment to see each edge and its weight in the path
                path_weight_from *= g[path[i]][path[i+1]]["weight"]
            print("path from:", path, path_weight_from)
            
            # calculate total weight factor of path by multiplying TO and FROM pathways
            path_weight_factor = path_weight_to * path_weight_from
            print("total path weight factor", path_weight_factor)
                
            # update mins and maxes, if necessary
            if path_weight_factor > greatest_weight:
                greatest_weight = path_weight_factor
                greatest_path = path
            elif path_weight_factor < lowest_weight:
                lowest_weight = path_weight_factor
                lowest_path = path
                
    except:
        pass
    
# make returns calculations (again, for fun XD)
end_time = time.time()
total_time = round((end_time - start_time),2)
p_returns = (greatest_weight - 1) * 100
p_returns = round(p_returns, 4)
d_returns_in_time = (1000 * (1 + p_returns)) - 1000
d_returns = d_returns_in_time * (60 / total_time)
d_returns = round(d_returns, 2)

# print results
print("\n----------------------------------------------\n")        
print("Greatest path",greatest_path, "at weight: ", greatest_weight)
print("Least path", lowest_path, "at weight: ", lowest_weight)
print("Percent Returns: ", p_returns, "% in ", total_time, " seconds.", sep="")
print("Per-Minute Dollar Returns on $1000: $", d_returns, sep="")
input("\n<PRESS ENTER TO END>")