from itertools import combinations
from sympy.logic.boolalg import And, Not, to_cnf
from sympy.logic.inference import satisfiable


def generate_subsets(belief_base, n):
    return list(combinations(belief_base, n))

def generate_all_subsets(belief_base):
    subsets = []
    for n in range(1, len(belief_base)):
        subsets.extend(generate_subsets(belief_base, n))
    return subsets

def check_entailment(belief, belief_base):
    '''
    The function check for entailment
    return true if beleif is entailed
    '''
    cnf_belief = to_cnf(belief)
    belief_base_cnf = to_cnf(belief_base)
    new_set = And(*belief_base_cnf, Not(cnf_belief))
    return not satisfiable(new_set)


def test_closure_contraction(belief, belief_base):
    '''
    The function check for closure
    Closure: The belief base should not entail the contracted belief after contraction
    '''
    assert not check_entailment(belief, belief_base), "Closure it not satisfied"

def test_inclusion_contraction(initial_belief_base, belief_base):
    '''
    The funnction check for inclusion
    Inclusion: The contracted belief base should be a subset of the original base
    '''
    assert belief_base.issubset(initial_belief_base), "Inclusion is not satisfied"

def test_success_contraction(belief, belief_base):
    '''
    The function check for succefull contraction
    Success: After contraction, the belief should not be derived
    '''
    assert not check_entailment(belief, belief_base), "Contraction is not succeeded"

