#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Beschreibung:
'''
from os import path, sep
from os import getcwd as arbeitsverzeichnis
from os import chdir
from datetime import datetime
import numpy as np


### eigen Skripte ###



class DatenObjekt:
    def __init__(self):
        self.name = ""
        self.y_spur = []       # Alle Werte
        self.y_spur_mit = []   # Werte des selben Tags gemittelt
        self.einheit = ""
        self.beschreibung = ""
        self.x_spur = []
        self.x_einheit = ""
        self.x_beschreibung = ""
        self.x_spur_datetime = []
        self.x_spur_datetime_mit = []   # doppelte Daten wurden entfernt


def datei_einlesen(dateiname):
    '''
    Es wird eine Textdatei eingelesen

    Die Daten werden als Dictinary zurück gegeben

    {"SYS_Druck": messwert_obj, "DIA_Druck":messwert_obj, "Pulse": messwert_obj }

    Die Struktur des messwert_obj ist in der Klasse DatenObjekt beschrieben

    :return: dictionary {"SYS_Druck": messwert_obj, ...}
    '''

    # dateiname = "messwerte.txt"
    # prüft und wecheslt in den Pfad ../Daten
    pfad = verzeichnis_check()

    # prüft ob eine Messdatei.txt vorhanden ist
    datei_status = datei_check(pfad, dateiname)

    if datei_status:

        # Daten werden ein gelesen und sortiert
        # Die Daten können über den Namen angesprochen werden
        # z.B. daten_dict["SYS_Druck"].x_spur
        datenset = daten_einlesen(dateiname)

        # Daten werden sortiert und die Mittelwerte berechnet
        daten_dict = daten_sortieren(datenset)

        # Ins übergeordnete Verzeichnis zurück wechseln
        # chdir("..")
        status = True

        return status, daten_dict

    else:
        # Wenn die Datei nicht vorhanden ist
        status = False

        return status, pfad


def verzeichnis_check():
    if not path.isdir("Daten"):
        # Ins übergeordnete Verzeichnis wechseln
        chdir("..")

    # neuen Pfad festlegen
    pfad = sep.join([arbeitsverzeichnis(), "Daten"])

    # neuen Pfad setzen
    chdir(pfad)

    return pfad


def datei_check(pfad, dateiname):

    if path.isfile((sep.join([pfad, dateiname]))):
        print("Datei ist vorhanden")

        return True

    else:
        print("Die Messdatei ist nicht vorhanden")

        return False


def daten_einlesen(dateiname):
    '''
    Jede Zeile wird in als Liste in einer Liste gespeichert
    :param dateiname:
    :return:
    '''
    datenset =[]
    fobj = open(dateiname, "r")
    for line in fobj:
        # \n Zeilenumbruch entfernen
        daten = line.split("\n")
        daten = daten[0].split("\t")
        datenset.append(daten)

    fobj.close()

    return datenset


def daten_sortieren(datenset):
    '''
        Es wird ein Dictinary erstellt:
        Mit den Namen der Werte. Die Werte werden als Objekt wie
        in Klasse DatenOkjekt beschrieben erstellt

        Die Listen die nur Daten enthalten werden in ein numpy array
        konvertiert und dann transponiert damit die Untereinanderstehen
        Werte in eine eigene Liste kommen

        :param datenset: Liste mit Listen für jede Liste entspricht
        einer eingelesener Zeile
        :return:
    '''

    NAME = 1
    EINHEIT = 2
    daten = np.array(datenset[4:])
    daten = np.transpose(daten)

    daten_dict ={}
    mittlungsvektor = mittlungsmatrix(daten[0])

    # der erste Wert nicht als eigener Datensatz betrachtet und übersprungen
    #  er wird als Zeitspur als X-Spur verwendet
    # die letzten beiden Wert (Uhrzeit und Kommentar) nicht berücksichtig

    for e in range(1, len(datenset[1])):

        name = datenset[NAME][e]

        # Datenstruktur der Messdaten
        messwert_obj = DatenObjekt()

        # Zusatzdaten
        messwert_obj.name = name
        messwert_obj.einheit = datenset[EINHEIT][e]

        # Y-Spur
        if e < 4:
            messwert_obj.y_spur = daten[e].astype(float)

        else:  # Ab Spalte 5 Uhrzeit und Kommentar als String
            messwert_obj.y_spur = daten[e].astype(str)
        # X-Spuren
        messwert_obj.x_spur = daten[0]
        messwert_obj.x_einheit = "Zeit in Tagen / Datum"

        [messwert_obj.x_spur_datetime.append(datetime.strptime(e, '%Y-%m-%d'))
         for e in daten[0]]

        # Mittelung
        if e < 4:
            messwert_obj.y_spur_mit = mittelwert_berechnen(messwert_obj.y_spur,
                                                       mittlungsvektor)

            messwert_obj.x_spur_datetime_mit = sorted(set(messwert_obj.x_spur_datetime))

        daten_dict.update({name: messwert_obj})

    return daten_dict


def mittelwert_berechnen(daten, vektor):

    mittelwerte = []
    for v in vektor:
        von = v[0]
        bis = v[-1]+1
        anzahl = len(v)
        mw = int(sum(daten[von:bis])/anzahl)

        mittelwerte.append(mw)

    return mittelwerte


def mittlungsmatrix(daten):
    '''
    Es wird eine Liste erstellt in der der Index gleicher Werte wieder in einer Liste
    zusammen gefasst wird
    :param daten_dict:
    :return: [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], ...]
    '''

    mittlungsvektor = []
    satz = []
    for i, x in enumerate(daten):
        if i < len(daten)-1:
            # für alle Element ausser des letzten Elementes
            if daten[i] == daten[(i+1)]:
                satz.append(i)
            else:
                satz.append(i)
                mittlungsvektor.append(satz)
                satz = []
        else:
            # letztes Element
            satz.append(i)
            mittlungsvektor.append(satz)

    return mittlungsvektor


def hauptprogramm():
    datei_einlesen("messwerte.txt")
    pass


if __name__ == "__main__":
    hauptprogramm()
