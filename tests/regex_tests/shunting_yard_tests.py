import unittest
import src.regex.shunting_yard as shunting_yard


class ShuntingYard(unittest.TestCase):
    def test_get_alphabet(self):
        regex = 'a.b|c*.d'
        expected = {'a', 'b', 'c', 'd', 'ε'}
        self.assertEqual(shunting_yard.get_alphabet(regex), expected)

        regex = 'a(a|b)*b'
        expected = {'a', 'b', 'ε'}
        self.assertEqual(shunting_yard.get_alphabet(regex), expected)

    def test_insert_concat_operator(self):
        regex = 'a.b|c*.d'
        expected = 'a.b|c*.d'
        self.assertEqual(shunting_yard.insert_concat_operator(regex), expected)

        regex = 'a(a|b)*b'
        expected = 'a.(a|b)*.b'
        self.assertEqual(shunting_yard.insert_concat_operator(regex), expected)


if __name__ == '__main__':
    unittest.main()
