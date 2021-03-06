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
    "12 * (3 - 4))", "1 + (3 - 2)))) + 1"]
caso_rapido = "3 + 3 + 8 + 6 * 2 ^ 3#"
caso_segni_unari_multipli = "---3 + -56 / -(-(-(5)))#"
casi_semplici_Q = ["2^(3+4^5:2^7)#", "(2+4)/(3+4)#", "2/3/4#", "5/(6/7)#", "(2*3+4)/5#", "2/(3+4/5)#", "(((2+3)/4)/(5+6))/7#"]
casi_potenze = ["-2^(-2)", "(1/2)^3", "3^(2*1/2)", "2^[8/4]"]
caso_potenza_frazione_esponente = "2^(1/2)"
casi_frazioni = ["1/2/3", "1/2/3/4", "(1/2)/(3/4)", "4/1"]
caso_simbolo_non_riconosciuto = "13 * 4 + (ciao - 3)"
casi_N_ok = ["15 * 3 + 2 : 2", "15 - 4 - (3*3)", "1 * 4 - 8 + 5 - 2 + 3", "2^3", "4 / (2 * 2)"]
casi_N_non_ok = ["-2", "4 - 8", "2^(-1)", "2^(1-2)", "3/4", "3 : 4"]
casi_Z_ok = ["15 * 3 + 2 : 2", "15 - 4 - (3*3)", "1 * 4 - 8 + 5 - 2 + 3", "2^3", "4 / (2 * 2)",
    "-2", "4 - 8"]
casi_Z_non_ok = [ "2^(-1)", "2^(1-2)", "3/4", "3 : 4"]
caso_notazione_scientifica_ok_R = "4e100 - (8.2e1 + 5 - .2 * 3)"
caso_notazione_scientifica_non_ok_R = "4e100 - (8.2ee1 + 5 - .2 * 3)"
caso_notazione_scientifica_ok_N = "4 + (8.2e1 + 5 - 2 * 3)"
caso_notazione_scientifica_non_ok_N = "4 + (8.2e1 + 5 - .2 * 3)"
def test_prova():
    smp.string2latex(test_expr)
    assert True

def test_semplici_Q():
    for t in casi_semplici_Q:
        smp.string2latex(t, 'Q')
    assert True

# Tempo di esecuzione: +4 secondi (su macchina linux con processore i7 di 7ima gen)
# def test_lungo():
#     smp.string2latex(caso_lungo, 'Q')
#     assert True

# Tempo di esecuzione: +30 secondi (su macchina linux con processore i7 di 7ima gen)
# def test_lungo_2():
#     smp.string2latex(caso_lungo_2, 'Q')
#     assert True

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

def test_N_ok():
    for t in casi_N_ok:
        smp.string2latex(t, 'N')
    assert True

def test_N_non_ok():
    for t in casi_N_non_ok:
        with pytest.raises(exc.DomainException):
            smp.string2latex(t, 'N')
    assert True

def test_Z_ok():
    for t in casi_Z_ok:
        smp.string2latex(t, 'Z')
    assert True

def test_Z_non_ok():
    for t in casi_Z_non_ok:
        with pytest.raises(exc.DomainException):
            smp.string2latex(t, 'Z')
    assert True
def test_notazione_scientifica_R():
    smp.string2latex(caso_notazione_scientifica_ok_R, 'R')
    assert True
def test_notazione_scientifica_R_non_ok():
    with pytest.raises(exc.ParseException):
        smp.string2latex(caso_notazione_scientifica_non_ok_R, 'R')
    assert True
def test_notazione_scientifica_N_ok():
    smp.string2latex(caso_notazione_scientifica_ok_N, 'N')
    assert True
def test_notazione_scientifica_N_non_ok():
    with pytest.raises(exc.DomainException):
        smp.string2latex(caso_notazione_scientifica_non_ok_N, 'N')
    assert True
# 15 + 1 prima linea, poi 15. 600 operazioni -> 35 sec.
# Si mette in evidenza il fatto che il costo in termini di tempo dipende
# non solo dalla lunghezza dell'input, ma anche dalle sue caratteristiche.
# Questo poich?? in questo caso (no parentesi, operazioni miste, peggiorabile con
# pi?? tipi di operazioni) emergono le limitazioni di andare a percorre i sottoalberi
# alla ricerca del tipo dei nodi. Mi pare comunque che impiegare circa 5 secondi
# per un input di 300 operazioni possa essere ragionevole in questo contesto.
caso_lungo_2 = " 1 + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
    + 1 * 1  + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 + 1 * 1 \
"

caso_lungo = "-19 + 4 * 45 / {12^[3+60/6:5] - 7/4 + 3 * (13 - 5 * -2^3)} * 22 / \
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}-\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}+\
    143 - [13^2/45*3+3/(7+3^2)] : 3 - 1 + {12^(3+4)/12 + [5 - 3*4 + -(4^(9/3))]}\
    + 4 * (3+7^2)/{45 + 1 * 4 - [7/3 : 2 + 4 * (5 ^ 3 - 14) + 3] - 11^2}#"
