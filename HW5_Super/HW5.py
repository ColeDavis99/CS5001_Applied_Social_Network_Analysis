import networkx as nx
import matplotlib.pyplot as plt
import math
import community
from networkx.algorithms.community import centrality as c
from collections import defaultdict
from neo4j import GraphDatabase

#Uses Matplotlib library to output the graph it is passed
def drawGraph(g):
	pos = nx.spring_layout(g)
	plt.figure(figsize=(10,10))
	nx.draw_networkx(g, pos=pos, with_labels=True)
	plt.axis('off')
	plt.show()

#Returns the average degree of all nodes in a graph
def AverageDegree(g):
    degreeSum = 0
    for node in g:
        degreeSum += g.degree[node]
    print("Average Degree: ", degreeSum/len(g.nodes))

#Returns cleaned up name of a node. Replace spaces with underscores, and remove all commas, and append "_GROUP"
def cleanNodeName(n):
    newName = ""
    for char in n:
        if(char == ","):
            newName += ""
        elif(char == ";"):
            newName += ""
        elif(char == " "):
            newName += "_"
        else:
            newName += char
    newName += "_GROUP"

    return newName

'''
------------------------------------------------------------------------------------------------------------------------------------------------------------
'''


#Read in Data from file
G = nx.readwrite.edgelist.read_edgelist("clean_data.csv", delimiter=",")

#STEP 1
print("Number of nodes: ", end=" ")
print(len(list(G.nodes)))
print("Number of edges: ", end=" ")
print(len(list(G.edges)))
AverageDegree(G)





#STEP 2 Use the Louvain method to partition the nodes into communities. Output the number of communities found and the modularity of the partitioning.
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

print("\nThere are " + str(numPartitions+1) + " communities using the Louvain method.")
print("The modularity of the Louvain partitioning is " + str(modularity))





#STEP 3 Perform blockmodeling on the graph based on the Louvain partitioning from step2. Output the number of nodes, number of edges, and average degree in the blocked graph.
d = partition
result = defaultdict(list)
for key, val in sorted(d.items()):
    result[val].append(key)

blocks = []
for i in result:
    blocks.append(result[i])

exec(open("blockmodel.py").read())
blockedGraph=blockmodel(G, blocks)
# drawGraph(blockedGraph)

print("\nBlocked graph has " + str(len(list(blockedGraph.nodes()))) + " nodes.")
print("Blocked graph has " + str(len(list(blockedGraph.edges()))) + " edges.")
AverageDegree(blockedGraph)





#STEP 4 
#For each Louvain community, find the node with the highest degree

#Keys are 0,1,2,...25 and values are a list of the nodes in that community
communityDict = dict()
maxDegNodePerCommunity = dict()
keyList = list(range(numPartitions+1))
print(keyList)

#Initialize dicts with the community ID
for key in keyList:
    communityDict[key] = list()
    maxDegNodePerCommunity[key] = ""

#Populate the dict with node names, according to which community Louvaine partitioned them to
for node in partition:
    communityDict[partition[node]].append(node)

#Store the name of the largest degree node per community
maxNodeDeg = -1
for community in communityDict.keys():
    for node in communityDict[community]:
        if(G.degree[node] > maxNodeDeg):
            maxNodeDeg = G.degree[node]
            maxDegNodePerCommunity[community] = node
    maxNodeDeg = -1

#Prepare the dictionary to re-name the supernodes to the node with the highest degree in that community
nameMapping = dict()
for key in keyList:
    nameMapping[key] = cleanNodeName(maxDegNodePerCommunity[key])

#Relabel the nodes in the blocked graph
nx.relabel_nodes(blockedGraph, nameMapping, copy=False)
# drawGraph(blockedGraph)





#STEP 5
#Write out CSV so neo4j can import it. Also, manually put these headers at top of the csv file: supernode1,supernode2. 
contents = ""
nx.readwrite.edgelist.write_edgelist(blockedGraph, "C:/Users/Cole/.Neo4jDesktop/relate-data/dbmss/dbms-c8b10dae-58ca-4177-a7a0-55cf4c1fa27b/import/blocked_graph.csv", delimiter=",", encoding='utf-8', data=False)

fin = open("C:/Users/Cole/.Neo4jDesktop/relate-data/dbmss/dbms-c8b10dae-58ca-4177-a7a0-55cf4c1fa27b/import/blocked_graph.csv", "r")
for line in fin:
    contents += line
fin.close()

fout = open("C:/Users/Cole/.Neo4jDesktop/relate-data/dbmss/dbms-c8b10dae-58ca-4177-a7a0-55cf4c1fa27b/import/blocked_graph.csv", "w")
fout.write("supernode1,supernode2\n" + contents)
fout.close()

#Get API set up
uri = "bolt://127.0.0.1:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "cali"), max_connection_lifetime=1000)
session = driver.session()

#Clean slate neo4j
session.run('''
    MATCH (n)
    DETACH DELETE n
    ''')

#Create the new graph database via neo4j API by reading in the exported .csv file
session.run('''
    LOAD CSV WITH HEADERS FROM 'file:/blocked_graph.csv' AS row

    CREATE(sn1:Node {name: row.supernode1})
    CREATE(sn2:Node {name: row.supernode2})

    MERGE(sn1)-[:KNOWS]-(sn2)
    ''')

#Merge nodes together that are named the same
result = session.run('''
    MATCH (n:Node)
    WITH n.name AS name, COLLECT(n) AS nodelist, COUNT(*) AS count
    WHERE count > 1
    CALL apoc.refactor.mergeNodes(nodelist) YIELD node
    RETURN *    
    ''')

session.close()
driver.close()