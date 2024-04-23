# All functions for postulates and a functinos that check them all
# Extra functions (acts as utils.py)

from itertools import product

def generate_combinations(n):
    return list(product([True, False], repeat=n))