# PROGETTO LINGUAGGI E TRADUTTORI 2021
## Tirone Antonio

Al momento le specifiche implementate sono: 

* Dominio: **Q, R**
* Parser: **Shunting Yard**
* Operazioni: **addizione, sottrazione, moltiplicazione, divisione, frazioni, potenze, segno unario -**
* Parentesizzazione: **Semplice, libera**
* Eccezioni: **Trattazione semplice**

Le espressioni possono contenere whitespace, e possono essere terminate dal simbolo # o meno.
I simboli corrispondenti alle operazioni sono +, -, *, :, /, ^, ~. Il simbolo *:* indica la divisione, il simbolo */* una frazione. 

Solo il meno unario è implementato (il segno unario *+* no), ed è riconosciuto sia con il simbolo *-* sia con il simbolo *~*. Questo secondo simbolo è stato introdotto e mantenuto per gestire internamente la precedenza delle operazioni. 

Per specificare una base, esponente, numeratore o denominatore complesso è necessario racchiuderli in delle parentesi (non importa il tipo). Queste saranno rimosse dalla visualizzazione.

La scelta del dominio è parametrica, ma al momento sono implementati solo *Q* e *R*. 
Una chiamata di esempio:

`string2latex("2 + 2", 'R')`

Se si desidera visualizzare l'albero generato dal parser, si può usare la funzione `nodo2tree(nodo)` del modulo *utilities*. Per questa visualizzazione viene usato il supporto di liblet.

### Qualche dettaglio implementativo
La grammatica riconosciuta dal parser è

    E --> P {B P}
    P --> v | "(" E ")" | U P
    B --> "+" | "-" | "*" | ":" | "/" | "^" 
    U --> "-" | "~"
    
L'output prodotto è un albero in cui le precedenze degli operatori sono interpretate correttamente. Queste precedenze sono lette da un dizionario, rendendo semplici eventuali estensioni o modifiche. 

Per la rappresentazione degli alberi è stato scelto un albero binario, definito nella classe `Nodo` e nelle sottoclassi relative a ciascuna operazione. Oltre a mantenere i dati, questa struttura permette di chiamare alcuni metodi: 
* `numera(self,n)`: che numera ricorsivamente i nodi in modo da permettere una ricerca binaria veloce;
* `solve_step(self)`: risolve un passaggio dell'albero su cui è chiamato. Cerca un nodo che abbia solo foglie come figli e lo risolve, aggiornando ricorsivamente i nodi. Controlla inoltre se tutti i nodi eseguibili condividono lo stesso tipo di operazione, nel qual caso li risolve in un unico step. Inoltre colora di verde il nodo risolto.;
* `operate(self)` e `operate_Q(self)`: definiti per ciascuna operazione, risolvono il nodo assumendo che i figli siano foglie;
* `get_latex(self)`: ritorna ricorsivamente la rappresentazione in codice LaTeX dell'albero che ha il nodo come radice.
A questi si aggiungono altri metodi di utilità. 

Per l'effettiva risoluzione step-by-step dell'espressione viene usata la classe `Semplificatore`. Vengono dapprima cercate tutte le parentesi, con una visita depth first in post ordine, in modo da essere sicuri che parentesi più in profondità nell'albero siano "raccolte" prima. Quindi, seguendo l'ordine delle parentesi (tonde, poi quadre, poi graffe) vengono risolti i sottoalberi. Infine si risolve la radice. Nessun controllo viene fatto circa l'ordine delle parentesi

Il codice latex viene ritornato all'interno di un ambiente *align*, sotto forma di stringa. 

Nonostante l'uso abbastanza intenso di ricorsione, le prestazioni rimangono buone (qualche secondo per input dell'ordine di grandezza di 10^3). 
