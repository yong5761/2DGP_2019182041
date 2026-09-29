import time

from pico2d import *

open_canvas()

sheet1 = load_image('FreeCharacter-Sprite-Sheets-1.jpg')
sheet2 = load_image('FreeCharacter-Sprite-Sheets-2.jpg')
village = load_image('Village.jpg')

FRAME_W, FRAME_H = 144, 160
OFFSET_X = 370
CX, CY = 400, 125
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
    get_events()  # OS 이벤트 처리 (응답없음 방지)

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
    # 중앙 → 우
    while x < 720:
        draw_frame(sheet, bottom, f, x)
        delay(0.1)
        f = (f + 1) % frame_count
        x += speed
    # 우 → 좌 (반전)
    while x > 80:
        draw_frame(sheet, bottom, f, x, 'h')
        delay(0.1)
        f = (f + 1) % frame_count
        x -= speed
    # 좌 → 중앙
    while x < CX:
        draw_frame(sheet, bottom, f, x)
        delay(0.1)
        f = (f + 1) % frame_count
        x += speed

# Idle: sheet1 row0, 4 frames, bottom=800
play_animation(sheet1, 800, 4)

# Walk: sheet1 row1, 6 frames, bottom=640 (중앙→우→좌→중앙, speed=10)
walk_across(sheet1, 640, 6, 10)

# Run: sheet1 row2, 6 frames, bottom=480 (Walk과 같은 경로, 2배 속도)
walk_across(sheet1, 480, 6, 20)

# Jump: sheet1 row4, 6 frames, bottom=160
play_animation(sheet1, 160, 6)

close_canvas()
