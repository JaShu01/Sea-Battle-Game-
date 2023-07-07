


from func import *
class grafiks:
    def cells_look(coord, off_xachse, off_yachse, code, choosed, win):
        # Boards Darstellung (Grapisch)
        if choosed:
            win.attron(curses.color_pair(7))
            win.addstr(coord.y * ROWS_HIGH + off_yachse, coord.x * COLUMN_WIDTH + 1 + off_xachse,
                       str(code))  # Zellenfarbe auf das eingestellte Farbpaar ändern
            win.attroff(curses.color_pair(7))
        else:
            if code == HIT or code == DESTROYED:
                win.attron(curses.color_pair(6))
                win.addstr(coord.y * ROWS_HIGH + off_yachse, coord.x * COLUMN_WIDTH + 1 + off_xachse,
                           str(code))
                win.attroff(curses.color_pair(6))

            elif code == MISS:
                win.attron(curses.color_pair(1))
                win.addstr(coord.y * ROWS_HIGH + off_yachse, coord.x * COLUMN_WIDTH + 1 + off_xachse,
                           str(code))
                win.attroff(curses.color_pair(1))

            elif code == EMPTY:
                win.addstr(coord.y * ROWS_HIGH + off_yachse, coord.x * COLUMN_WIDTH + 1 + off_xachse, str(code))

            else:
                win.attron(curses.color_pair(5))
                win.addstr(coord.y * ROWS_HIGH + off_yachse, coord.x * COLUMN_WIDTH + 1 + off_xachse,
                           str(code))
                win.attroff(curses.color_pair(5))

        win.attron(curses.color_pair(3))
        win.addch(coord.y * ROWS_HIGH + off_yachse, coord.x * COLUMN_WIDTH + off_xachse, curses.ACS_VLINE)
        win.addch(coord.y * ROWS_HIGH + off_yachse, coord.x * COLUMN_WIDTH + COLUMN_WIDTH + off_xachse, curses.ACS_VLINE)
        for i in range(COLUMN_WIDTH + 1):  # Farbe der gesamten Spielerboard
            if i == 0:
                win.addch(coord.y * ROWS_HIGH + off_yachse - ROWS_HIGH // 2, coord.x * COLUMN_WIDTH + off_xachse + i, "-")
            elif i == COLUMN_WIDTH:
                win.addch(coord.y * ROWS_HIGH + off_yachse - ROWS_HIGH // 2, coord.x * COLUMN_WIDTH + off_xachse + i, "-")
            else:
                win.addch(coord.y * ROWS_HIGH + off_yachse - ROWS_HIGH // 2, coord.x * COLUMN_WIDTH + off_xachse + i, "-")
        for i in range(COLUMN_WIDTH + 1):
            if i == 0:
                win.addch(coord.y * ROWS_HIGH + off_yachse + ROWS_HIGH // 2, coord.x * COLUMN_WIDTH + off_xachse + i, "-")
            elif i == COLUMN_WIDTH:
                win.addch(coord.y * ROWS_HIGH + off_yachse + ROWS_HIGH // 2, coord.x * COLUMN_WIDTH + off_xachse + i, "-")
            else:
                win.addch(coord.y * ROWS_HIGH + off_yachse + ROWS_HIGH // 2, coord.x * COLUMN_WIDTH + off_xachse + i, "-")
        win.attroff(curses.color_pair(3))

        win.refresh()
