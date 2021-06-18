import shuntingyard as sy
import semplificatore as smp

def string2latex(s, domain='R'):
    n = sy.parse_expr(s, domain)
    simpler = smp.Semplificatore(n)
    texts = simpler.solve()
    text = '\n\\\\&'.join(texts)
    text = "\\begin{align}" + text + "\n\end{align}"
    return text
