import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
import wikipedia
import urllib.request

#Builds entire graph, but then prunes it to nodes of degree >= 2. Also removes self edges.
def build_graph(SEED, depth, charLimit):

	#Ignore these wikipedia links (they're just extras)
	STOPS = ("International Standard Serial Number",
	"Issn (Identifier)",
	"International Standard Book Number", "Isbn (Identifier)",
	"International Standard Name Identifier", "Isni (Identifier)",
	"International Standard Book Number (Identifier)",
	"Pubmed Identifier", "Pubmed Central", "Viaf (Identifier)",
	"Ndl (Identifier)", "Gnd (Identifier)", "S2Cid (Identifier)",
	"Geographic Coordinate System", "Bibcode (Identifier)",
	"Digital Object Identifer","Doi (Identifier)", "Arxiv",
	"Wayback Machine", "Citeseerx (Identifier)",
	"Proc Natl Acad Sci Usa", "Bibcode (Identifier)",
	"Worldcat Identities (Identifier)",
	"Library of Congress Control Number", "Lccn (Identifier)", "Jstor")

	#Keep track of pages to process; we'll only do 2 layers
	#Process links as a breadth-first-search
	toDo_list = [(0,SEED)]
	toDo_set = set(SEED)
	done_set = set()

	#Create a directed graph
	F = nx.DiGraph()

	layer, page = toDo_list[0] #Initially, layer=0 and page=SEED


	#Loop through the Wikipedia articles and build the graph
	while layer <= depth:
		del toDo_list[0]
		done_set.add(page)
		print(layer, page)
		if((layer > 0) and (page > charLimit)):
			break #Enough already (only wikipedia pages between a and c)
		try:
			#Download the selected Wikipedia page
			wiki = wikipedia.page(page, auto_suggest=False)
		except:
			layer, page = toDo_list[0]
			print("Could not load page ", page)
			continue
		for link in wiki.links:	#Go through the links on that page
			link = link.title()
			if link not in STOPS and not link.startswith("List Of"):
				if link not in toDo_set and link not in done_set:
					toDo_list.append((layer+1, link))
					toDo_set.add(link)
				F.add_edge(page, link)
				print("Added link", link, "for page", page)
			if(len(toDo_list) == 0):
				print("toDo_list is empty")
				break
			layer, page = toDo_list[0]


	# Many Wikipedia pages exist under > 1 name (e.g., "KC Chief"
	# and "KC Chiefs") and one may redirect to the former;
	# the following will get rid of some "self loops"
	F.remove_edges_from(nx.selfloop_edges(F))


	# F is a pretty big graph!
	# We can make a smaller subgraph by only including nodes
	# that have degree >= 2
	core = [node for node, deg in dict(F.degree()).items() if deg >= 2]
	G = nx.subgraph(F, core)
	# G is a lot smaller (1k nodes, 2k edges)
	# print("{} nodes, {} edges".format(len(G), nx.number_of_edges(G)))

	return G


def DisplayGraph(G):
	# Display the smaller graph
	pos = nx.spring_layout(G)
	plt.figure(figsize=(15, 7))
	nx.draw_networkx(G, pos=pos, with_labels=True, font_color="green")
	plt.axis('off')
	plt.show()


def DisplayTopInDegreeSubjects(G):
	# Display a list of subjects sorted by in-degree
	top_indegree = sorted(dict(G.in_degree()).items(),reverse=True, key=itemgetter(1))[:100]
	print("\n".join(map(lambda t: "{} {}".format(*reversed(t)), top_indegree)))


def SimilarityRank(G):
	s = nx.algorithms.similarity.simrank_similarity(G)
	for key in s:
		for key2 in s[key]:
			if(s[key][key2] >= 0.015):
				print(key, "to", key2, ": ", s[key][key2])


def NodeIntersection(G_one, G_two):
	print()
	G1 = nx.DiGraph(G_one)
	G2 = nx.DiGraph(G_two)
	G1_Node_Removal = list()
	G2_Node_Removal = list()


	#Loop through G1's nodes and remove G1 nodes that are not found anywhere within G2
	for key in G1:
		if(key not in G2):
			#print(key, "is not in G2 so remove from G1")
			G1_Node_Removal.append(key)
	G1.remove_nodes_from(G1_Node_Removal)


	#Loop through G2's nodes and remove G2 nodes that are not found anywhere within G1
	for key in G2:
		if(key not in G1):
			#print(key, "is not in G1, so remove from G2")
			G2_Node_Removal.append(key)
	G2.remove_nodes_from(G2_Node_Removal)
 
	#print("{} nodes, {} edges".format(len(G1), nx.number_of_edges(G1)))
	#print("{} nodes, {} edges".format(len(G2), nx.number_of_edges(G2)))

	I = nx.intersection(G1, G2)
	print(type(I))
	print(nx.info(I))

#Builds core graph with no self loops and nodes with degree >= 2
R = build_graph("Rabbits (film)", 1, "C")
T = build_graph("Toototabon", 1, "C")
# DisplayGraph(R)
# DisplayTopInDegreeSubjects(R)
# SimilarityRank(R)


#New intersection of T and R graphs called I
NodeIntersection(T,R)


#DisplayGraph(T)
#DisplayGraph(R)


#print(list(T.edges)) #Prints out name of each edge
