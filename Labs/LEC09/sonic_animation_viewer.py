from pico2d import *

CANVAS_W, CANVAS_H = 1200, 800

open_canvas(CANVAS_W, CANVAS_H)

image = load_image('sonic-sprite.png')

while True:
    clear_canvas()
    update_canvas()
    get_events()
