import shuntingyard as sy
import semplificatore as smp

def string2latex(s):
    n = sy.parse_expr(s, 'Q')
    simpler = smp.Semplificatore(n)
    texts = simpler.solve()
    text = '\n\\\\&'.join(texts)
    text = "\\begin{align}" + text + "\n\end{align}"
    return text
