from pico2d import *

CANVAS_W, CANVAS_H = 1200, 800
CX, CY = 600, 400
SCALE  = 3

# (name, pico_bot, fh, x_off, fw, frame_count, delay)
ANIMATIONS = []

def draw_frame(pico_bot, fh, x_off, fw, frame_idx):
    clip_x = x_off + frame_idx * fw
    image.clip_draw(clip_x, pico_bot, fw, fh,
                    CX, CY, fw * SCALE, fh * SCALE)

def play_once(anim):
    _, pico_bot, fh, x_off, fw, frame_count, frame_delay = anim
    for f in range(frame_count):
        clear_canvas()
        draw_frame(pico_bot, fh, x_off, fw, f)
        update_canvas()
        delay(frame_delay)
        get_events()

open_canvas(CANVAS_W, CANVAS_H)

image = load_image('sonic-sprite.png')

while True:
    clear_canvas()
    update_canvas()
    get_events()
