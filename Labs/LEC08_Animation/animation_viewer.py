import time

from pico2d import *

open_canvas()

sheet1 = load_image('FreeCharacter-Sprite-Sheets-1.jpg')
sheet2 = load_image('FreeCharacter-Sprite-Sheets-2.jpg')
village = load_image('Village.jpg')

FRAME_W = 144
FRAME_H = 148  # 기본값: 행 상단 12px 스킵
OFFSET_X = 370
CX, CY = 400, 125
DRAW_W, DRAW_H = 160, 160
DURATION = 5.0

def draw_frame(sheet, bottom, f, x, flip='', frame_h=FRAME_H):
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

def play_animation(sheet, bottom, frame_count, frame_delay=0.1, frame_h=FRAME_H):
    f = 0
    start = time.time()
    while time.time() - start < DURATION:
        draw_frame(sheet, bottom, f, CX, frame_h=frame_h)
        delay(frame_delay)
        f = (f + 1) % frame_count

def walk_across(sheet, bottom, frame_count, speed, frame_h=FRAME_H):
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

# Idle: sheet1 row0, 4 frames, bottom=800
play_animation(sheet1, 800, 4)

# Walk: sheet1 row1, 6 frames, bottom=640
walk_across(sheet1, 640, 6, 10)

# Run: sheet1 row2, 6 frames, bottom=480
walk_across(sheet1, 480, 6, 20)

# Jump: bottom=165 (경계에서 5px 띄워 Hurt 행 블리드 방지)
play_animation(sheet1, 165, 6, frame_h=140)

close_canvas()
