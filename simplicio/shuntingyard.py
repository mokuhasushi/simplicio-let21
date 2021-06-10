# Il riferimento per questa implementazione è:
# https://www.engr.mun.ca/~theo/Misc/exp_parsing.htm
from utilities import Stack
from exceptions import ParseException
import nodi
operatori_binari = {'+', '-', '*', ':', '/', '^'}
# TODO: rappresentare il meno unario con un -
operatori_unari = {'~'}
parentesi = {'(':')', '[':']', '{':'}'}
nodi_parentesi = {'(': nodi.NodoParentesiTonde, '[': nodi.NodoParentesiQuadre,
    '{':nodi.NodoParentesiGraffe}

# Precedenze degli operatori.
precedenze_operatori = {'^' : 5, '/' : 4, '~' : 3,
    '*' : 2, ':' : 2, '+' : 1, '-': 1, 'x' : 0}

# Operatori e nodi. Per il momento sto aggiungendo molte cose, per vedere cosa funziona
# in seguito tornerò a fare ordine TODO
operatori_e_nodi = {
    '+':nodi.NodoAddizione, '-':nodi.NodoSottrazione,
    '*':nodi.NodoMoltiplicazione, ':':nodi.NodoDivisione, '/':nodi.NodoFrazione,
    '^':nodi.NodoPotenza, '~':nodi.NodoMenoUnario
}

# Funzione di utilità per controllare la precedenza .
def gt(op1, op2):
    '''
    True if op1 ha una precedenza maggiore di op2
    '''
    return precedenze_operatori[op1] > precedenze_operatori[op2]

# Funzione principale da chiamare
def parse_expr(expr):
    stripped_expr = "".join(expr.split())
    try:
        return parse(stripped_expr)
    except ParseException as pe:
        print(pe)#,
#        "\noperatori: ", pe.operands,
#        "\noperandi: ", pe.operators,
#        "\nespressione rimanente: ", pe.expr)

def parse(expr):
    operatori = Stack()
    operandi = Stack()
    # x è il simbolo 'sentinella', come descritto nella referenza
    operatori.push('x')
    expr_stacked = Stack(expr[::-1])
    e(operatori, operandi, expr_stacked)
    # Controllo se il parsing è terminato correttamente
    # TODO: Controllare se basta controllare lo stack vuoto
    if (expr_stacked.peek() != '#'):
        raise ParseException("Carattere terminale non trovato!",
            operatori,
            operandi,
            expr_stacked)
    return operandi.peek()

# Corrisponde alla regola della grammatica di riferimento:
# E --> P {B P}*
def e(operatori, operandi, expr):
    p(operatori, operandi, expr)
    n = expr.peek()
    while n in operatori_binari:
        pushOp(n, operatori, operandi)
        expr.pop()
        p(operatori, operandi, expr)
        n = expr.peek()
    while operatori.peek() != 'x':
        popOp(operatori, operandi)
    return operatori, operandi, expr

#Corrisponde alla regola della grammatica di riferimento:
# P --> v | "(" E ")" | U P
def p(operatori, operandi, expr):
    next_token = expr.peek()
    # caso valore numerico --> v
    if next_token.isdigit():
        operandi.push(mkLeaf(expr.pop()))
    # caso parentesi --> "(" E ")"
    elif next_token in parentesi.keys():
        # salvo il tipo di parentesi
        lp = expr.pop()
        # faccio il push del simbolo sentinella prima di iniziare a parsare il
        # contenuto della parentesi, quindi chiamo e
        operatori.push('x')
        e(operatori, operandi, expr)
        # controllo che la parentesizzazione sia corretta
        if expr.pop() != parentesi[lp]:
            raise ParseException("Errore di parentesizzazione",
                operatori, operandi, expr)
        # aggiungo un nodo per le parentesi, con un singolo figlio
        tree = operandi.pop()
        #TODO vari tipi di parentesi
        operandi.push(nodi_parentesi[lp](0, [tree]))
        # rimuovo il simbolo sentinella
        operatori.pop()
    elif next_token in unOps:
        pushOp(expr.pop(), operatori, operandi)
        p(operatori, operandi, expr)
    else:
        raise ParseException("Errore in p: regola non trovata!",
            operatori, operandi, expr)
    return operatori, operandi, expr

# Le foglie sono i valori numerici dell'espressione
def mkLeaf(num):
    return nodi.NodoNumero(int(num))
# I nodi potrebbero essere unari o binari
def mkNode(op, t0, t1=None):
    if t1 is None:
        return operatori_e_nodi[op](0,[t0])
    else:
        return operatori_e_nodi[op](0, [t0, t1])
# Pop di un operatore con conseguente push sullo stack degli operandi
def popOp(operatori, operandi):
    if operatori.peek() in operatori_binari:
        # i due operandi sono invertiti
        t1 = operandi.pop()
        t0 = operandi.pop()
        operandi.push(mkNode(operatori.pop(), t0, t1))
    else:
        operandi.push(mkNode(operatori.pop(), operandi.pop()))
    return operatori, operandi

# Push di un operatore. Prima però bisogna costruire un albero con tutti gli
# operatori di precedenza maggiore, per ottenere un albero ordinato in maniera
# corretta. Si può dire che questo è il cuore dell'algoritmo (?)(!)
def pushOp(op, operatori, operandi):
    while gt(operatori.peek(), op):
        popOp(operatori, operandi)
    operatori.push(op)
    return operatori, operandi
