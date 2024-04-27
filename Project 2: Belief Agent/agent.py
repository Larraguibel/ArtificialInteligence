from sympy.logic.boolalg import And, Not, to_cnf
from sympy import symbols
from sympy.logic.inference import satisfiable
from utils import generate_all_subsets
import numpy as np

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
        sorted_beliefs = sorted(self.beliefs_priorities, key=lambda x: (-x[1]))   
        while self.check_entailment(extract_belief):
            entailed_formulas = []
            all_subsets = generate_all_subsets(self.beliefs)
            for subset in all_subsets:
                if self.check_entailment(formula=extract_belief, belief_base=set(subset)):
                    entailed_formulas.append(subset)
            
            lowest_priority = - np.inf
            formula_to_remove = None
            for sub_belief_set in entailed_formulas:
                for formula in sub_belief_set:
                    if self.priorities[formula] > lowest_priority:
                        lowest_priority = self.priorities[formula]
                        formula_to_remove = formula
            self.remove(formula_to_remove)
                        
    def revise(self, belief):
        # Levi's identity
        self.contract(Not(belief))
        self.expand(belief)

    def check_entailment(self, formula, belief_base=None):
        if belief_base is None:
            cnf_formula = to_cnf(formula)
            belief_base_cnf = to_cnf(self.beliefs)
            new_set = And(*belief_base_cnf, Not(cnf_formula))
            return not satisfiable(new_set)
        else:
            cnf_formula = to_cnf(formula)
            belief_base_cnf = to_cnf(belief_base)
            new_set = And(*belief_base_cnf, Not(cnf_formula))
            return not satisfiable(new_set)         

    def __str__(self):
        return "{" + ", ".join(map(str, self.beliefs)) + "}"

    def __repr__(self):
        return "{" + ", ".join(map(str, self.beliefs)) + "}"