import time

from pico2d import *

open_canvas()

sheet1 = load_image('FreeCharacter-Sprite-Sheets-1.jpg')
sheet2 = load_image('FreeCharacter-Sprite-Sheets-2.jpg')
village = load_image('Village.jpg')

FRAME_W  = 144
OFFSET_X = 370
CX, CY   = 400, 125
DRAW_W   = 160
DRAW_H   = 160
DURATION = 5.0

# 픽셀 스캔 기반 실제 캐릭터 위치 (bottom = 발 y_img, frame_h = 캐릭터 높이+버퍼)
IDLE = (799,  92)   # 실제 발 y_img=801, 위로 92px
WALK = (648, 153)   # 실제 발 y_img=650, 위로 153px (캐릭터 150px)
RUN  = (503,  94)   # 실제 발 y_img=505, 위로 94px (캐릭터 90px)
JUMP = (161, 141)   # 실제 발 y_img=161, Hurt(y_img=160) 바로 위 — 발색=Hurt색 동일해 JPEG 번짐 무시됨

def draw_frame(sheet, bottom, f, x, flip='', frame_h=148):
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

play_animation(sheet1, IDLE, 4)
walk_across   (sheet1, WALK, 6, 10)
walk_across   (sheet1, RUN,  6, 20)
play_animation(sheet1, JUMP, 6)

close_canvas()
