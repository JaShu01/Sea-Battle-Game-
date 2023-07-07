

from func import *
import Player
import Coordinate


def main(par):
    curses.curs_set(0)  # um Mauscurser unsichbar zu machen
    # in der Spiel benutrere Farben
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)  # ya
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # orillas
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)  # ya esta
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_RED)  # ya que pones color de fonfo y letra
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_CYAN)  # cursor
    par.border(0)  # Standardbildschirm Rand
    curses.mousemask(1)  # Abhören Aktivierung (Maus)
    main_menu(par, 0)


def main_menu(winner, rows_index):
    winner.keypad(1)  # Tastaturereignissen abzuhören
    h, w = winner.getmaxyx()  # maximale Höhe und Breite des Curses-Fensters
    while True:
        winner.clear()
        for index, row in enumerate(menu):
            x = w // 2 - len(row) // 2  # Zentrierung der Zeilen bei X-achse
            y = h // 2 - len(menu) + index  # Zentrierung der Zeilen bei Y-achse

            if index == rows_index:
                winner.attron(curses.color_pair(1))  # die ausgewählte Option kennzuzeichnen
                winner.addstr(y, x, row)
                winner.attroff(curses.color_pair(1))
            else:
                winner.addstr(y, x, row)
        winner.refresh()

        input = winner.getch()
        winner.clear()

        # Optionen von Tastatur eintipp
        if input == curses.KEY_UP:
            rows_index -= 1

        elif input == curses.KEY_DOWN:
            rows_index += 1

        elif input == curses.KEY_ENTER or input in [10, 13]:
            game_starting(winner, rows_index)

        # Unterlauf- und Überlaufbehandlung
        if rows_index < 0:
            rows_index = len(menu) - 1
        elif rows_index >= len(menu):
            rows_index = 0


def game_starting(win, option):
    if option == 0:
        friend_game_starting(win)  # Spiel gegen Freund
    elif option == 1:
        sys.exit(0)


