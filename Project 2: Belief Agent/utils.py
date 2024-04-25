from itertools import combinations

def generate_subsets(belief_base, n):
    return list(combinations(belief_base, n))
