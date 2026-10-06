# Drill #9 - 소년 상하 좌우 이동 및 방향 바꾸기
from pico2d import *

# ── 상수 ──────────────────────────────────────────────────────────────
TUK_W, TUK_H = 1280, 1024   # 캔버스 크기

SPEED        = 5             # 이동 속도 (px/프레임)
MARGIN       = 50            # 화면 경계 여유 (스프라이트 반크기)
CELL         = 100           # 스프라이트 셀 한 변 크기
FRAME_COUNT  = 8             # 행당 프레임 수

# 스프라이트 행 인덱스 (pico2d: y=0이 화면 하단)
# animation_sheet.png 행 구성
#   Row 3 (clip_y=300) : 최상단 → IDLE
#   Row 2 (clip_y=200) : WALK (미사용)
#   Row 1 (clip_y=100) : RUN 오른쪽
#   Row 0 (clip_y=  0) : RUN 왼쪽
ROW_IDLE      = 3
ROW_RUN_RIGHT = 1
ROW_RUN_LEFT  = 0

# ── 캔버스·이미지 로드 ─────────────────────────────────────────────────
open_canvas(TUK_W, TUK_H)
bg  = load_image('TUK_GROUND.png')
spr = load_image('animation_sheet.png')

# ── 전역 상태 변수 ────────────────────────────────────────────────────
running = True
x, y    = TUK_W // 2, TUK_H // 2   # 초기 위치: 화면 중앙
frame   = 0                          # 현재 애니메이션 프레임 인덱스
facing  = 'right'                    # 마지막 좌우 방향 ('right' | 'left')

# 키 누름 상태: KEYDOWN → True, KEYUP → False
# 딕셔너리로 관리해 다중 키 동시 입력을 정확히 처리
keys = {
    SDLK_RIGHT: False,
    SDLK_LEFT:  False,
    SDLK_UP:    False,
    SDLK_DOWN:  False,
}

# ── 이벤트 핸들러 ─────────────────────────────────────────────────────
def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key in keys:
                keys[event.key] = True
