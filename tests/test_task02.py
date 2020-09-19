from pygraphblas.matrix import Matrix
from pygraphblas.types import BOOL
from Graph import Graph
from main import intersect, output

def test_read_from_file():
    g = Graph()
    g.from_trans("input.txt")
    
    a_mtrx = Matrix.sparse(BOOL, 4, 4)
    a_mtrx[0,1] = True
    b_mtrx = Matrix.sparse(BOOL, 4, 4)
    b_mtrx[1,1] = True
    c_mtrx = Matrix.sparse(BOOL, 4, 4)
    c_mtrx[1,2] = True
    d_mtrx = Matrix.sparse(BOOL, 4, 4)
    d_mtrx[1,3] = True
    
    a_eq = g.get_by_label('a').iseq(a_mtrx)
    b_eq = g.get_by_label('b').iseq(b_mtrx)
    c_eq = g.get_by_label('c').iseq(c_mtrx)
    d_eq = g.get_by_label('d').iseq(d_mtrx)
    
    assert a_eq and b_eq and c_eq  and d_eq


def test_intersect_simple():
    g = Graph()
    g.from_trans("input.txt")
    h = Graph()
    h.from_regex("input2.txt")
    expected = Graph()
    expected.from_trans("expected.txt")
    
    actual = intersect(g, h)
    
    equality = True
    
    for label in expected.labels():
        equality += actual.get_by_label(label).nvals == expected.get_by_label(label).nvals
    
    assert equality
    
def test_transitive_closure():
    ex = Graph()
    ex.from_trans("expected.txt")
    
    actual = Matrix.sparse(BOOL, 3, 3)
    actual[0,1] = True
    actual[0,2] = True
    actual[1,1] = True
    actual[1,2] = True
    
    expected = ex.transitive_closure()
    
    assert actual.iseq(expected)


def test_intersect_space():
    g = Graph()
    g.from_trans("input.txt")
    h = Graph()
    expected = Graph()
    
    actual = intersect(g, h)
    
    equality = True
    
    for label in expected.labels():
        equality += actual.get_by_label(label).nvals == expected.get_by_label(label).nvals
    
    assert equality


def test_intersect_parallel():
    g = Graph()
    g.from_trans("input.txt")
    h = Graph()
    h.from_trans("parallel.txt")
    expected = Graph()
    expected.from_trans("expected2.txt")
    
    actual = intersect(g, h)
    
    equality = True
    
    for label in expected.labels():
        equality += actual.get_by_label(label).nvals == expected.get_by_label(label).nvals
    
    assert equality


def test_intersect_single():
    g = Graph()
    g.from_trans("input.txt")
    h = Graph()
    h.from_regex("single.txt")
    expected = Graph()
    expected.from_trans("expected2.txt")
    
    actual = intersect(g, h)
    
    equality = True
    
    for label in expected.labels():
        equality += actual.get_by_label(label).nvals == expected.get_by_label(label).nvals
    
    assert equality