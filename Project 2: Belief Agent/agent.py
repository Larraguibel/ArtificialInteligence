from sympy.logic.boolalg import And, Not, Or, Implies, to_cnf
from sympy import symbols
import numpy as np
from func import generate_all_subsets, check_entailment, test_closure_contraction, test_inclusion_contraction, test_success_contraction

class BeliefBase:
    def __init__(self, atomic_symbols: str):
        
        "We initiate our belief set and our symbols."
        
        self.beliefs = set()
        self.beliefs_priorities = set()
        self.symbols = symbols(atomic_symbols)
        self.priorities = {}

    def expand(self, belief, priority):
        
        """
        Adds a given belief to the belief set. All beliefs are
        stored in there CNF form, to garantee compatibility between
        functions. It also saves the priorities in two different forms:
        as tuples in the form of (belief, its priority) and
        as a dictionary.
        """
        
        cnf_belief = to_cnf(belief)
        self.beliefs.add((cnf_belief))
        self.beliefs_priorities.add((cnf_belief, priority))
        self.priorities[cnf_belief] = priority

    def remove(self, belief, belief_set=None):
        
        """
        _summary_
        Convert the belief argument into CNF form, and removes it from the
        belief set if it is there.
        """
        
        cnf_belief = to_cnf(belief)
        if belief_set is None:
            if cnf_belief in self.beliefs:
                self.beliefs.remove(cnf_belief)
        else:
            if cnf_belief in belief_set:
                belief_set.remove(cnf_belief)

    def contract(self, extract_belief):
        """
        _summary_
        Contracts using priority
        
        Args:
            extract_belief: belief 
        """
        initial_belief_base = self.beliefs

        while check_entailment(extract_belief, self.beliefs):
            entailed_formulas = []
            all_subsets = generate_all_subsets(self.beliefs)
            for subset in all_subsets:
                if check_entailment(extract_belief, set(subset)):
                    entailed_formulas.append(subset)
            
            lowest_priority = - np.inf
            formula_to_remove = None
            for sub_belief_set in entailed_formulas:
                for formula in sub_belief_set:
                    if self.priorities[formula] > lowest_priority:
                        lowest_priority = self.priorities[formula]
                        formula_to_remove = formula
            self.remove(formula_to_remove)
        
        test_closure_contraction(extract_belief, self.beliefs)
        test_inclusion_contraction(initial_belief_base, self.beliefs)
        test_success_contraction(extract_belief, self.beliefs)

    def revise(self, belief):
        '''
        revise the belief by first contracting and efterwards expanding using levi's identity
        '''
        self.contract(Not(belief))
        self.expand(belief)


    def __str__(self):
        return "{" + ", ".join(map(str, self.beliefs)) + "}"

    def __repr__(self):
        return "{" + ", ".join(map(str, self.beliefs)) + "}"

""" if __name__ == "__main__":
    belief_base = BeliefBase('p q')
    p, q = belief_base.symbols
    # Expand belief base
    belief_base.expand(p, 1)
    belief_base.expand(Implies(p,q), 2)
    print(belief_base.beliefs)
    belief_base.contract(q)
    print(belief_base.beliefs)  """

if __name__ == "__main__":
    belief_base = BeliefBase('p q')  
    p, q = belief_base.symbols
    # Expand belief base
    belief_base.expand(p, 3)
    belief_base.expand(q, 2)
    belief_base.expand(Implies(p, q), 1)
    print(belief_base.beliefs)
    
    belief_base.contract(q)
    print("\nFinal belief base:")
    print(belief_base.beliefs) 