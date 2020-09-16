from Graph import Graph
from pygraphblas import *

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
        print (label)
        print(graph.get_by_label(label).nvals)

def all_path(graph):
    adj = graph.transitive_closure()
    adj.select(lib.GxB_NONZERO)
    for i, j, _ in zip(*adj.to_lists()):
        print(f'from {i} to {j}')
        
def from_bunch(graph, filename):
    input_file = open(filename)
    vertices = input_file.read().rstrip().split('\n')
    input_file.close()
    result = [int(item) for item in vertices]
    print(result)
    
    adj = graph.transitive_closure()
    adj.select(lib.GxB_NONZERO)
    for i, j, _ in zip(*adj.to_lists()):
        if i in result:
            print(f'from {i} to {j}')
            
def from_bunch_to_bunch(graph, filename_1, filename_2):
    input_file = open(filename_1)
    vertices = input_file.read().rstrip().split('\n')
    input_file.close()
    result_1 = [int(item) for item in vertices]
    
    input_file = open(filename_2)
    vertices = input_file.read().rstrip().split('\n')
    input_file.close()
    result_2 = [int(item) for item in vertices]
    
    
    adj = graph.transitive_closure()
    adj.select(lib.GxB_NONZERO)
    for i, j, _ in zip(*adj.to_lists()):
        if (i in result_1) and (j in result_2):
            print(f'from {i} to {j}')

def main():
    g = Graph()
    g.from_trans("input.txt")
    g.start_vertices.add(0)
    g.final_vertices.add(1)
    
    h = Graph()
    h.from_regex("input2.txt")
    h.start_vertices.add(0)
    h.final_vertices.add(1)
    
    inter = intersect(g, h)
    output(inter)
    '''all_path(inter)
    from_bunch(inter, "start.txt")
    from_bunch_to_bunch(inter, "start.txt", "end.txt")'''
    
        
if __name__ == "__main__":
    main()