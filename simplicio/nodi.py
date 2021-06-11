class Nodo():
    def __init__(self, value=None, children=None):
        self.id = -1
        self.value = value
        if children == None:
            children = []
        self.children = children
        self.colore = ""
        self.boxed = False
    def add_children(self, nodo):
        self.children.append(nodo)
    def get_type(self):
        return "Nodo"
    def get_annotated(self):
        return {'type':self.get_type(), 'id':self.id, 'colore':self.colore}
    def get_latex(self):
        main_text = self.get_latex_main()
        if self.colore != "":
            return "\\color{" + self.colore + "} {" + main_text + "}"
        return main_text
    def get_latex_main(self):
        return ""
    def numera(self, n):
        size = len(self.children)
        if size == 0:
            self.id = n
            return n+1
        elif size == 1:
            n = self.children[0].numera(n)
            self.id = n
            n += 1
        elif size == 2:
            n = self.children[0].numera(n)
            self.id = n
            n += 1
            n = self.children[1].numera(n)
        # Questo caso è pericolo, rovina la ricerca binaria.
        # Servirà solo se si vorrà unire vari nodi es 3 + 3 + 3 + 1 ...
        else:
            for c in self.children:
                n = c.numera(n)
            self.id = n
            n += 1
        return n
    # Non so se servono
    # def colora(self, colore, id=-1):
    #     def colora_helper(nodo, colore):
    #         nodo.colore = colore
    #     self.cerca_id_df(id, colora_helper, colore)
    #     return self
    # def decolora(self):
    #     self.colore = ""
    # def cerca_id_df(self, id, f, arg=None):
    #     if id == self.id or id < 0:
    #         if arg == None:
    #             f(self)
    #         else:
    #             f(self, arg)
    #     else:
    #         self.children = [c.cerca_id_df(id, f, arg) for c in self.children]
    #     return self
    def __repr__(self):
        return f"{self.get_annotated()}, {[n for n in self.children]}"


class NodoParentesiTonde(Nodo):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "ParentesiTonde"

    def get_latex_main(self):
        main_text = f"\\left( {self.children[0].get_latex()} \\right)"
        return main_text

class NodoParentesiQuadre(Nodo):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "ParentesiQuadre"
    def get_latex_main(self):
        return f"\\left[ {self.children[0].get_latex()} \\right]"

class NodoParentesiGraffe(Nodo):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "ParentesiGraffe"
    def get_latex_main(self):
        return "\\left\{" + f" {self.children[0].get_latex()} " + "\\right\}"

class NodoAddizione(Nodo):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Addizione"
    def get_latex_main(self):
        return f"{self.children[0].get_latex()} + {self.children[1].get_latex()}"

class NodoSottrazione(Nodo):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Sottrazione"
    def get_latex_main(self):
        return f"{self.children[0].get_latex()} - {self.children[1].get_latex()}"

class NodoMoltiplicazione(Nodo):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Moltiplicazione"
    def get_latex_main(self):
        return f"{self.children[0].get_latex()} \\times {self.children[1].get_latex()}"

class NodoDivisione(Nodo):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Divisione"
    def get_latex_main(self):
        return f"{self.children[0].get_latex()} : {self.children[1].get_latex()}"

class NodoMenoUnario(Nodo):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "MenoUnario"
    def get_latex_main(self):
        return f"- {self.children[0].get_latex()}"

class NodoFrazione(Nodo):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Frazione"
    def get_latex_main(self):
        return f"\\frac{{{self.children[0].get_latex()}}} {{{self.children[1].get_latex()}}}"

class NodoPotenza(Nodo):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Potenza"
    def get_latex_main(self):
        return f"{self.children[0].get_latex()} ^ {{{self.children[1].get_latex()}}}"

class NodoNumero(Nodo):
    def __init__(self, value):
        super().__init__(value)
    def get_type(self):
        return "Numero"
    def get_annotated(self):
        d = super().get_annotated()
        d['value'] = self.value
        return d
    def get_latex_main(self):
        return f"{self.value}"
