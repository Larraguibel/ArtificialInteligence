from sympy.logic.boolalg import And, Not, Or, Implies, to_cnf  
from sympy import symbols  
import numpy as np  
from func import generate_all_subsets, check_entailment, test_closure_contraction, test_inclusion_contraction, test_success_contraction  

class BeliefBase:
    """
    A class representing a base of beliefs with contraction and expansion operations.
    Beliefs are maintained in Conjunctive Normal Form (CNF) for compatibility.
    """

    def __init__(self, atomic_symbols: str):
        """
        Initialize the belief base with a set for storing beliefs,
        and another for storing beliefs with priorities.
        """
        self.beliefs = set()  # Set to hold the beliefs
        self.beliefs_priorities = set()  # Set to hold beliefs with priorities
        self.symbols = symbols(atomic_symbols)  # Create symbols from input string
        self.priorities = {}  # Dictionary to track priority of each belief

    def expand(self, belief, priority):
        """
        Add a given belief to the belief base.
        Convert the belief to CNF for compatibility.
        Store the priority of the belief.
        """
        cnf_belief = to_cnf(belief)  # Convert the belief to CNF
        self.beliefs.add(cnf_belief)  # Add the belief to the set
        self.beliefs_priorities.add((cnf_belief, priority))  # Store the belief with its priority
        self.priorities[cnf_belief] = priority  # Keep track of priority in a dictionary

    def remove(self, belief, belief_set=None):
        """
        Remove a given belief from the belief base.
        Convert the belief to CNF before removal.
        If a specific belief_set is provided, remove from it.
        Otherwise, remove from the default belief set.
        """
        cnf_belief = to_cnf(belief)  # Convert the belief to CNF
        if belief_set is None:
            belief_set = self.beliefs  # Use the default belief set
        if cnf_belief in belief_set:
            belief_set.remove(cnf_belief)  # Remove the belief from the set

    def contract(self, extract_belief):
        """
        Contract the belief base by removing beliefs that entail the given belief.
        Contracting is done based on priorities to minimize impact.
        """
        initial_belief_base = self.beliefs.copy()  # Save the initial belief base
        
        while check_entailment(extract_belief, self.beliefs):
            entailed_formulas = []  # List to store subsets of beliefs that entail the given belief
            all_subsets = generate_all_subsets(self.beliefs)  # Generate all subsets of the belief base
            
            for subset in all_subsets:
                if check_entailment(extract_belief, set(subset)):  # Check if subset entails the belief
                    entailed_formulas.append(subset)  # Add to the list of entailed subsets
            
            # Find the subset with the highest priority for contraction
            lowest_priority = -np.inf  # Initialize with a very low value
            formula_to_remove = None  # Placeholder for the formula to be removed
            
            for sub_belief_set in entailed_formulas:
                for formula in sub_belief_set:
                    if self.priorities[formula] > lowest_priority:  # Find the highest priority
                        lowest_priority = self.priorities[formula]
                        formula_to_remove = formula
            
            self.remove(formula_to_remove)  # Remove the formula with the highest priority
        
        # Ensure the belief base satisfies contraction properties
        test_closure_contraction(extract_belief, self.beliefs)
        test_inclusion_contraction(initial_belief_base, self.beliefs)
        test_success_contraction(extract_belief, self.beliefs)

    def revise(self, belief):
        """
        Revise the belief base by first contracting and then expanding with the given belief.
        The contraction is done using Levi's identity, which requires removing the negation
        of the belief first.
        """
        self.contract(Not(belief))  # Contract by removing beliefs that entail the negation of the belief
        self.expand(belief)  # Expand by adding the given belief

    def __str__(self):
        return "{" + ", ".join(map(str, self.beliefs)) + "}"  # String representation of the belief base

    def __repr__(self):
        return "{" + ", ".join(map(str, self.beliefs)) + "}"  # Representation of the belief base

if __name__ == "__main__":
    # Create a belief base with specified atomic symbols
    belief_base = BeliefBase('p q')  
    p, q = belief_base.symbols  # Extract the symbols
    
    # Expand the belief base with some beliefs and their priorities
    belief_base.expand(p, 3)
    belief_base.expand(q, 2)
    belief_base.expand(Implies(p, q), 1)
    
    print("Initial belief base:")
    print(belief_base.beliefs)  # Display the current belief base
    
    # Contract the belief base by removing beliefs that entail 'q'
    print("\n Contraction with q\n")
    belief_base.contract(q)
    
    print("\n Belief base after contraction:")
    print(belief_base.beliefs)  # Display the final belief base after contraction
 
    print("\nRevision with q:")
    belief_base.revise(q)
    
    print("\n Belief base after revision:")
    print(belief_base.beliefs)