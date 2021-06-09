class ParseException(Exception):
    def __init__(self, msg="Error during parsing",
            operators=None, operands=None, expr=None):
        self.operators = operators
        self.operands = operands
        self.expr = expr
