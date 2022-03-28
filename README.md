# A.M.M.E (2-D)
Eine einfache Verschlüsselung, welche mit Geradengleichungen im 2-Dimensionalen Raum rechnet dessen Schnittwinkel zu Buchstaben und Zeichen zugeteilt werden.

Zur Berechnung der Variablen **r** und **s** aus den Geradengleichungen wird das Python-Modul <code>sympy</code> verwendet.

# Funktion

Zu Begin werden pro Buchstabe **vier** Vektoren generiert. Dabei handelt es sich um jeweils zwei Stütz- und zwei Richtungsvektoren. Aus diesen Vektoren werden zwei Geradengleichungen erstellt, woraus ein Schnittwinkel berechnet wird. Jeder Schnittwinkel wird einem Buchstaben oder einem Zeichen zugeteilt und wird später als string ausgegeben (der sogenannte Schlüssel), damit man die Nachricht schlussendlich entschlüsseln kann.
