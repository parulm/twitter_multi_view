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

def IRWKV(G1, G2, G3, G4):
    print ('Finding kernel by random walk...')
    #Parameters
    stop_prob = 0.1   # Stopping probability for each node
    trans_prob = 0.01  # Transition probability
    r0 = stop_prob * stop_prob
    views = 3

    nodes1 = G1.nodes()
    nodes2 = G2.nodes()
    nodes3 = G3.nodes()
    nodes4 = G4.nodes()


    shape = (len(nodes1), len(nodes1))
    shapeT = (len(nodes1) * len(nodes1), len(nodes1) * len(nodes1))
    shapeR = (len(nodes1)*len(nodes1), 1)

    R01 = np.array([(len(set.intersection(set(G1.neighbors(x)), set(G1.neighbors(y))))+1) /
      len(set.union(set(G1.neighbors(x)), set(G1.neighbors(y))))
      for x in nodes1 for y in nodes1])
    R01.shape = shape

    Pt1 = np.array([((int(G1.has_edge(x1, x)) * (1 - stop_prob - trans_prob * (views - 1)))+1) / (len(G1.neighbors(x))+1)
      for x in nodes1 for x1 in nodes1])
    Pt1.shape = shape


    r11 = np.array([sum([Pt1[x1, x] * R01[x1, y1] * Pt1[y1, y]  for x1 in nodes1 for y1 in nodes1])
        for x in nodes1 for y in nodes1])
    r11.shape = shape

    T1 = np.array([Pt1[x1, x] * R01[x1, z1] * Pt1[z1, z]
        for x in nodes1 for z in nodes1 for x1 in nodes1 for z1 in nodes1])
    T1.shape = shapeT




    R02 = np.array([(len(set.intersection(set(G2.neighbors(x)), set(G2.neighbors(y))))+1) /
      (len(set.union(set(G2.neighbors(x)), set(G2.neighbors(y))))+1)
      for x in nodes2 for y in nodes2])
    R02.shape = shape

    Pt2 = np.array([((int(G2.has_edge(x1, x)) * (1 - stop_prob - trans_prob * (views - 1)))+1) / (len(G2.neighbors(x))+1)
      for x in nodes2 for x1 in nodes2])
    Pt2.shape = shape


    r12 = np.array([sum([Pt2[x1, x] * R02[x1, y1] * Pt2[y1, y]  for x1 in nodes2 for y1 in nodes2])
        for x in nodes2 for y in nodes2])
    r12.shape = shape

    T2 = np.array([Pt2[x1, x] * R02[x1, z1] * Pt2[z1, z]
        for x in nodes2 for z in nodes2 for x1 in nodes2 for z1 in nodes2])
    T2.shape = shapeT


    R03 = np.array([(len(set.intersection(set(G3.neighbors(x)), set(G3.neighbors(y))))+1) /
      (len(set.union(set(G3.neighbors(x)), set(G3.neighbors(y))))+1)
      for x in nodes3 for y in nodes3])
    R03.shape = shape

    Pt3 = np.array([((int(G3.has_edge(x1, x)) * (1 - stop_prob - trans_prob * (views - 1)))+1) / (len(G3.neighbors(x))+1)
      for x in nodes3 for x1 in nodes3])
    Pt3.shape = shape


    r13 = np.array([sum([Pt3[x1, x] * R03[x1, y1] * Pt3[y1, y]  for x1 in nodes3 for y1 in nodes3])
        for x in nodes3 for y in nodes3])
    r13.shape = shape

    T3 = np.array([Pt3[x1, x] * R03[x1, z1] * Pt3[z1, z]
        for x in nodes3 for z in nodes3 for x1 in nodes3 for z1 in nodes3])
    T3.shape = shapeT


    R04 = np.array([(len(set.intersection(set(G4.neighbors(x)), set(G4.neighbors(y))))+1) /
      (len(set.union(set(G4.neighbors(x)), set(G4.neighbors(y))))+1)
      for x in nodes4 for y in nodes4])
    R04.shape = shape

    Pt4 = np.array([((int(G4.has_edge(x1, x)) * (1 - stop_prob - trans_prob * (views - 1)))+1) / (len(G4.neighbors(x))+1)
      for x in nodes4 for x1 in nodes4])
    Pt4.shape = shape


    r14 = np.array([sum([Pt4[x1, x] * R04[x1, y1] * Pt4[y1, y]  for x1 in nodes4 for y1 in nodes4])
        for x in nodes4 for y in nodes4])
    r14.shape = shape

    T4 = np.array([Pt4[x1, x] * R04[x1, z1] * Pt4[z1, z]
        for x in nodes4 for z in nodes4 for x1 in nodes4 for z1 in nodes4])
    T4.shape = shapeT



    R1 = R01
    R2 = R02
    R3 = R03
    R4 = R04

    R1.shape = shapeR
    R2.shape = shapeR
    R3.shape = shapeR
    R4.shape = shapeR

    r11.shape = shapeR
    r12.shape = shapeR
    r13.shape = shapeR
    r14.shape = shapeR

    for i in range(10):
        R1 = r11 + np.matmul(T1, R1) + trans_prob * R2 + trans_prob * R3 + trans_prob * R4
        R2 = r12 + np.matmul(T2, R2) + trans_prob * R1 + trans_prob * R3 + trans_prob * R4
        R3 = r13 + np.matmul(T3, R3) + trans_prob * R1 + trans_prob * R2 + trans_prob * R4
        R4 = r14 + np.matmul(T4, R4) + trans_prob * R1 + trans_prob * R2 + trans_prob * R3


    K1 = R1
    K2 = R2
    K3 = R3
    K4 = R4

    K1.shape = shape
    K2.shape = shape
    K3.shape = shape
    K4.shape = shape

    return [K1, K2, K3, K4]