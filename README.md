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
    - PIO Projekt im EMG-Sensor-PIO-Ordner
  - [x]  Daten aufbereiten
  - [x]  EMG Recorder EXE 
    - eine Datei: https://studmailwhsde-my.sharepoint.com/:u:/g/personal/nils_hochstrat_studmail_w-hs_de/ESB7t-cu--xGgFi5KqoSMdABcJ-_2TpTpCY-BPDijaR5Bw?e=FqbNSb
    - ein Ordner mit viele kleinen Datein: https://studmailwhsde-my.sharepoint.com/:u:/g/personal/nils_hochstrat_studmail_w-hs_de/EU9l-VjcJ59Ip8eAAARAp78BdtF12FbcpOL0Gj7ub3tPUA?e=d2HwNX
  - [x]  Fusion EXE
    - im "EMG_Data_Fusion-Ordner"
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
