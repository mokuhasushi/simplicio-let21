class Nodo():
    def __init__(self, value, children=None):
        self.value = value
        if children == None:
            children = []
        self.children = children
    def visita_df(self, visit, *args):
        f_r = visit(self, args)
        for t in children:
            t.visita_df(visit, args, f_r)
    def add_children(self, nodo):
        self.children.append(nodo)
    def get_type(self):
        return "Nodo"
    def get_annotated(self):
        return {'type':self.get_type()}
    def get_latex(self):
        return ""
    def __repr__(self):
        return f"{self.get_type()}: value: {self.value}, children:" + \
            f"{[n for n in self.children]}"


class NodoParentesiTonde(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "ParentesiTonde"
    def get_latex(self):
        return f"\\left( {self.children[0].get_latex()} \\right)"

class NodoParentesiQuadre(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "ParentesiQuadre"
    def get_latex(self):
        return f"\\left[ {self.children[0].get_latex()} \\right]"

class NodoParentesiGraffe(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "ParentesiGraffe"
    def get_latex(self):
        return "\\left\{" + f" {self.children[0].get_latex()} " + "\\right\}"

class NodoAddizione(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Addizione"
    def get_latex(self):
        return f"{self.children[0].get_latex()} + {self.children[1].get_latex()}"

class NodoSottrazione(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Sottrazione"
    def get_latex(self):
        return f"{self.children[0].get_latex()} - {self.children[1].get_latex()}"

class NodoMoltiplicazione(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Moltiplicazione"
    def get_latex(self):
        return f"{self.children[0].get_latex()} \\times {self.children[1].get_latex()}"

class NodoDivisione(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Divisione"
    def get_latex(self):
        return f"{self.children[0].get_latex()} : {self.children[1].get_latex()}"

class NodoMenoUnario(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "MenoUnario"
    def get_latex(self):
        return f"- {self.children[0].get_latex()}"

class NodoFrazione(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Frazione"
    def get_latex(self):
        return f"\\frac{{{self.children[0].get_latex()}}} {{{self.children[1].get_latex()}}}"

class NodoPotenza(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Potenza"
    def get_latex(self):
        return f"{self.children[0].get_latex()} ^ {{{self.children[1].get_latex()}}}"

class NodoNumero(Nodo):
    def __init__(self, value):
        super().__init__(value)
    def get_type(self):
        return "Numero"
    def get_annotated(self):
        return {'type': self.get_type(), 'value': self.value}
    def get_latex(self):
        return f"{self.value}"
