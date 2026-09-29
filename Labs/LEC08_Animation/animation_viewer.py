import time

from pico2d import *

open_canvas()

sheet1  = load_image('sheet1.png')
sheet2  = load_image('sheet2.png')
village = load_image('Village.jpg')

# sheet1 프레임 설정 (라벨 370px)
FRAME_W  = 144
OFFSET_X = 370
CX, CY   = 400, 130
DRAW_W, DRAW_H = 160, 160
DURATION = 5.0

# sheet2 프레임 설정 (라벨 구간 다름: 캐릭터 x=480부터 시작, 셀 폭=148px)
S2_FW  = 148
S2_OFX = 480

# Sheet1 클립 (bottom, frame_h)
IDLE = (801, 148)   # Row0: Idle  4프레임
WALK = (650, 140)   # Row1: Walk  6프레임
RUN  = (505, 130)   # Row2: Run   6프레임
JUMP = (200, 118)   # Row4: Jump  6프레임
HURT = (  1, 155)   # Row5: Hurt  3프레임

# Sheet2 클립 (bottom, frame_h)
DEATH   = (805, 145)  # Row0 Death:   6프레임
ATTACK1 = (325, 135)  # Row3 Attack1: 6프레임
ATTACK2 = (165, 130)  # Row4 Attack2: 6프레임
ATTACK3 = (  5, 150)  # Row5 Attack3: 6프레임

def draw_frame(sheet, bottom, f, x, flip='', frame_h=160, fw=FRAME_W, off_x=OFFSET_X):
    clear_canvas()
    village.draw(400, 300, 800, 600)
    clip_x = off_x + f * fw
    if flip:
        sheet.clip_composite_draw(clip_x, bottom, fw, frame_h, 0, flip, x, CY, DRAW_W, DRAW_H)
    else:
        sheet.clip_draw(clip_x, bottom, fw, frame_h, x, CY, DRAW_W, DRAW_H)
    update_canvas()
    get_events()

def play_animation(sheet, clip, frame_count, frame_delay=0.1, duration=DURATION,
                   fw=FRAME_W, off_x=OFFSET_X):
    bottom, frame_h = clip
    f, start = 0, time.time()
    while time.time() - start < duration:
        draw_frame(sheet, bottom, f, CX, frame_h=frame_h, fw=fw, off_x=off_x)
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

while True:
    play_animation(sheet1, IDLE,    4)
    walk_across   (sheet1, WALK,    6, 10)
    walk_across   (sheet1, RUN,     6, 20)
    play_animation(sheet1, JUMP,    6)
    play_animation(sheet1, HURT,    3)
    play_animation(sheet2, ATTACK1, 6, fw=S2_FW, off_x=S2_OFX)
    play_animation(sheet2, ATTACK2, 6, fw=S2_FW, off_x=S2_OFX)
    play_animation(sheet2, ATTACK3, 6, fw=S2_FW, off_x=S2_OFX)
    play_animation(sheet2, DEATH,   6, duration=3.0, fw=S2_FW, off_x=S2_OFX)
