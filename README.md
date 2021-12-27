# Praktikum intelligente Systeme (ISYS)

Aufnahme von elektrischen Signalen von Muskeln, um mithilfe eines neuronalen Netzes Handzeichen zu erkennnen.

## To Do:
- [x] ASCII Ausgabe von Messweten vom Arduino
- [x] Ausgabe auf 4 ADCs begrenzen (spart Serielle Bandbreite)
- [x] Übertragen der 10 Bit ADC Werte als 2 Byte pro Kanal und 0xAAAA als Startbit
- [x] Serieller Monitor
- [x] Logdatei erstellen
- [x] Serieller Plotter
- [x] Bildausgabe für Handbewegung (Stein, Schere, Papier)
- [x] Logdatein zusammenführen
- [ ] Audio Feedback für Recorder
- [ ] Klassifkatoren für NN definieren

## Zeitplan:
- Mitte November  (18.11.2021):
  - [x]  Frischbier Ausarbeitung gelesen und verstanden
  - [ ]  Entwicklungsumgebung in Betrieb nehme(Matplot)  
- Anfang Dezember (02.12.2021):
  - [x]  Daten aufnehmen
  - [x]  Daten aufbereiten
  - [ ]  EMG Recorder EXE 
  - [x]  Fusion EXE
- Mitte Dezember  (16.12.2021):
  - [ ]  Training des Netzes:
    - [ ]  Jan hat angelernt
    - [ ]  Luca hat angelernt
    - [ ]  Nils hat angelernt
    - [ ]  David hat angelernt
- Ende Dezember    (30.12.2021):
  - [ ]  Daten auswerten
  - [ ]  evtl. Programm zum Spielen (Schere,Stein,Papier) erstellen
- Mitte Januar     (13.01.2021):
  - [ ]  Ausarbeitung fertigstellen
  - [ ]  Präsentation erstellen

## Positionen zum Elektrodenaufkleben
| Channel | Graphfarbe  | AIN_SEL | Wie finde ich die Stelle? |
| :-----: | :---------: | :-----: | :------------------------ |
| 0       | Rot         | 1       | zwischen 1 und 2 Außenseite|
| 1       | Grün        | 3       | Handfläche auf Tisch; Ringfinger anheben|
| 2       | Blau        | 5       | Handfläche zum Gesicht; Ringfinger einklappen|
| 3       | Orange      | 7       | zwischen 1 und 2 Innenseite|

Weitere einstellungen am Olimexstack:
- 5V auswählen, ***nicht*** 3V!
- D4/D9, REF_E und CAL ***nicht*** brücken!
### oben
![Elektroden oben](https://user-images.githubusercontent.com/16342158/147500835-68ff520e-373e-4e80-90be-bbeeecd310fd.jpeg)
An der Elektrode am Handgelenk soll Masse (schwarz) einmal angeschlossen werden. Restliche schwarze Kabel nicht anschließen!
Ansonsten ist das weiße Kabel immer näher am Handgelenk als das rote Kabel.
### unten
![Elektroden unten](https://user-images.githubusercontent.com/16342158/147500837-deea14c6-fd5a-405a-9d72-bac341e57882.jpeg)
### Außenseite
![Elektroden Außenseite](https://user-images.githubusercontent.com/16342158/147500838-4150cb35-9299-49eb-85b1-e9b3fcf2a000.jpeg)
## Neuronales Netz erstellen
### 1. EMG auslesen (Arduino Programm)
Zunächst laden wir das Platform IO Projekt vom Ordner "EMG-Sensor-PIO" auf das Olimex Board.
Desweiteren müssen wir mithilfe der blauen Potentiometer an den Aufsteckplatinen noch den Gain für die Kanäle einstellen. Dazu empfiehlt dich das Programm aus dem nächsten Schritt, wobei man darauf achtet, dass die Ausschäge möglichst groß sind, aber nie bei 0 oder 1024 clippen.
### 2. Daten aufnehmen
Hier nutzen wir das Pythonprogramm aus dem Ordner "EMG_Recorder", welches wir mit "python main.py" ausführen können.
Nachdem wir uns mit dem Board verbunden haben können wir mithilfe des Knopfs "Aufnahme starten" beginn die EMG Daten aufzunehmen und im Unterordner "data" abspeichern zu lassen. Da jedes Label seperat abgespeichert wird kann die Aufnahme zu jedem Zeitpunkt unterbrochen werden.

Zur Standardisierung soll bis 3 Sekunden vor Ende der 10 sekündigen Pause, der Arm entspannt werden, sodass kaum Schwankungen im EMG-Signal zu sehen sind.
Anschließend soll die im Bild dargestellte Haltung eingenommen werden bis zu nächsten Pause 10 Sekunden später.
### 3. Daten aufbereiten
Um nun aus den ganzen kleinen einzelnen Label Dateien eine große Datei zu erstellen, müssen wir die "Fusion.exe" in einen Ordner mit den Labledateien verschieben und dort ausführen. Es sollte sich ein Terminalfenster mit dem aktuellen Status öffnen und eine CSV-Datei erstellt werden.

Da es währende der Aufnahme aufgrund von Unachtsamkeiten oder äußeren Einflüssen hin und wieder zu Messfehlern kommen kann, gibt es zwei Möglichkeiten zum Entfernen jener Fehler:
- Manuell: Man lässt sich in Excel einen Graphen der Messwerte plotten, identifizier & entfernt fehlerbehaftete Labledateien, um im Anschluss erneut "Fusion.exe" auszuführen.
- Automatisiert mit einem Quantil-Filter: Im Ordner "EMG_Peak_Remover_9000" kann man mit "python Peakremover.py -i <inputfile.csv> [-f <filter_size>]" eine belliebige Anzahl von Extremen werten aus der CSV (oben und unten gleichermaßen) von allen vier Kanälen entfernen lassen.
- Automatisiert mit einem Median-Filter: dieser wurde im Programm für den nächsten Schritt bereits integriert
### 4. Features extrahieren
Hier ist es zurzeit noch stark Work in Progress! Mithilfe der features-V1.4.exe lassen sich unter Angabe diverser Parameter 4 verschiedene Parameter pro Kanal berechnen:
- favg: Mittelwert der Messwerte
- len: Bahnlänge des Signals (Linienlänge auf dem Graphen)
- f_zero_count: Anzahl der Nulldurchgänge
- fturns: Anzahl der Richtungswechsel

Die Ausgabe muss zurzeit mithilfe eines Shifts ">>" in eine Datei verschoben werden, um die später in ein NN einzupflegen.
Beispiel Aufruf: "features-V1.4.exe -i a -f 1000 -n 4 -l 150 -k 50 >> features.txt"
### 5. Daten in ein NN einpflegen
Um später Daten zu klassifizieren müssen wir zunächst ein NN anlernen. Es gibt jedoch eine Alternative, wenn wir ein Daten auf ihre Brauchbarkeit testen wollen - kNN.
Dies befindet sich zurzeit im "EMG_Klassifikator" Ordner in einem Jupyter Notebook, welches sich mit "jupyter notebook" öffnen lässt.

Hier schmeißt er aber zur Zeit noch einen Fehler bezüglich inkonsequenter Daten raus... :(



Fehler im Text einfach abändern. War was müde als ich (Nils) das geschrieben habe, aber es gibt scheinbar keine Entwurfsfunktion... zZz
