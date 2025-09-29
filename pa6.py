import turtle                       # Turtle 그래픽 라이브러리 불러오기 (화면, 거북이, 글자 등)
import random                       # 무작위 처리를 위해 random 모듈 불러오기 (덱 섞기 등)

# 전역 상태 및 설정 변수
game_over = False                   # 게임이 끝났는지 여부를 저장하는 플래그 (초기값: False)
betting_mode = True                 # 배팅 가능한 상태인지 표시 (True이면 아직 배팅 전)
player_bet = None                   # 플레이어가 선택한 거북이(말)의 이름을 저장할 변수
horse_names = []                    # 사용자 정의 거북이 이름들을 저장할 리스트

# 화면 설정 및 결승선, 패널티 라인
screen = turtle.Screen()            # Turtle 스크린(창) 객체 생성
screen.title("트럼프 거북이 경주")   # 창의 제목 설정
screen.bgcolor("lightgreen")        # 배경색을 연두색으로 설정
screen.setup(width=1000, height=600)# 창의 크기(픽셀) 설정

pixels_per_meter = 5                # 내부 단위: 1m를 5픽셀로 취급 (거리 변환용)
start_x = -300                      # 말들이 출발할 x 좌표 (픽셀)
left_shift = -50                    # 좌측 여백(추가 x 이동)
finish_line = start_x + left_shift + 80 * pixels_per_meter  # 결승선 x 좌표 (출발+여백+80m)

# 결승선 그리기
line = turtle.Turtle()              # 결승선을 그릴 터틀 생성
line.speed(6)                       # 그리기 속도 설정
line.penup()                        # 펜 들어서 이동(선 그리지 않음)
line.goto(finish_line, 250)         # 결승선의 위쪽 시작 좌표로 이동
line.pendown()                      # 펜 내리고 선 그리기 시작
line.right(90)                      # 오른쪽으로 90도 회전하여 수직선 방향으로 설정
line.forward(410)                   # 아래쪽으로 410픽셀 만큼 선 그리기 (결승선 완성)
line.hideturtle()                   # 그린 후 커서(거북이 모양)를 숨김

# 패널티 선 (10m 간격)
penalty_line_distances = [i for i in range(10, 71, 10)]  # 10,20,...,70m 위치에 표시선
penalty_lines = turtle.Turtle()     # 패널티 선 그리기용 터틀 생성
penalty_lines.speed(6)              # 그리기 속도 설정
penalty_lines.hideturtle()          # 터틀 숨김 (선만 보이게)
penalty_lines.penup()               # 펜 올려서 이동
penalty_lines.color("red")          # 패널티 선 색을 빨간색으로
penalty_lines.pensize(3)            # 선 두께 설정

for pd in penalty_line_distances:   # 각 패널티 위치마다 선을 그림
    x = start_x + left_shift + pd * pixels_per_meter  # 해당 거리의 x 좌표 계산
    penalty_lines.goto(x, 250)      # 선의 위쪽 시작점으로 이동
    penalty_lines.pendown()         # 펜 내리고 선 그리기
    penalty_lines.goto(x, -160)     # 아래쪽 끝까지 수직선 그림
    penalty_lines.penup()           # 펜 올림

# 패널티 발동 거리 (15m 간격)
penalty_trigger_distances = [i for i in range(15, 76, 15)]  # 15,30,45,60,75m에서 패널티 조건 검사

# 말(거북이) 설정
symbols = ['♥', '♠', '♣', '♦']      # 각 말(거북이)을 식별할 카드 심볼
colors = ['red', 'black', 'green', 'blue']  # 각 말의 색상
horses = []                         # 거북이 객체들을 담을 리스트
start_y = 200                       # 첫 번째 말의 y좌표(세로 위치 기준)

# 거북이 4마리 생성
for i in range(4):                  # 0부터 3까지 총 4마리 생성
    horse = turtle.Turtle()         # 새 거북이 객체 생성
    horse.shape("turtle")           # 모양을 '거북이'로 설정
    horse.color(colors[i])          # 해당 인덱스의 색상 적용
    horse.penup()                   # 초기 이동시 선이 그려지지 않도록 펜 올림
    horse.speed(10)                 # 이동 애니메이션 속도 설정
    horse.goto(start_x + left_shift, start_y - (i * 100))  # 세로로 100픽셀 간격으로 배치
    horses.append(horse)            # 리스트에 추가

