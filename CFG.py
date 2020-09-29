from typing import AbstractSet, Iterable
from pyformlang.cfg import *
from pygraphblas import *
from Graph import Graph
from itertools import product
from collections import deque

class CNF(CFG):
    def __init__(self,
                 variables: AbstractSet[Variable] = None,
                 terminals: AbstractSet[Terminal] = None,
                 start_symbol: Variable = None,
                 productions: Iterable[Production] = None):

        cfg = CFG(
            variables = variables,
            terminals = terminals,
            start_symbol = start_symbol,
            productions = productions
        )

        self.generates_epsilon = cfg.generate_epsilon()
        cfg = cfg.to_normal_form()

        if self.generates_epsilon:
            cfg._productions |= {Production(cfg.start_symbol, [])}

        super(CNF, self).__init__(
            variables=cfg._variables,
            terminals=cfg._terminals,
            start_symbol=cfg._start_symbol,
            productions=cfg._productions
        )

        self.heads_for_body = dict()

        for production in self._productions:
            if len(production.body) == 1:
                body = production.body[0]
            else:
                body = tuple(production.body)
            self.heads_for_body[body] = self.heads_for_body.get(body, set()) | {production.head}


    @classmethod
    def from_file(self, path):
        productions = []
        with open(path, 'r') as input_file:
            for line in input_file:
                production = line.split()
                productions.append(production[0] + ' -> ' + ' '.join(production[1:]))

        cfg = CFG.from_text('\n'.join(productions))

        return CNF(
            variables=cfg.variables,
            terminals=cfg.terminals,
            start_symbol=cfg.start_symbol,
            productions=cfg.productions
        )


    def CYK(self, input_string):
        n = len(input_string)
        if n == 0:
            return self.generates_epsilon
        
        r = len(self._variables)
        produced = [[set() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            produced[i][0] |= self.heads_for_body.get(Terminal(input_string[i]), set())

        for l in range(2, n + 1):
            for s in range(n - l + 1):
                for p in range(s + 1, s + l):
                    for left in produced[s][p - s - 1]:
                        for right in produced[p][l - p + s - 1]:
                            produced[s][l - 1] |= self.heads_for_body.get((left, right), set())

        return self.start_symbol in produced[0][n - 1]


    def Hellings(self, graph):
        n = graph.n_vertices
        cur_edges_by_end = [set() for i in range(n)]
        cur_edges_by_start = [set() for i in range(n)]
        m = deque()
        for (label, label_matrix) in graph.label_matrices.items():
            [fros, tos, _] = label_matrix.to_lists()
            for i in range(len(fros)):
                fro = fros[i]
                to = tos[i]
                variables = self.heads_for_body.get(Terminal(label), set())
                for var in variables:
                    cur_edges_by_end[to].add((var, fro))
                    cur_edges_by_end[fro].add((var, to))
                    m.append((var, fro, to))
                    
        ans = []
        while(len(m) > 0):
            (var_1, v, u) = m.pop()
            cur_edges_mid = list(cur_edges_by_end[v])
            for (var_2, w) in cur_edges_mid:
                for var_3 in self.heads_for_body.get((var_2, var_1), set()):
                    if (var_3, w) not in cur_edges_by_end[u]:
                        m.append((var_3, w, u))
                        cur_edges_by_end[u].add((var_3, w))
                        if u == v:
                            cur_edges_mid.append((var_3, w))
                        if var_3 == self.start_symbol:
                            ans.append((w, u))
            cur_edges_mid = list(cur_edges_by_start[u])
            for (var_2, w) in cur_edges_mid:
                for var_3 in self.heads_for_body.get((var_1, var_2), set()):
                    if (var_3, w) not in cur_edges_by_start[v]:
                        m.append((var_3, v, w))
                        cur_edges_by_start[v].add((var_3, w))
                        if v == u:
                            cur_edges_mid.append((var_3, w))
                        if var_3 == self.start_symbol:
                            ans.append((v, w))
        if self.generates_epsilon:
            for i in range(n):
                ans.append((i, i))

        return ans
