import unittest
from src.regex.shunting_yard import *;
import src.regex.shunting_yard as sy


class ShuntingYard(unittest.TestCase):
    def setUp(self):
        self.sy = sy.ShuntingYard()

    def test_get_alphabet(self):
        regex = 'a.b|c*.d'
        expected = {'a', 'b', 'c', 'd', 'ε'}
        self.assertEqual(get_alphabet(regex), expected)

        regex = 'a(a|b)*b'
        expected = {'a', 'b', 'ε'}
        self.assertEqual(get_alphabet(regex), expected)

    def test_insert_concat_operator(self):
        regex = 'a.b|c*.d'
        expected = 'a.b|c*.d'
        self.assertEqual(insert_concat_operator(regex), expected)

        regex = 'a(a|b)*b'
        expected = 'a.(a|b)*.b'
        self.assertEqual(insert_concat_operator(regex), expected)

    def test_get_postfix(self):
        regex = 'a(a|b)*b'
        expected = 'aab|*.b.'
        self.sy.set_regex(regex)
        self.assertEqual(self.sy.get_postfix(), expected)

        regex = 'ab|c*d'
        expected = 'ab.c*d.|'
        self.sy.set_regex(regex)
        self.assertEqual(self.sy.get_postfix(), expected)


if __name__ == '__main__':
    unittest.main()
