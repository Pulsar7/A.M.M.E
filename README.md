# A.M.M.E (2-D)
Eine einfache Verschlüsselung, welche mit Geradengleichungen im 2-Dimensionalen Raum rechnet dessen Schnittwinkel zu Buchstaben und Zeichen zugeteilt werden.

Zur Berechnung der Variablen **r** und **s** aus den Geradengleichungen wird das Python-Modul <code>sympy</code> verwendet.

# Funktion

Zu Begin werden pro Buchstabe **vier** Vektoren generiert. Dabei handelt es sich um jeweils zwei Stütz- und zwei Richtungsvektoren. Aus diesen Vektoren werden zwei Geradengleichungen erstellt, woraus ein Schnittwinkel berechnet wird. Jeder Schnittwinkel wird einem Buchstaben oder einem Zeichen zugeteilt und wird später als string ausgegeben (der sogenannte Schlüssel), damit man die Nachricht schlussendlich entschlüsseln kann.

# Beispiel

    Nachricht: Das ist eine geheime Nachricht

    Verschlüsselte-Nachricht: 
    
    53, 43;23, 8;14, 40;34, 35;30, 23;22, 32;1, 50;1, 27;28, 13;10, 9;54, 55;8, 25;16, 11;21, 22;25, 18;20, 53;15, 20;28, 18;8, 2;25, 45;28, 13;10, 9;54, 55;8, 25;20, 17;51, 33;12, 43;22, 3;16, 11;21, 22;25, 18;20, 53;50, 35;8, 43;40, 5;40, 50;15, 20;28, 18;8, 2;25, 45;41, 24;16, 31;47, 40;46, 46;50, 35;8, 43;40, 5;40, 50;16, 11;21, 22;25, 18;20, 53;30, 0;5, 7;18, 2;47, 23;50, 35;8, 43;40, 5;40, 50;25, 9;4, 15;4, 30;55, 54;50, 35;8, 43;40, 5;40, 50;15, 20;28, 18;8, 2;25, 45;38, 15;54, 28;18, 10;26, 8;50, 35;8, 43;40, 5;40, 50;16, 11;21, 22;25, 18;20, 53;41, 24;16, 31;47, 40;46, 46;30, 23;22, 32;1, 50;1, 27;51, 18;20, 26;35, 29;52, 25;25, 9;4, 15;4, 30;55, 54;53, 30;52, 7;49, 8;3, 51;15, 20;28, 18;8, 2;25, 45;51, 18;20, 26;35, 29;52, 25;25, 9;4, 15;4, 30;55, 54;20, 17;51, 33;12, 43;22, 3
    
    Schlüssel:
    
    A-1+B-22+C-14+D-25+E-44+F-17+G-20+H-38+I-47+J-4+K-90+L-64+M-12+N-5+O-18+P-6+Q-15+R-77+S-27+T-67+U-50+V-42+W-13+X-32+Y-63+Z-3+ -34+,-26+!-28+?-30+Ü-8+Ö-43+Ä-10+
    

