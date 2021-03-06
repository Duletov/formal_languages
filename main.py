from Graph import Graph
from pygraphblas import *
import argparse
import time
import copy

res_trans1 = list()
res_trans2 = list()
res_pairs = list()
res = list()

def intersect(graph_1, graph_2):
    result = Graph()
    result.n_vertices = graph_1.n_vertices * graph_2.n_vertices
    for i in graph_1.start_vertices:
        for j in graph_2.start_vertices:
            result.start_vertices.add(i * graph_1.n_vertices + j)

    for i in graph_1.final_vertices:
        for j in graph_2.final_vertices:
            result.final_vertices.add(i * graph_1.n_vertices + j)

    for label in graph_1.labels() | graph_2.labels():
        result.label_matrices[label] = graph_1.get_by_label(label).kronecker(graph_2.get_by_label(label))

    return result


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


def main():
    time1 = time.time()
    g = Graph()
    g.from_trans(args.graph)
    time2 = time.time()
    print(f"Time to built graph {time2 - time1}")
    
    input_file = open(args.regex)
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
        
    '''print(res_inter)
    print(res_trans1)
    print(res_trans2)
    print(res_pairs)
    print(res)'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='command line interface for simple graph/dfa operations')
    parser.add_argument(
        '--graph',
        required=True,
        type=str,
        help='path to the graph file',
    )
    parser.add_argument(
        '--regex',
        required=True,
        type=str,
        help='path to file with names of regex files',
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

    main()
