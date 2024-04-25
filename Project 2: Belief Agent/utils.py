from itertools import combinations
from math import factorial

def generate_subsets(n, belief_base):
    return list(combinations(belief_base, n))

def neighbours(beliefs: set):
    if len(beliefs) == 1:
        return None

    elif len(beliefs) > 1:
        neigh = []
        for clause in beliefs:
            new_set = beliefs.copy()
            new_set.remove(clause)
            neigh.append(new_set)
        return neigh

def create_graph(belief_set):
    graph = dict()
    total_nodes_in_max_depth = factorial(len(belief_set))
    counter = 0
    current_set = belief_set
    while counter <= total_nodes_in_max_depth:
        neigh = neighbours(current_set)
        if neigh is None:
            counter += 1
    
        else:
            graph[tuple(current_set)] = neigh
            counter += 1
            current_set = neigh  # Explore all neighbors
    print(f"Out of loop after {counter} iterations")
    return graph

