import nodi
import exceptions

class Semplificatore():
    # Questo dizionario mi è servito all'inizio quando non ero sicuro di che nomi
    # dare ai tipi. Mi pare comunque un bel disaccoppiamento, quindi ho deciso di
    # lasciarlo
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
    # i nodi con una visita in post ordine. E' stato aggiunta una funzione di
    # aiuto per rendere il metodo statico
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
        # E' stato deciso di lasciare come prima stringa l'espressione iniziale
        texts = ["&"+self.root.get_latex()]
        # Prima si eseguono le parentesi, nell'ordine tonde, quadre, graffe
        for nodo_id in self.parenthesis_ordered:
            par, cur = self.trova_nodo(nodo_id)
            cur.colore = "blue"
            # Le parentesi hanno sempre un solo figlio
            solving = cur.children[0]
            # Finchè il nodo che stiamo risolvendo non è una foglia
            while not solving.leaf:
                # Riquadro in rosso l'operazione da svolgere
                solving.box_leaf()
                # Aggiungo la rappresentazione latex (e implicitamente rimuovo
                # i boxing verdi precedenti)
                texts.append(self.root.get_latex())
                # Risolvo uno step. Il valore di ritorno è il nodo aggiornato o
                # un nuovo nodo in caso il risultato sia una foglia
                solving = solving.solve_step()
                # Se il nodo che stiamo risolvendo è una foglia, ho finito
                if solving.leaf:
                    # La parentesi era il figlio sx del padre
                    if par.children[0].id == cur.id:
                        par.children[0] = solving
                    # La parentesi era il figlio dx del padre
                    elif len(par.children) > 1 and par.children[1].id == cur.id:
                        par.children[1] = solving
                    # caso particolare, ottenuto mettendo tutta l'espressione
                    # dentro le parentesi. il metodo trova nodo ritorna
                    # par = cur = root. I test sui figli ovviamente falliscono
                    elif par.id == cur.id:
                        par = solving
                    # Come dice l'errore, non dovrebbe mai accadere. Tuttavia
                    # è stata lasciata la riga come promemoria
                    else:
                        raise Exception("Non dovrebbe mai succedere... Semplificatore")
        # Ho finito con le parentesi, risolvo la radice, con la stessa logica
        solving = self.root
        while not solving.leaf:
            solving.box_leaf()
            texts.append(self.root.get_latex())
            solving = solving.solve_step()
            if solving.leaf:
                self.root = solving
        texts.append(self.root.get_latex())
        return texts

    # Questo metodo fa uso della numerazinoe binaria intelligente dell'albero
    def trova_nodo(self, id):
        par, cur = self.root, self.root
        if id == self.root.id :
            return par, cur
        # albero binario, tutti i nodi a sx hanno id < del padre, a dx > 
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
