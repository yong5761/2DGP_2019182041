import time

from pico2d import *

open_canvas()

sheet1 = load_image('FreeCharacter-Sprite-Sheets-1.jpg')
sheet2 = load_image('FreeCharacter-Sprite-Sheets-2.jpg')
village = load_image('Village.jpg')

FRAME_W  = 144
FRAME_H  = 148   # 전체 통일 (행 상단 12px 스킵 → 배율 일정)
OFFSET_X = 370
CX, CY   = 400, 125
DRAW_W, DRAW_H = 160, 160
DURATION = 5.0

def draw_frame(sheet, bottom, f, x, flip=''):
    clear_canvas()
    village.draw(400, 300, 800, 600)
    if flip:
        sheet.clip_composite_draw(
            OFFSET_X + f * FRAME_W, bottom, FRAME_W, FRAME_H,
            0, flip, x, CY, DRAW_W, DRAW_H
        )
    else:
        sheet.clip_draw(
            OFFSET_X + f * FRAME_W, bottom, FRAME_W, FRAME_H,
            x, CY, DRAW_W, DRAW_H
        )
    update_canvas()
    get_events()

def play_animation(sheet, bottom, frame_count, frame_delay=0.1):
    f = 0
    start = time.time()
    while time.time() - start < DURATION:
        draw_frame(sheet, bottom, f, CX)
        delay(frame_delay)
        f = (f + 1) % frame_count

def walk_across(sheet, bottom, frame_count, speed):
    f = 0
    x = CX
    while x < 720:
        draw_frame(sheet, bottom, f, x)
        delay(0.1)
        f = (f + 1) % frame_count
        x += speed
    while x > 80:
        draw_frame(sheet, bottom, f, x, 'h')
        delay(0.1)
        f = (f + 1) % frame_count
        x -= speed
    while x < CX:
        draw_frame(sheet, bottom, f, x)
        delay(0.1)
        f = (f + 1) % frame_count
        x += speed

# Sheet1
play_animation(sheet1, 800, 4)   # Idle:  row0
walk_across   (sheet1, 640, 6, 10)  # Walk:  row1
walk_across   (sheet1, 480, 6, 20)  # Run:   row2
play_animation(sheet1, 162, 6)   # Jump:  row4 (bottom+2 → Hurt 경계 블리드 방지)

close_canvas()
