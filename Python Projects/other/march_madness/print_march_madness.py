"""
May, 2023
A project built for one of the Python courses I took at USU. I wanted to use predictions made by the winner of the 2023 NCAA Men's 
March Madness Kaggle competition to actually build out a visual bracket. This was the first time I used recursion in a (somewhat) 
practical application. To accomplish this, I recursively created a hierarchy of "Team" objects to populate a binary search tree,
used networkx to turn that into a directed graph, then visualized it with matplotlib.
"""

from full_print_tree import *
import json
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

class Node:
    def __init__(self, team1, team2, pred, label_pred):
        self.team1 = team1
        self.team2 = team2
        self.pred = pred
        self.left = None
        self.right = None
        self.winner = None
        self.label_pred = label_pred
        
class Team:
    def __init__(self, name, seed, pair, tid, rid):
        self.name = name
        self.seed = seed
        self.pair = pair
        self.tid = tid
        self.rid = rid

south_teams = ["Alabama", "Arizona", "Baylor", "Virginia", "San Diego St", "Creighton", "Missouri", "Maryland", "West Virginia", "Utah St", "NC State", "Charleston So", "Furman", "UC Santa Barbara", "Princeton", "Texas A&M"]  
east_teams = ["Purdue", "Marquette", "Kansas St", "Tennessee", "Duke", "Kentucky", "Michigan St", "Memphis", "FL Atlantic", "USC", "Providence", "Oral Roberts", "Louisiana", "Montana St", "Vermont", "F Dickinson"]
midwest_teams = ["Houston", "Texas", "Xavier", "Indiana", "Miami FL", "Iowa St", "Texas A&M", "Iowa", "Auburn", "Penn St", "Pittsburgh", "Drake", "Kent", "Kennesaw", "Colgate", "N Kentucky"]
west_teams = ["Kansas", "UCLA", "Gonzaga", "Connecticut", "St Mary's CA", "TCU", "Northwestern", "Arkansas", "Illinois", "Boise St", "Arizona St", "VCU", "Iona", "Grand Canyon", "UNC Asheville", "Howard"]
regions = [south_teams, east_teams, midwest_teams, west_teams]

data_filepath = ''
preds_dct = json.load(open(data_filepath + '/preds.json', 'r'))
team_ids_dct = json.load(open(data_filepath + '/team_ids.json', 'r'))
all_teams_dct = {}

rid = 1
for region in regions:
    seed = 1
    pair = 16
    for team in region:
        all_teams_dct[str(rid) + "_" + str(seed)] = Team(team, seed, pair, team_ids_dct[team], rid)
        seed += 1
        pair -= 1
    rid += 1
    
teams_in_order = {}
matchup_order = [1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15]

for rid in range(1,5):
    for seed in matchup_order:
        teams_in_order[str(rid) + "_" + str(seed)] = all_teams_dct.pop(str(rid) + "_" + str(seed))
        

root = Node(None, None, None, None)
edges = []
teams_list = list(teams_in_order.keys())


def pop_bracket(node, depth):
    if depth == 0:
        team1 = teams_in_order.pop(list(teams_in_order.keys())[0])
        team2 = teams_in_order.pop(list(teams_in_order.keys())[0])
        node.team1 = team1
        node.team2 = team2
        dec_pred = preds_dct[str(team1.tid) + "_" + str(team2.tid)]
        pct_pred = round(dec_pred * 100, 2)
        label_pred = str(pct_pred) + "%"
        node.pred = dec_pred
        node.label_pred = label_pred
        
    else:
        node.left = pop_bracket(Node(None,None,None,None), depth-1)
        node.right = pop_bracket(Node(None,None,None,None), depth-1)
        
    return node
        
pop_bracket(root, 5)
pos = {}
labels = {}
last_width = {5:0, 4:0, 3:0, 2:0, 1:0, 0:0}
full_width = 150
full_height = 30
def fill_bracket(node, depth=0):
    # base case
    if node.pred is not None:
        if node.pred > 0.5:
            node.winner = node.team1
        else:
            node.winner = node.team2
            
        last_width[depth] += full_width / (2 ** depth + 1)
        x = last_width[depth]
        y = full_height - (depth * 5)
        pos[node] = (x, y)
        
        labels[node] = node.team1.name + " v. " + node.team2.name
        
        return node
    
    # recursive logic
    else:
        fill_bracket(node.left, depth+1)
        fill_bracket(node.right, depth+1)
        node.team1 = node.left.winner
        node.team2 = node.right.winner
        dec_pred = preds_dct[str(node.team1.tid) + "_" + str(node.team2.tid)]
        pct_pred = round(dec_pred * 100, 2)
        label_pred = str(pct_pred) + "%"
        node.pred = dec_pred
        node.label_pred = label_pred
        
        if node.pred > 0.5:
            node.winner = node.team1
        else:
            node.winner = node.team2
            
        edges.append((node.left, node, node.left.label_pred))
        edges.append((node.right, node, node.right.label_pred))
        
        last_width[depth] += full_width / (2 ** depth + 1)
        x = last_width[depth]
        y = full_height - (depth * 5)
        pos[node] = (x, y)
        
        labels[node] = node.team1.name + " v. " + node.team2.name
        
        return node
    
fill_bracket(root)

g = nx.DiGraph()
g.add_weighted_edges_from(edges)
plt.figure(figsize=(full_width, full_height))
nx.draw_networkx(g, pos, labels=labels)
edge_labels = nx.get_edge_attributes(g,'weight')
nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
filepath = ''
plt.savefig(filepath + "/full_bracket.png")

print("Predicted championship:", root.team1.name, "vs", root.team2.name)
print("Predicted winner:", root.winner.name)
