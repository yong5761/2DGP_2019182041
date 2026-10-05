import os

import pico2d as _p2d
from pico2d import *

CANVAS_W, CANVAS_H = 1200, 800
CX, CY   = 600, 400
SCALE    = 3

# 이동 동작: 이름 → 프레임당 이동 픽셀 (없으면 화면 중앙 고정)
MOVING_SPEED = {
    'Walk':     5,
    'Run':      10,
    'Run Fast': 16,
    'Skate Run': 12,
}

# 불균일 간격 행: 각 프레임의 x 시작좌표를 직접 지정
RUN_X   = [8, 37, 65, 97, 135, 170, 206, 238, 263, 295, 334, 370]
SKATE_X = [1, 31, 64,  99, 136, 176, 217, 254]

# (name, pico_bot, fh, x_off, fw, frame_count, frame_delay)
# pico_bot: pico2d 하단-y 좌표 = 524 - PIL_bottom
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

FRAME_X = {'Run': RUN_X, 'Skate Run': SKATE_X}


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            close_canvas(); exit()
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            close_canvas(); exit()


def draw_frame(pico_bot, fh, clip_x, fw, draw_x=None):
    x = draw_x if draw_x is not None else CX
    image.clip_draw(clip_x, pico_bot, fw, fh,
                    x, CY, fw * SCALE, fh * SCALE)


def play_once(anim, start_x=None):
    name, pico_bot, fh, x_off, fw, frame_count, frame_delay = anim
    xs    = FRAME_X.get(name)
    speed = MOVING_SPEED.get(name, 0)
    x     = start_x if (speed and start_x is not None) else (-(fw * SCALE) // 2 if speed else CX)
    for f in range(frame_count):
        clip_x = xs[f] if xs else x_off + f * fw
        clear_canvas()
        draw_frame(pico_bot, fh, clip_x, fw, x if speed else None)
        font.draw(20, CANVAS_H - 20, name, (255, 255, 0))
        update_canvas()
        delay(frame_delay)
        handle_events()
        if speed:
            x += speed
            if x > CANVAS_W + fw * SCALE // 2:
                x = -(fw * SCALE) // 2
    return x


def play_animation(anim, repeat=5, pause_sec=1.0):
    name, _, _, _, fw, _, _ = anim
    speed = MOVING_SPEED.get(name, 0)
    x = -(fw * SCALE) // 2 if speed else None
    for _ in range(repeat):
        x = play_once(anim, x)
    delay(pause_sec)


open_canvas(CANVAS_W, CANVAS_H)
image = load_image('sonic-sprite.png')

_font_path = os.path.join(os.path.dirname(_p2d.__file__), 'data', 'ConsolaMalgun.ttf')
font = Font(_font_path, 24)

while True:
    for anim in ANIMATIONS:
        play_animation(anim)
