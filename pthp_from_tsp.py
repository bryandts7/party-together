import networkx as nx
from mtsp_dp import mtsp_dp
from student_utils import *

def create_G_prime(G, nodes):
    G_prime = nx.complete_graph(nodes)
    for i in G_prime.nodes():
        for j in G_prime.nodes():
            if i != j:
                 G_prime[int(i)][int(j)]['weight'] = nx.shortest_path_length(G, int(i), int(j), 'weight')
    return G_prime

def create_php_tour(G, mtsp_tour):
    tour = [0]
    for i in range(len(mtsp_tour) - 1):
        path = nx.shortest_path(G, mtsp_tour[i], mtsp_tour[i+1], 'weight')
        tour += path[1:]
    return tour

def pthp_solver_from_tsp(G, H):
    """
    PTHP sovler via reduction to Euclidean TSP.
    Input:
        G: a NetworkX graph representing the city.\
        This directed graph is equivalent to an undirected one by construction.
        H: a list of home nodes that you must vist.
    Output:
        tour: a list of nodes traversed by your car.

    All nodes are reprented as integers.

    You must solve the question by first transforming a PTHP\
    problem to a TSP problem. After solving TSP via the dynammic\
    programming algorithm introduced in lectures, construct a solution\
    for the original PTHP problem.
    
    The tour must begin and end at node 0.
    It can only go through edges that exist in the graph..
    It must visit every node in H.
    """
    
    # reduction
    new_nodes = list(set([0] + H))
    G_prime = create_G_prime(G, new_nodes)
    mtsp_tour = mtsp_dp(G_prime)
    print(mtsp_tour)
    php_tour = create_php_tour(G, mtsp_tour)
    print(php_tour)
    return php_tour


if __name__ == "__main__":
    pass