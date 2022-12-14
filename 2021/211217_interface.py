# pip install pgzero
# pgzrun 211217_interface.py

import pgzrun
from importlib import import_module
util = import_module('211217').First(False)

WIDTH = 400
HEIGHT = 600
SIZE = 2
Y_MAX = -1
OFFSET = (0, HEIGHT // 6)
x, y = 10, 10
TARGET = None


def get_target(i=2):
    global TARGET
    examples = list(util.examples)
    TARGET = util.pre_treat(examples[i])


def resize(coord):
    x, y = coord
    return (x * SIZE, y * SIZE)


def coord2pt(coord):
    x, y = resize(coord)
    return (x + OFFSET[0], -y + OFFSET[1])


def draw_dot(pt):
    screen.draw.filled_circle(coord2pt(pt), SIZE // 2, 'white')


def draw_steps(vel):
    y_max = -1
    for i, j in util.get_pos((x, y), TARGET):
        y_max = max(y_max, j)
        draw_dot((i, j))
    return y_max


def draw_target():
    x, a, b, y = TARGET
    w, h = abs(a - x), abs(b - y)
    screen.draw.filled_rect(Rect((coord2pt((x, y)), resize((w, h)))), (245, 138, 61))


def on_key_up(key, mod):
    global x, y
    if key == keys.K_1:
        get_target(0)
    if key == keys.K_2:
        get_target(1)
    if key == keys.K_3:
        get_target(2)
    if key == keys.RIGHT:
        x += 1
    if key == keys.LEFT:
        x -= 1
    if key == keys.UP:
        y += 1
    if key == keys.DOWN:
        y -= 1
    if key == keys.ESCAPE:
        exit()


def draw():
    global x, y
    screen.clear()
    draw_target()
    screen.draw.line(coord2pt((0, 0)), coord2pt((x, y)), 'white')
    y_max = draw_steps((x, y))
    screen.draw.text(f'x: {x}, y: {y}\nMax height: {y_max}', (WIDTH//2, 20), fontsize=30)
    screen.draw.text(f'Use arrows to move initial velocity.\nPress esc. to quit.\nPress 1, 2, 3 to change target area.',
        (WIDTH//2, 100), fontsize=15)


get_target()
pgzrun.go()