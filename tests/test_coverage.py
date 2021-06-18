# questi non sono test di unita
# import unittest
from .context import shuntingyard as sy
from .context import semplificatore as smp
test_expr = "1 + {2 * [(3 + 4 : 2) + 5] * 6} - [7 + (1 + 8) : 3] * [9 : (2 + 1) + 2]#"

def test_simple():
    n = sy.parse_expr(test_expr)
    simpler = smp.Semplificatore(n)
    texts = simpler.solve()
    assert True

# if __name__ == '__main__':
#     unittest.main()
