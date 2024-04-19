from sympy.logic.boolalg import And, Or, Not, Implies
from sympy import symbols

class BeliefBase:
    def __init__(self):
        self.beliefs = set()

    def expand(self, belief):
        self.beliefs.add(belief)

    def contract(self, belief):
        if belief in self.beliefs:
            self.beliefs.remove(belief)
            self.make_consistent_beliefs()
    
    def revise(self, belief):
        self.contract(Not(belief))
        self.expand(belief)

    def make_consistent_beliefs(self):
        pass

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
