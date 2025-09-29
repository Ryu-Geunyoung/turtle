import turtle
import random

# =========================
# 전역 상태 및 설정 변수
# =========================

game_over = False           # 게임 종료 여부
betting_mode = True         # 배팅 가능 상태 여부
player_bet = None           # 플레이어가 선택한 거북이 이름
horse_names = []            # 사용자 정의 거북이 이름 저장

# =========================
# 화면 설정 및 결승선, 패널티 라인
# =========================

screen = turtle.Screen()
screen.title("트럼프 거북이 경주")   # 윈도우 제목
screen.bgcolor("lightgreen")        # 배경색
screen.setup(width=1000, height=600)

pixels_per_meter = 5               # 1m = 5픽셀
start_x = -300                     # 말 출발 위치 x좌표
left_shift = -50                   # 좌측 여백
finish_line = start_x + left_shift + 80 * pixels_per_meter  # 결승선 위치

# 결승선 그리기
line = turtle.Turtle()
line.speed(6)
line.penup()
line.goto(finish_line, 250)
line.pendown()
line.right(90)
line.forward(410)
line.hideturtle()

# 패널티 선 (10m 간격)
penalty_line_distances = [i for i in range(10, 71, 10)]
penalty_lines = turtle.Turtle()
penalty_lines.speed(6)
penalty_lines.hideturtle()
penalty_lines.penup()
penalty_lines.color("red")
penalty_lines.pensize(3)

for pd in penalty_line_distances:
    x = start_x + left_shift + pd * pixels_per_meter
    penalty_lines.goto(x, 250)
    penalty_lines.pendown()
    penalty_lines.goto(x, -160)
    penalty_lines.penup()

# 패널티 발동 거리 (15m 간격)
penalty_trigger_distances = [i for i in range(15, 76, 15)]

# =========================
# 말(거북이) 설정
# =========================

symbols = ['♥', '♠', '♣', '♦']    # 각 말의 심볼 (카드 심볼과 연결됨)
colors = ['red', 'black', 'green', 'blue']
horses = []
start_y = 200

# 거북이 4마리 생성
for i in range(4):
    horse = turtle.Turtle()
    horse.shape("turtle")
    horse.color(colors[i])
    horse.penup()
    horse.speed(10)
    horse.goto(start_x + left_shift, start_y - (i * 100))
    horses.append(horse)

# 이름 라벨 저장용
name_labels = []

# 화면 우측 텍스트 출력 좌표
text_x = finish_line + 60

# 카드 및 메시지 출력용 터틀
card_display = turtle.Turtle()
card_display.hideturtle()
card_display.penup()
card_display.goto(text_x, 150)

announce = turtle.Turtle()
announce.hideturtle()
announce.penup()
announce.goto(text_x, 100)

# 배팅 상태 출력 터틀
bet_display = turtle.Turtle()
bet_display.hideturtle()
bet_display.penup()
bet_display.goto(0, 250)

# =========================
# 카드 뽑기 버튼
# =========================

button = turtle.Turtle()
button.shape("square")
button.color("black", "white")
button.shapesize(stretch_wid=2, stretch_len=10)
button.penup()
button.goto(0, -200)

label = turtle.Turtle()
label.hideturtle()
label.penup()
label.color("black")
label.goto(0, -210)
label.write("카드 뽑기", align="center", font=("Arial", 16, "bold"))

# =========================
# 다시 시작 버튼
# =========================

restart_button = turtle.Turtle()
restart_button.shape("square")
restart_button.color("black", "white")
restart_button.shapesize(stretch_wid=1.5, stretch_len=8)
restart_button.penup()
restart_button.goto(0, -260)

restart_label = turtle.Turtle()
restart_label.hideturtle()
restart_label.penup()
restart_label.color("black")
restart_label.goto(0, -270)
restart_label.write("다시 시작", align="center", font=("Arial", 14, "bold"))

# =========================
# 게임 상태 초기화용 변수
# =========================

deck = []                   # 카드 덱 (심볼을 여러 장 포함)
triggered_penalties = []    # 이미 발생한 패널티 거리 저장


# =========================
# 보조 함수들
# =========================

def update_bet_display():
    """현재 배팅 상태 표시"""
    bet_display.clear()
    if player_bet:
        bet_display.write(f"당신의 선택: {player_bet}", align="center", font=("Arial", 23, "bold"))
    else:
        bet_display.write("거북이를 클릭하여 선택하세요", align="center", font=("Arial", 23, "bold"))

def clear_name_labels():
    """기존 이름 라벨 삭제"""
    for label in name_labels:
        label.clear()
        label.hideturtle()
    name_labels.clear()

def input_horse_names():
    """사용자로부터 거북이 이름 입력받기"""
    global horse_names
    horse_names.clear()
    for i, sym in enumerate(symbols):
        name = screen.textinput("거북이 이름 짓기", f"거북이 {sym}의 이름을 입력하세요 (기본은 심볼):")
        if name is None or name.strip() == "":
            name = sym
        horse_names.append(name)


# =========================
# 메인 게임 함수들
# =========================