def friend_game_starting(win):
    win.clear()
    # Spieler inizialisierung
    jabrail = Player("[JABRAIL]")
    diego = Player("[DIEGO]")

    # Schiffe für Spieler 1-(Jabrail) platzieren
    jabrail.shiff_placing(win)
    win.clear()
    h, w = win.getmaxyx()
    message = jabrail.name + " ALL IS SET. CLICK ONE KEY TO CONTINUE  "  # Bildshirm Meldung
    win.addstr(h // 2, w // 2 - len(message) // 2, message)
    win.refresh()

    win.getch()

    # Schiffe für Spieler 2-(Diego) platzieren
    diego.shiff_placing(win)
    win.clear()
    h, w = win.getmaxyx()
    message = diego.name + " ALL IS SET. CLICK ONE KEY TO CONTINUE "
    win.addstr(h // 2, w // 2 - len(message) // 2, message)
    win.refresh()
    win.getch()

    game_running(jabrail, diego, win)  # Spielshleife Start


def draw(j, d, w):
    w.clear()
    h, w = w.getmaxyx()
    w.addstr(h // 2, w // 2 - 1, " IT'S A DRAW! ")  # Unentschieden Fall
    off_xachse = COLUMN_WIDTH
    off_yachse = ROWS_HIGH * 3
    w.refresh()
    # Zeigt die beiden Karten als nicht ausgeblendet an.
    j.board_show(off_xachse, off_yachse, Coordinate(-1, -1), False, w)
    d.board_show(off_xachse + columns * (COLUMN_WIDTH) + 2 * off_xachse, off_yachse, Coordinate(-1, -1), False, w)

    w.refresh()
    main_menu(w, 0)


def game_over(winner, loser, win):
    win.clear()
    h, w = win.getmaxyx()
    curses.flash()
    curses.flash()
    curses.flash()  # Blink von Bildshirm

    off_xachse = COLUMN_WIDTH
    off_yachse = ROWS_HIGH * 3

    win.addstr(h // 2, w // 2 + 38, "GAME OVER ")
    win.addstr(h // 2 + 1, w // 2 + 38, winner.name + " WINS! ")  # Meldung in Terminal stellen

    win.refresh()

    # Boards anzeigen
    winner.board_show(off_xachse, off_yachse, Coordinate(-1, -1), False, win)
    loser.board_show(off_xachse + columns * (COLUMN_WIDTH) + 2 * off_xachse, off_yachse, Coordinate(-1, -1), False, win)
    win.getch()
    main_menu(win, 0)


def game_running(j, d, win):
    # Schleife um, fürs Schießen von Terminal, fürs Verfehlen, Treffen und Versenken von Schiffen

    # Offsets sind für Ursprung
    off_xachse = COLUMN_WIDTH
    off_yachse = 3 * ROWS_HIGH

    win.refresh()

    # Jabrail-(Spieler 1) spielt erst
    aktual_player = j
    opponent = d

    selected_cell = Coordinate(0, 0)

    # Verbleibende Runde Anzahl
    turns = 0

    # user input
    user_row = 0
    user_column = 0

    while True:
        win.clear()

        while True:
            # Anzahl der Zuge gleich ist = Beide haben gespielt
            # Gewinnen Prüfung wird erst nach Zugsgleichheit durchgeführt
            if turns % 2 == 0:
                # Prüfung wird Durchgeführt
                if aktual_player.lost() and opponent.lost():
                    draw(aktual_player, opponent, win)
                elif aktual_player.lost():
                    game_over(winner=opponent, loser=aktual_player, win=win)
                elif opponent.lost():
                    game_over(winner=aktual_player, loser=opponent, win=win)

            # Nachricht über Wahloptionen
            win.addstr(0, 0, " " * COLUMN_WIDTH * 5 + aktual_player.name + "' TURN " + space)
            win.addstr(1, 0, "OPT1 > CLICK ON A COORDINATE OF YOUR RIVAL'S BOARD TO FIRE" + space)
            win.addstr(2, 0,
                       "OPT2 > CHOOSE A COORDINATE AND CLICK SPACEBAR TO FIRE")
            win.addstr(3, 0,
                       "OPT3 > WRITE THE COORDINATE  MANUALLY (E5) ")
            # Boards und Ergebnisse von Spielern anzeigen
            show_boards_and_results(aktual_player, opponent, off_xachse, off_yachse, selected_cell, win)

            # Benutzereingaben Korrigierung
            order = win.getch()

            if ord('A') <= order <= ord('Z') or ord('a') <= order <= ord('z'):
                user_column = order - ord('A') + 1 if order <= ord('Z') else order - ord(
                    'a') + 1  # a/A heist userspalte = 1
                user_row = 0

            elif chr(order).isdigit():  # als REIHEN<=10, also ist y immer eine einzelne Ziffer( oder ein Zeichen)
                user_row = user_row * 10 + order - ord(
                    '0')  # Verwendet wird die eingegebenen Ziffern, um eine Zahl zu bilden


            elif order not in [10, 13]:  # wenn Bruch,beide l neu zuweisen
                user_row = 0
                user_column = 0

            # Tastatureingabe
            if order == curses.KEY_DOWN:
                selected_cell.y += 1
            elif order == curses.KEY_UP:
                selected_cell.y -= 1
            elif order == curses.KEY_LEFT:
                selected_cell.x -= 1
            elif order == curses.KEY_RIGHT:
                selected_cell.x += 1

            # Unterflow- und Overflowbehandlung
            if selected_cell.x < 0:
                selected_cell.x = columns - 1
            if selected_cell.x >= columns:
                selected_cell.x = 0
            if selected_cell.y < 0:
                selected_cell.y = rows - 1
            if selected_cell.y >= rows:
                selected_cell.y = 0

                # Mauseingabe
            elif order == curses.KEY_MOUSE:

                click = curses.getmouse()
                mouse_xachse = click[1]
                mouse_yachse = click[2]
                row = (mouse_yachse - off_yachse) // ROWS_HIGH
                column = (mouse_xachse - 1 - off_xachse) // COLUMN_WIDTH
                selected_cell = Coordinate(column, row)
                if columns <= selected_cell.x or selected_cell.x < 0 or selected_cell.y < 0 or selected_cell.y >= rows:
                    continue

            # Taste gedrückt oder Mause gegklicked heißt Feuer
            if order == ord(' ') or order == curses.KEY_MOUSE or (
                    order in [10, 13] and user_column > 0 and user_row > 0):
                if user_row > 0 and user_column > 0:
                    selected_cell = Coordinate(user_column - 1, user_row - 1)
                    user_row = 0
                    user_column = 0
                # Auf gewähltee Zelle feuern
                success, message = opponent.hited_place(selected_cell)
                if success:
                    show_boards_and_results(aktual_player, opponent, off_xachse, off_yachse, selected_cell, win)
                    aktual_player, opponent = opponent, aktual_player
                    turns += 1
                    selected_cell = Coordinate(0, 0)
                    message += ". CLICK KEY TO CONTINUE. IT'S YOUR RIVAL'S TURN " + space  # Bildschirmansicht wechseln, um zu verhindern, dass der Gegner die gegnerische Board sieht.
                    win.attron(curses.color_pair(2))
                    win.addstr(0, 0, message)
                    win.addstr(1, 0, space + space)
                    win.addstr(2, 0, space + space)
                    win.addstr(3, 0, space + space)
                    win.refresh()
                    win.attroff(curses.color_pair(2))

                    win.getch()

                    win.clear()
                    h, w = win.getmaxyx()

                    # Dies verhindert, dass die Spieler versehentlich die Karte des anderen sehen
                    message = aktual_player.name + " YOUR TURN. CLICK KEY TO CONTINUE "  # Bildschirmansicht wechseln, um zu verhindern, dass der Gegner die gegnerische Board sieht.
                    win.addstr(h // 2, w // 2 - len(message) // 2, message)
                    win.refresh()
                    win.getch()
                    win.clear()
                    win.refresh()

                else:
                    # Missed Feuer, die Meldung anzeigen und die Runde nicht zählen
                    win.addstr(1, 0, space + space)
                    win.addstr(2, 0, space + space)
                    win.addstr(3, 0, space + space)
                    win.attron(curses.color_pair(4))
                    win.addstr(0, 0, message + space + space)
                    win.attroff(curses.color_pair(4))
                    win.refresh()
                    win.getch()

def show_boards_and_results(aktual_player, opponent, off_xachse, off_yachse, choosed_cell, win):
    # Anzeigen von Opponents Schiffen
    titel = "RIVAL'S BOARD"
    opponent.board_show(off_xachse, off_yachse, choosed_cell, True, win)
    win.addstr(off_yachse + ROWS_HIGH * (rows) + 1, off_xachse + COLUMN_WIDTH * columns // 2 - len(titel), titel)
    destroyed = 0  # Anzahl der versenkten eigenen Schiffe
    destroyed = opponent.destroyed_shifs_counting()
    scoring = 'SUNKEN SHIPS: ' + str(destroyed)
    win.addstr(off_yachse + ROWS_HIGH * (rows + 1), off_xachse + COLUMN_WIDTH * columns // 2 - len(titel), scoring)
    scoring = 'REMAINING SHIPS: ' + str(
        len(opponent.schiffe) - destroyed)  # verbleibend = gesamt - versenkt
    win.addstr(off_yachse + ROWS_HIGH * (rows + 1) + 1, off_xachse + COLUMN_WIDTH * columns // 2 - len(titel), scoring)

    # Aktuelles Stand und Schiffes anzeigen
    titel = "MY BOARD"
    off_xachse2 = off_xachse + columns * (COLUMN_WIDTH) + 2 * off_xachse
    win.addstr(off_yachse + ROWS_HIGH * (rows) + 1, off_xachse2 + COLUMN_WIDTH * columns // 2 - len(titel), titel)
    aktual_player.board_show(off_xachse2, off_yachse, Coordinate(-1, -1), False, win)
    destroyed = aktual_player.destroyed_shifs_counting()
    scoring = 'SUNKEN SHIPS: ' + str(destroyed)
    win.addstr(off_yachse + ROWS_HIGH * (rows + 1), off_xachse2 + COLUMN_WIDTH * columns // 2 - len(titel), scoring)
    scoring = 'REMAINING SHIPS: ' + str(len(aktual_player.schiffe) - destroyed)
    win.addstr(off_yachse + ROWS_HIGH * (rows + 1) + 1, off_xachse2 + COLUMN_WIDTH * columns // 2 - len(titel), scoring)

    win.refresh()  # das Fenster aktualisieren


curses.wrapper(main)