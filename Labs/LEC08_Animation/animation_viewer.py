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
IDLE = (801, 148)   # 발 y_img=801, 행 경계(y_img=960)와 안전 간격
WALK = (650, 140)   # 발 y_img=649, h=140으로 Idle 번짐 영역(y_img=790~800) 제외
RUN  = (505, 130)   # 발 y_img=505, h=130으로 Walk 번짐 영역(y_img=634~640) 제외
JUMP = (200, 118)   # bottom=200으로 Hurt행 JPEG번짐(y_img≈162~199) 완전 차단
HURT = (  1, 155)   # Row5: 피격 3프레임 (빨간 캐릭터)

# Sheet2 애니메이션 클립 (bottom, frame_h)
ATTACK1 = (325, 135)  # Row3 Attack1: 6프레임
ATTACK2 = (165, 130)  # Row4 Attack2: 6프레임
ATTACK3 = (  5, 150)  # Row5 Attack3: 6프레임
DEATH   = (805, 145)  # Row0 Death:   6프레임

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

def play_animation(sheet, clip, frame_count, frame_delay=0.1, duration=DURATION):
    bottom, frame_h = clip
    f, start = 0, time.time()
    while time.time() - start < duration:
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

while True:
    play_animation(sheet1, IDLE,    4)
    walk_across   (sheet1, WALK,    6, 10)
    walk_across   (sheet1, RUN,     6, 20)
    play_animation(sheet1, JUMP,    6)
    play_animation(sheet1, HURT,    3)
    play_animation(sheet2, ATTACK1, 6)
    play_animation(sheet2, ATTACK2, 6)
    play_animation(sheet2, ATTACK3, 6)
    play_animation(sheet2, DEATH,   6, duration=3.0)
