# Il riferimento per questa implementazione è:
# https://www.engr.mun.ca/~theo/Misc/exp_parsing.htm
# La grammatica è stata però modificata per consentire la notazione scientifica:
# E --> P {B P}*
# P --> V | "(" E ")" | U P
# B --> "+" | "-" | "*" | ":" | "/" | "^"
# U --> "-" | "~"
# V --> (([0-9]+(\.[0-9]*)?)|(\.[0-9]+))(e[0-9]+)?

# Dove V è stato espresso per comodità con una regex. Qui sotto una versione più
# leggibile. Quella sopra è dovuta al caso accettato ".1", ovvero numero decimale
# scritto partendo con un punto
# V --> [0-9]+(\.[0-9]*)?(e[0-9]+)?

import utilities
from exceptions import ParseException, EmptyStringException, DomainException
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
# Per operatori binari con associatività a sinistra è opportuno confrontare
# usando >=
def gt(op1, op2):
    if op1 in {"*", ":", "+", "-"}:
        return precedenze_operatori[op1] >= precedenze_operatori[op2]
    else:
        return precedenze_operatori[op1] > precedenze_operatori[op2]

# Funzione principale da chiamare
def parse_expr(expr, domain='R'):
    if expr == "" or expr[0] == "#":
        raise EmptyStringException()
    stripped_expr = "".join(expr.split())
    stripped_expr += '#'
    return parse(stripped_expr, domain)

def parse(expr, domain):
    operatori = utilities.Stack()
    operandi = utilities.Stack()
    # x è il simbolo 'sentinella', come descritto nella referenza
    operatori.push('x')
    # Il nastro viene simulato come Stack, con l'espressione inserita al
    # contrario (poichè struttura LIFO).
    expr_stacked = utilities.Stack(expr[::-1])
    # Il parsing inizia sempre con E
    e(operatori, operandi, expr_stacked, domain)
    # Controllo se il parsing è terminato correttamente
    # es in cui si entra nel branch: 1 + (1 + 1) )
    if (expr_stacked.peek() != '#'):
        raise ParseException("Carattere terminale non trovato!",
            operatori,
            operandi,
            expr_stacked)
    return operandi.peek()

# Corrisponde alla regola della grammatica di riferimento:
# E --> P {B P}*
def e(operatori, operandi, expr, domain):
    # P
    p(operatori, operandi, expr, domain)
    # {B P}*
    n = expr.peek()
    while n in operatori_binari:
        pushOp(n, operatori, operandi, domain)
        expr.pop()
        p(operatori, operandi, expr, domain)
        n = expr.peek()
    # Svuoto lo stack degli operatori creando nodi operandi
    while operatori.peek() != 'x':
        popOp(operatori, operandi, domain)
    return operatori, operandi, expr

#Corrisponde alla regola della grammatica:
# P --> V | "(" E ")" | U P
def p(operatori, operandi, expr, domain):
    next_token = expr.peek()
    # caso valore numerico --> V
    if next_token.isdigit() or next_token == '.':
        v(operandi, expr, domain)
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
    # caso operatore unario --> U P
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

def v(operandi, expr, domain):
    n = expr.pop()
    e = '0'
    while expr.peek().isdigit():
        n += expr.pop()
    if expr.peek() == '.':
        n += expr.pop()
        while expr.peek().isdigit():
            n += expr.pop()
    if expr.peek() in {'e', 'E'}:
        expr.pop()
        e = expr.pop()
        while expr.peek().isdigit():
            e += expr.pop()
    operandi.push(mkLeaf(n, e, domain))


# Le foglie sono i valori numerici dell'espressione
def mkLeaf(num, e, domain):
    if domain == 'R':
        return nodi.NodoNumero(float(num)*10**float(e), domain=domain)
    # E' stato scelto di NON implementare un convertitore
    # numero decimale -> numero frazionario
    else:
        n = float(num)*10**int(e)
        if int(n) != n:
            raise DomainException("Numeri con la virgola ammessi solo in R!")
        return nodi.NodoNumero(int(n), domain=domain)
# I nodi potrebbero essere unari o binari
def mkNode(op, t0, t1=None, domain='R'):
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
    return operatori, operandi

# Push di un operatore. Prima però bisogna costruire un albero con tutti gli
# operatori di precedenza maggiore, per ottenere un albero ordinato in maniera
# corretta. Si può dire che questo è il cuore dell'algoritmo (?)(!)
def pushOp(op, operatori, operandi, domain):
    while gt(operatori.peek(), op):
        popOp(operatori, operandi, domain)
    operatori.push(op)
    return operatori, operandi
