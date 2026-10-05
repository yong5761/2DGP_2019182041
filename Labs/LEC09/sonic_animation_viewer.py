from pico2d import *

CANVAS_W, CANVAS_H = 1200, 800
CX, CY = 600, 400
SCALE  = 3

# (name, pico_bot, fh, x_off, fw, frame_count, delay)
ANIMATIONS = []

open_canvas(CANVAS_W, CANVAS_H)

image = load_image('sonic-sprite.png')

while True:
    clear_canvas()
    update_canvas()
    get_events()
