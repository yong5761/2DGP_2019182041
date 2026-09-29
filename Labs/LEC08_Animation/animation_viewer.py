import time

from pico2d import *

open_canvas()

sheet1 = load_image('FreeCharacter-Sprite-Sheets-1.jpg')
sheet2 = load_image('FreeCharacter-Sprite-Sheets-2.jpg')
village = load_image('Village.jpg')

FRAME_W, FRAME_H = 144, 100
OFFSET_X = 370
CX, CY = 400, 140
DRAW_W, DRAW_H = 160, 160
DURATION = 5.0

def play_animation(sheet, bottom, frame_count):
    f = 0
    start = time.time()
    while time.time() - start < DURATION:
        clear_canvas()
        village.draw(400, 300, 800, 600)
        sheet.clip_draw(OFFSET_X + f * FRAME_W, bottom, FRAME_W, FRAME_H, CX, CY, DRAW_W, DRAW_H)
        update_canvas()
        delay(0.1)
        f = (f + 1) % frame_count

# Idle: sheet1 row0, 4 frames, bottom=800
play_animation(sheet1, 800, 4)

close_canvas()
