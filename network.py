mport networkx as nx
import sqlite3
import re
import json
import heapq

def make_network():

        G = nx.Graph()

        connection = sqlite3.connect("metadata.db")
        c = connection.cursor()

        to_from_info = c.execute("SELECT SENT_TO, SENT_FROM FROM MESSAGES")
        count = 0
        for email in to_from_info:
                count += 1
                if count % 10000 == 0:
                        print("{} Emails processed".format(count))
                to = process(email[0])
                frm = process(email[1])
                G.add_nodes_from(to)
                G.add_nodes_from(frm)
                if to != [] and frm != []: #Make sure valid sender and receiver(s) 
                        frm = frm[0]
                        for person in to:
                                try:
                                        G[frm][person]['weight'] += 1 #order doesn't matter for a nx object
                                except KeyError:
                                        G.add_edge(person, frm, weight = 1)
        return G

def save_ranks(G):
#'''
#given a graph
#gets the page rank for each node as a dictionary and
#saves it to ranks.json
#'''
        pr_dict = nx.pagerank(G, weight = 'weight')
        print("There are {} unique people in the graph".format(len(pr_dict.keys())))
        l = [('',0)]*10
        heapq.heapify(l)

        for node in pr_dict:
                min_person, min_rank = l[0]
                if pr_dict[node] > min_rank:
                        heapq.heapreplace(l, (node, pr_dict[node]))

        print(l)
        with open('ranks.json', 'w') as f:
                json.dump(pr_dict, f)


def process(s):
#'''
#Given a string containing all of the people an email was sent to or 
#the person who sent the email
#Returns a list of names that can be used directly in
#the networkx object
#'''
        people_list = re.findall('[A-Z][a-z]+ (?:[A-Z][ ])*[A-Z][a-z]+', s)
        return people_list

if __name__ == '__main__':
        graph = make_network()
        save_ranks(graph)
