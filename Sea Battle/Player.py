
from func import *
import Coordinate
import Ship
import grafiks

class Player:

    def __init__(self, name):
        self.name = name  # Spielerattributen festlegen
        self.board = []
        self.schiffe = []
        self.opponent = None
        #self.ist_cpu = False

        # Leere Karte von REIHEN durch SPALTEN initialisieren
        for r in range(rows):
            self.board.append([EMPTY] * columns)

    def place_ship(self, ship, koords, orientierung):
        if orientierung in vertical:
            if koords.y + ship.length > rows:  # Schiff in die Lage nicht passt
                return False  #  Fehler

        elif orientierung in horizontal:
            if koords.x + ship.length > columns:  # Schiff in Lage nicht  passt
                return False   #Fehler


        ship.place(koords.x, koords.y, orientierung)  # das Schiff platzieren

        # Koordinate außerhalb Grenzen, bedeutet dies einen Ausfall
        for c in ship.koords:
            if self.board[c.y][c.x] != EMPTY:
                return False

        # keine ungültigen Koordinaten in Schiff, dann aktualisieren Sie die Karte
        for c in ship.koords:
            self.board[c.y][c.x] = ship.code
        self.schiffe.append(ship)  # das Schiff fürs Spieler aufnehmen
        return True  # bedeutet Erfolg

    def hited_place(self, coord):  # Stellen die Getroffen, Missed waren
        code = self.board[coord.y][coord.x]
        message = ""

        if code == HIT or code == DESTROYED or code == MISS:
            return False, "ALREADY SHOT! "

        if code == EMPTY:
            self.board[coord.y][coord.x] = MISS
            return True, "MISS!"

        else:
            # Ein Treff wenn Schiff dort liegt
            for ship in self.schiffe:
                message += ship.name + " : "
                for c in ship.koords:
                    message += str(c) + " "
                    if c == coord:
                        ship.hits = ship.hits + 1  # Trefferanzahl um ein erhöhen
                        if ship.is_destroyed():  # Desstroyed, dann alle Zeilen markiert
                            for c2 in ship.koords:
                                self.board[c2.y][c2.x] = DESTROYED
                            return True, "YOU SUNK MY " + ship.name

                        else:
                            # Mal getroffen, dann getroffene Zeile als getroffen markieren
                            self.board[c.y][c.x] = HIT
                            return True, "HIT!"  # Erfolg
                    message += "\n"

        return False, "REACHED END OF METHOD" + code + "\n" + message


    def lost(self):
        # ein Schiff noch da, läuft spiel weiter
        for ship in self.schiffe:
            if not ship.is_destroyed():
                return False
        return True

    def destroyed_shifs_counting(self):
        destroyed = 0  # Versenkte Schiffe Zähler
        for ship in self.schiffe:
            if ship.is_destroyed():
                destroyed += 1
        return destroyed

    def random_ship_placing(self, type):
        ship = Ship(type)

        while True:
            orientierung = 'h' if random.random() < 0.5 else 'v'  # zufällige 50/50  Orientierung

            # zufällige Koordinaten
            x = secrets.randbelow(columns)
            y = secrets.randbelow(rows)

            # Sicherstellung, kein Schiff außer Zellen ist
            if orientierung == 'h':
                if x + ship.length > columns:
                    x -= (x + ship.length - columns)
            elif orientierung == 'v':
                if y + ship.length > rows:
                    y -= (y + ship.length - rows)

            if self.place_ship(ship, Coordinate(x, y), orientierung):
                return

    def shiff_placing(self, win):
        win.clear()  # Option Schiffe Manuel oder Automatisch platzieren
        win.refresh()
        h, w = win.getmaxyx()
        win.addstr(0, 0, self.name + "  OPT1 >  CLICK ENTER TO USE THIS POSITIONS")
        win.addstr(1, 0,
                   self.name + "  OPT2 >  CLICK  SPACEBAR  TO POSITION YOUR SHIPS MANUALLY ")
        for type in SCHIFF_TYPEN:
            self.random_ship_placing(type)
        win.refresh()

        off_xachse = COLUMN_WIDTH
        off_yachse = 3 * ROWS_HIGH
        choosed_cell = Coordinate(-1, -1)
        self.board_show(off_xachse, off_yachse, choosed_cell, False, win)
        titel = self.name + "'s BOARD"
        win.addstr(off_yachse + ROWS_HIGH * (rows + 1), off_xachse + COLUMN_WIDTH * columns // 2 - len(titel) // 2, titel)
        win.refresh()

        while True:
            key = win.getch()
            if key == curses.KEY_ENTER or key in [10, 13]:
                return

            elif key == ord(' '):
                self.board = []
                for r in range(rows):
                    self.board.append([EMPTY] * columns)
                self.schiffe = []
                break

        choosed_cell = Coordinate(0, 0)
        for type in SCHIFF_TYPEN:  # Falls Manuele Schiffstellung, dann Optionen h-v Stellung
            while True:
                win.addstr(0, 0, self.name + " PLACE YOUR SHIPS " + space)
                win.addstr(1, 0, "SHIP: " + type[0] + space)

                mouse_kontrolle_msg = ["USE CURSOR KEYS OR MAUS TO PLACE THE SHIPS"]
                keyboard_kontrolle_msg = ["CLICK " + "H" + " FOR HORIZONTAL PLACEMENT",
                                          "CLICK " + "V" + " FOR VERTICAL PLACEMENT"]

                kontrolle_msg = [mouse_kontrolle_msg, keyboard_kontrolle_msg]

                cx = off_xachse + rows * COLUMN_WIDTH + off_xachse
                cy = off_yachse + columns // 2

                win.addstr(cy - ROWS_HIGH, cx + len(mouse_kontrolle_msg[0]) // 2 - len("CONTROL") // 2,
                                "CONTROL")
                for cm in kontrolle_msg:
                    for m in cm:
                        win.addstr(cy, cx, m)
                        cy += 1
                    cy += 1
                win.refresh()

                win.refresh()
                self.board_show(off_xachse, off_yachse, choosed_cell, False, win)
                orientierung = 'none'

                key = win.getch()

                if key == curses.KEY_DOWN:
                    choosed_cell.y += 1
                elif key == curses.KEY_UP:
                    choosed_cell.y -= 1
                elif key == curses.KEY_LEFT:
                    choosed_cell.x -= 1
                elif key == curses.KEY_RIGHT:
                    choosed_cell.x += 1


                elif key == curses.KEY_MOUSE:

                    _, mousex, mousey, _, bstate = curses.getmouse()

                    row = (mousey - off_yachse) // ROWS_HIGH
                    col = (mousex - 1 - off_xachse) // COLUMN_WIDTH
                    choosed_cell = Coordinate(col, row)

                    if columns <= choosed_cell.x or choosed_cell.x < 0 or choosed_cell.y < 0 or choosed_cell.y >= rows:
                        continue

                if choosed_cell.x < 0:
                    choosed_cell.x = columns - 1
                if choosed_cell.x >= columns:
                    choosed_cell.x = 0
                if choosed_cell.y < 0:
                    choosed_cell.y = rows - 1
                if choosed_cell.y >= rows:
                    choosed_cell.y = 0

                if key == ord('h'):
                    orientierung = 'h'

                elif key == ord('v'):
                    orientierung = 'v'

                if orientierung != 'none':
                    ship = Ship(type)
                    erfolg = self.place_ship(ship, choosed_cell, orientierung)
                    if erfolg:
                        win.clear()
                        win.attron(curses.color_pair(2))
                        win.addstr(h - ROWS_HIGH * 2, 0, type[0] + " ADDED")
                        win.attron(curses.color_pair(2))
                        self.board_show(off_xachse, off_yachse, choosed_cell, False, win)

                        break
                    else:
                        win.clear()
                        win.attron(curses.color_pair(4))
                        win.addstr(h - ROWS_HIGH * 2, 0, " CAN NOT PLACE IT THERE! ")
                        win.attroff(curses.color_pair(4))

                win.refresh()
                # self.board_anzeigen(offx, offy, ausgewählte_zelle, False, gewinnen)

    def board_show(self, off_xachse, off_yachse, choosed_cell, hidden, win):

        for y in range(rows):
            for x in range(columns):

                if x == 0:
                    win.addstr(off_yachse + y * ROWS_HIGH, off_xachse - COLUMN_WIDTH // 2, str(y + 1))

                if y == 0:
                    win.addstr(off_yachse - ROWS_HIGH, off_xachse + COLUMN_WIDTH * x + COLUMN_WIDTH // 2, chr(65 + x))

                code = self.board[y][x]

                ausgewähltes = Coordinate(x, y) == choosed_cell

                if code == EMPTY or code == HIT or code == MISS or code == DESTROYED:
                    grafiks.cells_look(Coordinate(x, y), off_xachse, off_yachse, code, ausgewähltes, win)
                else:
                    if hidden:
                        grafiks.cells_look(Coordinate(x, y), off_xachse, off_yachse, EMPTY, ausgewähltes, win)
                    else:
                        grafiks.cells_look(Coordinate(x, y), off_xachse, off_yachse, " " + code + " ", ausgewähltes, win)


