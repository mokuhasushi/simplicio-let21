class ParseException(Exception):
    def __init__(self, msg="Error during parsing",
            operators=None, operands=None, expr=None):
        self.operators = operators
        self.operands = operands
        self.expr = expr

class NodeException(Exception):
    def __init__(self, msg="Errore nella gestione dei nodi", nodo=None):
        self.nodo = nodo

class DomainException(Exception):
    def __init__(self, msg="Errore nell'espressione dovuta al dominio'", nodo=None):
        self.nodo = nodo
