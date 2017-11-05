import networkx as nx
import timeit
import SingleViewKernel as sg

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
#G_reply = nx.read_edgelist('/home/parul/repos/twitter_multi_view/reply.txt', nodetype=int)
#G_mention = nx.read_edgelist('/home/parul/repos/twitter_multi_view/mention.txt', nodetype=int)
#G_retweet = nx.read_edgelist('/home/parul/repos/twitter_multi_view/retweet.txt', nodetype=int)
#G_social = nx.read_edgelist('/home/parul/repos/twitter_multi_view/social1.txt', nodetype=int)
#G_social = add_edges_from(G_social, '/home/parul/repos/twitter_multi_view/social2.txt')

G = nx.gnm_random_graph(100,1000,directed=False)

print (sg.find_kernel(G))

stop = timeit.default_timer()

print (stop-start)

#outf = '/home/parul/repos/twitter_multi_view/reply.graphml'
#nx.write_graphml(G, outf)