import curses
import time 
import random

def draw_screen(window):
    window.clear()
    window.border(0)

def draw_actor(actor, window,char):
    window.addch(actor[0], actor[1], char)

def draw_snake(snake,window):
    head = snake[0]
    body = snake[1:]
    draw_actor(head,window,char="@")

    for body_part in body:
        draw_actor(body_part,window,char="s")

def get_new_fruit(window):
    height, width = window.getmaxyx()
    return [random.randint(1, height-2),random.randint(1, width-2)]

def get_new_direction(window, timeout=1000):
    window.timeout(timeout)
    direction = window.getch()
    if direction in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT,curses.KEY_RIGHT]:
        return direction
    return None

def move_actor(actor, direction):
    match direction:
        case curses.KEY_UP: 
            actor[0] -= 1
        case curses.KEY_LEFT: 
            actor[1] -= 1
        case curses.KEY_DOWN: 
            actor[0] += 1
        case curses.KEY_RIGHT: 
            actor[1] += 1
        case _:
            pass

def move_snake(snake, direction):
    head = snake[0].copy()
    snake.insert(0, head)
    move_actor(head, direction)
    snake.pop()

def actor_hit_border(actor,window):
    height, width = window.getmaxyx()
    if (actor[0] <= 0) or (actor[0] >= height-1):
        return True
    if (actor[1] <= 0) or (actor[1] >= width-1):
        return True
    return False

def snake_hit_border(snake, window):
    head = snake[0]
    return actor_hit_border(head,window)

def snake_hit_fruit(snake,fruit):
    return fruit in snake

def game_loop(window):
    # Setup Inicial
    curses.curs_set(0)
    snake = [[10, 15],[9, 15],[8, 15],[7, 15]]
    fruit = get_new_fruit(window)
    current_direction = curses.KEY_DOWN
    
    while True:
        draw_screen(window)
        draw_snake(snake, window)
        draw_actor(fruit,window,curses.ACS_DIAMOND)
        direction = get_new_direction(window,timeout=1000)

        if direction is  None:
            direction = current_direction

        move_snake(snake, direction)
        
        if snake_hit_border(snake,window):
            return
        
        if snake_hit_fruit(snake,fruit):
            fruit = get_new_fruit(window)
        
        current_direction = direction

if __name__ == '__main__':
    curses.wrapper(game_loop)
    print('Perdeu!')