import pytest
from .context import simplicio as smp
from .context import exceptions as exc
test_expr = "1 + {2 * [(3 + 4 : 2) + 5] * 6} - [7 + (1 + 8) : 3] * [9 : (2 + 1) + 2]#"
caso_riassuntivo = "3 + 13 * ~(1+3) / (2^(1+4) - 6)#"
casi_parentesi = ["3/(4+2) + 2 * {3:(4+5) + 2^(6*1/2)}-(2*[5*(3+4)+5]-1)/6#",
    "3/(4+2) + 2 * (3:(4+5) + 2^(6*1/2))-(2*(5*(3+4)+5)-1)/6#",
    "3/(4+2) + 2 * (3:(4+5) : 2^(6*1/2))-(2*(5*(3+4)+5)-1)/6#",
    "{3-4*(2+6^[13 + 2])}"]
casi_parentesi_sbagliate = ["{([3 + 4) * 2 ] - 9}", "(((15 * 3) + 4) - 2",
    "12 * (3 - 4))"]
caso_rapido = "3 + 3 + 8 + 6 * 2 ^ 3#"
caso_segni_unari_multipli = "---3 + -56 / -(-(-(5)))#"
caso_lungo = "-19 + 4 * 45 / {12^[3+60/6:5] - 7/4 + 3 * (13 - 5 * -2^3)} * 22 / \
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}#"
casi_semplici_Q = ["2^(3+4^5:2^7)#", "(2+4)/(3+4)#", "2/3/4#", "5/(6/7)#", "(2*3+4)/5#", "2/(3+4/5)#", "(((2+3)/4)/(5+6))/7#"]
casi_potenze = ["-2^(-2)", "(1/2)^3", "3^(2*1/2)", "2^[8/4]"]
caso_potenza_frazione_esponente = "2^(1/2)"
casi_frazioni = ["1/2/3", "1/2/3/4", "(1/2)/(3/4)", "4/1"]
caso_simbolo_non_riconosciuto = "13 * 4 + (ciao - 3)"

def test_prova():
    smp.string2latex(test_expr)
    assert True

def test_semplici_Q():
    for t in casi_semplici_Q:
        smp.string2latex(t, 'Q')
    assert True

def test_lungo():
    smp.string2latex(caso_lungo, 'Q')
    assert True

def test_riassuntivo():
    smp.string2latex(caso_riassuntivo, 'Q')
    assert True

def test_stringa_vuota():
    with pytest.raises(exc.EmptyStringException):
        smp.string2latex("")

def test_parentesi_sbagliate():
    for t in casi_parentesi_sbagliate:
        with pytest.raises(exc.ParseException):
            smp.string2latex(t)

def test_simbolo_non_riconosciuto():
    with pytest.raises(exc.ParseException):
        smp.string2latex(caso_simbolo_non_riconosciuto)

def test_parentesi():
    for t in casi_parentesi:
        smp.string2latex(t, 'Q')
    assert True

def test_stessa_operazione_piu_nodi():
    smp.string2latex(caso_rapido)
    assert True

def test_segni_unari_multipli():
    smp.string2latex(caso_segni_unari_multipli)
    assert True

def test_frazioni():
    for t in casi_frazioni:
        smp.string2latex(t, 'Q')
    assert True

def test_potenze():
    for t in casi_potenze:
        smp.string2latex(t, 'Q')
    assert True

def test_frazione_all_esponente():
    with pytest.raises(exc.DomainException):
        smp.string2latex(caso_potenza_frazione_esponente, 'Q')
