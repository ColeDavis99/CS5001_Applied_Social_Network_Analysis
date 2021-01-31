import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
import wikipedia
import urllib.request


#Specify name of starting page
SEED = "Missouri S&T"

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
while layer <= 1:
	del toDo_list[0]
	done_set.add(page)
	print(layer, page)
	if((layer > 0) and (page > "C")):
		break #Enough already (only wikipedia pages between a and c)
	try:
		#Download the selected Wikipedia page
		wiki = wikipedia.page(page)
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


	
#Here's the graph we made (6k nodes, 8k edges; with depth 2)
print("{} nodes, {} edges". format(len(F),nx.number_of_edges(F)))	


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
print("{} nodes, {} edges".format(len(G), nx.number_of_edges(G)))


# Display the smaller graph
pos = nx.spring_layout(F) #G is the smaller graph (only deg >= 2)
plt.figure(figsize=(50,50))
nx.draw_networkx(G, pos=pos, with_labels=True)
plt.axis('off')
plt.show()

# Display a list of subjects sorted by in-degree
top_indegree = sorted(dict(G.in_degree()).items(),
reverse=True, key=itemgetter(1))[:100]
print("\n".join(map(lambda t: "{} {}".format(*reversed(t)), top_indegree)))



