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
    V --> (([0-9]+(\.[0-9]*)?)|(\.[0-9]+))(e[0-9]+)?

Le espressioni possono contenere **whitespace**, e possono essere terminate dal simbolo # (comunque aggiunto automaticamente).
I simboli corrispondenti alle operazioni sono +, -, *, :, /, ^, ~. Il simbolo *:* indica la divisione, il simbolo */* una frazione.

Solo il **meno unario** è implementato (il segno unario *+* no), ed è riconosciuto sia con il simbolo *-* sia con il simbolo *~*. Questo secondo simbolo è stato introdotto e mantenuto per gestire internamente la precedenza delle operazioni.

Per specificare una **base, esponente, numeratore o denominatore** complesso è necessario racchiuderli in delle parentesi (non importa il tipo). Queste saranno rimosse dalla rappresentazione interna.

E' possibile esprimere i numeri in **notazione scientifica**. In R sono sempre accettati, in N, Z, Q solo se rappresentano un intero (no conversione verso Q). Esempi di input accettati sono 1, 1.0, .1, 1., 1e1, 1.0E1, .1e1, 1.e1.\
Per assicurarmi di non aver commesso errori, aggiungo qui una spiegazione di come è costruita la regex per V, `(([0-9]+(\.[0-9]*)?)|(\.[0-9]+))(e[0-9]+)?`:

* `([0-9]+(\.[0-9]*)?)` corrisponde al match di uno o più numeri possibilmente seguiti da un `.` e 0 o più numeri. Match con 1, 1.0, 1.
* `(\.[0-9]+)` corrisponde al match di un punto seguito da uno o più numeri. Match con .1
* `(([0-9]+(\.[0-9]*)?)|(\.[0-9]+))` chiede che il numero inizi con una delle due opzioni precedenti
* `(e[0-9]+)?` corrisponde al match potenziale di `e` seguito da uno o più numeri. E' accettato anche `E`, sebbene non sia segnalato. Match con e1


Una chiamata di esempio:

`simplicio.string2latex("2 + 2", 'R')`

Se si desidera visualizzare l'albero generato dal parser, si può usare la funzione `node2tree(nodo)` del modulo *utilities*. Per questa visualizzazione viene usato il supporto di liblet.

### Problemi noti
Rispetto alle specifiche richieste, il solo problema noto riguarda l'ordine di esecuzione delle operazioni. Infatti, benchè la computazione sia corretta, puù capitare che operazioni con un ordine di precedenza più basso vengano eseguite prima di altre con un ordine più alto. \
Espressione di esempio: 1 + 2^3 + 12:3. In questo caso l'operazione 12:3 viene eseguita prima di 2^3\
Questo problema è dovuto al fatto che la maggior parte delle funzioni usate non hanno come scopo la modifica dell'albero, ovvero con poche eccezioni non vengono salvate informazioni sul tipo di operazioni corrispondenti ai nodi dei sottoalberi. L'ordine corretto di esecuzione è assicurato dalla struttura dell'albero generato dal parser (shunting yard), che interpreta correttamente le associatività e le precedenza delle operazioni.\
Vengono inizialmente cercate le parentesi, e queste sono salvate e risolte nella maniera corretta, ma non si salvano e utilizzano informazioni sui loro sottoalberi. L'unico controllo effettuato è sui figli diretti, che permette di evitare situazioni del tipo: 1 + 1 + 1 * 2, in cui altrimenti verrebbe prima risolta l'addizione sinistra, poi la moltiplicazione e infine l'addizione. Con il controllo si ottiene invece la risoluzione delle due addizioni in un singolo passo. Questo controllo è sufficiente (grazie alla struttura dell'albero generato) per una situazione simile in cui vi è un numero arbitrario di somme o differenze (ma la cosa resta valida per le altre operazioni).

<<<<<<< HEAD
Una soluzione a questo problema che è stata pensata prevede, nel momento in cui si va a risolvere una parentesi o la radice, di salvare tutti i tipi di nodi nel sottoalbero, ed eseguire in ordine di precedenza le operazioni. TENTATIVO IN CORSO, ultima cosa prima della consegna.
=======
Una soluzione a questo problema che è stata pensata prevede, nel momento in cui si va a risolvere una parentesi o la radice, di salvare tutti i tipi di nodi nel sottoalbero, ed eseguire in ordine di precedenza le operazioni. Tuttavia questo richiede alcune modifiche non banali al codice. 
>>>>>>> fb5698de16bbf601b598689ebbf83a1d55cb0584

Un altro problema noto è il costo in termini di tempo e memoria, che non dipende linearmente dalla lunghezza dell'input. Infatti per via della struttura binaria dell'albero e della scelta di non salvare le informazioni sui sottoalberi, è necessario a ogni passo risolutivo controllare se tutti i nodi nel sottoalbero sono dello stesso tipo, al fine di risolverli in un unico step. Questo introduce nella complessità una dipendenza dalla grandezza dei sottoalberi: infatti un'espressione senza parentesi e con operazioni di vario tipo sarà più lenta di un input contenente diverse parentesi (sottoalberi risolti indipendentemente).
I tempi di risoluzioni sono comunque parsi ragionevoli sulla macchina di sviluppo, con un input "buono" di anche 1000 operazioni risolto in pochi secondi, mentre uno cattivo di circa 300 operazioni risolto nello stesso tempo. (sono presenti alcuni test al riguardo)

### Qualche dettaglio implementativo

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
