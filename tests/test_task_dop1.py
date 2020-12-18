from pyformlang.regular_expression import Regex
from differ import differ, nullable, reduce


def test_simple_regex():
    regexes = ["a", "a b", "a | b", "a*"]
    answers = ["a", "ab", "b", "aaa"]
    for i in range(4):
        regex = Regex(regexes[i])
        word = answers[i]
        for letter in word:
            regex = differ(regex, letter)
            for i in range(len(word)):
                regex = reduce(regex)
        assert(nullable(regex))


def test_wrong_regex():
    regexes = ["a", "a b", "a | b", "a*"]
    answers = ["b", "a", "ab", "aba"]
    for i in range(4):
        regex = Regex(regexes[i])
        word = answers[i]
        for letter in word:
            regex = differ(regex, letter)
            for i in range(len(word)):
                regex = reduce(regex)
        assert(not nullable(regex))


def test_default_regex():
    answers = ["", "a", "ab", "aaab"]
    for word in answers:
        regex = Regex("a * | a * b")
        for letter in word:
            regex = differ(regex, letter)
            for i in range(len(word)):
                regex = reduce(regex)
        assert(nullable(regex))