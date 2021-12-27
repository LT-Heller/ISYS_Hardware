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
| Channel | AIN_SEL |
| :-----: | :-----: |
| 0       | 1       |
| 1       | 3       |
| 2       | 5       |
| 3       | 7       |

Weitere einstellungen am Olimexstack:
- 5V auswählen, ***nicht*** 3V!
- D4/D9, REF_E und CAL ***nicht*** brücken!
### oben
![Elektroden oben](https://user-images.githubusercontent.com/16342158/147500835-68ff520e-373e-4e80-90be-bbeeecd310fd.jpeg)
An der Elektrode am Handgelenk soll Masse (schwarz) einmal angeschlossen werden. Restliche schwarze Kabel nicht anschließen!
### unten
![Elektroden unten](https://user-images.githubusercontent.com/16342158/147500837-deea14c6-fd5a-405a-9d72-bac341e57882.jpeg)
### Außenseite
![Elektroden Außenseite](https://user-images.githubusercontent.com/16342158/147500838-4150cb35-9299-49eb-85b1-e9b3fcf2a000.jpeg)
