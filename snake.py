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

def move_snake(snake, direction,ate_fruit):
    head = snake[0].copy()
    snake.insert(0, head)
    move_actor(head, direction)
    if not ate_fruit:
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

def snake_hit_itself(snake):
    head = snake[0]
    body = snake[1:]
    return head in body

def direction_is_opposite(direction,current_direction):
    match direction:
        case curses.KEY_UP: 
            return current_direction == curses.KEY_DOWN
        case curses.KEY_LEFT: 
            return current_direction == curses.KEY_RIGHT
        case curses.KEY_DOWN: 
            return current_direction == curses.KEY_UP
        case curses.KEY_RIGHT: 
            return current_direction == curses.KEY_LEFT

def finish_game(score, window):
    height, width = window.getmaxyx()
    s = f'Você perdeu! Coletou {score} frutas!'
    y = int(height/2)
    x = int((width - len(s)) / 2)
    window.addstr(y, x, s)
    window.refresh()
    time.sleep(10)

def select_difficulty():
    difficulty = {
        '1': 1000,
        '2': 500,
        '3': 150,
        '4': 90,
        '5': 35,
    }
    while True:
        answer = input('Selecione a dificuldade de 1 a 5: ')
        game_speed = difficulty.get(answer)
        if game_speed is not None:
            return game_speed
        print('Escolha a dificuldade de 1 a 5! \n')


def game_loop(window,game_speed):
    # Setup Inicial
    curses.curs_set(0)
    snake = [[10, 15],[9, 15],[8, 15],[7, 15]]
    fruit = get_new_fruit(window)
    ate_fruit = False
    current_direction = curses.KEY_DOWN
    score = 0
    
    while True:
        draw_screen(window)
        draw_snake(snake, window)
        draw_actor(fruit,window,curses.ACS_DIAMOND)
        direction = get_new_direction(window,game_speed)

        if direction is  None:
            direction = current_direction
        
        if direction_is_opposite(direction,current_direction):
            direction = current_direction

        move_snake(snake, direction,ate_fruit)
        
        if snake_hit_border(snake,window):
            break
        
        if snake_hit_itself(snake):
            break

        if snake_hit_fruit(snake,fruit):
            fruit = get_new_fruit(window)
            ate_fruit = True
            score += 1
        else:
            ate_fruit = False
        
        current_direction = direction
    
    finish_game(score,window)

if __name__ == '__main__':
    curses.wrapper(game_loop, game_speed=select_difficulty())