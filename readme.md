---
bibliography:
- documentazione.bib
nocite: '[@*]'
---

ALMA MATER STUDIORUM -- UNIVERSITÀ DI BOLOGNA\

SCUOLA DI INGEGNERIA E ARCHITETTURA\
Dipartimento di Informatica - Scienza e Ingegneria\
DISI\
**Corso di Laurea magistrale in ingegneria informatica**\
**Progetto**\
di\
*Sistemi Digitali M*\
**Stalker-bot**\

**Professori:\
Prof. Stefano Mattoccia\
Prof. Matteo Poggi**

**Autori:\
Davide Di Molfetta\
Lorenzo Venerandi\
**

**Anno Accademico 2022-2023**

Abstract {#abstract .unnumbered}
========

Stalker-bot è un piccolo robot mobile, cingolato, controllato da un
Raspberry Pi 4B che comunica con un Arduino Nano. Il suo compito è
quello di unire la potenza del riconoscimento facciale all'efficacia dei
dispositivi embedded. Grazie ad una camera e ad una prima fase di
addestramento in cui Stalker-bot impara a riconoscere una specifica
persona (proprietario), egli è in grado di individuare la posizione del
volto e di seguirne i movimenti.

Introduzione {#introduzione .unnumbered}
============

Motivazioni {#motivazioni .unnumbered}
-----------

Le motivazioni dietro la realizzazione di \"Stalker-bot\" sono
principalmente legate alla volontà di acquisire conoscenze e competenze
per l'integrazione tra più sistemi embedded e principi di machine
learning e computer vision. Per poter affrontare questo progetto è stato
necessario acquisire una maggiore dimestichezza nell'utilizzo di
strumenti software e hardware coinvolti. Nello specifico, OpenCV si è
rivelato fondamentale per la realizzazione in prima battuta
dell'addestramento e in secondo luogo del riconoscimento facciale .

Riconoscimento facciale {#riconoscimento-facciale .unnumbered}
-----------------------

Il riconoscimento facciale è una tecnica molto diffusa al giorno d'oggi
che permette di individuare e riconoscere volti umani. Questa tecnica
sottintende la capacità di individuare la presenza e la posizione di
determinati oggetti all'interno di un'immagine o di un video. Questa
sotto-capacità è conosciuta anche come \"object-detection\". Grazie
all'object detection, spesso viene segnalata la posizione dell'oggetto,
all'interno dell'immagine o del video, tramite una bounding box, ovvero
un rettangolo che circonda l'oggetto.

Contenuti {#contenuti .unnumbered}
---------

Questo progetto descrive il flusso di lavoro per lo sviluppo di un
piccolo robot mobile in grado, mediante una camera e uno stream video
fornito da essa, di: imparare come è fatto il volto del suo proprietario
(anche più di uno), riconoscere quest'ultimo e seguire i movimenti del
suo volto. In prima battuta è stato necessario scegliere i sistemi
embedded più opportuni; in secondo luogo sono stati selezionati tutti i
componenti elettronici da coinvolgere; successivamente è stato
sviluppato il software per addestrare il robot a riconoscere il suo
proprietario e per riconoscimento durante uno flusso video; infine, dopo
aver effettuato una serie di test soddisfacenti, ci si è occupati di
creare la struttura fisica che dovesse contenere il tutto: la scelta è
ricaduta sulla stampa 3D.

Organizzazione {#organizzazione .unnumbered}
--------------

Nel primo capitolo viene riportata una descrizione della libreria
utilizzata per la realizzazione dell'addestramento e del riconoscimento
facciale. Nel secondo capitolo, invece, viene prima fornita una
panoramica su tutti i componenti utilizzati per la realizzazione di
questo progetto, e successivamente viene riportata una descrizione più
dettagliata dei principali componenti. Nel terzo capitolo viene prima
descritta la struttura del robot, in particolare vengono mostrati i
collegamenti tra i vari componenti elettronici e sono riportati i vari
elementi che compongono la scocca del robot. In fondo a questo capitolo
viene anche mostrato come è stato assemblato il tutto. Nel quarto
capitolo viene riportato e commentato come è stato realizzato lato
software l'addestramento, il riconoscimento e come viene controllato lo
spostamento del robot. Infine, vengono anche fatte delle considerazioni
su eventuali sviluppi futuri.

Software
========

OpenCV
------

La libreria open source OpenCV (Open Source Computer Vision) offre la
possibilità di elaborare immagini ed è un ottimo supporto per la
computer vision. Essa è disponibile per diversi sistemi operativi tra
cui Linux, Windows, macOS, Android e iOS. OpenCV è scritta
principalmente in C++, ma ha anche interfacce per Python, Java e MATLAB.
Questa libreria offre molte funzionalità per l'elaborazione delle
immagini, come il rilevamento dei bordi, la correzione della
distorsione, la segmentazione e la ricostruzione 3D. Inoltre, OpenCV
include anche algoritmi di computer vision per il rilevamento dei volti,
il tracciamento e la classificazione degli oggetti. OpenCV può essere
utilizzato per l'object detection, ovvero l'identificazione e la
localizzazione degli oggetti all'interno di un'immagine o di un video.
Grazie alll'object detection, con OpenCV è possibile anche effettuare
rilevamento dei volti. Per utilizzare OpenCV per l'object detection, è
necessario prima definire il modello che deve essere utilizzato per il
rilevamento degli oggetti. Questo può essere fatto addestrando un
classificatore di immagini con un dataset di immagini. Ci sono anche
modelli pre-addestrati disponibili online, che possono essere scaricati
e utilizzati direttamente con OpenCV. Una volta che il modello è pronto,
OpenCV viene utilizzato per caricare un'immagine o un video e passare
ogni frame attraverso il modello di rilevamento degli oggetti. Il
modello identificherà gli oggetti nell'immagine o nel video, restituendo
le coordinate della bounding box che circonda l'oggetto. Queste
coordinate possono quindi essere utilizzate per disegnare la bounding
box sull'immagine o sul video in modo da evidenziare gli oggetti
identificati. E anche possibile utilizzare queste coordinate per
eseguire ulteriori analisi sugli oggetti identificati, ad esempio per
determinare la loro posizione.

Elettronica ed assemblaggio
===========================

Hardware
--------

In questo capitolo verrà elencata la lista di componenti hardware
utilizzati per la costruzione di Stalker-Bot.

### Raspberry Pi 4B {#raspberry-pi-4b .unnumbered}

r0.35
![image](images/components/raspberry-pi-4.png){width="0.85\\linewidth"}

Il Raspberry è un computer in miniatura sviluppato e prodotto dalla
**Raspberry pi Foundation**. Si tratta di un computer a scheda singola
dotato di un SoC ARM prodotto da Broadcom.\
In questo progetto abbiamo utilizzato la versione 4B, l'ultima
rilasciata dalla casa produttrice e con le seguenti caratteristiche:

-   **CPU** -- Broadcom BCM2711, Quad core Cortex-A72 (ARM v8) 64-bit
    SoC 1.8GHz

-   **RAM** -- 4 Gb DDR4

-   **Interfacce video** -- 2x Micro HDMI ports

-   **Interfacce USB**

    -   USB type C per alimentazione

    -   2x USB 2.0

    -   2x USB 3.0

-   **Interfacce di rete**

    -   Gigabit Ethernet

    -   2.4 GHz e 5.0 GHz IEEE 802.11ac Wi-Fi

    -   Bluetooth 5.0

-   **Dispositivi esterni** -- Supporto per camera e display MIPI

-   **Interfacce GPIO** -- Header GPIO con 40 pin

r0.2 ![image](images/components/pi-camera.png){width="0.9\\linewidth"}

### Camera Pi Module {#camera-pi-module .unnumbered}

La Raspberry Pi Camera è un modulo che si collega direttamente alla
porta CSI situata sul Raspberry.\
Questa, nella versione 1.3 utilizzata, consente di catturare immagini
con risoluzione massima di 5 MPixel e video a 1080p 30 fps, nonostante
il basso costo a cui viene venduta(intorno ai 15 Euro).\

### Arduino Nano {#arduino-nano .unnumbered}

r0.30
![image](images/components/arduino_nano.jpg){width="0.85\\linewidth"}

[\[fig:wrapfig\]]{#fig:wrapfig label="fig:wrapfig"}

Arduino è un'azienda italiana specializzata nella produzione di
micro-controllori, utilizzati soprattutto per piccoli progetti homemade
o per didattica.\
In questo progetto è stato utilizzato Arduino Nano v3, per le seguenti
caratteristiche:

-   Dimensioni notevolmente ridotte, adatte anche al posizionamento su
    una breadboard

-   Alimentazione a 5 Volt e comunicazione seriale via micro-usb

-   Dotato di micro-controllore ATmega328, lo stesso della versione più
    \"potente\" Arduino Uno

-   Presenza di 12 porte GPIO, anche con PWM (Pulse With Modulation) ed
    anche 6 porte per letture analogiche

### L298N DC Motor Controller {#l298n-dc-motor-controller .unnumbered}

r0.25 ![image](images/components/l298n.jpg){width="0.9\\linewidth"}

[\[fig:wrapfig\]]{#fig:wrapfig label="fig:wrapfig"}

Questo modulo, dotato di un chip L298N, consente di controllare due
motori a spazzola (o corrente diretta) con un range operativo di 5- 35
Volt tramite dei segnali a 5 volt.\
La velocità ed il verso di rotazione di entrambi i motori è
controllabile tramite i pin situati nella parte frontale, insieme
all'alimentazione; l'output dei motori si trova invece sui lati.\

::: {#tab:requisiti_funzionali}
  --------------- ---------------------------------------------------------------------
      **VCC**     Alimentazione del modulo, range 7 - 24 Volt
      **GND**     Ground
      **+5V**     Output di 5V per alimentazione di controllori o periferiche esterne
      **ENA**     Segnale PWM (0-255) per regolare la velocità del motore A
   **IN1 e IN2**  Impostano il verso del motore A
   **IN3 e IN4**  Impostano il verso del motore B
      **ENB**     Segnale PWM (0-255) per regolare la velocità del motore B
  --------------- ---------------------------------------------------------------------

  : L298N Motor Controller Pinout
:::

### Motori a corrente diretta {#motori-a-corrente-diretta .unnumbered}

Per far muovere Stalker-Bot sono stati utilizzati 4 motori a corrente
diretta (2 per lato) dotati di scatola con riduttore, questo aumenta la
coppia del motore a scapito della velocità.

![DC Motor with
gearbox](images/components/motor_geared.jpg){#fig:wrapfig
width="0.25\\linewidth"}

### Batterie {#batterie .unnumbered}

r0.25 ![image](images/components/18650.jpg){width="0.4\\linewidth"}

L'alimentazione ai motori viene fornita da due batterie agli ioni di
Litio, in particolare le 18650.\
Esse sono batterie ricaricabili,hanno un range di voltaggio da 3.6 a 4.2
Volt e una buona autonomia (circa 5000 mAh ognuna); inoltre l'output
massimo di corrente di 4 A consente di avere sufficiente alimentazione
per il movimento di un robot cingolato.\
Vengono utilizzate due batterie alla volta, posizionate in serie in modo
da ottenere un voltaggio finale che varia da 7.4 a 8.4 Volt.

### Powerbank e cablaggi {#powerbank-e-cablaggi .unnumbered}

Per l'alimentazione del Raspberry pi sarà necessario utilizzare un
powerbank che riesca a fornire almeno 15 Watt di potenza.\
Per quanto riguarda i cablaggi, saranno necessari due cavetti usb, uno
per collegare il powerbank al Raspberry e l'altro il Raspberry
all'Arduino Nano. Oltre a questo serviranno dei cavetti jumper ed una
breadboard, per collegare Arduino alle periferiche.

![Jumper
wires](images/components/breadboard.jpg){width="0.85\\linewidth"
height="0.18\\textheight"}

![Jumper wires](images/components/jumpers.jpg){width="0.65\\linewidth"
height="0.18\\textheight"}

Collegamenti
------------

Di seguito viene riportato lo schema dei collegamenti fra Arduino Nano e
le periferiche di Stalker-Bot.

![Wiring Stalker-Bot](images/circuito.drawio.pdf){width="12cm"}

La comunicazione fra il Raspberry ed Arduino avviene invece tramite
comunicazione seriale via USB.

![Comunicazione seriale](images/raspberry-arduino.pdf){width="10cm"}

Scocca
------

### Modellazione 3D

La scocca di Stalker-Bot è stata progettata utilizzando Autodesk Fusion
360. I modelli ed i file STL (per la stampa) sono reperibili reperibili
sul sito thingiverse[^1].

![Assieme motore](images/motori_no_spigoli.png){width="13cm"}

-2cm ![Assieme
Stalker-Bot](images/assieme_stalker_bot.png "fig:"){width="18cm"}

### Stampa 3D

r0.25 ![image](images/components/stampante.png){width="0.9\\linewidth"}

L'intera scocca dello Stalker-Bot è stata stampata in 3D, compresi i
cingoli. È stata utilizzata la stampante fdm Artillery Genius.\
I materiali utilizzati sono PETG rosso e nero (scocca ed ingranaggi) e
PLA giallo (cingoli e case Raspberrry).

### Assemblaggio

Per l'assemblaggio saranno necessari due \"assieme motore\", cioè la
parte in cui vengono situati i motori insieme agli ingranaggi che poi
metteranno in moto i cingoli.\
I due \"blocchi motore\" vengono quindi collegati dal case del robot,
all'interno del quale si trovano Arduino, il controller dei motori e le
batterie.\
Sopra la scocca vengono montati quindi il powerbank, il Raspberry e la
Pi Camera.

### Risultato

![Stalker-Bot fronte](images/robot-front.jpg){width="13cm"}

![Stalker-Bot retro](images/robot-back.jpg){width="11cm"}

![Stalker-Bot cablaggi](images/robot-cablaggi.jpg){width="11cm"}

Implementazione {#cap: Implementazione}
===============

Per la fase di addestramento prima e di riconoscimento facciale dopo, è
stato impiegato un classificatore di volti umani preaddestrato, offerto
da OpenCV in formato XML. In particolare, il modello utilizzato
\"haarcascade\_frontalface\_default.xml\" è in grado di identificare
volti umani all'interno di un frame. Nelle prossime sezioni non viene
riportato il codice per intero, che rimane comunque consultabile
all'indirizzzo
$\\$[\"https://github.com/Lore09/Stalker-bot\"](https://github.com/Lore09/Stalker-bot),
ma solo le parti ritenute fondamentali.

Addestramento
-------------

La fase di addestramento si divide in due ulteriori fasi: una prima in
cui vengono catturati trenta frame al proprietario e una seconda in cui
viene effettivamente addestrato il riconoscitore.$\\$

### Cattura immagini del proprietario

Acquisizione camera:

python cam = cv2.VideoCapture(0) cam.set(3, 640) \# set video width
cam.set(4, 480) \# set video height

Inizializzazione del riconoscitore tramite il modello preaddestrato:

Acquisizione di un frame dalla camera, conversione del frame in scala di
grigi per rendere computazionalmente più leggera l'identificazione dei
volti:

Ciascun volto localizzato viene racchiuso in un rettangolo e
quest'ultimo viene codificato in quattro valori, rispettivamente:
coordinata iniziale lungo l'asse orizzontale (x), coordinata iniziale
lungo l'asse verticale (y), larghezza (w) e altezza (h). Per ogni volto
riconosciuto viene salvata un'immagine in formato .jpg che ha dimensioni
pari a quelle del rettangolo che racchiude il volto stesso:

### Addestramento del riconoscitore

Come riconoscitore viene istanziata una classe, sempre fornita da
OpenCV, che verrà successivamente allenata per riconoscere i volti
precedentemente salvati:

Viene definito il metodo getImagesAndLabels(path) (qui non riportato)
che restituisce: le immagini dal dataset sotto forma di numpy array e il
nome dell'utente associato a quelle immagini. Successivamente viene
allenato il riconoscitore e viene salvato il modello appena creato:

python path = 'dataset'

faces,ids = getImagesAndLabels(path) recognizer.train(faces,
np.array(ids))

\# Save the model into trainer/trainer.yml recognizer.write( path +
'/trainer.yml')

Esecuzione Stalker-Bot
----------------------

Una volta addestrato il riconoscitore è possibile mettere in moto
Stalker-Bot.\
Il software in questo caso viene eseguito sia su Raspberry
(riconoscimento e generazione comandi) che su Arduino (conversione
comandi del raspberry in comandi per i motori).

### Riconoscimento

In questa sezione viene mostrato come effettivamente è possibile
utilizzare il riconoscitore (allenato nella sezione precedente) affinché
riconosca il suo padrone in un flusso video. Inizialmente viene
effettuato un setup in cui: viene inizializzato il riconoscitore
(LBPHFaceRecognizer\_create()), quest'ultimo legge il modello creato
durante la fase di addestramento, viene inizializzato un detector, con
lo stesso classificatore preaddestrato visto nell'introduzione del
capitolo [3](#cap: Implementazione){reference-type="ref"
reference="cap: Implementazione"}, che si occuperà di cercare,
all'interno di ciascun frame, dei volti umani. Viene, inoltre, riportata
l'acquisizione della camera:

A ciascun frame (prima convertito in scala di grigi per alleggerire il
carico computazionale) viene applicata la normalizzazione per ottenere
un contrasto maggiore. Quindi si cercano, al loro interno, i volti:

Ogni volto umano localizzato viene passato al riconoscitore che
restituisce l'identificatore di ciascuno dei volti presenti nel dataset
usato per l'addestramento con associato un valore (confidence) che
rappresenta quanto il volto localizzato si avvicina al volto presente
nel dataset:

python for (x, y, w, h) in faces: id, confidence =
recognizer.predict(imageNp\[y:y + h, x:x + w\])

### Movimento

Una volta riconosciuto il proprietario, Stalker-bot deve seguire i
movimenti del suo volto. Per fare ciò lo script calcola quanto la faccia
del proprietario si discosta dal centro dell'immagine, entro un certo
range.\
Viene inoltre definita la funzione `arduino_map()`, utile per convertire
valori appartenenti a domini differenti.

Il seguente algoritmo prende le coordinate x ed y corrispondenti alla
faccia del proprietario e li utilizza per calcolare i valori di sterzata
ed accelerazione del robot.

Questi valori vengono poi utilizzati per comporre il comando che verrà
inviato, tramite comunicazione seriale, ad Arduino.\
La struttura del comando è `acceleration,turn,time\n` in cui time è la
durata del comando (in millisecondi), acceleration e turn
rispettivamente la velocità di avanzamento e di sterzata e variano nel
range (-100,100).

python string = str(acc) + \",\" + str(turn) + \",100\"
ser.write(string.encode('utf-8'))

### Arduino

Di seguito viene riportato il codice in esecuzione su Arduino Nano.
Questo script si occupa di leggere i dati in arrivo dalla comunicazione
seriale con il Raspberry, impartire i comandi ai motori e alle luci.\
All'inizio vengono inizializzate le variabili globali:

La funzione moveMotors() si occupa di convertire i valori acceleration e
turn in arrivo dal Raspberry in comandi per i due motori.

La funzione stop() viene utilizzata per fermare tutti i motori ed
impostare le velocità a 0.

C++ void stop() digitalWrite(in1, LOW); digitalWrite(in2, LOW);
digitalWrite(in3, LOW); digitalWrite(in4, LOW); analogWrite(enA, 0);
analogWrite(enB, 0);

La funzione checkPortaSeriale() si occupa di controllare se nella coda
della comunicazione seriale sono presenti dei comandi e, nel caso ci
siano, di ottenerne i valori.

All'interno della funzione Setup(), che verrà eseugita una sola volta
all'avvio del programma, vengono impostati i GPIO in modalità OUTPUT e
viene avviata la comunicazione seriale, con baud rate 9600.

La funzione loop() è quella che viene eseguita a regime. Ad ogni
iterazione il programma controlla la porta seriale e, se sono presenti
nuovi comandi, resetta lo `start_time` del comando.\
A questo punto, se la durata del comando in esecuzione è inferiore a
quella massima specificata nel comando stesso, il programma muoverà i
motori utilizzando i valori specificati; in caso la durata superi quella
massima il robot verrà fermato.

Conclusioni {#conclusioni .unnumbered}
===========

Questo progetto si è concentrato sull'integrazione tra sistemi embedded,
machine learning e computer vision, in particolare sullo sviluppo di un
robot in grado di individuare la posizione di un volto, verificare che
questo coincida con quello del suo proprietario e di seguirne i
movimenti. Si è visto come è possibile addestrare, con una serie di
immagini, una rete affinché possa riconoscere, durante un flusso video,
un volto umano. Un eventuale sviluppo futuro di questo progetto potrebbe
essere quello di sostituire la Picamera con una camera a più alta
risoluzione, in modo da poter incrementare il grado di confidenza
durante la fase di riconoscimento facciale.

[^1]: Modelli: https://www.thingiverse.com/thing:6069512
