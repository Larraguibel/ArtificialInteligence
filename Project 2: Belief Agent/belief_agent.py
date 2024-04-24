from sympy.logic.boolalg import And, Or, Not, Implies, Equivalent, to_cnf
from sympy import symbols
from sympy.logic.inference import satisfiable
from utils import generate_combinations

class BeliefBase:
    def __init__(self, atomic_symbols: str):
        self.beliefs = set()
        self.symbols = symbols(atomic_symbols)
        self.possible_symbol_values = generate_combinations(len(self.symbols))
        self.priorities = {value: i for i, value in enumerate(self.possible_symbol_values)}

    def expand(self, belief):
        cnf_belief = self._convert_to_cnf(belief)
        self.beliefs.add(cnf_belief)

    def remove(self, belief, belief_set=None):
        cnf_belief = self._convert_to_cnf(belief)
        if belief_set is None:
            if cnf_belief in self.beliefs:
                self.beliefs.remove(cnf_belief)
        else:
            if cnf_belief in belief_set:
                belief_set.remove(cnf_belief)

    def contract(self, belief):
        # Erase lowest priority if contradicts new info
        cnf_belief = self._convert_to_cnf(belief)
        if cnf_belief in self.beliefs:
            self.remove(cnf_belief)
            while self.check_entailment(cnf_belief):
                for clause in self.beliefs:
                    copy_beliefs = self.beliefs.copy()
                    self.remove(clause, belief_set=copy_beliefs)
                    if self.check_entailment(cnf_belief, copy_beliefs):
                        pass

    def revise(self, belief):
        # Levi's identity
        self.contract(Not(belief))
        self.expand(belief)

    def to_CNF(self, belief_base=None):
        if belief_base is None:
            cnf_beliefs = set()
            for belief in self.beliefs:
                cnf_beliefs.add(self._convert_to_cnf(belief))
            return And(*cnf_beliefs)
        else:
            cnf_beliefs = set()
            for belief in belief_base:
                cnf_beliefs.add(self._convert_to_cnf(belief))
            return And(*cnf_beliefs)

    def _convert_to_cnf(self, belief):
        if isinstance(belief, And):
            return And(*(self._convert_to_cnf(arg) for arg in belief.args))
        
        elif isinstance(belief, Or):
            return Or(*(self._convert_to_cnf(arg) for arg in belief.args))

        elif isinstance(belief, Not):
            return Not(self._convert_to_cnf(belief.args[0]))

        elif isinstance(belief, Implies):
            return Or(Not(self._convert_to_cnf(belief.args[0])), self._convert_to_cnf(belief.args[1]))
        
        elif isinstance(belief, Equivalent):
            return And(self._convert_to_cnf(Implies(belief.args[0], belief.args[1])),
                    self._convert_to_cnf(Implies(belief.args[1], belief.args[0])))
        else:
            return belief

    def check_entailment(self, formula, belief_base=None):
        if belief_base is None:
            cnf_formula = self._convert_to_cnf(formula)
            belief_base_cnf = self.to_CNF()
            new_set = And(belief_base_cnf, Not(cnf_formula))
            return not satisfiable(new_set)
        else:
            cnf_formula = self._convert_to_cnf(formula)
            belief_base_cnf = self.to_CNF(belief_base)
            new_set = And(belief_base_cnf, Not(cnf_formula))
            return not satisfiable(new_set)         

        

# Test
if __name__ == "__main__":
    belief_base = BeliefBase('A B C')  
    A, B, C = belief_base.symbols
    # Expand belief base
    belief_base.expand(A)
    belief_base.expand(B)
    print("Belief Base:", belief_base)
    print("Belief Base CNF:", belief_base.to_CNF())

    # Check entailment of a formula
    formula = Implies(A, C)
    print("Entailment of {}: {}".format(formula, belief_base.check_entailment(formula)))
