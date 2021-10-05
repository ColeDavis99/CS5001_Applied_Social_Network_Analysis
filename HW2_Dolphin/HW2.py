import networkx as nx
import matplotlib.pyplot as plt
import math

def drawGraph(g):
	pos = nx.spring_layout(g)
	plt.figure(figsize=(10,10))
	nx.draw_networkx(g, pos=pos, with_labels=True)
	plt.axis('off')
	plt.show()

#Read in Data from file
DolphinGraph = nx.readwrite.gml.read_gml("dolphins.gml")	


#(1) Output Degree Stats
def DegreeOutput(g):
	#Init
	for node in g:	
		minDegree = g.degree[node]
		maxDegree = g.degree[node]
		degreeSum = 0
		break
	
	
	for node in g:
		if(g.degree[node] < minDegree):
			minDegree = g.degree[node]
		if(g.degree[node] > maxDegree):
			maxDegree = g.degree[node]
			
		degreeSum += g.degree[node]
	
	print("=============== #1 ===============")
	print("Max Degree: ", maxDegree)
	print("Min Degree: ", minDegree)
	print("Average Degree: ", degreeSum/len(g.nodes))
	
	
	
def CharacteristicPathLength(g):
	print("\n=============== #2 ===============")
	print("Average Shortest Path Length: ", nx.average_shortest_path_length(g))
	
def Diameter(g):
	print("\n=============== #3 ===============")
	print("Diameter: ", nx.diameter(g))
	
def CenterAndPeripheral(g):
	print("\n=============== #4 ===============")
	print("Center Nodes: ", nx.center(g))
	print("Peripheral Nodes: ", nx.periphery(g))

	
#I think you can calculate it if you take the entries in the apsp matrix (minus the ones along the diagonal), sort them, and take the average of the top 90%. Try that on the example we did in class.
def EffectiveEccentricity(g):
	print("\n=============== #5 ===============")
	totalDolphins = len(list(g.nodes))
	dolphinsToKeep = math.floor(totalDolphins * 0.9)

	#Calculate every shortest path for every dolphin
	spaths = dict(nx.all_pairs_shortest_path_length(g))

	paths = list()
	ctr = 0
	
	for node1 in spaths:
		for node2 in spaths[node1]:
			if(node1 != node2):
				paths.append(spaths[node1][node2])

	#Sort in descending order
	paths.sort(reverse=True)

	for i in range(len(paths)):
		if(paths[i] == 1):
			ctr = ctr+1

	#Keep top 90% highest values
	paths = paths[:math.floor(len(paths)*.9)]

	#Average of this list (consisting of top 90% of shortest path values)
	print("Effective Eccenctricity: ", sum(paths)/len(paths))
	
	
def Density(g):
	print("\n=============== #6 ===============")
	print("Density: ", nx.density(g))
	

def ClusterCoeff(g):
	'''A graph is small-worldif C is significantly higher than it would be for a random graph constructed on the same vertex set with approximately the same diameter'''
	c = nx.clustering(g)
	
	# compute overall coefficient
	sum = 0
	for x in c:
		sum = sum + c[x]
		
	print("\n=============== #7 ===============")
	print("Cluster Coefficient: ", sum/g.number_of_nodes())
	
	
def Transitivity(g):
	print("\n=============== #8 ===============")
	print("Transitivity: ", nx.transitivity(g))
	
	
def BetweennessCentrality(g):
	BC = nx.betweenness_centrality(g, normalized=True)
	node_color = [5000 * g.degree(v) for v in g]
	node_size = [v * 10000 for v in BC.values()]
	
	plt.figure(figsize=(20,20))
	nx.draw_networkx(g, with_labels=True, node_color=node_color, node_size=node_size, font_size=9, font_color="black")
	plt.axis('off')
	plt.show()
	
def EigenvectorCentrality(g):
	EC = nx.eigenvector_centrality(g)
	node_color = [5000 * g.degree(v) for v in g]
	node_size = [v * 6000 for v in EC.values()]
	
	plt.figure(figsize=(20,20))
	nx.draw_networkx(g, with_labels=True, node_color=node_color, node_size=node_size, font_size=9, font_color="black")
	plt.axis('off')
	plt.show()


def ClosenessCentrality(g):
	CC = nx.closeness_centrality(g)
	node_color = [5000 * g.degree(v) for v in g]
	node_size = [v * 3500 for v in CC.values()]
	
	plt.figure(figsize=(20,20))
	nx.draw_networkx(g, with_labels=True, node_color=node_color, node_size=node_size, font_size=9, font_color="black")
	plt.axis('off')
	plt.show()

							
#1-8 drivers
DegreeOutput(DolphinGraph)
CharacteristicPathLength(DolphinGraph)
Diameter(DolphinGraph)
CenterAndPeripheral(DolphinGraph)
EffectiveEccentricity(DolphinGraph)
Density(DolphinGraph)
ClusterCoeff(DolphinGraph)
Transitivity(DolphinGraph)

#9 Drivers
BetweennessCentrality(DolphinGraph)
EigenvectorCentrality(DolphinGraph)
ClosenessCentrality(DolphinGraph)

#drawGraph(DolphinGraph)









