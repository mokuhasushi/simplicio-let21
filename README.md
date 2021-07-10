# PROGETTO LINGUAGGI E TRADUTTORI 2021
## Tirone Antonio

Le specifiche implementate sono:

* Dominio: **N, Z, Q, R**
* Parser: **Shunting Yard, notazione scientifica**
* Operazioni: **addizione, sottrazione, moltiplicazione, divisione, frazioni, potenze, segno unario -**
* Parentesizzazione: **Semplice, libera**
* Eccezioni: **Trattazione semplice**

La grammatica riconosciuta dal parser è

    E --> P {B P}
    P --> V | "(" E ")" | U P
    B --> "+" | "-" | "*" | ":" | "/" | "^"
    U --> "-" | "~"
    V --> (([0-9]+(\.[0-9]*)?)|(\.[0-9]+))(e-?[0-9]+)?

Le espressioni possono contenere **whitespace**, e possono essere terminate dal simbolo # (comunque aggiunto automaticamente).
I simboli corrispondenti alle operazioni sono +, -, *, :, /, ^, ~. Il simbolo *:* indica la divisione, il simbolo */* una frazione.

Solo il **meno unario** è implementato (il segno unario *+* no), ed è riconosciuto sia con il simbolo *-* sia con il simbolo *~*. Questo secondo simbolo è stato introdotto e mantenuto per gestire internamente la precedenza delle operazioni.

Per specificare una **base, esponente, numeratore o denominatore** complesso è necessario racchiuderli in delle parentesi (non importa il tipo). Queste saranno rimosse dalla rappresentazione interna.

E' possibile esprimere i numeri in **notazione scientifica**. In R sono sempre accettati, in N, Z, Q solo se rappresentano un intero (no conversione verso Q). Esempi di input accettati sono 1, 1.0, .1, 1., 1e1, 1.0E1, .1e1, 1.e1.\
Per assicurarmi di non aver commesso errori, aggiungo qui una spiegazione di come è costruita la regex per V, `(([0-9]+(\.[0-9]*)?)|(\.[0-9]+))(e-?[0-9]+)?`:

* `([0-9]+(\.[0-9]*)?)` corrisponde al match di uno o più numeri possibilmente seguiti da un `.` e 0 o più numeri. Match con 1, 1.0, 1.
* `(\.[0-9]+)` corrisponde al match di un punto seguito da uno o più numeri. Match con .1
* `(([0-9]+(\.[0-9]*)?)|(\.[0-9]+))` chiede che il numero inizi con una delle due opzioni precedenti
* `(e-?[0-9]+)?` corrisponde al match potenziale di `e` seguito o meno da `-` e da uno o più numeri. E' accettato anche `E`, sebbene non sia segnalato. Match con e1


Una chiamata di esempio:

`simplicio.string2latex("2 + 2", 'R')`

Se si desidera visualizzare l'albero generato dal parser, si può usare la funzione `node2tree(nodo)` del modulo *utilities*. Per questa visualizzazione viene usato il supporto di liblet.

### Problemi noti

Il problema dell'ordine di esecuzione è stato risolto cercando, all'inizio della risoluzione di ogni sottoalbero, i nodi di tipo potenza, frazione e meno unario. Quando questi vengono risolti si passa a svolgere i conti relativi alla radice. Le restanti operazioni sono gestite correttamente grazie alla struttura dell'albero.

**Un difetto minore introdotto da questo approccio sta nel fatto che catene di potenze, frazioni e meno unari vengono risolte un passaggio alla volta. Considerato che il supporto per i meno unari multipli non è richiesto dalle specifiche, e tra gli esempi forniti ve n'è uno in cui le frazioni sono risolte una alla volta, non si è provveduto a cercare una soluzione.**

Un altro problema noto è il costo in termini di tempo e memoria, che non dipende linearmente dalla lunghezza dell'input. Infatti per via della struttura binaria dell'albero e della scelta di non salvare le informazioni sui sottoalberi, è necessario a ogni passo risolutivo controllare se tutti i nodi nel sottoalbero sono dello stesso tipo, al fine di risolverli in un unico step. Questo introduce nella complessità una dipendenza dalla grandezza dei sottoalberi: infatti un'espressione senza parentesi e con operazioni di vario tipo sarà più lenta di un input contenente diverse parentesi (sottoalberi risolti indipendentemente).
I tempi di risoluzioni sono comunque parsi ragionevoli sulla macchina di sviluppo, con un input "buono" di anche 1000 operazioni risolto in pochi secondi, mentre uno cattivo di circa 300 operazioni risolto nello stesso tempo. (sono presenti alcuni test al riguardo).

### Qualche dettaglio implementativo

L'output prodotto è un albero in cui le precedenze degli operatori sono interpretate correttamente. Queste precedenze sono lette da un dizionario, rendendo semplici eventuali estensioni o modifiche.

Per la rappresentazione degli alberi è stato scelto un albero binario, definito nella classe `Nodo` e nelle sottoclassi relative a ciascuna operazione. Oltre a mantenere i dati, questa struttura permette di chiamare alcuni metodi:
* `numera(self,n)`: che numera ricorsivamente i nodi in modo da permettere una ricerca binaria veloce;
* `solve_step(self)`: risolve un passaggio dell'albero su cui è chiamato. Cerca un nodo che abbia solo foglie come figli e lo risolve, aggiornando ricorsivamente i nodi. Controlla inoltre se tutti i nodi eseguibili condividono lo stesso tipo di operazione, nel qual caso li risolve in un unico step. Inoltre colora di verde il nodo risolto;
* `operate_X(self)`: definiti per ciascun dominio `X \in R, N, Z, Q` e per ciascun operazione, risolvono il nodo assumendo che i figli siano foglie;
* `get_latex(self)`: ritorna ricorsivamente la rappresentazione in codice LaTeX dell'albero che ha il nodo come radice.
A questi si aggiungono altri metodi di utilità.

Per l'effettiva risoluzione step-by-step dell'espressione viene usata la classe `Semplificatore`. Vengono dapprima cercate tutte le parentesi, con una visita depth first in post ordine, in modo da essere sicuri che parentesi più in profondità nell'albero siano "raccolte" prima. Quindi, seguendo l'ordine delle parentesi (tonde, poi quadre, poi graffe) vengono risolti i sottoalberi. Infine si risolve la radice. Nessun controllo viene fatto circa l'ordine delle parentesi.

Il codice latex viene ritornato all'interno di un ambiente *align*, sotto forma di stringa.

Nonostante l'uso abbastanza intenso di ricorsione, le prestazioni rimangono buone (qualche secondo per input dell'ordine di grandezza di 10^3).

Per testare il codice si è fatto uso di `pytest` e `coverage`, oltre all'uso di notebook jupyter per visualizzare il codice latex prodotto. 
