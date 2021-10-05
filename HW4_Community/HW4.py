import networkx as nx
import matplotlib.pyplot as plt
import community
import math
import matplotlib.cm as cm
from networkx.algorithms.community import centrality as c

def drawGraph(g, node_colors=["Red"], with_labels=True):
	pos = nx.spring_layout(g)
	plt.figure(figsize=(10,10))
	nx.draw_networkx(g, pos=pos, with_labels=with_labels, node_color=node_colors)
	plt.axis('off')
	plt.show()

'''
################################################
Step 1:
Create and display graph
################################################'''
fin=open("GameOfThrones.txt", 'rb')
G = nx.read_edgelist('GameOfThrones.txt', nodetype=str, delimiter=",", data=(("weight", int),("season", int)))
fin.close()

drawGraph(G)


'''
################################################
Step 2 output:
a) No. of maximal cliques
b) Size of largest maximal clique
c) No. of maximal cliques of the largest size
##################################################'''
maxCliques = nx.find_cliques(G)
biggestClique = 0
numBiggestCliques = 0

ctr = 0
for clique in maxCliques:
	ctr += 1
	if(len(clique) > biggestClique):
		biggestClique = len(clique)	
	
print("Number of Maximal Cliques: " + str(ctr))
print("Size of Largest Maximal Clique: " + str(biggestClique))

#Could only loop through generator once, so just remake it
maxCliques = nx.find_cliques(G)
ctr=0
for clique in maxCliques:
	if(len(clique) == biggestClique):
		ctr += 1
print("Number of maximal cliques of largest size: " + str(ctr))


'''
################################################
Step 3 output:
a) No. of nodes in the main core
b) K-value that gives the main core
c) Display main core with nodes labeled
##################################################'''
mainCore = nx.k_core(G).nodes()
mainCoreEdges = nx.k_core(G).edges()
nodeCoreDict = nx.core.core_number(G)

print("\nNumber of nodes in main core: " + str(len(mainCore)))

maxKValue = 0
for node in nodeCoreDict:
	if(nodeCoreDict[node] > maxKValue):
		maxKValue = nodeCoreDict[node]
		
print("K value that gives the main core: " + str(maxKValue))

#Create subgraph that contains just the main core
coreGraph = nx.Graph()
for edge in mainCoreEdges:
	coreGraph.add_edge(edge[0], edge[1])
drawGraph(coreGraph)



'''
################################################
Step 4 output:
a) Number of nodes in the main crust
##################################################'''
print("\nNumber of nodes in the main crust: " + str(len(nx.k_crust(G).nodes())))


'''
################################################
Step 5 output:
a) Number of nodes in the k-corona where k is the max k-val (main core kval)
##################################################'''
print("\nNumber of nodes in the k-corona: " + str(len(nx.k_corona(G, k=maxKValue).nodes())))
coronaGraph = nx.Graph()
coronaEdges = nx.k_corona(G, k=maxKValue).edges()
for edge in coronaEdges():
	coronaGraph.add_edge(edge[0], edge[1])

drawGraph(coronaGraph)

'''
################################################
Step 6 output:
a) Number of nodes in the main shell
##################################################'''
mainShell = nx.k_shell(G).nodes()
mainShellEdges = nx.k_shell(G).edges()
print("\nNumber of nodes in main shell: " + str(len(mainShell)))

#Create subgraph that contains just the main shell
mainShellGraph = nx.Graph()
for edge in mainShellEdges:
	mainShellGraph.add_edge(edge[0], edge[1])
drawGraph(mainShellGraph)


'''
################################################
Step 7 output:
a) Display graph with red main core and blue main crust, no labels
##################################################'''
crustNodes = nx.k_crust(G).nodes()
coreNodes = mainCore
node_colors = list()

#Create color list for displaying the graph
for node in G.nodes():
	if node in coreNodes:
		node_colors.append("Red")
	else:
		node_colors.append("Blue")

drawGraph(G, node_colors, False)



'''
######################################################################################################################################
Step 8 output: Louvain Method
a) Output the number of communities, the size of largest community, size of smallest community, and modularity of this partitioning
######################################################################################################################################'''
partition = community.best_partition(G)
modularity = community.modularity(partition, G)


numPartitions = 0
populationList = dict()

#Loop through the Louvain partition
for node in partition:
	if(partition[node] > numPartitions):		#Get the number of partitions
		numPartitions = partition[node]

	if(partition[node] not in populationList):	#Count the number of people in each partition
		populationList[partition[node]] = 1
	else:
		populationList[partition[node]] += 1


#Loop through the population list of each community
maxPop = 0
minPop = len(list(G.nodes()))+1
for key in populationList:
	if(populationList[key] > maxPop):
		maxPop = populationList[key]
	if(populationList[key] < minPop):
		minPop = populationList[key]


print("\nThere are " + str(numPartitions) + " communities using the Louvain method.")
print("The smallest community has " + str(minPop) + " people.")
print("The largest community has " + str(maxPop) + " people.")
print("The modularity of the Louvain partitioning is " + str(modularity))


'''
#######################################################################
Step 9 output:
a) Display the Louvain graph color coded 
#######################################################################'''
color_list = list()
for node in G.nodes():
	if(partition[node] == 0):
		color_list.append("Red")
	elif(partition[node] == 1):
		color_list.append("Blue")
	elif(partition[node] == 2):
		color_list.append("Orange")
	elif(partition[node] == 3):
		color_list.append("Blue")
	elif(partition[node] == 4):
		color_list.append("Purple")
	elif(partition[node] == 5):
		color_list.append("Green")
	elif(partition[node] == 6):
		color_list.append("Brown")

drawGraph(G, color_list, False)


'''
#######################################################################
Step 10 output: Girvan-Newman
a) Output the number of communities, the size of largest community, size of smallest community, and modularity of this partitioning
#######################################################################'''
components = c.girvan_newman(G)
i=0
for row in components:
	if(i==0):
		finalResult = row
	# print(row)
	i += 1

minCommunity = len(list(G.nodes))+1
maxCommunity = 0
ctr = 0
partitions = dict()
L = list(finalResult)
p=0
for comp in L:
	for entry in comp:
		partitions[entry] = p
		ctr += 1
	if(ctr < minCommunity):
		minCommunity = ctr
	if(ctr > maxCommunity):
		maxCommunity = ctr
	p += 1
	ctr = 0


print("\nThere are " + str(p) + " communitites using the Girvan-Newman method.")
print("The smallest community has " + str(minCommunity) + " people.")
print("The largset community has " + str(maxCommunity) + " people.")
print("The modularity of the Girvan-Newman partitioning is " + str(community.modularity(partitions, G)))


'''
#######################################################################
Step 11 output:
a) The Girvan-Newman graph color coded
#######################################################################'''
color_list = list()
for node in G.nodes():
	if(partitions[node] == 0):
		color_list.append("Red")
	elif(partitions[node] == 1):
		color_list.append("Blue")

drawGraph(G, color_list, False)



# # 12 a code: 
# maxCliques = nx.find_cliques(G)

# for clique in maxCliques:
# 	if(len(clique) >= 10):
# 		for node in clique:
# 			print(node + "\t" + str(partition[node]))
# 		print("========")