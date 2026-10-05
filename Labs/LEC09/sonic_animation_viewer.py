from pico2d import *

CANVAS_W, CANVAS_H = 1200, 800
CX, CY = 600, 400
SCALE  = 3

# (name, pico_bot, fh, x_off, fw, frame_count, delay)
ANIMATIONS = [
    ('Walk',         447, 39,   1, 30, 11, 0.10),
    ('Run',          407, 39,   8, 33, 12, 0.07),
    ('Run Fast',     361, 43,   1, 43,  6, 0.06),
    ('Spin Dash',    325, 33,   1, 33,  9, 0.05),
    ('Ball Roll',    292, 27,   1, 35,  6, 0.06),
    ('Insta-Shield', 251, 36,   1, 37,  6, 0.06),
    ('Spin (small)', 207, 35,   1, 35,  2, 0.08),
    ('Spin Attack',  207, 35,  72, 50,  4, 0.07),
    ('Idle',         154, 45,   1, 30,  6, 0.12),
    ('Hurt',         154, 45, 184, 48,  2, 0.10),
    ('Skate Run',    108, 40,   1, 36,  8, 0.07),
    ('Victory',       56, 43,   6, 47,  2, 0.15),
    ('Standing',      56, 43,  96, 29,  2, 0.20),
]

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

def play_animation(anim, repeat=5, pause_sec=1.0):
    for _ in range(repeat):
        play_once(anim)
    delay(pause_sec)

open_canvas(CANVAS_W, CANVAS_H)

image = load_image('sonic-sprite.png')

while True:
    for anim in ANIMATIONS:
        play_animation(anim)
