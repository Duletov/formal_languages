from pygraphblas.matrix import Matrix
from pygraphblas.types import BOOL
from pyformlang.regular_expression import Regex

class Graph:
    def __init__(self):
        self.n_vertices = 0
        self.label_matrices = dict()
        self.start_vertices = set()
        self.final_vertices = set()

    def from_trans(self, filename):
        input_file = open(filename)
        edges = input_file.read().rstrip().split('\n')
        input_file.close()
        max_vertice_number = 0
        for edge in edges:
            fro, label, to = edge.split(' ')
            max_vertice_number = max(max_vertice_number, int(fro))
            max_vertice_number = max(max_vertice_number, int(to))            

        self.n_vertices = max_vertice_number + 1
        for edge in edges:
            fro, label, to = edge.split(' ')
            self.get_by_label(label)[int(fro), int(to)] = True

    def from_regex(self, filename):
        input_file = open(filename)
        regex = Regex(input_file.read().rstrip())
        dfa = regex.to_epsilon_nfa().to_deterministic().minimize()
        self.n_vertices = len(dfa.states)
        state_renumeration = dict()
        i = 0
        for state in dfa.states:
            state_renumeration[state] = i
            i += 1
            
        for fro, label, to in dfa._transition_function.get_edges():
            self.get_by_label(str(label))[state_renumeration[fro], state_renumeration[to]] = True

        self.start_vertices.add(state_renumeration[dfa.start_state])

        for state in dfa.final_states:
            self.final_vertices.add(state_renumeration[state])
        
    def transitive_closure_1(self):
        adj_matrix = Matrix.sparse(BOOL, self.n_vertices, self.n_vertices)
        for label_matrix in self.label_matrices.values():
            adj_matrix += label_matrix

        if adj_matrix.nvals != 0:
            while True:
                old = adj_matrix.nvals
                adj_matrix += adj_matrix @ adj_matrix
                if old == adj_matrix:
                    break

        return adj_matrix
        
    
    def transitive_closure_2(self):
        adj_matrix = Matrix.sparse(BOOL, self.n_vertices, self.n_vertices)
        result = Matrix.sparse(BOOL, self.n_vertices, self.n_vertices)
        for label_matrix in self.label_matrices.values():
            adj_matrix += label_matrix

        if adj_matrix.nvals != 0:
            while True:
                old = result.nvals
                result += adj_matrix
                if old == result.nvals:
                    break

        return result


    def labels(self):
        return self.label_matrices.keys()


    def get_by_label(self, label):
        if label not in self.label_matrices.keys():
            self.label_matrices[label] = Matrix.sparse(BOOL, self.n_vertices, self.n_vertices)
        return self.label_matrices[label]
