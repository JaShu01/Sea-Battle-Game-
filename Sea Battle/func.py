import argparse
import curses
import random
import secrets
import sys

parser = argparse.ArgumentParser(description= "BATTLESHIP 1 VS 1 GAME")  # Initialisieren Sie den Argument-Parser

parser.add_argument("x_axis", type=int, help="NUMBER OF COLUMNS IN GAME [ 5 < x_axis <=10]")  # xaxis argument
parser.add_argument("y_axis", type=int, help="NUMBER OF ROWS IN GAME [ 5 < y_axis <=10] ")  # yaxis argument

args = parser.parse_args()

# Zeilen und Spalten zuweisen
rows = args.y_axis
columns = args.x_axis
#  ZEILEN und SPALTEN Beschränkung
if rows < 5:
    rows = 5
if rows > 10:
    rows = 10
if columns < 5:
    columns = 5
if columns > 10:
    columns = 10

#DarstellungsCode
EMPTY = '   '
HIT = ' X '
MISS = ' O '
DESTROYED = ' $ '

ROWS_HIGH = 2
COLUMN_WIDTH = len(EMPTY) + 1  # +1 zur Berücksichtigung der Breite des Zellenrandes

# Menüoptionen
menu = [" [ JABRAIL VS DIEGO ]  ", " [ EXIT GAME ] "]
# Stellungs Positionierungs Möglichkeiten
horizontal = ["horizontal", "h"]
vertical = ["vertikal", "v"]
# Alle Schiffstypen. beitere Schiffstypen können in dieser Liste hi
SCHIFF_TYPEN = [("DESTROYER", 1, "D"), ("SUBMARINE", 2, "S"), ("CRUSIER", 2, "CS"), ("BATTLESHIP", 3, "B"),
                ("CARRIER", 4, "CR")]
# Leerplatz, um zwischen Text PLatz zuzuweisen, wird in Code oftmals benutzt.
space = "                                                 "


