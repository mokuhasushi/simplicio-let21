import math
import exceptions
import utilities

tipo_parentesi = {"ParentesiTonde", "ParentesiQuadre", "ParentesiGraffe"}
class Nodo():
    def __init__(self, value=None, children=None, domain='R'):
        self.id = -1
        self.value = value
        if children == None:
            children = []
        self.children = children
        self.colore = ""
        self.boxed = False
        self.leaf = False
        self.clear_after_read_flag = False
        self.domain = domain
        self.precedence = -1
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
            raise NodeException("Albero non binario!")
        return n
    def solve_step(self):
        #risoluzione in un passaggio di tutte le operazioni simili
        if self.check_all_children_have_same_precedence(self.precedence):
            self.children[0] = self.children[0].solve_chain()
            if len(self.children) > 1:
                self.children[1] = self.children[1].solve_chain()
        elif not self.children[0].leaf:
            self.children[0] = self.children[0].solve_step()
            return self
        elif len(self.children) > 1 and not self.children[1].leaf:
            self.children[1] = self.children[1].solve_step()
            return self
        # Ogni figlio del nodo è una foglia, controllo il dominio e risolvo
        if self.domain == 'R':
            ret = NodoNumero(self.operate(), self.id)
        elif self.domain == 'N':
            ret = self.operate_N()
            # Questo controllo viene eseguito qui per via della risoluzione a catena
            if ret.value < 0:
                print(self)
                raise exceptions.DomainException("Valori negativi non ammessi in N!")
            if int(ret.value) != ret.value:
                raise exceptions.DomainException("Solo numeri interi in N!")
        elif self.domain == 'Z':
            ret = self.operate_Z()
            if int(ret.value) != ret.value:
                raise exceptions.DomainException("Solo numeri interi in Z!")
        else:
            ret = self.operate_Q()
        ret.boxed = True
        ret.colore = "green"
        ret.clear_after_read_flag = True
        return ret
    def solve_chain(self):
        if self.leaf: return self
        self.children[0] = self.children[0].solve_chain()
        if len(self.children) > 1:
            self.children[1] = self.children[1].solve_chain()
        if self.domain == 'R':
            ret = NodoNumero(self.operate(), self.id)
        elif self.domain == 'N':
            ret = self.operate_N()
        elif self.domain == 'Z':
            ret = self.operate_Z()
        else:
            ret = self.operate_Q()
        return ret
    def box_leaf(self):
        if not self.check_all_children_have_same_precedence(self.precedence):
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
    def operate_N(self):
        pass
    def operate_Z(self):
        pass
    def operate_Q(self):
        pass
    def get_num_and_den(self):
        raise exceptions.NodeException("Errore, get num and den chiamato su un \
        nodo operazione!", nodo=self)
    def get_children_nums_and_dens(self):
        n1, d1 = self.children[0].get_num_and_den()
        n2, d2 = self.children[1].get_num_and_den()
        return n1, d1, n2, d2
    def reduce_frac(num, den, id=-1):
        gcd = math.gcd(num, den)
        if gcd > 1:
            num //= gcd
            den //= gcd
        if den != 1:
            ret = NodoFrazione(children=[NodoNumero(num), NodoNumero(den)], domain='Q')
            ret.leaf = True
            return ret
        else:
            return NodoNumero(num, domain='Q')
    def check_all_children_have_same_precedence(self, prec):
        #I nodi foglia vanno bene
        if self.precedence != prec and self.leaf == False:
            return False
        ret = True
        for c in self.children:
            ret = ret and c.check_all_children_have_same_precedence(prec)
        return ret
    def __repr__(self):
        return f"{self.get_annotated()}, {[n for n in self.children]}"


class NodoParentesiTonde(Nodo):
    def __init__(self, value=None, children=None, domain='R'):
        super().__init__(value, children, domain)
    def get_type(self):
        return "ParentesiTonde"
    def operate(self):
        return self.children[0].value
    def operate_N(self):
        return self.children[0]
    def operate_Z(self):
        return self.children[0]
    def operate_Q(self):
        return self.children[0]
    def get_latex_main(self):
        main_text = f"\\left( {self.children[0].get_latex()} \\right)"
        return main_text

class NodoParentesiQuadre(Nodo):
    def __init__(self, value=None, children=None, domain='R'):
        super().__init__(value, children, domain)
    def get_type(self):
        return "ParentesiQuadre"
    def operate(self):
        return self.children[0].value
    def operate_N(self):
        return self.children[0]
    def operate_Z(self):
        return self.children[0]
    def operate_Q(self):
        return self.children[0]
    def get_latex_main(self):
        return f"\\left[ {self.children[0].get_latex()} \\right]"

