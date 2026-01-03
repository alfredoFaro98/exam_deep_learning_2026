# Step 0: Context and Objectives

## 1. Obiettivo Reale (Goal)
L'obiettivo di questo progetto è sviluppare un modello di **Deep Learning** capace di simulare la **Dinamica Molecolare (MD)** di una proteina. 
Nello specifico:
- Vogliamo predire la posizione futura degli atomi (o la loro traiettoria) basandoci sulla storia passata.
- Vogliamo un modello che sia computazionalmente più efficiente delle simulazioni fisiche classiche (basate su campi di forza e leggi di Newton).

## 2. Perché lo facciamo?
Le simulazioni MD classiche sono potentissime ma richiedono **tempi di calcolo enormi** (giorni o settimane su supercomputer) per simulare pochi microsecondi di vita della proteina. 
Un modello neurale (surrogate model) ben addestrato può accelerare questo processo di ordini di grandezza, permettendo:
- **Drug Discovery Rapida**: Capire come un farmaco si lega a una proteina in pochi secondi.
- **Biotech**: Progettare enzimi più efficienti.

## 3. Le Sfide del Caso d'Uso
Questo non è un semplice problema di regressione su serie temporali. Le difficoltà principali sono:

1.  **Alta Dimensionalità**: Abbiamo 138 atomi, ciascuno con 3 coordinate (X, Y, Z). Lo spazio degli stati ha 414 dimensioni, tutte correlate tra loro.
2.  **Correlazioni non Lineari**: Gli atomi interagiscono in modo complesso (legami covalenti, forze di Van der Waals, elettrostatica). Il modello deve "imparare la fisica" dai dati.
3.  **Memoria a Lungo Termine**: La configurazione attuale dipende dalla storia passata (ripiegamenti, inerzia). Ecco perché una semplice rete Feed-Forward non basta; servono **RNN** o **CNN 1D**.
4.  **Caoticità**: Piccole perturbazioni iniziali possono portare a traiettorie molto diverse (Effetto farfalla). Il modello deve essere robusto.

## 4. Disponibilità Esperti
Gli esperti del dominio (biologi, chimici computazionali) sono una risorsa cruciale. In caso di dubbi sulla validità fisica di una predizione (es. due atomi che si sovrappongono o distanze di legame assurde), possiamo e dobbiamo consultarli.
