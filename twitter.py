import networkx as nx
import timeit


start = timeit.default_timer()
G_reply = nx.read_edgelist('/home/parul/repos/twitter_multi_view/reply.txt', nodetype=int)
G_mention = nx.read_edgelist('/home/parul/repos/twitter_multi_view/mention.txt', nodetype=int)
G_retweet = nx.read_edgelist('/home/parul/repos/twitter_multi_view/retweet.txt', nodetype=int)
G_social = nx.read_edgelist('/home/parul/repos/twitter_multi_view/social.txt', nodetype=int)
stop = timeit.default_timer()

print stop-start

#outf = '/home/parul/repos/twitter_multi_view/reply.graphml'
#nx.write_graphml(G, outf)