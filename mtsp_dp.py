import networkx as nx

def mtsp_dp(G):
    """
    TSP solver using dynamic programming.
    Input:
        G: a NetworkX graph representing the city.
           This directed graph is equivalent to an undirected one by construction.
    Output:
        tour: a list of nodes traversed by your car.

    All nodes are represented as integers.

    The tour must begin and end at node 0.
    It can only go through edges that exist in the graph.
    It must visit every node in G exactly once.
    """

    # Number of nodes in the graph
    N = G.number_of_nodes()

    # Initialize dynamic programming table with infinity
    memo = [[float('inf')] * N for _ in range(1 << N)]

    # Initialize the starting point with zero cost
    memo[1][0] = 0

    # Create a list of nodes and edge weights
    nodes = list(G.nodes())
    edge = {(u, v): G[u][v]['weight'] for u in nodes for v in nodes if u != v}
    edge_weights = [[edge.get((nodes[u], nodes[v]), float('inf')) if u != v else 0 for v in range(N)] for u in range(N)]

    # Dynamic programming to compute the shortest paths
    for mask in range(1 << N):
        for u_idx in range(N):
            if mask & (1 << u_idx):
                for v_idx in range(N):
                    if u_idx != v_idx and not (mask & (1 << v_idx)):
                        new_mask = mask | (1 << v_idx)
                        new_cost = memo[mask][u_idx] + edge_weights[u_idx][v_idx]
                        memo[new_mask][v_idx] = min(memo[new_mask][v_idx], new_cost)

    # Find the minimum cost and the corresponding last node
    min_cost = float('inf')
    last_node = -1
    for i in range(1, N):
        cost = memo[(1 << N) - 1][i] + edge_weights[0][i]
        if cost < min_cost:
            min_cost = cost
            last_node = i

    # Reconstruct the tour
    tour = [0]
    mask = (1 << N) - 1
    while last_node != 0:
        tour.append(nodes[last_node])
        next_node = -1
        for v in range(N):
            if memo[mask][last_node] == memo[mask ^ (1 << last_node)][v] + edge_weights[last_node][v]:
                next_node = v
                break
        mask ^= (1 << last_node)
        last_node = next_node

    tour.append(0)

    return tour


# # Example usage:
# # Create a NetworkX graph representing the city
# G = nx.Graph()
# G.add_nodes_from(range(5))
# G.add_edge(0, 1, weight=10)
# G.add_edge(0, 2, weight=15)
# G.add_edge(0, 3, weight=20)
# G.add_edge(0, 4, weight=25)
# G.add_edge(1, 2, weight=35)
# G.add_edge(1, 3, weight=25)
# G.add_edge(1, 4, weight=30)
# G.add_edge(2, 3, weight=30)
# G.add_edge(2, 4, weight=35)
# G.add_edge(3, 4, weight=40)

# # Solve TSP using dynamic programming
# tour = mtsp_dp(G)
# print("Optimal tour:", tour)