# 이름 라벨 저장용
name_labels = []                    # 왼쪽에 거북이 이름을 표시할 라벨 터틀들을 저장

# 화면 우측 텍스트 출력 좌표
text_x = finish_line + 60           # 오른쪽 정보 패널(카드/메시지) 시작 x 좌표

# 카드 및 메시지 출력용 터틀
card_display = turtle.Turtle()      # 뽑은 카드 표시용 터틀
card_display.hideturtle()           # 커서 숨김
card_display.penup()                # 이동 시 선이 그려지지 않게 펜 올림
card_display.goto(text_x, 150)      # 카드 표시 위치로 이동

announce = turtle.Turtle()          # 안내 / 결과 메시지 출력용 터틀
announce.hideturtle()               # 커서 숨김
announce.penup()                    # 펜 올림
announce.goto(text_x, 100)          # 안내 메시지 위치로 이동

# 배팅 상태 출력 터틀
bet_display = turtle.Turtle()       # 현재 배팅 상태(선택한 말) 표시용 터틀
bet_display.hideturtle()            # 커서 숨김
bet_display.penup()                 # 펜 올림
bet_display.goto(0, 250)            # 화면 상단 중앙에 배치

# 카드 뽑기 버튼
button = turtle.Turtle()             # 카드 뽑기 버튼을 시각적으로 만들 터틀
button.shape("square")               # 사각형 모양으로
button.color("black", "white")       # 테두리 검정, 내부 흰색
button.shapesize(stretch_wid=2, stretch_len=10)  # 버튼 크기 조정
button.penup()                       # 버튼은 이동만 (선 안 그림)
button.goto(0, -200)                 # 버튼 위치 설정

label = turtle.Turtle()              # 버튼 위에 텍스트를 쓰는 터틀
label.hideturtle()                   # 커서 숨김
label.penup()                        # 펜 올림
label.color("black")                 # 글자 색 검정
label.goto(0, -210)                  # 버튼 아래에 위치
label.write("카드 뽑기", align="center", font=("Arial", 16, "bold"))  # 버튼 텍스트 표시

# 다시 시작 버튼
restart_button = turtle.Turtle()     # 다시 시작 버튼용 터틀
restart_button.shape("square")       # 사각형
restart_button.color("black", "white")  # 테두리/배경 색
restart_button.shapesize(stretch_wid=1.5, stretch_len=8)  # 크기 조정
restart_button.penup()               # 펜 올림
restart_button.goto(0, -260)         # 버튼 위치

restart_label = turtle.Turtle()      # 다시 시작 텍스트용 터틀
restart_label.hideturtle()           # 커서 숨김
restart_label.penup()                # 펜 올림
restart_label.color("black")         # 글자 색
restart_label.goto(0, -270)          # 텍스트 위치
restart_label.write("다시 시작", align="center", font=("Arial", 14, "bold"))  # 텍스트 표시

# 게임 상태 초기화용 변수
deck = []                            # 카드 덱(심볼들이 들어있는 리스트)
triggered_penalties = []             # 이미 패널티가 발동한 거리들을 저장 (중복 방지)

# 보조 함수들
def update_bet_display():
    """현재 배팅 상태 표시"""
    bet_display.clear()              # 이전 내용 지우기
    if player_bet:                   # 플레이어가 선택했으면
        bet_display.write(f"당신의 선택: {player_bet}", align="center", font=("Arial", 23, "bold"))
    else:                            # 선택 전이면 안내 문구 표시
        bet_display.write("거북이를 클릭하여 선택하세요", align="center", font=("Arial", 23, "bold"))

def clear_name_labels():
    """기존 이름 라벨 삭제"""
    for label in name_labels:        # 라벨 터틀들 모두 지우고 숨김
        label.clear()
        label.hideturtle()
    name_labels.clear()              # 라벨 리스트 비우기

def input_horse_names():
    """사용자로부터 거북이 이름 입력받기"""
    global horse_names
    horse_names.clear()              # 기존 이름 초기화
    for i, sym in enumerate(symbols):# 각 심볼에 대해 이름 입력받기
        name = screen.textinput("거북이 이름 짓기", f"거북이 {sym}의 이름을 입력하세요 (기본은 심볼):")
        if name is None or name.strip() == "":  # 취소하거나 빈 문자열이면 기본 심볼 사용
            name = sym
        horse_names.append(name)     # 리스트에 추가

