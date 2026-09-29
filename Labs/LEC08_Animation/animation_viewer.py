import time

from pico2d import *

open_canvas()

sheet1 = load_image('FreeCharacter-Sprite-Sheets-1.jpg')
sheet2 = load_image('FreeCharacter-Sprite-Sheets-2.jpg')
village = load_image('Village.jpg')

FRAME_W  = 144
OFFSET_X = 370
CX, CY   = 400, 125
DRAW_W, DRAW_H = 160, 160
DURATION = 5.0

# (bottom, frame_h) — 픽셀 스캔 측정값 + 2px 경계 버퍼
IDLE    = (800, 88)
WALK    = (650, 148)
RUN     = (506, 88)
JUMP    = (162, 154)
HURT    = (74,  84)
DEATH   = (802, 84)
ATTACK1 = (362, 111)
ATTACK2 = (162, 154)
ATTACK3 = (74,  84)

def draw_frame(sheet, bottom, f, x, flip='', frame_h=80):
    clear_canvas()
    village.draw(400, 300, 800, 600)
    if flip:
        sheet.clip_composite_draw(
            OFFSET_X + f * FRAME_W, bottom, FRAME_W, frame_h,
            0, flip, x, CY, DRAW_W, DRAW_H
        )
    else:
        sheet.clip_draw(
            OFFSET_X + f * FRAME_W, bottom, FRAME_W, frame_h,
            x, CY, DRAW_W, DRAW_H
        )
    update_canvas()
    get_events()

def play_animation(sheet, clip, frame_count, frame_delay=0.1):
    bottom, frame_h = clip
    f = 0
    start = time.time()
    while time.time() - start < DURATION:
        draw_frame(sheet, bottom, f, CX, frame_h=frame_h)
        delay(frame_delay)
        f = (f + 1) % frame_count

def walk_across(sheet, clip, frame_count, speed):
    bottom, frame_h = clip
    f = 0
    x = CX
    while x < 720:
        draw_frame(sheet, bottom, f, x, frame_h=frame_h)
        delay(0.1)
        f = (f + 1) % frame_count
        x += speed
    while x > 80:
        draw_frame(sheet, bottom, f, x, 'h', frame_h=frame_h)
        delay(0.1)
        f = (f + 1) % frame_count
        x -= speed
    while x < CX:
        draw_frame(sheet, bottom, f, x, frame_h=frame_h)
        delay(0.1)
        f = (f + 1) % frame_count
        x += speed

play_animation(sheet1, IDLE,  4)
walk_across   (sheet1, WALK,  6, 10)
walk_across   (sheet1, RUN,   6, 20)
play_animation(sheet1, JUMP,  6)

close_canvas()
