from itertools import combinations

def generate_subsets(belief_base, n):
    return list(combinations(belief_base, n))

def generate_all_subsets(belief_base):
    subsets = []
    for n in range(len(belief_base)):
        subsets.append(*generate_subsets(belief_base, n))
    return subsets