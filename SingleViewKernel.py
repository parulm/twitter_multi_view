import networkx as nx
import numpy as np
from numpy.linalg import inv

def find_kernel(G):
	print ('Finding kernel...')
	
	#Parameters
	stop_prob = 0.1   # Stopping probability for each node
	r0 = stop_prob * stop_prob
	
	nodes = G.nodes()
	edges = G.edges()
	
	shape = (len(nodes), len(nodes))
	shapeT = (len(nodes) * len(nodes), len(nodes) * len(nodes))
	shapeR = (len(nodes)*len(nodes), 1)
	
	R0 = np.array([len(set.intersection(set(G.neighbors(x)), set(G.neighbors(y)))) / len(set.union(set(G.neighbors(x)), set(G.neighbors(y)))) for x in nodes for y in nodes])
	R0.shape = shape
	
	Pt = np.array([int(G.has_edge(x1, x)) * (1 - stop_prob) / len(G.neighbors(x)) for x in nodes for x1 in nodes])
	Pt.shape = shape
	
	
	r1 = np.array([sum([Pt[x1, x] * R0[x1, y1] * Pt[y1, y]  for x1 in nodes for y1 in nodes]) for x in nodes for y in nodes])
	r1.shape = shape

	T = np.array([Pt[x1, x] * R0[x1, z1] * Pt[z1, z] for x in nodes for z in nodes for x1 in nodes for z1 in nodes])
	T.shape = shapeT

	identity = np.eye(len(nodes) * len(nodes))
	H = identity - T

	r1.shape = shapeR
	
	K = np.matmul(inv(H),r1)
	
	'''
	factor1 = np.matmul(T, r1)
	#factor2 = np.matmul(T, factor1)
	#factor3 = np.matmul(T, factor2)
	
	K = r1 + factor1
	'''
	
	K.shape = shape
	return K


def IRWK(G):
	print ('Finding kernel by random walk...')
	
	#Parameters
	stop_prob = 0.1   # Stopping probability for each node
	trans_prob = 0.01  # Transition probability 
	r0 = stop_prob * stop_prob
	
	nodes = G.nodes()
	edges = G.edges()
	
	shape = (len(nodes), len(nodes))
	shapeT = (len(nodes) * len(nodes), len(nodes) * len(nodes))
	shapeR = (len(nodes)*len(nodes), 1)
	
	R0 = np.array([len(set.intersection(set(G.neighbors(x)), set(G.neighbors(y)))) / len(set.union(set(G.neighbors(x)), set(G.neighbors(y)))) for x in nodes for y in nodes])
	R0.shape = shape
	
	Pt = np.array([int(G.has_edge(x1, x)) * (1 - stop_prob) / len(G.neighbors(x)) for x in nodes for x1 in nodes])
	Pt.shape = shape
	
	
	r1 = np.array([sum([Pt[x1, x] * R0[x1, y1] * Pt[y1, y]  for x1 in nodes for y1 in nodes]) for x in nodes for y in nodes])
	r1.shape = shape

	T = np.array([Pt[x1, x] * R0[x1, z1] * Pt[z1, z] for x in nodes for z in nodes for x1 in nodes for z1 in nodes])
	T.shape = shapeT

	identity = np.eye(len(nodes) * len(nodes))
	H = identity - T
	
	R = R0
	R.shape = shapeR
	r1.shape = shapeR
	
	for i in range(10):
		R = r1 + np.matmul(T, R)
    
	K = R

	K.shape = shape
	return K


'''
# Test Case
G=nx.Graph()

G.add_nodes_from([1, 2, 3, 4, 5])
G.add_edges_from([(1,3),(1,4),(2,3),(3,4), (4,5)])
nodes = G.nodes()
edges = G.edges()
print find_kernel(G)
'''