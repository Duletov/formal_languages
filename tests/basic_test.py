from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol
from pygraphblas import *


def test_matrix_product():
    
    A = Matrix.from_lists(
        [0, 0, 1, 3, 3, 4, 1, 5],
        [1, 3, 2, 4, 5, 2, 5, 4],
        [9, 3, 8, 6, 1, 4, 7, 2],)
    
    B = Matrix.from_lists(
        [0, 0, 1, 3, 3, 4, 1, 5],
        [2, 3, 3, 2, 5, 4, 5, 4],
        [9, 3, 8, 6, 2, 4, 5, 2],)
    actual = A @ B
    print (actual)
    expected = Matrix.from_lists(
        [0, 0, 0, 1, 3, 5],
        [2, 3, 5, 4, 4, 4],
        [18, 72, 51, 14, 26, 8],)
    assert expected.iseq(actual)


def test_pda_intersection():
    dfa_1 = DeterministicFiniteAutomaton()
    dfa_2 = DeterministicFiniteAutomaton()
    dfa = DeterministicFiniteAutomaton()

    # Creation of the states
    state0 = State(0)
    state1 = State(1)
    state2 = State(2)
    state3 = State(3)

    # Creation of the symbols
    symb_a = Symbol("a")
    symb_b = Symbol("b")
    symb_c = Symbol("c")
    symb_d = Symbol("d")

    # Add a start state
    dfa_1.add_start_state(state0)
    dfa_2.add_start_state(state0)

    # Add two final states
    dfa_1.add_final_state(state2)
    dfa_1.add_final_state(state3)
    dfa_2.add_final_state(state2)


    # Create transitions
    dfa_1.add_transition(state0, symb_a, state1)
    dfa_1.add_transition(state1, symb_b, state1)
    dfa_1.add_transition(state1, symb_c, state2)
    dfa_1.add_transition(state1, symb_d, state3)
    dfa_2.add_transition(state0, symb_a, state1)
    dfa_2.add_transition(state1, symb_b, state1)
    dfa_2.add_transition(state1, symb_c, state2)
    dfa_2.add_transition(state0, symb_d, state1)

    # Check if a word is accepted
    dfa = dfa_1 & dfa_2
    assert dfa.accepts([symb_a, symb_b, symb_c])
    assert dfa.accepts([symb_a, symb_b, symb_b, symb_c])
    assert not dfa.accepts([symb_a, symb_b, symb_d])
    assert not dfa.accepts([symb_d, symb_b, symb_c])