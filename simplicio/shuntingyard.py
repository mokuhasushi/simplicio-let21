# Il riferimento per questa implementazione è:
# https://www.engr.mun.ca/~theo/Misc/exp_parsing.htm
from utilities import Stack
from exceptions import ParseException

operatori_binari = {'+', '-', '*', ':', '/', '^'}
# TODO: rappresentare il meno unario con un -
operatori_unari = {'~'}
parentesi = {'(':')', '[':']', '{':'}'}

# Precedenze degli operatori.
precedenze_operatori = {'^' : 5, '/' : 4, '~' : 3,
    '*' : 2, ':' : 2, '+' : 1, '-': 1}

# Funzione di utilità per controllare la precedenza .
def gt(op1, op2):
    '''
    True if op1 ha una precedenza maggiore di op2
    '''
    return precedenze_operatori[op1] > precedenze_operatori[op2]

# Funzione principale da chiamare
def parse_expr(expr):
    operators = Stack()
    operands = Stack()
    # x è il simbolo 'sentinella', come descritto nella referenza
    operators.push('x')
    expr_stacked = Stack(expr[::-1])
    e(operators, operands, expr_stacked)
    # Controllo se il parsing è terminato correttamente
    # TODO: Controllare se basta controllare lo stack vuoto
    if (expr_stacked.peek() != '#'):
        raise ParseException("ParseError: carattere terminale non trovato!",
            expr=expr_stacked)
    return operands.peek()

def e(operators, operands, expr):
    pass
