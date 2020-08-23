#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Beschreibung:
'''

import matplotlib.pyplot as plt


def diagramm_zeichnen(daten_dict, *args):

    demodaten = len(args)
    messwerte_sys = daten_dict["DIA_Druck"]

    y_spur= messwerte_sys.y_spur_mit
    x_spur = messwerte_sys.x_spur_datetime_mit
    plt.plot(x_spur,y_spur,linestyle='-', marker='o')

    messwerte_sys = daten_dict["Pulse"]

    y_spur= messwerte_sys.y_spur_mit
    x_spur = messwerte_sys.x_spur_datetime_mit
    plt.plot(x_spur,y_spur,linestyle='-', marker='o')

    messwerte_sys = daten_dict["SYS_Druck"]

    y_spur= messwerte_sys.y_spur_mit
    x_spur = messwerte_sys.x_spur_datetime_mit
    plt.plot(x_spur,y_spur,linestyle='-', marker='o')

    # plt.axis([0,2020,0,200] )
    plt.ylim(0,200)
    x_beschriftung = messwerte_sys.x_einheit
    plt.xlabel(x_beschriftung)
    y_beschriftung = messwerte_sys.name +" ["+ messwerte_sys.einheit +"]"
    plt.ylabel(y_beschriftung )

    if demodaten == 0:
        plt.title('Verlauf Blutdruck')

    else:
        plt.title('!!! Dies sind Demodaten es wurde keine Datei mit Messdaten gefunden!!!')

    plt.grid(True)

    plt.show()


def hauptprogramm():
    diagramm_zeichnen()
    pass


if __name__ == "__main__":
    hauptprogramm()
