import re
import sys
import random
import unittest
from argparse import ArgumentParser
from collections import deque


"""          TEST START          """


class TestTokenize(unittest.TestCase):
    def tokenize_list(self, input):
        res = []
        for token in tokenize(input):
            res.append(token)
        return res

    def assertTokenizedAs(self, string, l):
        self.assertListEqual(self.tokenize_list(string), l)

    def test_1(self):
        s = "Hello, World!123"
        self.assertTokenizedAs(s, ["Hello", ",", " ", "World", "!", "123"])

    def test_newline(self):
        s = "Yo\nTest \n "
        self.assertTokenizedAs(s, ["Yo", "\n", "Test", " ", "\n", " "])

    def test_unicode(self):
        s = "Привет, мир\nПривет, привет."
        self.assertTokenizedAs(s, ["Привет", ",", " ", "мир", "\n",
                                   "Привет", ",", " ", "привет", "."])

    def test_mixed(self):
        s = "Приветworld, hi. world\nмир"
        self.assertTokenizedAs(s, ["Приветworld", ",", " ", "hi", ".",
                                   " ", "world", "\n", "мир"])

    def test_symbols(self):
        s = ".,!? \t\n#$@"
        self.assertTokenizedAs(s, [".", ",", "!", "?", " ", "\t", "\n", "#", "$", "@"])


class TestProbabilities(unittest.TestCase):
    def test_simple(self):
        s = "First test sentence\nSecond test line"
        probs = get_probabilities(s, 1, normalize=False)
        ans = {('First',): {'test': 1},
               (): {'line': 1, 'First': 1, 'Second': 1, 'test': 2, 'sentence': 1},
               ('Second',): {'test': 1},
               ('test',): {'line': 1, 'sentence': 1}}
        self.assertDictEqual(ans, probs)


"""           TEST END           """


def tokenize(input):
    specs = [
        ("WORD", r'[^\W\d_]+'),
        ("NUMBER", r'\d+'),
        ("SYMBOL", '.'),
    ]
    pattern = "|".join('(?P<%s>%s)' % spec for spec in specs)
    for match_object in re.finditer(pattern, input, flags=re.DOTALL):
        yield match_object.group(0)


def get_probabilities(input, depth, letters_only=True, lines_independent=True, normalize=True):
    window = deque()
    probs = dict()
    for token in tokenize(input):
        if lines_independent and token == '\n':
            window.clear()
            continue
        if letters_only and not token.isalpha():
            continue
        window.append(token)
        if len(window) > depth + 1:
            window.popleft()
        chain = list(window)
        target = chain[-1]
        max_len = min(depth, len(chain) - 1)
        for start in range(0, 1 + max_len):
            subchain = tuple(chain[start:max_len])
            if subchain not in probs:
                probs[subchain] = dict()
            if target not in probs[subchain]:
                probs[subchain][target] = 0
            probs[subchain][target] += 1
    if normalize:
        for chain in probs:
            no_of_occurances = sum(probs[chain].values())
            for target in probs[chain]:
                probs[chain][target] /= no_of_occurances
    return probs


def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w


def generate(probs, size):
    window = deque()
    tokens = []
    for i in range(size):
        while tuple(window) not in probs:
            window.popleft()
        target = weighted_choice(probs[tuple(window)].items())
        tokens.append(target)
        window.append(target)
    return "".join(tokens)


def main():
    parser = ArgumentParser()
    parser.add_argument("action", choices=["tokenize", "generate", "probabilities", "test"])
    parser.add_argument("--depth", type=int)
    parser.add_argument("--size", type=int)
    res = parser.parse_args(input().split())
    if res.action == "tokenize":
        if res.depth or res.size:
            parser.print_help()
            return
        for token in tokenize(input()):
            print(token)
    elif res.action == "probabilities":
        if not res.depth or res.size:
            parser.print_help()
            return
        probs = get_probabilities("".join(sys.stdin.readlines()), res.depth,
                                  letters_only=True, lines_independent=True)
        for chain in sorted(probs.keys()):
            print(*chain)
            for target in sorted(probs[chain].keys()):
                print("  %s: %.2f" % (target, probs[chain][target]))
    elif res.action == "generate":
        if not res.depth or not res.size:
            parser.print_help()
            return
        probs = get_probabilities("".join(sys.stdin.readlines()), res.depth,
                                  letters_only=False, lines_independent=False)
        print(generate(probs, res.size))
    elif res.action == "test":
        if res.depth or res.size:
            parser.print_help()
            return
        unittest.main()
    else:
        raise NotImplementedError()


if __name__ == "__main__":
    main()
