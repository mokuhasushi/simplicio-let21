import nodi
import exceptions

class Semplificatore():
    node_types = {
        "nodo"  : nodi.Nodo().get_type(),
        "tonde" : nodi.NodoParentesiTonde().get_type(),
        "quadre": nodi.NodoParentesiQuadre().get_type(),
        "graffe": nodi.NodoParentesiGraffe().get_type(),
        "add"   : nodi.NodoAddizione().get_type(),
        "sub"   : nodi.NodoSottrazione().get_type(),
        "mul"   : nodi.NodoMoltiplicazione().get_type(),
        "div"   : nodi.NodoDivisione().get_type(),
        "meno"  : nodi.NodoMenoUnario().get_type(),
        "frac"  : nodi.NodoFrazione().get_type(),
        "pow"   : nodi.NodoPotenza().get_type(),
        "value" : nodi.NodoNumero(0).get_type()
    }
    def __init__(self, root):
        # dizionario: tipo -> nodi di quel tipo
        self.root = root
        self.root.numera(0)
        node_types2node_id = Semplificatore.get_nodes_type(self.root)
        self.parenthesis_ordered = []
        self.parenthesis_ordered += (node_types2node_id[self.node_types['tonde']])
        self.parenthesis_ordered += (node_types2node_id[self.node_types['quadre']])
        self.parenthesis_ordered += (node_types2node_id[self.node_types['graffe']])
    # Percorre ricorsivamente l'albero e salva i nodi per tipo
    # Per risolvere la parentesizzazione libera è stato sufficiente recuperare
    # i nodi con una visita in post ordine
    def get_nodes_type(tree):
        nt2nid = {
            Semplificatore.node_types['nodo'] : [],
            Semplificatore.node_types['tonde'] : [],
            Semplificatore.node_types['quadre'] : [],
            Semplificatore.node_types['graffe'] : [],
            Semplificatore.node_types['add'] : [],
            Semplificatore.node_types['sub'] : [],
            Semplificatore.node_types['mul'] : [],
            Semplificatore.node_types['div'] : [],
            Semplificatore.node_types['meno'] : [],
            Semplificatore.node_types['frac'] : [],
            Semplificatore.node_types['pow'] : [],
            Semplificatore.node_types['value'] : []
        }
        return Semplificatore.get_nodes_type_rec(tree, nt2nid)
    def get_nodes_type_rec(tree, nt2nid):
        for c in tree.children:
            Semplificatore.get_nodes_type_rec(c, nt2nid)
        nt2nid[tree.get_type()].append(tree.id)
        return nt2nid
    # risolve tutta l'equazione, a partire dalle parentesi
    def solve(self):
        texts = ["&"+self.root.get_latex()]
        tree = self.root
        for nodo_id in self.parenthesis_ordered:
            par, cur = self.trova_nodo(nodo_id)
            cur.colore = "blue"
            # texts.append(self.root.get_latex())
            solving = cur.children[0]
            while not solving.leaf:
                solving.box_leaf()
                texts.append(self.root.get_latex())
                solving = solving.solve_step()
                # Se il nodo che stiamo risolvendo è una foglia, ho finito
                if solving.leaf:
                    if par.children[0].id == cur.id:
                        par.children[0] = solving
                    elif len(par.children) > 1 and par.children[1].id == cur.id:
                        par.children[1] = solving
                    # caso particolare, ottenuto mettendo tutta l'espressione
                    # dentro le parentesi. il metodo trova nodo ritorna
                    # par = cur = root. I test sui figli ovviamente falliscono
                    elif par.id == cur.id:
                        par = solving
                    else:
                        raise Exception("Non dovrebbe mai succedere... Semplificatore")

            cur.colore = ""
        solving = self.root
        while not solving.leaf:
            solving.box_leaf()
            texts.append(self.root.get_latex())
            solving = solving.solve_step()
            if solving.leaf:
                self.root = solving
        texts.append(self.root.get_latex())
        return texts
    def trova_nodo(self, id):
        par, cur = self.root, self.root
        if id == self.root.id :
            return par, cur
        # assumo albero binario
        if id < par.id:
            cur = par.children[0]
        else:
            cur = par.children[1]
        while id != cur.id:
            par = cur
            if id < par.id:
                cur = par.children[0]
            else:
                cur = par.children[1]
        return par,cur
