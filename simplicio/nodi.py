class Nodo():
    def __init__(self, value=None, children=None):
        self.id = -1
        self.value = value
        if children == None:
            children = []
        self.children = children
        self.colore = ""
        self.boxed = False
        self.leaf = False
        self.clear_after_read_flag = False
    def add_children(self, nodo):
        self.children.append(nodo)
    def get_type(self):
        return "Nodo"
    def get_annotated(self):
        d = {'type':self.get_type(), 'id':self.id}
        if self.colore != "": d['colore'] = self.colore
        return d
    def get_latex(self):
        main_text = self.get_latex_main()
        if self.boxed:
            main_text = "\\boxed{" + main_text + "}"
        if self.colore != "":
            main_text = "\\color{" + self.colore + "} {" + main_text + "}"
        if self.clear_after_read_flag:
            self.colore = ""
            self.boxed = False
            self.clear_after_read_flag = False
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
    def solve_step(self):
        if not self.children[0].leaf:
            self.children[0] = self.children[0].solve_step()
            return self
        elif len(self.children) > 1 and not self.children[1].leaf:
            self.children[1] = self.children[1].solve_step()
            return self
        ret = NodoNumero(self.operate(), self.id)
        ret.boxed = True
        ret.colore = "green"
        ret.clear_after_read_flag = True
        return ret
    def box_leaf(self):
        if not self.children[0].leaf:
            self.children[0].box_leaf()
            return
        elif len(self.children) > 1 and not self.children[1].leaf:
            self.children[1].box_leaf()
            return
        self.boxed = True
        self.colore = "red"
        return

    def operate(self):
        pass
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
    def operate(self):
        return self.children[0].value
    def get_latex_main(self):
        main_text = f"\\left( {self.children[0].get_latex()} \\right)"
        return main_text

class NodoParentesiQuadre(Nodo):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "ParentesiQuadre"
    def operate(self):
        return self.children[0].value
    def get_latex_main(self):
        return f"\\left[ {self.children[0].get_latex()} \\right]"

class NodoParentesiGraffe(Nodo):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "ParentesiGraffe"
    def operate(self):
        return self.children[0].value
    def get_latex_main(self):
        return "\\left\{" + f" {self.children[0].get_latex()} " + "\\right\}"

class NodoAddizione(Nodo):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Addizione"
    def operate(self):
        return self.children[0].value + self.children[1].value
    def get_latex_main(self):
        return f"{self.children[0].get_latex()} + {self.children[1].get_latex()}"

class NodoSottrazione(Nodo):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Sottrazione"
    def operate(self):
        return self.children[0].value - self.children[1].value
    def get_latex_main(self):
        return f"{self.children[0].get_latex()} - {self.children[1].get_latex()}"

class NodoMoltiplicazione(Nodo):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Moltiplicazione"
    def operate(self):
        return self.children[0].value * self.children[1].value
    def get_latex_main(self):
        return f"{self.children[0].get_latex()} \\times {self.children[1].get_latex()}"

class NodoDivisione(Nodo):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "Divisione"
    def operate(self):
        return self.children[0].value // self.children[1].value
    def get_latex_main(self):
        return f"{self.children[0].get_latex()} : {self.children[1].get_latex()}"

class NodoMenoUnario(Nodo):
    def __init__(self, value=None, children=None):
        super().__init__(value, children)
    def get_type(self):
        return "MenoUnario"
    def operate(self):
        return -self.children[0].value
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
    def operate(self):
        return self.children[0].value ** self.children[1].value
    def get_latex_main(self):
        return f"{self.children[0].get_latex()} ^ {{{self.children[1].get_latex()}}}"

class NodoNumero(Nodo):
    def __init__(self, value, id=-1):
        super().__init__(value)
        self.leaf = True
        self.id = id
    def get_type(self):
        return "Numero"
    def get_annotated(self):
        d = super().get_annotated()
        d['value'] = self.value
        return d
    def get_latex_main(self):
        return f"{self.value}"
