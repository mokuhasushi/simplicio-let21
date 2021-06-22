# Il riferimento per questa implementazione è:
# https://www.engr.mun.ca/~theo/Misc/exp_parsing.htm
import utilities
from exceptions import ParseException, EmptyStringException
import nodi
operatori_binari = {'+', '-', '*', ':', '/', '^'}
# Il simbolo '~' è una rappresentazione interna non ambigua del '-' unario. E'
# anche riconosciuto e accettato a livello di parsing.
operatori_unari = {'-', '~'}
parentesi = {'(':')', '[':']', '{':'}'}

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
nodi_parentesi = {'(': nodi.NodoParentesiTonde, '[': nodi.NodoParentesiQuadre,
    '{':nodi.NodoParentesiGraffe}

# Funzione di utilità per controllare la precedenza .
# Problema: accettare l'uguaglianza fa in modo di avere l'associatività a sinistra
# per le operazioni. Tuttavia questo genera problemi per i segni unari multipli,
# in quanto non hanno un operando a sinistra
# Esempio ---3 darebbe problemi
def gte(op1, op2):
    if op1 in operatori_unari and op2 in operatori_unari: return False
    return precedenze_operatori[op1] >= precedenze_operatori[op2]

# Funzione principale da chiamare
def parse_expr(expr, domain='R'):
    if expr == "" or expr == "#":
        raise EmptyStringException()
    stripped_expr = "".join(expr.split())
    stripped_expr += '#'
    return parse(stripped_expr, domain)#, debug

def parse(expr, domain='R'):
    operatori = utilities.Stack()
    operandi = utilities.Stack()
    # x è il simbolo 'sentinella', come descritto nella referenza
    operatori.push('x')
    expr_stacked = utilities.Stack(expr[::-1])
    e(operatori, operandi, expr_stacked, domain)
    # Controllo se il parsing è terminato correttamente
    # TODO: Serve?
    if (expr_stacked.peek() != '#'):
        raise ParseException("Carattere terminale non trovato!",
            operatori,
            operandi,
            expr_stacked)
    return operandi.peek()

# Corrisponde alla regola della grammatica di riferimento:
# E --> P {B P}*
def e(operatori, operandi, expr, domain='R'):
    p(operatori, operandi, expr, domain)
    n = expr.peek()
    while n in operatori_binari:
        pushOp(n, operatori, operandi, domain)
        expr.pop()
        p(operatori, operandi, expr, domain)
        n = expr.peek()
    while operatori.peek() != 'x':
        popOp(operatori, operandi, domain)
    return operatori, operandi, expr

#Corrisponde alla regola della grammatica di riferimento:
# P --> v | "(" E ")" | U P
def p(operatori, operandi, expr, domain='R'):
    next_token = expr.peek()
    # caso valore numerico --> v
    if next_token.isdigit():
        v = expr.pop()
        while expr.peek().isdigit():
            v += expr.pop()
        operandi.push(mkLeaf(v, domain))
    # caso parentesi --> "(" E ")"
    elif next_token in parentesi.keys():
        # salvo il tipo di parentesi
        lp = expr.pop()
        # faccio il push del simbolo sentinella prima di iniziare a parsare il
        # contenuto della parentesi, quindi chiamo e
        operatori.push('x')
        e(operatori, operandi, expr, domain)
        # controllo che la parentesizzazione sia corretta
        if expr.pop() != parentesi[lp]:
            raise ParseException("Errore di parentesizzazione",
                operatori, operandi, expr)
        # aggiungo un nodo per le parentesi, con un singolo figlio
        tree = operandi.pop()
        operandi.push(nodi_parentesi[lp](0, [tree]))
        # rimuovo il simbolo sentinella
        operatori.pop()
    elif next_token in operatori_unari:
        # Questo è un trucco: il riconoscimento di un operatore unario avviene
        # senza problemi in questa funzione, ma in seguito può causare danni.
        # Quindi scambio '-' con '~', evitando di incorrere in problemi
        _op = expr.pop()
        if _op == '-':
            _op = '~'
        pushOp(_op, operatori, operandi, domain)
        p(operatori, operandi, expr, domain)
    else:
        raise ParseException("Errore in p: regola non trovata!",
            operatori, operandi, expr)
    return operatori, operandi, expr

# Le foglie sono i valori numerici dell'espressione
def mkLeaf(num, domain):
    return nodi.NodoNumero(int(num), domain=domain)
# I nodi potrebbero essere unari o binari
def mkNode(op, t0, t1=None, domain='N'):
    if t1 is None:
        return operatori_e_nodi[op](0,[t0], domain=domain)
    else:
        return operatori_e_nodi[op](0, [t0, t1], domain=domain)
# Pop di un operatore con conseguente push sullo stack degli operandi
def popOp(operatori, operandi, domain):
    if operatori.peek() in operatori_binari:
        # i due operandi sono invertiti
        t1 = operandi.pop()
        t0 = operandi.pop()
        operandi.push(mkNode(operatori.pop(), t0, t1, domain))
    else:
        operandi.push(mkNode(operatori.pop(), operandi.pop(), domain=domain))
    # debug.append(utilities.nodo2tree(operandi.peek()))
    return operatori, operandi

# debug = []
# Push di un operatore. Prima però bisogna costruire un albero con tutti gli
# operatori di precedenza maggiore, per ottenere un albero ordinato in maniera
# corretta. Si può dire che questo è il cuore dell'algoritmo (?)(!)
def pushOp(op, operatori, operandi, domain):
    while gte(operatori.peek(), op):
        popOp(operatori, operandi, domain)
    operatori.push(op)
    return operatori, operandi
