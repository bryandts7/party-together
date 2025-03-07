import networkx as nx
from itertools import combinations

def mtsp_dp(G):
    """
    TSP solver using dynamic programming.
    Input:
        G: a NetworkX graph representing the city.\
        This directed graph is equivalent to an undirected one by construction.
    Output:
        tour: a list of nodes traversed by your car.

    All nodes are reprented as integers.

    You must solve the problem using dynamic programming.
    
    The tour must begin and end at node 0.
    It can only go through edges that exist in the graph..
    It must visit every node in G exactly once.
    """
    n = G.number_of_nodes()
    nodes = list(G.nodes())
    edge_weight = {}
    for u in nodes:
        for v in nodes:
            if u != v:                
                edge_weight[(u, v)] = G[u][v]['weight']
    edge_weights = [[0]*(n+1)] + [[0]+[edge_weight[(nodes[u], nodes[v])] if u != v else 0 for v in range(n)] for u in range(n)]
    
    print(edge_weights)
   
    memo = [[-1]*(1 << (n+1)) for _ in range(n+1)]
    
    global path
    path = []
 
    def fun(i, mask):
        # base case
        # if only ith bit and 1st bit is set in our mask,
        # it implies we have visited all other nodes already
        if mask == ((1 << i) | 3):
            return edge_weights[1][i]
    
        # memoization
        if memo[i][mask] != -1:
            return memo[i][mask]
    
        res = 10**9  # result of this sub-problem
        best_path = []
        # we have to travel all nodes j in mask and end the path at ith node
        # so for every node j in mask, recursively calculate cost of 
        # travelling all nodes in mask
        # except i and then travel back from node j to node i taking 
        # the shortest path take the minimum of all possible j nodes
        for j in range(1, n+1):
            if (mask & (1 << j)) != 0 and j != i and j != 1:
                old_res = res
                res = min(res, fun(j, mask & (~(1 << i))) + edge_weights[j][i])
                if res < old_res:
                    path.append(i)


        memo[i][mask] = res  # storing the minimum value
        return res
    
    
    # Driver program to test above logic
    ans = 10**9
    for i in range(1, n+1):
        # try to go from node 1 visiting all nodes in between to i
        # then return from i taking the shortest route to 1
        ans = min(ans, fun(i, (1 << (n+1))-1) + edge_weights[i][1])



    return path
        

# Example usage:
# Create a NetworkX graph representing the city
G = nx.Graph()
G.add_nodes_from(range(5))
G.add_edge(0, 1, weight=10)
G.add_edge(0, 2, weight=15)
G.add_edge(0, 3, weight=20)
G.add_edge(0, 4, weight=25)
G.add_edge(1, 2, weight=35)
G.add_edge(1, 3, weight=25)
G.add_edge(1, 4, weight=30)
G.add_edge(2, 3, weight=30)
G.add_edge(2, 4, weight=35)
G.add_edge(3, 4, weight=40)

# Solve TSP using dynamic programming
tour = mtsp_dp(G)
print("Optimal tour:", tour)