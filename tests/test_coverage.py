# questi non sono test di unita
# import unittest
from .context import simplicio as smp
test_expr = "1 + {2 * [(3 + 4 : 2) + 5] * 6} - [7 + (1 + 8) : 3] * [9 : (2 + 1) + 2]#"
caso_pow = "2^(3+4^5:2^7)#"
caso_frac_1 = "(2+4)/(3+4)#"
caso_riassuntivo = "3 + 13 * ~(1+3) / (2^(1+4) - 6)#"
caso_parentesi_semplice = "3/(4+2) + 2 * {3:(4+5) + 2^(6*1/2)}-(2*[5*(3+4)+5]-1)/6#"
caso_parentesi_libere = "3/(4+2) + 2 * (3:(4+5) + 2^(6*1/2))-(2*(5*(3+4)+5)-1)/6#"
caso_parentesi_libere2 = "3/(4+2) + 2 * (3:(4+5) : 2^(6*1/2))-(2*(5*(3+4)+5)-1)/6#"
caso_rapido = "3 + 3 + 8 + 6 * 2#"
caso_segni_unari_multipli = "---3 + -56 * -(-(-(5)))#"
caso_lungo = "-19 + 4 * 45 / {12^[3+60/6:5] - 7/4 + 3 * (13 - 5 * -2^3)} * 22 / \
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}#"
casi_semplici = ["(2+4)/(3+4)#", "2/3/4#", "5/(6/7)#", "(2*3+4)/5#", "2/(3+4/5)#", "(((2+3)/4)/(5+6))/7#"]
casi_potenze = ["-2^(-2)", "(1/2)^3"]

def test_prova():
    smp.string2latex(test_expr)
    assert True

def test_semplici():
    for t in casi_semplici:
        smp.string2latex(t)
    assert True

def test_lungo():
    smp.string2latex(caso_lungo)
    assert True

def test_riassuntivo():
    smp.string2latex(caso_riassuntivo)
    assert True

# if __name__ == '__main__':
#     unittest.main()
