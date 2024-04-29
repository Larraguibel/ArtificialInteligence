from itertools import combinations 
from sympy.logic.boolalg import And, Not, to_cnf 
from sympy.logic.inference import satisfiable  


def generate_subsets(belief_base, n):
    """
    Generate all subsets of a given size `n` from a belief base.
    
    Parameters:
        belief_base: The set of beliefs from which subsets are generated.
        n: The size of subsets to generate.
    
    Returns:
        A list of subsets of size `n`.
    """
    return list(combinations(belief_base, n))  # Return all subsets of size `n`


def generate_all_subsets(belief_base):
    """
    Generate all subsets of the belief base, excluding the empty set and the full set.
    
    Parameters:
        belief_base: The set of beliefs to generate subsets from.
    
    Returns:
        A list of all possible subsets from size 1 to size len(belief_base) - 1.
    """
    subsets = []  # Initialize an empty list to store subsets
    for n in range(1, len(belief_base) + 1):
        subsets.extend(generate_subsets(belief_base, n))  # Generate subsets of size `n` and add them to the list
    return subsets  # Return the complete list of subsets


def check_entailment(belief, belief_base):
    """
    Check whether a given belief is entailed by a belief base.
    
    Parameters:
        belief: The belief to check for entailment.
        belief_base: The belief base to check against.
    
    Returns:
        True if the belief base entails the belief, False otherwise.
    """
    cnf_belief = to_cnf(belief)  # Convert the given belief to Conjunctive Normal Form (CNF)
    belief_base_cnf = to_cnf(belief_base)  # Convert the belief base to CNF
    # Create a conjunction of the belief base with the negation of the given belief
    new_set = And(*belief_base_cnf, Not(cnf_belief))
    # If this new set is satisfiable, then the original belief is not entailed
    return not satisfiable(new_set)  # If not satisfiable, then entailment is true


def test_closure_contraction_bb(belief, belief_base):
    """
    Check for the closure property in a contracted belief base.
    
    Parameters:
        belief: The belief that was contracted.
        belief_base: The belief base after contraction.
    
    Assertion:
        Assert that the belief base does not entail the contracted belief.
    """
    # If the belief base still entails the contracted belief, closure is not satisfied
    assert not check_entailment(belief, belief_base), "Closure is not satisfied"


def test_inclusion_contraction_bb(initial_belief_base, belief_base):
    """
    Check for the inclusion property in a contracted belief base.
    
    Parameters:
        initial_belief_base: The original belief base before contraction.
        belief_base: The belief base after contraction.
    
    Assertion:
        Assert that the contracted belief base is a subset of the original base.
    """
    # The contracted belief base must be a subset of the original base
    assert belief_base.issubset(initial_belief_base), "Inclusion is not satisfied"


def test_success_contraction_bb(belief, belief_base):
    """
    Check for the success property in a contracted belief base.
    
    Parameters:
        belief: The belief that was contracted.
        belief_base: The belief base after contraction.
    
    Assertion:
        Assert that the contracted belief cannot be derived from the current belief base.
    """
    # If the belief base does not entail the contracted belief, then success is achieved
    assert not check_entailment(belief, belief_base), "Contraction did not succeed"
