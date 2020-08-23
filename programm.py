#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Beschreibung:  Aufbau der Oberfläche und positionierung der Anzeigeelemente mit Kivy

    Bildquelle:
    https://cdn.pixabay.com/photo/2020/01/15/07/14/mountain-climbing-4767088_960_720.jpg
'''

### kivy ###

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.button import Button

from os import getcwd as arbeitsverzeichnis
from os import chdir
from os import path
from datetime import datetime
import sys

### eigene Module ###
from tools.Check_Zahl import eingabe_in_eine_zahl_konvertieren
from tools.Diagramm import diagramm_zeichnen
from tools.Datei_einlesen import datei_einlesen

### Variablen ###

err0 = ":  Es wurde kein Wert eingegeben\n"
err1 = ":  Der Wert ist keine Zahl\n"

# Pfad des Arbeitsverzeichnisses setzen
av = path.dirname(sys.argv[0])
chdir(av)

# Pfad für die Messdatei
pfad = arbeitsverzeichnis() + "/Daten/"

dateiname = "messwerte.txt"
dateiname_beispiel = 'messwerte_Beispiel.txt'

### Programm ###


class Knopf(Button):

    def werte_speichern(self):
        hbs = self.parent.parent.parent.parent

        # Eingaben prüfen
        daten = eingabe_pruefen(hbs)

        if daten is not None:
            datenspeichern(daten)

            # Eingabe zurückset bei erfolgreicher Speicherung
            eingabe_zuruecksetzen(hbs, daten)

    def diagramm_anzeigen(self):

        hbs = self.parent.parent.parent.parent

        status, daten_dict = datei_einlesen(dateiname)

        if status:
            diagramm_zeichnen(daten_dict)
        else:
            meldung = "Die Messdatei ist nicht im Verzeichnis\n\n" \
                      "" + daten_dict + "  \n\nvorhanden!"
            hbs.ids.l1.text = meldung

            # Beispieldaten anzeigen
            status,daten_dict = datei_einlesen(dateiname_beispiel)
            diagramm_zeichnen(daten_dict,"DEMODATEN")


def eingabe_pruefen(hbs):
    '''
    Es wird geprüft ob ein Wert eigegeben wurde
    Er wird geprüft ob eine Zahl eingegeben wurde

    Bei Fehlern wird auf Anzeige 1 eine Meldung ausgegeben

    :param hbs: Hauptsceen kivy-Objekt
    :return: daten liste [1,2,3]
    '''
    fehlermeldung = ""
    druck1_obj = hbs.ids.Texteingabe1
    druck2_obj = hbs.ids.Texteingabe2
    pulse_obj = hbs.ids.Texteingabe3
    kommentar_obj = hbs.ids.Texteingabe4
    anzeige = hbs.ids.l1
    daten = []

    werte = [druck1_obj, druck2_obj, pulse_obj, kommentar_obj]

    for i, e in enumerate(werte):

        # Kein Wert eingegeben
        if len(e.text) == 0:
            fehlermeldung = fehlermeldung + e.name + err0

        else:
            if i < 3:  # gilt für die ersten 3 Eingabefenster
                zahl = eingabe_in_eine_zahl_konvertieren(e.text)

                # Der Wert ist keine Zahl
                if type(zahl) == str:
                    # Reaktion
                    e.text = ""
                    fehlermeldung = fehlermeldung + e.name + err1
                else:
                    daten.append(zahl)
            else:  # gilt für das Kommentarfenster
                daten.append(e.text)

    # Ausgabe der Fehlermeldung auf dem Anzeigenfeld
    # falls ein Fehleraufgetreten ist

    if len(fehlermeldung) > 0:
        anzeige.text = fehlermeldung
    else:
        anzeige.text = "Dies ist eine Anzeige"

    # Daten nur zurückgeben wenn sie vollständig und richtig sind
    if len(daten) == 4:
        return daten
    else:
        return None


def datenspeichern(daten):
    # Daten Format
    print(daten)
    zeit = datetime.now().strftime('%H:%M:%S')
    datum = datetime.now().strftime('%Y-%m-%d')
    wertenamen = "Datum\tSYS_Druck\tDIA_Druck\tPulse\tUhrzeit\tKommentar\n"
    unit = "-\tmmHg\tmmHg\tPulse/min\t\t\n\n"
    kopf = "Messdatei\n" + wertenamen + unit
    datenset = str(datum) \
               + "\t" + str(int(daten[0])) \
               + "\t" + str(int(daten[1]))\
               + "\t" + str(int(daten[2])) \
               + "\t" + str(zeit) \
               + "\t" + str(daten[3]) + "\n"

    chdir(pfad)  # wechsel in den Unterordner ./daten

    if path.isfile((pfad + "/" + dateiname)):

        fobj = open(dateiname, "a")
        fobj.write(datenset)
        fobj.close()

    else:

        datenset = kopf + datenset
        fobj = open(dateiname, "w")
        fobj.write(datenset)
        fobj.close()
        print("Die Messdatei ist nicht da!")

    chdir("../") # Zurück wechseln in den Programmordner
    return datenset


def eingabe_zuruecksetzen(hbs, daten):
    hbs.ids.Texteingabe1.text = ""
    hbs.ids.Texteingabe2.text = ""
    hbs.ids.Texteingabe3.text = ""

    hbs.ids.l1.text = "SYS_Druck: " + str(daten[0]) + "\n" \
                      + "DIA_Druck:  " + str(daten[1]) + "\n" \
                      + "Puls:            " + str(daten[2]) + "\n" \
                      + "wurden in die Datei geschrieben!"


# Alle im der KV Datei verwendeten Klassen müssen vor dem Laden definiert sein
# Die Klassen werden dann beim Laden aufgerufen
# Kivy_Beschreibung_laden = Builder.load_file('oberflaeche.kv')

Kivy_Beschreibung_laden = Builder.load_file('oberflaeche.kv')


class oberflaeche(App):
    title = 'Bedienoberfläche für Aktienanalyse'

    def build(self):
        # Window.clearcolor = (0.38, 0.35, 0.35, 1)
        # Window.size = (1600, 960)
        # Window.maximize=True
        # Window._set_window_pos(480,140)
        # Window._set_window_pos(180, 40)
        # Window.borderless = True
        # Window.size = (2560, 1440)
        Window.size = (1920, 1080)
        Window.fullscreen = True
        # print(help(Window))
        # pos=Window._get_window_pos()
        # print(pos)
        return Kivy_Beschreibung_laden


def hauptprogramm():

    # ein Objekt erzeugen
    bild_obj = oberflaeche()
    bild_obj.run()


if __name__ == "__main__":
    hauptprogramm()
