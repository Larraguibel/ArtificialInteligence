from sympy.logic.boolalg import And, Or, Not, Implies
from sympy import symbols

class BeliefBase:
    def __init__(self):
        self.beliefs = set()
        self.priorities = dict()

    def expand(self, belief, priority=1):
        self.beliefs.add(belief)
        self.assign_priority(belief, priority)

    def contract(self, belief):
        if belief in self.beliefs:
            self.beliefs.remove(belief)
            self.make_consistent_beliefs()
    
    def revise(self, belief):
        # Levi's identity
        self.contract(Not(belief))
        self.expand(belief)

    def make_consistent_beliefs(self):
        pass

    def assign_priority(self, belief, priority=None):
        if priority is None:
            self.priorities[belief.__str__()] = len(self.beliefs)
        else:
            self.priorities[belief.__str__()] = priority
            
    def to_CNF(self):
        cnf_beliefs = set()
        for belief in self.beliefs:
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
        else:
            return belief
            

    def __str__(self):
        return "{" + ", ".join(map(str, self.beliefs)) + "}"

    def __repr__(self):
        return "{" + ", ".join(map(str, self.beliefs)) + "}" 
   
    def __add__(self, belief):
        self.expand(belief)

    def __truediv__(self, belief):
        self.contract(belief)
    
    def __mul__(self, belief):
        self.revise(belief)

    # contractions with Horn Clauses

    def contract_using_resolution(self, belief):
        cnf_belief = self._convert_to_cnf(belief)
        
        # Identify Horn clauses with belief to contract
        horn_clauses = []
        for clause in cnf_belief.args:
            if is_horn_clause(clause):
                horn_clauses.append(clause)
        
        # Select largest set of clauses containing belief
        largest_set = select_largest_set(horn_clauses, belief)
        
        # Apply resolution
        new_clauses = apply_resolution(largest_set, belief)
        
        # Remove the contracted belief
        self.contract(belief)
        
        # Remove contradictory clauses
        for clause in new_clauses:
            if Not(clause) in self.beliefs:
                self.contract(Not(clause))
        
        # Add new clauses to the belief base
        for clause in new_clauses:
            self.expand(clause)
        
        # Ensure consistency
        self.make_consistent_beliefs()
