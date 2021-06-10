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
    def __repr__(self):
        return f"{self.get_type()}: value: {self.value}, children:" + \
            f"{[n for n in self.children]}"


class NodoParentesiTonde(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "ParentesiTonde"

class NodoParentesiQuadre(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "ParentesiQuadre"

class NodoParentesiGraffe(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "ParentesiGraffe"

class NodoAddizione(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Addizione"

class NodoSottrazione(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Sottrazione"

class NodoMoltiplicazione(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Moltiplicazione"

class NodoDivisione(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Divisione"

class NodoMenoUnario(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "MenoUnario"

class NodoFrazione(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Frazione"

class NodoPotenza(Nodo):
    def __init__(self, value, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Potenza"

class NodoNumero(Nodo):
    def __init__(self, value):
        super().__init__(value)
    def get_type(self):
        return "Numero"
    def get_annotated(self):
        return {'type': self.get_type(), 'value': self.value}