def draw_card(x, y):
    """카드 뽑기 버튼 눌렀을 때 동작"""
    global deck, triggered_penalties, game_over, betting_mode

    # 버튼 클릭 범위 벗어나면 무시
    if not (-100 < x < 100 and -220 < y < -180):
        return

    # 베팅 안 했으면 안내
    if betting_mode:
        announce.clear()
        announce.write("먼저 선택을 완료하세요!", align="left", font=("Arial", 18, "bold"))
        return

    if game_over:
        return

    if not deck:
        announce.clear()
        announce.write("카드가 모두 소진되었습니다!", align="left", font=("Arial", 18, "bold"))
        game_over = True
        return

    # 카드 1장 뽑기
    symbol = deck.pop()
    card_display.clear()
    card_display.write(f"뽑은 카드: {symbol}", align="left", font=("Arial", 22, "bold"))

    if symbol in symbols:
        idx = symbols.index(symbol)

        # 현재 위치에 따라 이동 거리 결정
        pos_m = (horses[idx].xcor() - start_x - left_shift) / pixels_per_meter
        distance = 15 if abs(pos_m - 0) < 0.001 else 10
        horses[idx].forward(distance * pixels_per_meter)

        # 결승선 도달 시 우승 처리
        if horses[idx].xcor() >= finish_line:
            announce.clear()
            winner_name = horse_names[idx]
            announce.write(f"{winner_name} 거북이가 우승했습니다!", align="left", font=("Arial", 20, "bold"))
            announce.goto(text_x, 70)
            if player_bet == winner_name:
                announce.write("축하합니다! 우승에 성공했습니다!", align="left", font=("Arial", 18, "bold"))
            else:
                announce.write("아쉽지만 우승에 실패했습니다.", align="left", font=("Arial", 18, "bold"))
            game_over = True
            return

    # 패널티 체크
    for penalty_m in penalty_trigger_distances:
        if penalty_m in triggered_penalties:
            continue
        penalty_x = start_x + left_shift + (penalty_m * pixels_per_meter)
        if all(horse.xcor() >= penalty_x for horse in horses):
            triggered_penalties.append(penalty_m)
            if deck:
                penalty_symbol = deck.pop()
                card_display.clear()
                card_display.write(f"페널티 카드: {penalty_symbol}", align="left", font=("Arial", 22, "bold"))
                if penalty_symbol in symbols:
                    penalty_idx = symbols.index(penalty_symbol)
                    pos_m = (horses[penalty_idx].xcor() - start_x - left_shift) / pixels_per_meter
                    back_dist = 15 if abs(pos_m - 15) < 0.001 else 10
                    new_x = horses[penalty_idx].xcor() - back_dist * pixels_per_meter
                    new_x = max(new_x, start_x + left_shift)
                    horses[penalty_idx].goto(new_x, horses[penalty_idx].ycor())
                    announce.clear()
                    announce.write(f"{horse_names[penalty_idx]} 거북이가 패널티로 뒤로 이동했습니다!", align="left", font=("Arial", 16, "bold"))
            break


def place_bet(x, y):
    """거북이를 클릭하여 베팅"""
    global player_bet, betting_mode
    if not betting_mode:
        return
    for i, horse in enumerate(horses):
        hx, hy = horse.position()
        if hx - 20 < x < hx + 20 and hy - 20 < y < hy + 20:
            player_bet = horse_names[i]
            update_bet_display()
            announce.clear()
            announce.write(f"{player_bet} 거북이에 선택하셨습니다.\n'카드 뽑기'를 눌러 게임을 시작하세요!", align="left", font=("Arial", 16, "bold"))
            betting_mode = False
            return


def restart_game(x, y):
    """게임 초기화"""
    global deck, triggered_penalties, game_over, betting_mode, player_bet

    # 다시 시작 버튼 눌렀는지 확인
    if not (-90 < x < 90 and -280 < y < -240) and (x != 0 or y != 0):
        return

    input_horse_names()  # 이름 입력
    deck = symbols * 10
    random.shuffle(deck)

    for i, horse in enumerate(horses):
        horse.goto(start_x + left_shift, start_y - (i * 100))

    # 말 이름 라벨 표시
    clear_name_labels()
    left_text_x = -480
    for i in range(4):
        name_label = turtle.Turtle()
        name_label.hideturtle()
        name_label.penup()
        name_label.goto(left_text_x, start_y - (i * 100) - 45)
        name_label.color(colors[i])
        name_label.write(f"{symbols[i]}: {horse_names[i]}", align="left", font=("Arial", 21, "bold"))
        name_labels.append(name_label)

    card_display.clear()
    announce.clear()
    triggered_penalties.clear()
    game_over = False
    betting_mode = True
    player_bet = None
    update_bet_display()


def handle_click(x, y):
    """전체 클릭 처리 함수"""
    place_bet(x, y)
    draw_card(x, y)
    restart_game(x, y)

# =========================
# 게임 시작
# =========================

update_bet_display()
screen.onclick(handle_click)
restart_game(0, 0)   # 초기화 자동 시작
screen.mainloop()
