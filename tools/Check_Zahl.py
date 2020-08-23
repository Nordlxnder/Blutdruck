#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Beschreibung:
'''


def eingabe_in_eine_zahl_konvertieren(wert):
    '''
    Die Funktion konvertiert den Stringwert in eine Zahl
    Sollte es sich nicht um eine Zahl handeln wird der Stringwert
    einfach wieder zurück gegeben

    Das Komma wird automatisch durch einen Punkt ersetzt

    :param wert: Type String
    :return: zahl als Float / im Fehlerfall als String
    '''

    if type(wert) == str:
        # möglichen Kommafehler beseitigen
        wert = wert.replace(",",".")
        try:
            zahl = float(wert)
        except ValueError:
            zahl = wert

    return zahl

def hauptprogramm():
    eingabe_in_eine_zahl_konvertieren(-1,1)
    pass


if __name__ == "__main__":
    hauptprogramm()
