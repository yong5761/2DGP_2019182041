import time

from pico2d import *

open_canvas()

sheet1  = load_image('sheet1.png')   # 배경 투명 PNG
sheet2  = load_image('sheet2.png')
village = load_image('Village.jpg')

FRAME_W  = 144
OFFSET_X = 370
CX, CY   = 400, 130
DRAW_W, DRAW_H = 160, 160
DURATION = 5.0

# 픽셀스캔 기준 실제 발 위치 → 모든 애니메이션 발이 화면 동일 높이에 위치
# 투명 PNG이므로 h=150 내 빈 공간은 그냥 배경이 보임 (회색박스 없음)
IDLE = (801, 150)   # 발 y_img=801
WALK = (650, 150)   # 발 y_img=650
RUN  = (505, 135)   # 발 y_img=505, 행 상단(y_img=640)까지 135px
JUMP = (161, 150)   # 발 y_img=161, Hurt(160)와 같은 빨간색 → 1px JPEG 번짐 무시 가능

def draw_frame(sheet, bottom, f, x, flip='', frame_h=160):
    clear_canvas()
    village.draw(400, 300, 800, 600)
    if flip:
        sheet.clip_composite_draw(
            OFFSET_X + f * FRAME_W, bottom, FRAME_W, frame_h,
            0, flip, x, CY, DRAW_W, DRAW_H)
    else:
        sheet.clip_draw(
            OFFSET_X + f * FRAME_W, bottom, FRAME_W, frame_h,
            x, CY, DRAW_W, DRAW_H)
    update_canvas()
    get_events()

def play_animation(sheet, clip, frame_count, frame_delay=0.1):
    bottom, frame_h = clip
    f, start = 0, time.time()
    while time.time() - start < DURATION:
        draw_frame(sheet, bottom, f, CX, frame_h=frame_h)
        delay(frame_delay)
        f = (f + 1) % frame_count

def walk_across(sheet, clip, frame_count, speed):
    bottom, frame_h = clip
    f, x = 0, CX
    while x < 720:
        draw_frame(sheet, bottom, f, x, frame_h=frame_h)
        delay(0.1); f = (f + 1) % frame_count; x += speed
    while x > 80:
        draw_frame(sheet, bottom, f, x, 'h', frame_h=frame_h)
        delay(0.1); f = (f + 1) % frame_count; x -= speed
    while x < CX:
        draw_frame(sheet, bottom, f, x, frame_h=frame_h)
        delay(0.1); f = (f + 1) % frame_count; x += speed

play_animation(sheet1, IDLE, 4)
walk_across   (sheet1, WALK, 6, 10)
walk_across   (sheet1, RUN,  6, 20)
play_animation(sheet1, JUMP, 6)

close_canvas()
