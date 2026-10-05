# PRD: Sonic Animation Viewer

커밋할때 메시지는 무조건 한글로 한다

## 개요

Classic Sonic 스프라이트 시트(`sonic-sprite.png`)에 담긴 모든 애니메이션을 순서대로 자동 재생하는 뷰어.
각 동작을 5회 반복 후 1초 정지, 전체 순환이 끝나면 처음부터 무한 반복한다.

---

## 기술 스택 & 제약

| 항목 | 내용 |
|------|------|
| 언어 | Python 3 |
| 라이브러리 | pico2d |
| 출력 파일 | `sonic_animation_viewer.py` (단일 파일) |
| 에셋 | `sonic-sprite.png` (동일 디렉터리) |

---

## 화면 설정

- 캔버스 크기: **1200 × 800**
- 배경: 단색 (검정)
- 소닉 렌더 크기: 원본 프레임 크기 × **3배** 확대
- 렌더 위치: 화면 중앙 (400, 300)

---

## 스프라이트 시트 실측 데이터

이미지 크기: **399 × 525 px (RGBA)**

pico2d는 **좌하단 원점** 좌표계를 사용한다.  
`pico_bot = 524 - PIL_bottom` (PIL y는 상단이 0)

### 좌표 테이블

| # | 동작 | pico_bot | fh | x_off | fw | frames | delay(s) | 비고 |
|---|------|----------|----|----|----|----|-------|------|
| 1 | Walk | 447 | 39 | 1 | 30 | 11 | 0.10 | 일부 프레임 인접, fw 미세조정 필요 |
| 2 | Run | 407 | 39 | 8 | 33 | 12 | 0.07 | 간격 불균일, 구현 시 검증 필요 |
| 3 | Run Fast | 361 | 43 | 1 | 43 | 6 | 0.06 | 슬래시 이펙트 포함 |
| 4 | Spin Dash | 325 | 33 | 1 | 33 | 9 | 0.05 | 균일 |
| 5 | Ball Roll | 292 | 27 | 1 | 35 | 6 | 0.06 | 균일 |
| 6 | Insta-Shield | 251 | 36 | 1 | 37 | 6 | 0.06 | 균일 |
| 7 | Spin (small) | 207 | 35 | 1 | 35 | 2 | 0.08 | Row 7 전반부 |
| 8 | Spin Attack | 207 | 35 | 72 | 50 | 4 | 0.07 | Row 7 후반부 (링 이펙트) |
| 9 | Idle | 154 | 45 | 1 | 30 | 6 | 0.12 | Row 8 전반부 |
| 10 | Hurt | 154 | 45 | 184 | 48 | 2 | 0.10 | Row 8 후반부 |
| 11 | Skate Run | 108 | 40 | 1 | 36 | 8 | 0.07 | 간격 불균일 |
| 12 | Victory | 56 | 43 | 6 | 47 | 2 | 0.15 | Row 10 전반부 |
| 13 | Standing | 56 | 43 | 96 | 29 | 2 | 0.20 | Row 10 후반부 |

### Row 2 / 11 실측 x_starts (불균일 행 참고용)

```
Run   (Row 2): x_starts = [8, 37, 65, 97, 135, 170, 206, 238, 263, 295, 334, 370]
Skate (Row11): x_starts = [1, 31, 64,  99, 136, 176, 217, 254]
```

> 불균일 행은 `clip_draw(x_starts[f], pico_bot, fw, fh, ...)` 방식으로
> 각 프레임의 정확한 x를 직접 지정하면 된다.

---

## 이동 동작 사양

이동이 포함된 동작은 화면 중앙 고정이 아니라 왼쪽→오른쪽으로 실제 이동한다.

| 동작 | 프레임당 이동(px) |
|------|-----------------|
| Walk | 5 |
| Run | 10 |
| Run Fast | 16 |
| Skate Run | 12 |

- 화면 오른쪽 끝을 벗어나면 왼쪽 끝에서 다시 등장 (wrap)
- 5회 반복 사이에도 x 위치를 유지해 끊김 없이 이어진다
- 나머지 동작(Spin Dash, Ball Roll, Idle 등)은 화면 중앙 고정

---

## 재생 로직

```
for each animation in ANIMATIONS:
    x = 화면 왼쪽 끝 (이동 동작) or CX (고정 동작)
    for _ in range(5):          # 5회 반복
        x = play_once(animation, start_x=x)
    delay(1.0)                  # 1초 정지

→ 전체 완료 후 처음으로 돌아가 무한 반복
```

- `play_once(anim, start_x)`: 프레임 0 → 마지막을 1사이클 재생, 최종 x 반환
- 이동 동작은 매 프레임 x += speed, 오른쪽 끝 초과 시 왼쪽 끝으로 wrap
- 프레임 간격: 동작별 delay 값 사용

---

## 코드 설계

