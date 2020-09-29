from CFG import CNF
from Graph import Graph

def test_read_from_file():
    mycnf = CNF.from_file("cnf.txt")
    print(mycnf)
    assert(mycnf.contains("ab") and mycnf.contains("aabb") and mycnf.contains(""))


def test_CYK_true():
    mycnf = CNF.from_file("cnf.txt")
    input = "ab"
    
    actual = mycnf.CYK(input)
    print(actual)
    
    assert(actual)


def test_CYK_false():
    mycnf = CNF.from_file("cnf.txt")
    input = "c"
    
    actual = mycnf.CYK(input)
    print(actual)
    
    assert(not actual)


def test_CYK_empty():
    mycnf = CNF.from_file("cnf.txt")
    input = ""
    
    actual = mycnf.CYK(input)
    print(actual)
    
    assert(actual)


def test_Helling_default():
    mycnf = CNF.from_file("cnf2.txt")
    g = Graph()
    g.from_trans("hell.txt")
    
    ans = mycnf.Hellings(g)
    expected = [(0, 2)]
    
    assert(ans == expected)
    
def test_Helling_epsilon():
    mycnf = CNF.from_file("cnf.txt")
    g = Graph()
    g.from_trans("hell.txt")
    
    ans = mycnf.Hellings(g)
    expected = [(0, 2), (0, 0), (1, 1), (2, 2)]
    
    assert(ans == expected)