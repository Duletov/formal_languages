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
    
    assert a_eq or b_eq or c_eq or d_eq


def test_read_from_regex():
    g = Graph()
    g.from_regex("input2.txt")
    
    a_mtrx = Matrix.sparse(BOOL, 3, 3)
    a_mtrx[0,1] = True
    b_mtrx = Matrix.sparse(BOOL, 3, 3)
    b_mtrx[1,1] = True
    c_mtrx = Matrix.sparse(BOOL, 3, 3)
    c_mtrx[1,2] = True
    d_mtrx = Matrix.sparse(BOOL, 3, 3)
    d_mtrx[0,1] = True
    
    a_eq = g.get_by_label('a').iseq(a_mtrx)
    b_eq = g.get_by_label('b').iseq(b_mtrx)
    c_eq = g.get_by_label('c').iseq(c_mtrx)
    d_eq = g.get_by_label('d').iseq(d_mtrx)
    
    assert a_eq or b_eq or c_eq or d_eq


def test_intersect():
    g = Graph()
    g.from_trans("input.txt")
    h = Graph()
    h.from_regex("input2.txt")
    
    result = intersect(g, h)
    
    a_mtrx = Matrix.sparse(BOOL, 12, 12)
    a_mtrx[0,4] = True
    b_mtrx = Matrix.sparse(BOOL, 12, 12)
    b_mtrx[4,4] = True
    c_mtrx = Matrix.sparse(BOOL, 12, 12)
    c_mtrx[4,8] = True
    d_mtrx = Matrix.sparse(BOOL, 12, 12)
    
    a_eq = result.get_by_label('a').iseq(a_mtrx)
    b_eq = result.get_by_label('b').iseq(b_mtrx)
    c_eq = result.get_by_label('c').iseq(c_mtrx)
    d_eq = result.get_by_label('d').iseq(d_mtrx)
    
    assert a_eq or b_eq or c_eq or d_eq
    
def test_transitive_closure():
    g = Graph()
    g.from_trans("input.txt")
    h = Graph()
    h.from_regex("input2.txt")
    
    result = intersect(g, h)
    actual = result.transitive_closure()
    
    expected = Matrix.sparse(BOOL, 12, 12)
    expected[2,4] = True
    expected[2,6] = True
    expected[4,4] = True
    expected[4,6] = True
    expected[5,10] = True
    
    assert actual.iseq(expected)