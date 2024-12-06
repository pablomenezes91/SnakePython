import curses
import time 

def game_loop(window):
    personagem = [10, 15]
    window.addch(personagem[0], personagem[1], curses.ACS_DIAMOND)
    while True:
        window.timeout(1000)
        char = window.getch()
        window.clear()

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
        window.addch(personagem[0], personagem[1], curses.ACS_DIAMOND)

if __name__ == '__main__':
    curses.wrapper(game_loop)