# 메인 게임 함수들
def draw_card(x, y):
    """카드 뽑기 버튼 눌렀을 때 동작"""
    global deck, triggered_penalties, game_over, betting_mode

    # 버튼 클릭 범위 벗어나면 무시
    if not (-100 < x < 100 and -220 < y < -180):  # 버튼 영역 좌표 검사
        return

    # 베팅 안 했으면 안내
    if betting_mode:                 # 아직 베팅이 완료되지 않았으면
        announce.clear()
        announce.write("먼저 선택을 완료하세요!", align="left", font=("Arial", 18, "bold"))
        return

    if game_over:                     # 게임이 이미 끝났으면 아무 동작 안 함
        return

    if not deck:                      # 덱이 비었다면 게임 종료 안내
        announce.clear()
        announce.write("카드가 모두 소진되었습니다!", align="left", font=("Arial", 18, "bold"))
        game_over = True
        return

    # 카드 1장 뽑기
    symbol = deck.pop()               # 덱의 마지막 요소를 꺼냄 (뽑기)
    card_display.clear()              # 이전 카드 표시 지우기
    card_display.write(f"뽑은 카드: {symbol}", align="left", font=("Arial", 22, "bold"))

    if symbol in symbols:             # 뽑은 카드가 유효한 심볼이면 해당 말 이동
        idx = symbols.index(symbol)   # 심볼과 말의 인덱스 매핑

        # 현재 위치에 따라 이동 거리 결정
        pos_m = (horses[idx].xcor() - start_x - left_shift) / pixels_per_meter
                                        # 현재 말의 위치를 'm' 단위로 환산
        distance = 15 if abs(pos_m - 0) < 0.001 else 10
                                        # 시작 지점(0m)에 있으면 15m, 아니면 10m 이동(설계상 가속 규칙)
        horses[idx].forward(distance * pixels_per_meter)
                                        # 계산된 거리만큼 픽셀 단위로 이동

        # 결승선 도달 시 우승 처리
        if horses[idx].xcor() >= finish_line:  # 말의 x좌표가 결승선 이상이면 우승
            announce.clear()
            winner_name = horse_names[idx]     # 우승한 말의 이름
            announce.write(f"{winner_name} 거북이가 우승했습니다!", align="left", font=("Arial", 20, "bold"))
            announce.goto(text_x, 70)
            if player_bet == winner_name:     # 플레이어가 맞췄는지 확인
                announce.write("축하합니다! 우승에 성공했습니다!", align="left", font=("Arial", 18, "bold"))
            else:
                announce.write("아쉽지만 우승에 실패했습니다.", align="left", font=("Arial", 18, "bold"))
            game_over = True                   # 게임 종료 플래그 세움
            return

    # 패널티 체크
    for penalty_m in penalty_trigger_distances:  # 각 패널티 트리거 거리마다 검사
        if penalty_m in triggered_penalties:     # 이미 발동한 패널티면 건너뜀
            continue
        penalty_x = start_x + left_shift + (penalty_m * pixels_per_meter)
                                        # 패널티 트리거의 x 좌표 계산
        if all(horse.xcor() >= penalty_x for horse in horses):
                                        # 모든 말이 해당 x좌표(라인)을 넘겼으면 패널티 발동
            triggered_penalties.append(penalty_m) # 중복 발동을 막기 위해 기록
            if deck:                            # 덱에 카드가 남아있다면 페널티 카드 뽑음
                penalty_symbol = deck.pop()
                card_display.clear()
                card_display.write(f"페널티 카드: {penalty_symbol}", align="left", font=("Arial", 22, "bold"))
                if penalty_symbol in symbols:   # 페널티 카드가 심볼이면 해당 말이 뒤로 감
                    penalty_idx = symbols.index(penalty_symbol)
                    pos_m = (horses[penalty_idx].xcor() - start_x - left_shift) / pixels_per_meter
                                            # 해당 말의 위치(미터)
                    back_dist = 15 if abs(pos_m - 15) < 0.001 else 10
                                            # 특정 조건(15m 근처)이면 15m, 아니면 10m 만큼 뒤로 이동
                    new_x = horses[penalty_idx].xcor() - back_dist * pixels_per_meter
                                            # 뒤로 이동한 최종 x좌표 계산
                    new_x = max(new_x, start_x + left_shift)
                                            # 출발선보다 뒤로 가지 않도록 방지
                    horses[penalty_idx].goto(new_x, horses[penalty_idx].ycor())
                                            # 해당 말의 좌표를 직접 이동시켜 뒤로 보냄
                    announce.clear()
                    announce.write(f"{horse_names[penalty_idx]} 거북이가 패널티로 뒤로 이동했습니다!", align="left", font=("Arial", 16, "bold"))
            break                 # 한 번의 패널티 트리거만 처리하고 루프 종료

