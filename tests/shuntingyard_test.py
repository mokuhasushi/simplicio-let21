import unittest
from .context import shuntingyard
from .context import exceptions

class TestSimpleParser(unittest.TestCase):
    def test_wrong_input(self):
        with self.assertRaises(exceptions.ParseException):
            shuntingyard.parse_expr("asd")

if __name__ == '__main__':
    unittest.main()
