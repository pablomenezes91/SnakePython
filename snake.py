import curses
import time 

def game_loop(window):

    curses.curs_set(0)
    window.border(0)
    height, width = window.getmaxyx()

    personagem = [10, 15]
    window.addch(personagem[0], personagem[1], curses.ACS_DIAMOND)
    while True:
        window.timeout(1000)
        char = window.getch()
        window.clear()
        window.border(0)

        match char:
            case curses.KEY_UP: 
                personagem[0] -= 1
            case curses.KEY_LEFT: 
                personagem[1] -= 1
            case curses.KEY_DOWN: 
                personagem[0] += 1
            case curses.KEY_RIGHT: 
                personagem[1] += 1
            case _:
                pass

        if (personagem[0] <= 0) or (personagem[0] >= height-1):
            return
        if (personagem[1] <= 0) or (personagem[1] >= width-1):
            return
        window.addch(personagem[0], personagem[1], curses.ACS_DIAMOND)

if __name__ == '__main__':
    curses.wrapper(game_loop)
    print('Perdeu!')