def place_bet(x, y):
    """거북이를 클릭하여 베팅"""
    global player_bet, betting_mode
    if not betting_mode:             # 베팅 모드가 아니면(이미 베팅했으면) 무시
        return
    for i, horse in enumerate(horses):  # 각 말의 위치와 클릭 위치를 비교
        hx, hy = horse.position()     # 말의 현재 좌표 읽기
        if hx - 20 < x < hx + 20 and hy - 20 < y < hy + 20:
            player_bet = horse_names[i]  # 클릭된 말의 이름을 플레이어 베팅으로 저장
            update_bet_display()         # 배팅 표시 업데이트
            announce.clear()
            announce.write(f"{player_bet} 거북이에 선택하셨습니다.\n'카드 뽑기'를 눌러 게임을 시작하세요!", align="left", font=("Arial", 16, "bold"))
            betting_mode = False        # 한 번 베팅하면 더 이상 베팅 불가
            return

def restart_game(x, y):
    """게임 초기화"""
    global deck, triggered_penalties, game_over, betting_mode, player_bet

    # 다시 시작 버튼 눌렀는지 확인
    if not (-90 < x < 90 and -280 < y < -240) and (x != 0 or y != 0):
        # 버튼 영역이 아니고, 초기 자동 호출(0,0)이 아니라면 무시
        return

    input_horse_names()            # 사용자에게 거북이 이름 입력받기 (텍스트 입력창)
    deck = symbols * 10            # 각 심볼을 10장씩 가진 덱 생성 (총 40장)
    random.shuffle(deck)           # 덱 섞기

    for i, horse in enumerate(horses):  # 말들을 출발 위치로 리셋
        horse.goto(start_x + left_shift, start_y - (i * 100))

    # 말 이름 라벨 표시
    clear_name_labels()
    left_text_x = -480
    for i in range(4):
        name_label = turtle.Turtle()    # 이름 표시용 터틀 생성
        name_label.hideturtle()
        name_label.penup()
        name_label.goto(left_text_x, start_y - (i * 100) - 45)  # 왼쪽에 이름 표시 위치
        name_label.color(colors[i])     # 해당 말 색으로 이름 표시
        name_label.write(f"{symbols[i]}: {horse_names[i]}", align="left", font=("Arial", 21, "bold"))
        name_labels.append(name_label)  # 라벨 리스트에 추가

    card_display.clear()           # 카드 표시 초기화
    announce.clear()               # 안내 메시지 초기화
    triggered_penalties.clear()    # 패널티 기록 초기화
    game_over = False              # 게임 상태 초기화
    betting_mode = True            # 다시 베팅 가능 상태로 설정
    player_bet = None              # 플레이어 베팅 초기화
    update_bet_display()           # 배팅 표시 갱신

def handle_click(x, y):
    """전체 클릭 처리 함수"""
    place_bet(x, y)     # 먼저 거북이 클릭으로 베팅 시도
    draw_card(x, y)     # 다음으로 카드 뽑기 버튼 영역이면 뽑기 처리
    restart_game(x, y)  # 마지막으로 다시 시작 버튼 영역이면 초기화 처리

# 게임 시작
update_bet_display()      # 초기 배팅 안내 표시
screen.onclick(handle_click)  # 화면의 클릭을 handle_click으로 바인딩
restart_game(0, 0)       # 초기화 자동 호출 (처음 실행 시 한 번 실행되도록)
screen.mainloop()        # 메인 루프 실행 (창이 닫힐 때까지 지속)
