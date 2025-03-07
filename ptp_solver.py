import networkx as nx
from student_utils import *
from pthp_from_tsp import create_php_tour, create_G_prime
from mtsp_dp import mtsp_dp
import time, random


def tsp(G, H, num_visits):
    all_pair_shortest_path = dict(nx.floyd_warshall(G))

    dist_home = [(all_pair_shortest_path[0][home], home) for home in H]
    dist_home.sort()

    homes_to_visit = [home[1] for home in dist_home]
    nodes = list(set([0] + homes_to_visit[:num_visits]))
    G_prime = create_G_prime(G, nodes)
    mtsp_tour = mtsp_dp(G_prime)
    php_tour = create_php_tour(G, mtsp_tour)

    return php_tour[1:]

def random_tsp(G, H, num_visits):
    homes_to_visit = random.sample(H, num_visits)
    nodes = list(set([0] + homes_to_visit[:num_visits]))
    G_prime = create_G_prime(G, nodes)
    mtsp_tour = mtsp_dp(G_prime)
    php_tour = create_php_tour(G, mtsp_tour)

    return php_tour[1:]


def ptp_algo(G, H, alpha):
    shortest_paths = dict(nx.all_pairs_dijkstra_path_length(G))
    def cost(T):
        driving = 0
        for i in range(len(T)-1):
            if T[i+1] in G[T[i]]:
                driving += G[T[i]][T[i+1]]['weight']
            else:
                return float('inf')
        
        if T[0] in G[T[-1]]:
            driving += G[T[-1]][T[0]]['weight']
        else:
            return float('inf')

        walk = 0
        for h in H:
            closest_pickup = min(T, key=lambda x: shortest_paths[h][x])
            walk += shortest_paths[h][closest_pickup]
        return alpha * driving + walk
    
    
    best_tours = [(cost([0]), [0])]

    node_visit = len(H) if len(H) <= 10 else len(H)-2
    if len(H) >= 20:
        for i in range(2, node_visit + 1, 2):
            T = tsp(G, H, i)
            best_tours.append((cost(T), T))
    else:
        for i in range(1, node_visit + 1):
            T = tsp(G, H, i)
            best_tours.append((cost(T), T))
    it = 0
    num_it = 650


    while it < num_it:
        it += 1
        if random.random() <= 0.7:
            ran = random.random()
            if G.number_of_nodes() < 4 or ran < 0.3:
                T = [0]
            elif ran < 0.6:
                T = random_tsp(G, H, random.randint(1, min(len(H), 6)))
            else:
                T = [0]
                T.append(random.choice([j for j in G.neighbors(T[-1])]))
                if random.random() < 0.95:
                    x = random.choice([j for j in G.neighbors(T[-1])])
                    cnt = 0
                    max_cnt = random.randint(10, 15) if len(H) > 15 else 10
                    while x == 0 and cnt < max_cnt:
                        x = random.choice([j for j in G.neighbors(T[-1])])
                        cnt += 1
                        if cnt < max_cnt and (x not in T):
                            T.append(x)
                
                T += T[::-1]
        else:
            chosen_tour = []
            visited = set()
            for _cost, tour_k in best_tours:
                index = min(4, len(tour_k))
                subset = tuple(tour_k[:index])
                if subset not in visited:
                    chosen_tour.append((_cost, tour_k))
                    visited.add(subset)
            T = random.choice(chosen_tour)[1].copy()
        
        nodes = list(G.nodes())
        random.shuffle(nodes)

        changed = True
        first = True
        max_len = random.randint(len(T), len(T) + int((2 / alpha)))

        while (changed or first) and len(T) < max_len:
            changed = False
            ranges = [i for i in range(1, len(G.nodes()))]
            best_cost = cost(T)
            # ranges = ranges[:random.randint(len(ranges)//2, len(ranges) - 1)]
            for i in ranges:
                if i in T:
                    pos = T.index(i)
                    new_tour = T[:pos] + T[pos+1:]
                    new_cost = cost(new_tour)
                    if new_cost < best_cost:
                        T = new_tour
                        best_cost = new_cost
                        changed = True
                else:
                    best_pos = None
                    for j in range(len(T)):
                        best_tour = None
                        if (T[j],i) in G.edges():
                            new_tour = T[:j+1] + [i] + T[j+1:]
                            new_cost = cost(new_tour)
                            if new_cost < best_cost:
                                best_cost = new_cost
                                best_tour = new_tour[:]

                    if best_tour is not None:
                        T = best_tour
                        changed = True
            
            if changed == False:
                if not any(tour == T for _cost, tour in best_tours):
                    if len(best_tours) < 20:
                        best_tours.append((best_cost, T))
                    else:
                        worst_tour_idx = max(range(len(best_tours)), key=lambda idx: best_tours[idx][0])
                        if best_tours[worst_tour_idx][0] > best_cost:
                            best_tours[worst_tour_idx] = (best_cost, T)
                    best_tours.sort()
            if first:
                first = False
                changed = True
        
        best_cost = cost(T)
        if not any(tour == T for _cost, tour in best_tours):
            if len(best_tours) < 20:
                best_tours.append((best_cost, T))
            else:
                worst_tour_idx = max(range(len(best_tours)), key=lambda idx: best_tours[idx][0])
                if best_tours[worst_tour_idx][0] > best_cost:
                    best_tours[worst_tour_idx] = (best_cost, T)
            best_tours.sort()

        best_cost = cost(T)
        if not any(tour == T for _cost, tour in best_tours):
            if len(best_tours) < 20:
                best_tours.append((best_cost, T))
            else:
                worst_tour_idx = max(range(len(best_tours)), key=lambda idx: best_tours[idx][0])
                if best_tours[worst_tour_idx][0] > best_cost:
                    best_tours[worst_tour_idx] = (best_cost, T)
            best_tours.sort()

    best_tour = best_tours[0][1]
    print(best_tour)
    if best_tour[0] != 0:
        best_tour = [0] + best_tour
    if best_tour[-1] != 0:
        best_tour =  best_tour + [0]

    return best_tour



def ptp_solver(G:nx.DiGraph, H:list, alpha:float):
    """
    PTP sovler.
    Input:
        G: a NetworkX graph representing the city.\
        This directed graph is equivalent to an undirected one by construction.
        H: a list of home nodes that you must vist.
        alpha: the coefficient of calculating cost.
    Output:
        tour: a list of nodes traversed by your car.
        pick_up_locs_dict: a dictionary of (pick-up-locations, friends-picked-up) pairs\
        where friends-picked-up is a list/tuple containing friends who get picked up at\
        that sepcific pick-up location. Friends are represented by their home nodes.

    All nodes are reprented as integers.
    
    The tour must begin and end at node 0.
    It can only go through edges that exist in the graph..
    Pick-up locations must be in the tour.
    Everyone should get picked up exactly once
    """
    tour = ptp_algo(G, H, alpha)
    shortest_paths = dict(nx.floyd_warshall(G))
    pick_up_locs_dict = dict()
    for home in H:
        best_pickup = min(set(tour), key = lambda x: shortest_paths[home][x])
        pick_up_locs_dict.setdefault(best_pickup, []).append(home)
    
    return tour, pick_up_locs_dict


if __name__ == "__main__":
    pass
