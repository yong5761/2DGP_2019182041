from pico2d import *

open_canvas()

sheet1 = load_image('FreeCharacter-Sprite-Sheets-1.jpg')
sheet2 = load_image('FreeCharacter-Sprite-Sheets-2.jpg')

village = load_image('Village.jpg')

FRAME_W, FRAME_H = 144, 100
OFFSET_X = 370
CX, CY = 400, 182
DRAW_W, DRAW_H = 160, 160

# Idle: sheet1 row0, 4 frames, bottom=800
for f in range(4):
    clear_canvas()
    village.draw(400, 300, 800, 600)
    sheet1.clip_draw(OFFSET_X + f * FRAME_W, 800, FRAME_W, FRAME_H, CX, CY, DRAW_W, DRAW_H)
    update_canvas()
    delay(0.1)

close_canvas()
