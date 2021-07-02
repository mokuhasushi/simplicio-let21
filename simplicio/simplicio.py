import shuntingyard as sy
import semplificatore as smp

def string2latex(s, domain='R'):
    # Parsing dell'espressione e produzione dell'albero
    n = sy.parse_expr(s, domain)
    # Preprocessing dell'albero: numerazione nodi e ricerca di nodi parentesi
    simpler = smp.Semplificatore(n)
    # Effettiva risoluzione, ritorna una lista con uno step per elemento
    texts = simpler.solve()
    text = '\n\\\\&'.join(texts)
    text = "\\begin{align}" + text + "\n\end{align}"
    return text