class NodoParentesiGraffe(Nodo):
    def __init__(self, value=None, children=None, domain='R'):
        super().__init__(value, children, domain)
    def get_type(self):
        return "ParentesiGraffe"
    def operate(self):
        return self.children[0].value
    def operate_N(self):
        return self.children[0]
    def operate_Z(self):
        return self.children[0]
    def operate_Q(self):
        return self.children[0]
    def get_latex_main(self):
        return "\\left\{" + f" {self.children[0].get_latex()} " + "\\right\}"

class NodoAddizione(Nodo):
    def __init__(self, value=None, children=None, domain='R'):
        super().__init__(value, children, domain)
        self.precedence = 1
    def get_type(self):
        return "Addizione"
    def operate(self):
        return self.children[0].value + self.children[1].value
    def operate_N(self):
        return NodoNumero(self.children[0].value + self.children[1].value, id=self.id)
    def operate_Z(self):
        return NodoNumero(self.children[0].value + self.children[1].value, id=self.id)
    def operate_Q(self):
        n1, d1, n2, d2 = self.get_children_nums_and_dens()
        den = utilities.lcm(d1, d2)
        num = n1 * (den//d1) + n2 * (den//d2)
        ret = Nodo.reduce_frac(num, den)
        ret.id = self.id
        return ret
    def get_latex_main(self):
        return f"{self.children[0].get_latex()} + {self.children[1].get_latex()}"

class NodoSottrazione(Nodo):
    def __init__(self, value=None, children=None, domain='R'):
        super().__init__(value, children, domain)
        self.precedence = 1
    def get_type(self):
        return "Sottrazione"
    def operate(self):
        return self.children[0].value - self.children[1].value
    def operate_N(self):
        return NodoNumero(self.children[0].value - self.children[1].value, id=self.id)
    def operate_Z(self):
        return NodoNumero(self.children[0].value - self.children[1].value, id=self.id)
    def operate_Q(self):
        n1, d1, n2, d2 = self.get_children_nums_and_dens()
        den = utilities.lcm(d1, d2)
        num = n1 * (den//d1) - n2 * (den//d2)
        ret = Nodo.reduce_frac(num, den)
        ret.id = self.id
        return ret
    def get_latex_main(self):
        return f"{self.children[0].get_latex()} - {self.children[1].get_latex()}"

class NodoMoltiplicazione(Nodo):
    def __init__(self, value=None, children=None, domain='R'):
        super().__init__(value, children, domain)
        self.precedence = 2
    def get_type(self):
        return "Moltiplicazione"
    def operate(self):
        return self.children[0].value * self.children[1].value
    def operate_N(self):
        return NodoNumero(self.children[0].value * self.children[1].value, id=self.id)
    def operate_Z(self):
        return NodoNumero(self.children[0].value * self.children[1].value, id=self.id)
    def operate_Q(self):
        n1, d1, n2, d2 = self.get_children_nums_and_dens()
        num = n1 * n2
        den = d1 * d2
        ret = Nodo.reduce_frac(num, den)
        ret.id = self.id
        return ret
    def get_latex_main(self):
        return f"{self.children[0].get_latex()} \\times {self.children[1].get_latex()}"

class NodoDivisione(Nodo):
    def __init__(self, value=None, children=None, domain='R'):
        super().__init__(value, children, domain)
        self.precedence = 2
    def get_type(self):
        return "Divisione"
    def operate(self):
        return self.children[0].value / self.children[1].value
    def operate_N(self):
        return NodoNumero(self.children[0].value * self.children[1].value, id=self.id)
    def operate_Z(self):
        return NodoNumero(self.children[0].value * self.children[1].value, id=self.id)
    def operate_Q(self):
        n1, d1, n2, d2 = self.get_children_nums_and_dens()
        num = n1 * d2
        den = d1 * n2
        ret = Nodo.reduce_frac(num, den)
        ret.id = self.id
        return ret
    def get_latex_main(self):
        return f"{self.children[0].get_latex()} : {self.children[1].get_latex()}"

class NodoMenoUnario(Nodo):
    def __init__(self, value=None, children=None, domain='R'):
        super().__init__(value, children, domain)
        self.precedence = 3
    def get_type(self):
        return "MenoUnario"
    def operate(self):
        return -self.children[0].value
    def operate_N(self):
        raise exceptions.DomainException("Numeri relativi non ammessi in N!")
    def operate_Z(self):
        return NodoNumero(-self.children[0].value, id=self.id)
    def operate_Q(self):
        if self.children[0].get_type() == "Numero":
            self.children[0].value *= -1
        else:
            self.children[0].children[0].value *= -1
        return self.children[0]

    def get_latex_main(self):
        return f"- {self.children[0].get_latex()}"

class NodoFrazione(Nodo):
    def __init__(self, value=None, children=None, domain='R'):
        super().__init__(value, children, domain)
        self.precedence = 4
        if(len(self.children) < 2): return #colpa di tipo nodi in Semplificatore
        # rimuovo le parentesi da num e den
        if self.children[0].get_type() in tipo_parentesi:
            self.children[0] = self.children[0].children[0]
        if self.children[1].get_type() in tipo_parentesi:
            self.children[1] = self.children[1].children[0]
    def get_type(self):
        return "Frazione"
    def operate(self):
        return self.children[0].value / self.children[1].value
    def operate_N(self):
        raise exceptions.DomainException("Numeri frazionari non ammessi in N!")
    def operate_Z(self):
        raise exceptions.DomainException("Numeri frazionari non ammessi in Z!")
    def operate_Q(self):
        num, den = self.children[0], self.children[1]
        if num.get_type() == "Frazione" and den.get_type() == "Frazione":
            n_num = num.children[0].value * den.children[1].value
            n_den = num.children[1].value * den.children[0].value
        elif num.get_type() == "Frazione":
            n_num = num.children[0].value
            n_den = num.children[1].value * den.value
        elif den.get_type() == "Frazione":
            n_num = num.value * den.children[1].value
            n_den = den.children[0].value
        else:
            n_num, n_den = num.value, den.value
        ret = Nodo.reduce_frac(n_num, n_den)
        ret.id = self.id
        ret.leaf = True
        return ret
    def get_num_and_den(self):
        return self.children[0].value, self.children[1].value
    def get_latex_main(self):
        num = self.children[0].get_latex()
        den = self.children[1].get_latex()
        if self.children[1].value == 1:
            return str(num)
        return f"\\frac{{{num}}} {{{den}}}"

class NodoPotenza(Nodo):
    def __init__(self, value=None, children=None, domain='R'):
        super().__init__(value, children, domain)
        self.precedence = 5
        if(len(self.children) < 2): return #colpa di tipo nodi in Semplificatore
        # Non ho bisogno di nodi parentesi per base ed esponente!
        if self.children[0].get_type() in tipo_parentesi:
            self.children[0] = self.children[0].children[0]
        if self.children[1].get_type() in tipo_parentesi:
            self.children[1] = self.children[1].children[0]
    def get_type(self):
        return "Potenza"
    def operate(self):
        return self.children[0].value ** self.children[1].value
    def operate_N(self):
        return NodoNumero(self.children[0].value ** self.children[1].value, id = self.id)
    def operate_Z(self):
        return NodoNumero(self.children[0].value ** self.children[1].value, id = self.id)
    def operate_Q(self):
        # L'esponente è una frazione. Lo valuto passando attraverso un reale.
        # Rischio di perdere in precisione, ma semplifica le operazioni
        if self.children[1].get_type() == "Frazione":
            exp = Nodo.reduce_frac(
                self.children[1].children[0].value,
                self.children[1].children[1].value)
            self.children[1] = exp
            if exp.get_type() == "Frazione":
                self.children[1].value = self.children[1].operate()
        # Controllo se il denominatore è una frazione, e lo elevo.
        if self.children[0].get_type() == "Frazione":
            ret = NodoPotenza.raise_frac_at_pow(self.children[0], self.children[1].value)
        # Se la base è un numero intero, ma l'esponente è negativo, prima la
        # trasformo in frazione, poi opero (per evitare problemi con i reali).
        elif self.children[1].value < 0:
            ret = NodoPotenza.raise_frac_at_pow(
                NodoFrazione(children=[self.children[0], NodoNumero(1)],
                domain='Q'),
                self.children[1].value)
        # Base intero, esponente positivo
        else:
            value = self.children[0].value ** self.children[1].value
            if int(value) != value:
                raise exceptions.DomainException("Frazioni all'esponente non supportata!")
            ret = NodoNumero(value, id=self.id)
        return  ret
    def raise_frac_at_pow(frac, exp):
        if exp < 0:
            tmp = frac.children[0]
            frac.children[0] = frac.children[1]
            frac.children[1] = tmp
            exp *= -1
        num = frac.children[0].value ** exp
        den = frac.children[1].value ** exp
        if int(num) != num or int(den) != den:
            raise exceptions.DomainException("Frazione all'esponente non supportata!")
        frac.children[0].value = int(num)
        frac.children[1].value = int(den)
        return frac

    def get_latex_main(self):
        exp = self.children[1].get_latex()
        return f"{self.children[0].get_latex()} ^ {{{exp}}}"

class NodoNumero(Nodo):
    def __init__(self, value, id=-1, domain='R'):
        super().__init__(value, domain=domain)
        self.leaf = True
        self.id = id
    def get_type(self):
        return "Numero"
    def get_annotated(self):
        d = super().get_annotated()
        d['value'] = self.value
        return d
    def get_num_and_den(self):
        return self.value, 1
    def get_latex_main(self):
        return f"{self.value}"
