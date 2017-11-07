import networkx as nx
import numpy as np
from numpy.linalg import inv

def kernel_formula(G):
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
	
	#uncomment the following lines of code if you prefer an approximation over an exact solution
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


def multiview_IRWK(Garr):
	#input an array of graphs
	print ('Finding kernel by random walk...')
	#Parameters
	stop_prob = 0.1   # Stopping probability for each node
	trans_prob = 0.01  # Transition probability
	r0 = stop_prob * stop_prob
	views = len(Garr)

	nodes = []
	for G in Garr:
		nodes.append(G.nodes())

	shape = (len(nodes[0]), len(nodes[0]))
	shapeT = (len(nodes[0]) * len(nodes[0]), len(nodes[0]) * len(nodes[0]))
	shapeR = (len(nodes[0])*len(nodes[0]), 1)
	
	R0, Pt, r1, T = [None]*views, [None]*views, [None]*views, [None]*views
	
	for i in range(views):
		R0[i] = np.array([(len(set.intersection(set(Garr[i].neighbors(x)), set(Garr[i].neighbors(y))))+1) / (len(set.union(set(Garr[i].neighbors(x)), set(Garr[i].neighbors(y))))+1) for x in nodes[i] for y in nodes[i]])
		R0[i].shape = shape

		Pt[i] = np.array([((int(Garr[i].has_edge(x1, x)) * (1 - stop_prob - trans_prob * (views - 1)))+1) / (len(Garr[i].neighbors(x))+1) for x in nodes[i] for x1 in nodes[i]])
		Pt[i].shape = shape

		r1[i] = np.array([sum([Pt[i][x1, x] * R0[i][x1, y1] * Pt[i][y1, y]  for x1 in range(len(nodes[i])) for y1 in range(len(nodes[i]))]) for x in range(len(nodes[i])) for y in range(len(nodes[i]))])
		r1[i].shape = shape

		T[i] = np.array([Pt[i][x1, x] * R0[i][x1, z1] * Pt[i][z1, z] for x in range(len(nodes[i])) for z in range(len(nodes[i])) for x1 in range(len(nodes[i])) for z1 in range(len(nodes[i]))])
		T[i].shape = shapeT


	R = [None]*views

	for j in range(views):
		R[i].shape = shapeR
		r1[i].shape = shapeR

	for i in range(10):
		for k in range(views):
			restM = None
			restM.shape = shapeR
			for j in range(views):
				if k!=j:
					restM+=R[j]
			R[k] = r1[k] + np.matmul(T[k], R[k]) + trans_prob*restM

	K = [None]*views
	for i in range(views):
		K[i] = R[i]
		K[i].shape = shape

	
	return K