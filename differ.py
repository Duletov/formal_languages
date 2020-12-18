from pyformlang.regular_expression.regex_objects import Union, Symbol, Concatenation, Epsilon, Empty, KleeneStar, Operator
import copy


def differ(regex, symbol):
    if type(regex.head) == Union:
        #print("Union")
        regex.sons[0] = differ(regex.sons[0], symbol)
        regex.sons[1] = differ(regex.sons[1], symbol)
        return regex
    elif type(regex.head) == Concatenation:
        #print("Concatenation")
        if nullable(regex.sons[0]):
            regex3 = copy.deepcopy(regex.sons[0])
            regex4 = copy.deepcopy(regex.sons[1])
            regex1 = differ(regex3, symbol)
            regex2 = regex1.concatenate(regex4)
            regex.head = Union()
            regex.sons[0] = regex2
            regex.sons[1] = differ(regex.sons[1], symbol)
        else:
            regex.sons[0] = differ(regex.sons[0], symbol)
        return regex
    elif type(regex.head) == KleeneStar:
        #print("KleeneStar")
        regex1 = copy.deepcopy(regex.sons[0])
        regex = differ(regex1, symbol).concatenate(regex)
        return regex
    else:
        if(regex.head.value == symbol):
            #print("Epsilon")
            regex.head = Epsilon()
            return regex
        else:
            #print("Empty")
            regex.head = Empty()
            return regex


def reduce(regex):
    if type(regex.head) == Union and type(regex.sons[0].head) == Empty:
        regex = copy.deepcopy(regex.sons[1])
    elif type(regex.head) == Union and type(regex.sons[1].head) == Empty:
        regex = copy.deepcopy(regex.sons[0])
    elif type(regex.head) == Concatenation and type(regex.sons[1].head) == Empty:
        regex = copy.deepcopy(regex.sons[1])
    elif type(regex.head) == (Union or Concatenation):
        regex.sons[0] = reduce(regex.sons[0])
        regex.sons[1] = reduce(regex.sons[1])
    return regex


def nullable(regex):
    if type(regex.head) == Union:
        return nullable(regex.sons[0]) or nullable(regex.sons[1])
    elif type(regex.head) == Concatenation:
        return nullable(regex.sons[0]) and nullable(regex.sons[1])
    elif type(regex.head) == KleeneStar:
        return True
    elif type(regex.head) == Epsilon:
        return True
    else:
        return False