```python
CANVAS_W, CANVAS_H = 1200, 800
CX, CY = 600, 400

# 이동 동작: 이름 → 프레임당 이동 픽셀
MOVING_SPEED = {
    'Walk':     5,
    'Run':      10,
    'Run Fast': 16,
    'Skate Run': 12,
}
SCALE  = 3
H_IMG  = 525          # 이미지 높이 (pico_bot 계산 기준)

# (name, pico_bot, fh, x_off, fw, frame_count, delay)
ANIMATIONS = [
    ('Walk',         447, 39,   1, 30, 11, 0.10),
    ('Run',          407, 39,   8, 33, 12, 0.07),
    ('Run Fast',     361, 43,   1, 43,  6, 0.06),
    ('Spin Dash',    325, 33,   1, 33,  9, 0.05),
    ('Ball Roll',    292, 27,   1, 35,  6, 0.06),
    ('Insta-Shield', 251, 36,   1, 37,  6, 0.06),
    ('Spin (small)', 207, 35,   1, 35,  2, 0.08),
    ('Spin Attack',  207, 35,  72, 50,  4, 0.07),
    ('Idle',         154, 45,   1, 30,  6, 0.12),
    ('Hurt',         154, 45, 184, 48,  2, 0.10),
    ('Skate Run',    108, 40,   1, 36,  8, 0.07),
    ('Victory',       56, 43,   6, 47,  2, 0.15),
    ('Standing',      56, 43,  96, 29,  2, 0.20),
]

def draw_frame(pico_bot, fh, clip_x, fw, draw_x=None):
    """단일 프레임을 SCALE배 확대해 draw_x(없으면 CX)에 그린다."""
    x = draw_x if draw_x is not None else CX
    image.clip_draw(clip_x, pico_bot, fw, fh, x, CY, fw * SCALE, fh * SCALE)

def play_once(anim, start_x=None):
    """클립을 1회 재생. 이동 동작이면 start_x에서 출발해 최종 x를 반환."""
    name, pico_bot, fh, x_off, fw, frame_count, frame_delay = anim
    speed = MOVING_SPEED.get(name, 0)
    x = start_x if (speed and start_x is not None) else (-(fw * SCALE) // 2 if speed else CX)
    xs = FRAME_X.get(name)
    for f in range(frame_count):
        clip_x = xs[f] if xs else x_off + f * fw
        clear_canvas()
        draw_frame(pico_bot, fh, clip_x, fw, x if speed else None)
        font.draw(20, CANVAS_H - 20, name, (255, 255, 0))
        update_canvas()
        delay(frame_delay)
        handle_events()
        if speed:
            x += speed
            if x > CANVAS_W + fw * SCALE // 2:
                x = -(fw * SCALE) // 2
    return x

def play_animation(anim, repeat=5, pause_sec=1.0):
    """클립을 repeat회 재생 후 pause_sec 정지. 이동 동작은 x를 이어서 유지."""
    name, _, _, _, fw, _, _ = anim
    speed = MOVING_SPEED.get(name, 0)
    x = -(fw * SCALE) // 2 if speed else None
    for _ in range(repeat):
        x = play_once(anim, x)
    delay(pause_sec)
```

---

## 커밋 계획 (26개)

> 모든 커밋 메시지는 **한글**로 작성한다.

### Phase 1 — 뼈대

| 커밋 | 내용 |
|------|------|
| 01 | 파일 생성, 캔버스 상수 정의, `open_canvas` 호출 |
| 02 | 스프라이트 시트 로드 및 빈 게임 루프 (`while True` + `get_events`) |
| 03 | `clear_canvas` / `update_canvas` 호출로 빈 화면 정상 렌더 확인 |

### Phase 2 — 렌더 기반

| 커밋 | 내용 |
|------|------|
| 04 | SCALE·CX·CY 상수 및 `ANIMATIONS` 리스트 뼈대 추가 |
| 05 | `draw_frame` 함수 구현 (clip_draw + SCALE 적용) |
| 06 | `play_once` 함수 구현 |
| 07 | `play_animation` 함수 구현 (5회 반복 + 1초 정지) |

### Phase 3 — 애니메이션 클립 등록

| 커밋 | 내용 |
|------|------|
| 08 | Walk 클립 추가 및 단독 재생 확인 |
| 09 | Run 클립 추가 |
| 10 | Run Fast 클립 추가 |
| 11 | Spin Dash 클립 추가 |
| 12 | Ball Roll 클립 추가 |
| 13 | Insta-Shield 클립 추가 |
| 14 | Spin (small) 클립 추가 |
| 15 | Spin Attack 클립 추가 |
| 16 | Idle 클립 추가 |
| 17 | Hurt 클립 추가 |
| 18 | Skate Run 클립 추가 |
| 19 | Victory 클립 추가 |
| 20 | Standing 클립 추가 |

### Phase 4 — 전체 순환 루프

| 커밋 | 내용 |
|------|------|
| 21 | 전체 `ANIMATIONS` 순환 루프 구현 |
| 22 | 무한 반복 (`while True`) 적용 및 동작 확인 |

### Phase 5 — 품질 & 마무리

| 커밋 | 내용 |
|------|------|
| 23 | 불균일 행(Run, Skate) 좌표 미세조정 |
| 24 | 동작별 `delay` 튜닝 |
| 25 | 현재 동작명 화면 상단 출력 |
| 26 | ESC 키 종료 처리 및 코드 정리 |

---

## 완료 기준

- [ ] 13개 애니메이션 클립이 모두 잘린 프레임 없이 재생된다
- [ ] 각 동작이 정확히 5회 반복 후 1초 정지된다
- [ ] 전체 순환 후 자동으로 처음부터 재시작된다
- [ ] 소닉이 화면 중앙에 3배 확대되어 표시된다
- [ ] ESC 키로 종료할 수 있다
- [ ] 단일 파일(`sonic_animation_viewer.py`)로 실행 가능하다
