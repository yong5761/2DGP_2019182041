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

- 캔버스 크기: **800 × 600**
- 배경: 단색 (검정 또는 짙은 파랑)
- 소닉 렌더 크기: 원본 프레임 크기 × **3배** 확대 (화면에서 명확히 보이도록)
- 렌더 위치: 화면 중앙 (400, 300)

---

## 스프라이트 시트 분석

`sonic-sprite.png` 는 Classic Sonic Sprites 시트로, 행(Row) 단위로 동작이 나뉜다.  
구현 전 `PIL` 또는 육안으로 각 행의 **y 좌표(top)**, **프레임 폭**, **프레임 높이**, **프레임 수**를 실측한다.

| # | 동작명 | 설명 | 프레임 수(예상) |
|---|--------|------|----------------|
| 1 | Run | 달리기 (1단계 속도) | 8 |
| 2 | Run Fast | 달리기 (2단계 속도) | 8 |
| 3 | Spin Dash | 스핀 대시 차지 | 8 |
| 4 | Ball Roll | 공 구르기 | 8 |
| 5 | Spin Attack | 링 스핀 공격 | 8 |
| 6 | Super Spin | 상위 스핀 변형 | 8 |
| 7 | Idle | 대기 포즈 | 6 |
| 8 | Hurt | 피격 | 4 |

> **주의:** 위 값은 초기 추정치다. 구현 Step 2(시트 분석 커밋)에서 실제 픽셀 좌표로 교체한다.

---

## 재생 로직

```
for each animation in ANIMATION_LIST:
    for repeat in range(5):          # 5회 반복
        play_animation(animation)
    pause(1.0)                       # 1초 정지

→ 전체 완료 시 처음으로 돌아가 무한 반복
```

- `play_animation`: 한 사이클(프레임 0 → 마지막) 을 1회 재생
- 프레임 간격(frame_delay): 기본 `0.08`초 (동작별로 조정 가능)

---

## 함수 설계

```python
# 상수
CANVAS_W, CANVAS_H = 800, 600
SCALE = 3          # 확대 배율
FPS_DELAY = 0.08   # 기본 프레임 간격

# 데이터 구조: 각 애니메이션 클립
# (name, row_top, frame_w, frame_h, frame_count, frame_delay)
ANIMATIONS = [
    ('Run',         ..., ..., ..., 8, 0.08),
    ('Run Fast',    ..., ..., ..., 8, 0.06),
    ('Spin Dash',   ..., ..., ..., 8, 0.07),
    ('Ball Roll',   ..., ..., ..., 8, 0.08),
    ('Spin Attack', ..., ..., ..., 8, 0.07),
    ('Super Spin',  ..., ..., ..., 8, 0.07),
    ('Idle',        ..., ..., ..., 6, 0.12),
    ('Hurt',        ..., ..., ..., 4, 0.10),
]

def draw_frame(image, top, frame_w, frame_h, frame_idx):
    """스프라이트 시트에서 단일 프레임을 확대해 중앙에 그린다."""

def play_once(image, clip):
    """클립을 1회 재생한다."""

def play_animation(image, clip, repeat=5, pause_sec=1.0):
    """클립을 repeat회 재생 후 pause_sec 정지한다."""
```

---

## 커밋 계획 (최소 20개)

### Phase 1 — 프로젝트 뼈대

| 커밋 | 내용 |
|------|------|
| 01 | `sonic_animation_viewer.py` 파일 생성, `open_canvas` 호출, 캔버스 상수 정의 |
| 02 | `sonic-sprite.png` 로드 및 빈 게임 루프(`while True` + `get_events`) 추가 |
| 03 | 배경 클리어 및 `update_canvas` 호출로 빈 화면 정상 렌더 확인 |

### Phase 2 — 스프라이트 시트 분석

| 커밋 | 내용 |
|------|------|
| 04 | 시트 각 행의 픽셀 좌표 주석으로 문서화, `ANIMATIONS` 리스트 뼈대 추가 |
| 05 | `draw_frame` 함수 구현 (clip_draw + 배율 적용) |

### Phase 3 — 애니메이션별 클립 등록 & 검증

| 커밋 | 내용 |
|------|------|
| 06 | Run 클립 좌표 확정 및 단독 재생 테스트 |
| 07 | Run Fast 클립 추가 |
| 08 | Spin Dash 클립 추가 |
| 09 | Ball Roll 클립 추가 |
| 10 | Spin Attack 클립 추가 |
| 11 | Super Spin 클립 추가 |
| 12 | Idle 클립 추가 |
| 13 | Hurt 클립 추가 |

### Phase 4 — 재생 제어 로직

| 커밋 | 내용 |
|------|------|
| 14 | `play_once` 함수 구현 (단일 사이클 재생) |
| 15 | `play_animation` 함수 구현 (5회 반복 + 1초 정지) |
| 16 | 전체 `ANIMATIONS` 순환 루프 구현 |
| 17 | 무한 반복(`while True`) 적용 및 동작 확인 |

### Phase 5 — 화면 품질 & 마무리

| 커밋 | 내용 |
|------|------|
| 18 | 확대 배율(SCALE) 상수화 및 중앙 좌표 계산 정리 |
| 19 | 동작별 `frame_delay` 개별 튜닝 (Run Fast 속도 증가 등) |
| 20 | 현재 동작명 화면 상단에 텍스트 출력 (`draw_text`) |
| 21 | 이벤트 처리 강화 (ESC 키 → 종료) |
| 22 | 코드 정리 및 최종 주석 정비 |

---

## 완료 기준

- [ ] 모든 애니메이션 클립이 잘린 프레임 없이 재생된다
- [ ] 각 동작이 정확히 5회 반복 후 1초 정지된다
- [ ] 전체 순환 후 자동으로 처음부터 재시작된다
- [ ] 소닉이 화면 중앙에 명확하게 확대되어 표시된다
- [ ] ESC 키로 종료할 수 있다
- [ ] 단일 파일(`sonic_animation_viewer.py`)로 실행 가능하다
