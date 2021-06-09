# PROGETTO LINGUAGGI E TRADUTTORI 2021
## Tirone Antonio

Inizio trascrivendo le specifiche concordate il 08-06-21. In grassetto evidenzio **le specifiche** che il progetto si pone di raggiungere necessariamente, in corsivo *le aggiunte* desiderabili. (Se legge questo readme prima di una versione più avanzata e revisionata, e nota qualche errore, me lo faccia sapere)

* Dominio: **Q**, *scelta parametrica tra N, Z, Q, R*
* Parser: **Shunting Yard**
* Operazioni: **addizione, sottrazione, moltiplicazione, divisione, frazioni, potenze, segno unario**
* Parentesizzazione: **Semplice, libera**
* Eccezioni: **Trattazione semplice**

Segno tre punti da chiedere al prossimo colloquio, in quanto mi pare non ne abbiamo discusso: *accorpamento di più operazioni dello stesso tipo consecutive*, *accorpamento di segni unari*, *simbolo di terminazione (#)*.

A seguito di quanto detto, sto valutando se usare liblet o meno. Un idea che mi è sorta è di definire la mia struttura, e creare un modulo di utilità per visualizzare grazie a liblet gli alberi.

P.S: mi sono preso la libertà di utilizzare questo README per scrivere anche osservazioni e note che normalmente non dovrebbero trovare posto qui. Chiaramente nella versione finale spariranno. Se per qualche motivo la cosa dovesse rappresentare un problema, me lo comunichi.
