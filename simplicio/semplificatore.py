import nodi
import exceptions
from utilities import list_diff

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
        "value" : nodi.NodoNumero(0).get_type(),
        "relvalue" : "NumeroRelativo"
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
            Semplificatore.node_types['value'] : [],
            Semplificatore.node_types['relvalue'] : []
        }
        return Semplificatore.get_nodes_type_rec(tree, nt2nid)
    def get_nodes_type_rec(tree, nt2nid):
        for c in tree.children:
            Semplificatore.get_nodes_type_rec(c, nt2nid)
        nt2nid[tree.get_type()].append(tree.id)
        return nt2nid
    def get_pfm_nodes(self, tree):
        nt2nid = Semplificatore.get_nodes_type(tree)
        to_solve = []
        # Per la struttura generata da shuntingyard dovrebbe bastare
        for t in ['pow', 'frac', 'meno']:
            to_solve += nt2nid[self.node_types[t]]
        return to_solve

    # Metodo per la risoluzione di un nodo
    # Ritorna il codice latex per ogni passaggio, e il nodo finale
    def solve_node(self, tree, to_solve):
        texts = []
        # inizio a risolvere il primo nodo. Lo cerco nel sottoalbero corrente.
        # Questo migliora le prestazioni (non devo cercare a partire dalla radice)
        # ma implica che il nodo radice del sottoalbero andrà alla fine rimpiazzato
        parent, solving = self.find_node(to_solve[0], tree)
        # Finchè il nodo che stiamo risolvendo non è una foglia
        while not solving.leaf:
            # Riquadro in rosso l'operazione da svolgere
            solving.box_leaf()
            # Aggiungo la rappresentazione latex (e implicitamente rimuovo
            # i boxing verdi precedenti)
            texts.append(self.root.get_latex())
            # Risolvo uno step. Il valore di ritorno è il nodo aggiornato o
            # un nuovo nodo in caso il risultato sia una foglia, più una lista
            # contenente gli ids dei nodi risolti
            solving, solved_ids = solving.solve_step()
            # aggiorno la lista dei nodi da risolvere
            to_solve = list_diff(to_solve, solved_ids)
            # Se il nodo che stiamo risolvendo è una foglia, ho finito. Passo
            # al successivo nella lista dei nodi da risolvere, dopo aver aggiornato
            # l'albero
            if solving.leaf:
                # Questo caso serve per la risoluzione della radice
                if self.root.id == solving.id:
                    self.root = solving
                # Il nodo risolto era il figlio sx del padre
                elif parent.children[0].id == solving.id:
                    parent.children[0] = solving
                # era il figlio dx del padre
                elif len(parent.children) > 1 and parent.children[1].id == solving.id:
                    parent.children[1] = solving
                # caso particolare, ottenuto mettendo tutta l'espressione
                # dentro le parentesi. il metodo trova nodo ritorna
                # par = cur = root. I test sui figli ovviamente falliscono
                # NON DOVREBBE PIU' SERVIRE. TUTTAVIA NON HO AVUTO MODO DI PENSARCI
                # A FONDO
                # elif parent.id == solving.id:
                    # parent = solving
                # Come dice l'errore, non dovrebbe mai accadere. Tuttavia
                # è stata lasciata la riga come promemoria. Durante lo sviluppo
                # è accaduto che venisse sollevata
                else:
                    raise Exception("Non dovrebbe mai succedere... Semplificatore")
                if len(to_solve) > 0:
                    parent, solving = self.find_node(to_solve[0])
        return solving, texts

    # risolve tutta l'equazione, a partire dalle parentesi
    def solve(self):
        # E' stato deciso di lasciare come prima stringa l'espressione iniziale
        texts = ["&"+self.root.get_latex()]
        # Prima si eseguono le parentesi, nell'ordine tonde, quadre, graffe
        for nodo_id in self.parenthesis_ordered:
            p_par, p_cur = self.find_node(nodo_id)
            p_cur.colore = "blue"
            # Per risolvere nell'ordine corretto, cerco i nodi di tipo potenza,
            # frazione e meno unario. mul, div, add, sub sono poi gestiti
            # automaticamente grazie alla struttura dell'albero
            to_solve = self.get_pfm_nodes(p_cur)
            to_solve += [p_cur.children[0].id]

            remove = []
            for i in range(len(to_solve) - 1):
                if abs(to_solve[i+1] - to_solve[i]) == 1:
                    remove += [to_solve[i]]
            to_solve = list_diff(to_solve, remove)

            solved, txts = self.solve_node(p_cur, to_solve)
            texts += txts
            # elimino la parentesi una volta che è stat risolta
            if p_par.children[0].id == p_cur.id:
                p_par.children[0] = solved
            # La parentesi era il figlio dx del padre
            elif len(p_par.children) > 1 and p_par.children[1].id == p_cur.id:
                p_par.children[1] = solved
            # caso particolare, ottenuto mettendo tutta l'espressione
            # dentro le parentesi. il metodo trova nodo ritorna
            # par = cur = root. I test sui figli ovviamente falliscono
            elif p_par.id == p_cur.id:
                p_par = solved

        # Ho finito con le parentesi, risolvo la radice, con la stessa logica
        to_solve = self.get_pfm_nodes(self.root)
        to_solve += [self.root.id]
        remove = []
        for i in range(len(to_solve) - 1):
            if abs(to_solve[i+1] - to_solve[i]) == 1:
                remove += [to_solve[i]]
        to_solve = list_diff(to_solve, remove)

        _, txts = self.solve_node(self.root, to_solve)

        texts += txts
        texts.append(self.root.get_latex())

        return texts

    # Questo metodo fa uso della numerazinoe binaria intelligente dell'albero
    def find_node(self, id, tree=None):
        if tree is None:
            tree = self.root
        par, cur = tree, tree
        if id == tree.id :
            return par, cur
        # albero binario, tutti i nodi a sx hanno id < del padre, a dx >
        if id < par.id:
            cur = par.children[0]
        else:
            cur = par.children[1]
        while id != cur.id:
            # print(id, par.id, cur.id)
            # print("par: ",par,"\n")
            par = cur
            if id < par.id:
                cur = par.children[0]
            else:
                cur = par.children[1]
        return par,cur
