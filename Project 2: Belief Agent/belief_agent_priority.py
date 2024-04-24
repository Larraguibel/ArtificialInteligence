from sympy.logic.boolalg import And, Or, Not, Implies, Equivalent, to_cnf
from sympy import symbols
from sympy.logic.inference import satisfiable
from utils import generate_combinations

class BeliefBase:
    def __init__(self, atomic_symbols: str):
        self.beliefs = set()
        self.beliefs_priorities = set()
        self.symbols = symbols(atomic_symbols)
        self.possible_symbol_values = generate_combinations(len(self.symbols))
        self.priorities = {}

    def expand(self, belief, priority):
        cnf_belief = to_cnf(belief)
        self.beliefs.add((cnf_belief))
        self.beliefs_priorities.add((cnf_belief, priority))
        self.priorities[belief] = priority

    def remove(self, belief, belief_set=None):
        cnf_belief = to_cnf(belief)
        if belief_set is None:
            if cnf_belief in self.beliefs:
                self.beliefs.remove(cnf_belief)
        else:
            if cnf_belief in belief_set:
                belief_set.remove(cnf_belief)

    def contract(self, extract_belief):
        sorted_beliefs = sorted(self.beliefs_priorities, key=lambda x: (-x[1]))

        for (belief, _) in sorted_beliefs:
            a = self.check_entailment(extract_belief, belief)
            print(belief, a)
            if a:
                print(belief)
                self.beliefs.remove(*[to_cnf(belief)])

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
            new_set = And(belief_base_cnf, Not(cnf_formula))
            return not satisfiable(new_set)         

# Test
if __name__ == "__main__":
    belief_base = BeliefBase('A B C')  
    A, B, C = belief_base.symbols
    # Expand belief base
    belief_base.expand(A, 1)
    belief_base.expand(B, 2)
    belief_base.expand(C, 3)
    belief_base.expand(C, 5)
    belief_base.expand(Not(B), 2)
    belief_base.expand(Or(C, B), 5)
    print(belief_base.beliefs)
    belief_base.contract(B)
    print(belief_base.beliefs) 

    """ print("Belief Base:", belief_base)
    print("Belief Base CNF:", belief_base.to_CNF())

    # Check entailment of a formula
    formula = Implies(A, C)
    print("Entailment of {}: {}".format(formula, belief_base.check_entailment(formula))) """