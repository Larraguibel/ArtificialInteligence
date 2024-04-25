from itertools import combinations

def generate_subsets(belief_base, n):
    return list(combinations(belief_base, n))

def generate_all_subsets(belief_base):
    subsets = []
    for n in range(1, len(belief_base)):
        subsets.extend(generate_subsets(belief_base, n))
    return subsets