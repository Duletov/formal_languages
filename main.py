from Graph import Graph, intersect
from CFG import CNF
from differ import differ, nullable, reduce
from pygraphblas import *
import argparse
import time
from pyformlang.regular_expression import Regex


res_trans1 = list()
res_trans2 = list()
res_pairs = list()
res = list()


def output(graph):
    for label in graph.labels():
        print(label, graph.get_by_label(label).nvals)


def call(graph, filename_1, filename_2):
    if filename_1 == None:
        result_1 = range(graph.n_vertices)
    else:
        input_file = open(filename_1)
        vertices = input_file.read().rstrip().split('\n')
        input_file.close()
        result_1 = [int(item) for item in vertices]

    if filename_2 == None:
        result_2 = range(graph.n_vertices)
    else:
        input_file = open(filename_2)
        vertices = input_file.read().rstrip().split('\n')
        input_file.close()
        result_2 = [int(item) for item in vertices]

    time3 = 0
    for i in range(5):
            time1 = time.time()
            adj = graph.transitive_closure_1()
            time2 = time.time()
            time3 += time2 - time1
    print(adj.nvals)
    print(f"Time to transitive_closure_1 {time3/5}")
    res_trans1.append(time3/5)
    
    res.append(adj.nvals)
    
    for i in range(5):
            time1 = time.time()
            adj = graph.transitive_closure_2()
            time2 = time.time()
            time3 += time2 - time1
    print(adj.nvals)
    print(f"Time to transitive_closure_2 {time3/5}")
    res_trans2.append(time3/5)
    
    for i in range(5):
            time1 = time.time()
            adj.select(lib.GxB_NONZERO)
            for i, j, _ in zip(*adj.to_lists()):
                if (i in result_1) and (j in result_2):
                    print(f'from {i} to {j}')
            time2 = time.time()
            time3 += time2 - time1
    print(adj.nvals)
    print(f"Time to calculate pairs {time3/5}")
    res_pairs.append(time3/5)


def main_regex():
    time1 = time.time()
    g = Graph()
    g.from_trans(args.graph)
    time2 = time.time()
    print(f"Time to built graph {time2 - time1}")
    
    input_file = open(args.query)
    regexes = input_file.read().rstrip().split('\n')
    input_file.close()
    
    res_inter = list()
    
    for file in regexes:
        print()
        print(file)
        h = Graph()
        h.from_regex(file)
        time3 = 0
        for i in range(5):
            time1 = time.time()
            inter = intersect(g, h)
            time2 = time.time()
            time3 += time2 - time1
        print(f"Time to intersect {time3/5}")
        res_inter.append(time3/5)
        
        output(inter)
        call(inter, args.start, args.end)


def main_cfg():
    input_file = open(args.graph)
    graphs = input_file.read().rstrip().split('\n')
    input_file.close()
    res_H = []
    res_A = []
    res_RA = []
    res_T = []
    for graph in graphs:
        time1 = time.time()
        g = Graph()
        print(graph)
        g.from_trans(graph)
        time2 = time.time()
        print(f"Time to built graph {time2 - time1}")
        
        input_file = open(args.query)
        cfg = input_file.read().rstrip().split('\n')
        input_file.close()
    
        for file in cfg:
            print()
            print(file)
            mycnf = CNF.from_file(file)
            time3 = 0
            for i in range(5):
                time1 = time.time()
                ans = mycnf.Hellings(g)
                time2 = time.time()
                time3 += time2 - time1
            print(f"Time Hellings {time3/5}")
            res_H.append(time3/5)
            time3 = 0
            for i in range(5):
                time1 = time.time()
                ans = mycnf.Azimov(g)
                time2 = time.time()
                time3 += time2 - time1
            print(f"Time Azimov {time3/5}")
            res_A.append(time3/5)
            time3 = 0
            for i in range(5):
                time1 = time.time()
                rec_auto, heads = mycnf.to_recursive_automaton()
                time2 = time.time()
                time3 += time2 - time1
            print(f"Time RecAuto {time3/5}")
            res_RA.append(time3/5)
            time3 = 0
            for i in range(5):
                time1 = time.time()
                ans = mycnf.Tenzor(g, rec_auto, heads)
                time2 = time.time()
                time3 += time2 - time1
            print(f"Time Tenzor {time3/5}")
            res_T.append(time3/5)
    print(res_H)
    print(res_A)
    print(res_RA)
    print(res_T)

            
def min_cfg():
    input_file = open(args.graph)
    graphs = input_file.read().rstrip().split('\n')
    input_file.close()
    res_H = []
    res_A = []
    res_RA = []
    res_T = []
    graph = graphs[7]
    time1 = time.time()
    g = Graph()
    print(graph)
    g.from_trans(graph)
    time2 = time.time()
    print(f"Time to built graph {time2 - time1}")
    input_file = open(args.query)
    cfg = input_file.read().rstrip().split('\n')
    input_file.close()
    
    file = cfg[0]
    print()
    print(file)
    mycnf = CNF.from_file(file)
    time3 = 0
    for i in range(5):
        time1 = time.time()
        ans = mycnf.Hellings(g)
        time2 = time.time()
        time3 += time2 - time1
    print(f"Time Hellings {time3/5}")
    res_H.append(time3/5)
    time3 = 0
    for i in range(5):
        time1 = time.time()
        ans = mycnf.Azimov(g)
        time2 = time.time()
        time3 += time2 - time1
    print(f"Time Azimov {time3/5}")
    res_A.append(time3/5)
    time3 = 0
    for i in range(5):
        time1 = time.time()
        rec_auto, heads = mycnf.to_recursive_automaton()
        time2 = time.time()
        time3 += time2 - time1
    print(f"Time RecAuto {time3/5}")
    res_RA.append(time3/5)
    time3 = 0

    print('job done')


def main_differ():
    input_file = open(args.graph)
    regex = Regex(input_file.read().rstrip())
    word = args.query
    print(regex.get_tree_str())
    for letter in word:
        regex = differ(regex, letter)
        for i in range(len(word)):
            regex = reduce(regex)
        print(regex.get_tree_str())
    print(nullable(regex))
    
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='command line interface for simple graph/dfa operations')
    parser.add_argument(
        '--mod',
        required=True,
        type=str,
        help='Reg or cfg',
    )
    parser.add_argument(
        '--graph',
        required=True,
        type=str,
        help='path to the graph file',
    )
    parser.add_argument(
        '--query',
        required=True,
        type=str,
        help='path to file with names of regex/cfg files',
    )
    parser.add_argument(
        '--start',
        required=False,
        type=str,
        help='path to the file with start vertices',
    )
    parser.add_argument(
        '--end',
        required=False,
        type=str,
        help='path to the file with end vertices',
    )
    args = parser.parse_args()

    space = [i for i in range(100000)]
    print('job done')
    
    if args.mod == 'reg':
        main()
    elif args.mod == 'dif':
        main_differ()
    else:
        min_cfg()
