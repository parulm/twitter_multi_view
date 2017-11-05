import networkx as nx
import timeit
import SingleViewKernel as sg

def network_intersection(G, H):
	Gnodes = set(list(G.nodes()))
	Hnodes = set(list(H.nodes()))
	cmnnodes = list(Gnodes & Hnodes)
	Gnew = G.subgraph(cmnnodes)
	Hnew = H.subgraph(cmnnodes)
	newnet = nx.intersection(Gnew, Hnew)
	return newnet

def add_edges_from(G, edgefile):
	efile = open(edgefile, 'r')
	for line in efile:
		split = line.split(' ')
		srcnd = int(split[0])
		endnd = split[1]
		if endnd[-1]=='\n':
			endnd = int(endnd[:-1])
		G.add_edge(srcnd, endnd)
	return G


G = nx.Graph()

start = timeit.default_timer()
G_reply = nx.read_edgelist('/home/parul/repos/twitter_multi_view/reply.txt', nodetype=int)
G_mention = nx.read_edgelist('/home/parul/repos/twitter_multi_view/mention.txt', nodetype=int)
G_retweet = nx.read_edgelist('/home/parul/repos/twitter_multi_view/retweet.txt', nodetype=int)
G_social = nx.read_edgelist('/home/parul/repos/twitter_multi_view/social1.txt', nodetype=int)
G_social = add_edges_from(G_social, '/home/parul/repos/twitter_multi_view/social2.txt')

G_rm = network_intersection(G_reply, G_mention)
G_rmr = network_intersection(G_rm, G_retweet)
G_final = network_intersection(G_rmr, G_social)
'''
rmrn = set(G_rmr.nodes())
rmre = set(G_rmr.edges())

socialn = set(G_social.nodes())
sociale = set(G_social.edges())

print rmrn<socialn
print rmre<sociale
'''
#print G_rmr.nodes()

#print nx.is_isomorphic(nx.union(G_rmr,G_social),G_social)

stop = timeit.default_timer()

print stop-start