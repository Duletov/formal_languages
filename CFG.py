from typing import AbstractSet, Iterable
from pyformlang.cfg import *
from pygraphblas import *
from Graph import Graph
from main import intersect
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
        
        self.terminal_productions = list()
        self.nonterminal_productions = list()

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
                self.terminal_productions.append(production)
            elif len(production.body) == 2:
                body = tuple(production.body)
                self.nonterminal_productions.append(production)
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
                    cur_edges_by_start[fro].add((var, to))
                    m.append((var, fro, to))

        ans = []
        if self.generates_epsilon:
            for i in range(n):
                cur_edges_by_end[i].add((self.start_symbol, i))
                cur_edges_by_start[i].add((self.start_symbol, i))
                ans.append((i, i))
                    
        
        while(len(m) > 0):
            (var_1, v, u) = m.pop()
            cur_edges_mid = list(cur_edges_by_end[v])
            for (var_2, w) in cur_edges_mid:
                for var_3 in self.heads_for_body.get((var_2, var_1), set()):
                    if (var_3, w) not in cur_edges_by_end[u]:
                        m.append((var_3, w, u))
                        cur_edges_by_end[u].add((var_3, w))
                        cur_edges_by_start[w].add((var_3, u))
                        if u == v:
                            cur_edges_mid.append((var_3, w))
                        if var_3 == self.start_symbol:
                            ans.append((w, u))
            cur_edges_mid = list(cur_edges_by_start[u])
            for (var_2, w) in cur_edges_mid:
                for var_3 in self.heads_for_body.get((var_1, var_2), set()):
                    if (var_3, w) not in cur_edges_by_start[v]:
                        m.append((var_3, v, w))
                        cur_edges_by_end[w].add((var_3, v))
                        cur_edges_by_start[v].add((var_3, w))
                        if v == u:
                            cur_edges_mid.append((var_3, w))
                        if var_3 == self.start_symbol:
                            ans.append((v, w))

        return ans
        
        
    def Azimov(self, graph):
        result = Graph()
        result.n_vertices = graph.n_vertices
        for production in self.terminal_productions:
            result.get_by_label(production.head.value)
            result.label_matrices[production.head.value] += graph.get_by_label(production.body[0].value)

        if self.generate_epsilon():
            for i in range(graph.n_vertices):
                result.get_by_label(self.start_symbol)[i, i] = True

        changes = True
        while changes:
            changes = False
            for production in self.nonterminal_productions:
                prev = result.get_by_label(production.head.value).nvals
                result.label_matrices[production.head.value] += result.get_by_label(production.body[0].value) @ result.get_by_label(production.body[1].value)
                if prev != result.label_matrices[production.head.value].nvals:
                    changes = True

        return list(zip(*result.label_matrices[self.start_symbol].to_lists()[:2]))
        
    def Tenzor(self, graph, rec_auto, heads):
        result = Graph()
        result.n_vertices = graph.n_vertices
        for label in graph.labels():
            result.get_by_label(label)
            result.label_matrices[label] = graph.label_matrices[label]
        result.start_vertices = graph.start_vertices
        result.final_vertices = graph.final_vertices
        
        result.get_by_label(self.start_symbol.value)
        if self.generate_epsilon():
            for i in range(graph.n_vertices):
                result.get_by_label(self.start_symbol)[i, i] = True
        changes = True
        intersection = Graph()
        intersection = intersect(result, rec_auto)
        transitive_closure = intersection.transitive_closure_1()
        n = intersection.n_vertices
        while changes:
            prev = transitive_closure.nvals
            for i in range(n):
                for j in range(n):
                    if (i, j) in transitive_closure:
                        s = i % rec_auto.n_vertices
                        f = j % rec_auto.n_vertices
                        if (s in rec_auto.start_vertices) and (f in rec_auto.final_vertices):
                            x = i // rec_auto.n_vertices
                            y = j // rec_auto.n_vertices
                            result.get_by_label(heads[s, f])[x, y] = True
            intersection = intersect(result, rec_auto)
            transitive_closure = intersection.transitive_closure_1()
            if transitive_closure.nvals == prev:
                changes = False
        return list(zip(*result.label_matrices[self.start_symbol].to_lists()[:2]))
        
    def to_recursive_automaton(self):
        rec_auto = Graph()
        heads = {}
        for production in self.productions:
            length = len(production.body)
            rec_auto.n_vertices += length + 1
        ver = 0
        for production in self.productions:
            length = len(production.body)
            rec_auto.start_vertices.add(ver)
            for i in range(length):
                rec_auto.get_by_label(production.body[i].value)[ver, ver + 1] = True
                ver += 1
            rec_auto.final_vertices.add(ver)
            heads[ver - length, ver] = production.head.value
            ver += 1
        return rec_auto, heads
