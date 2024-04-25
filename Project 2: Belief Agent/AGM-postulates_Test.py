import pytest
from sympy.logic.boolalg import And, Or, Not, Implies
from sympy import symbols
from belief_agent import BeliefBase
from sympy.logic.boolalg import to_cnf

# AGM Postulates for Belief Contraction

def test_closure_contraction():
    # Closure: The belief base should not entail the contracted belief after contraction
    belief_base = BeliefBase('p q')
    p, q = belief_base.symbols
    
    # Initial beliefs
    belief_base.expand(Implies(p, q), 1)  # `p → q`
    belief_base.expand(p, 2)  # `p`
    belief_base.expand(q, 3)  # `q`
    
    # Contract `q`
    belief_base.contract(q)

    # After contracting `q`, it should not be entailed
    assert not belief_base.check_entailment(q), "After contraction, `q` should not be entailed"



def test_inclusion_contraction():
    # C2 - Inclusion: The contracted belief base should be a subset of the original base
    belief_base = BeliefBase('p q')
    p, q = belief_base.symbols
    belief_base.expand(p, 1)  # Setting priorities for expand
    belief_base.expand(q, 2)  # Also set priority here
    initial_beliefs = belief_base.beliefs.copy()  # Copy original beliefs
    belief_base.contract(q)  # Contract `q`
    assert belief_base.beliefs.issubset(initial_beliefs)  # Contraction should create a subset

def test_vacuity_contraction():
    # C3 - Vacuity: If the belief isn't in the base, contraction should not affect it
    belief_base = BeliefBase('p q')
    p, q = belief_base.symbols
    belief_base.expand(p, 1)  # Add `p`
    initial_beliefs = belief_base.beliefs.copy()  # Original beliefs
    belief_base.contract(q)  # Contract `q`, which is not in the base
    assert belief_base.beliefs == initial_beliefs  # Should remain unchanged

def test_success_contraction():
    # C4 - Success: After contraction, the belief should not be derived
    belief_base = BeliefBase('p q')
    p, q = belief_base.symbols
    belief_base.expand(q, 1)  # Add `q`
    belief_base.contract(q)  # Contract `q`
    assert not belief_base.check_entailment(q)  # Should not be derived after contraction


def test_core_retention_contraction():
    # C5 - Core Retention: Contraction by a tautology should leave the belief base unchanged
    belief_base = BeliefBase('p q')
    p, q = belief_base.symbols
    belief_base.expand(p, 1)  # Add `p`
    belief_base.expand(q, 2)  # Add `q`
    initial_beliefs = belief_base.beliefs.copy()  # Copy original beliefs
    
    tautology = And(p, Not(p))  # Tautology: always true (contradiction)
    belief_base.contract(tautology)  # Contract a tautology
    
    assert belief_base.beliefs == initial_beliefs  # Should remain unchanged

def test_recovery_contraction():
    # C6 - Recovery: If you contract a belief and then expand it again, you should recover the original base
    belief_base = BeliefBase('p q')
    p, q = belief_base.symbols
    belief_base.expand(p, 1)  # Add `p` with priority
    belief_base.expand(q, 2)  # Add `q` with priority
    initial_beliefs = belief_base.beliefs.copy()  # Copy original beliefs
    
    print("Beliefs before contraction:", initial_beliefs)  # Debug
    belief_base.contract(q)  # Contract `q`
    print("Beliefs after contraction:", belief_base.beliefs)  # Debug
    
    belief_base.expand(q, 2)  # Expand `q` again
    assert belief_base.beliefs == initial_beliefs  # Should recover the original base

# AGM Postulates for Belief Revision

def test_closure_revision():
    # R1 - Closure: The belief base should remain consistent after revision
    belief_base = BeliefBase('p q')
    p, q = belief_base.symbols
    belief_base.expand(And(p, q), 1)  # Adding priority for expand
    belief_base.revise(And(p, q))  # Revise with `p ∧ q`
    assert belief_base.check_entailment(p)  # Should still be derived
    assert belief_base.check_entailment(q)  # Should still be derived

def test_inclusion_revision():
    # R3 - Inclusion: The revised belief base should contain the original beliefs, assuming consistency
    belief_base = BeliefBase('p q')
    p, q = belief_base.symbols
    belief_base.expand(q, 1)  # Adding `q`
    belief_base.revise(p)  # Revise with `p`
    
    # Convert beliefs to CNF to ensure proper checks
    cnf_q = to_cnf(q)
    cnf_p = to_cnf(p)
    
    # Check if the base contains the beliefs after revision
    assert cnf_q in belief_base.beliefs  # Should still have `q`
    assert cnf_p in belief_base.beliefs  # Should now have `p`

def test_success_revision():
    # R2 - Success: After revision, the revised belief should be part of the base
    belief_base = BeliefBase('p q')
    p, q = belief_base.symbols
    belief_base.expand(p, 1)  # Adding priority to fix missing positional argument issue
    belief_base.revise(p)  # Revise with `p`
    
    # Convert belief to CNF
    cnf_p = to_cnf(p)
    
    assert cnf_p in belief_base.beliefs  # `p` should be part of the base

def test_vacuity_revision():
    # R4 - Vacuity: If the revised belief is already in the base, it should not change
    belief_base = BeliefBase('p q')
    p, q = belief_base.symbols
    belief_base.expand(p, 1)  # Add `p`
    
    initial_beliefs = belief_base.beliefs.copy()  # Copy original beliefs
    belief_base.revise(p)  # Revise with `p`
    
    assert belief_base.beliefs == initial_beliefs  # The belief base should remain unchanged


def test_consistency_revision():
    # R5 - Consistency: The belief base should remain consistent after revision unless inherently inconsistent
    belief_base = BeliefBase('p q')
    p, q = belief_base.symbols
    belief_base.expand(p, 1)  # Adding priority to fix TypeError
    belief_base.revise(p)  # Revise with `p`
    assert belief_base.check_entailment(p)  # Should be consistent after revision

def test_superexpansion_revision():
    # R6 - Superexpansion: If a belief is derived from the revised belief base, revising with it should not affect entailment
    belief_base = BeliefBase('p q')
    p, q = belief_base.symbols
    belief_base.expand(Implies(p, q), 1)  # `Implies(p, q)`
    belief_base.revise(p)  # Revise with `p`
    assert belief_base.check_entailment(q)  # Should still derive `q`