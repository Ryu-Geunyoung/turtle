import turtle
import random

game_over = False
betting_mode = True
player_bet = None
horse_names = []

screen = turtle.Screen()
screen.title("트럼프 거북이 경주")
screen.bgcolor("lightgreen")
screen.setup(width=1000, height=600)

pixels_per_meter = 5
start_x = -300
left_shift = -50
finish_line = start_x + left_shift + 80 * pixels_per_meter

line = turtle.Turtle()
line.speed(6)
line.penup()
line.goto(finish_line, 250)
line.pendown()
line.right(90)
line.forward(410)
line.hideturtle()

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

penalty_trigger_distances = [i for i in range(15, 76, 15)]

symbols = ['♥', '♠', '♣', '♦']
colors = ['red', 'black', 'green', 'blue']
horses = []
start_y = 200

for i in range(4):
    horse = turtle.Turtle()
    horse.shape("turtle")
    horse.color(colors[i])
    horse.penup()
    horse.speed(10)
    horse.goto(start_x + left_shift, start_y - (i * 100))
    horses.append(horse)

name_labels = []

text_x = finish_line + 60

card_display = turtle.Turtle()
card_display.hideturtle()
card_display.penup()
card_display.goto(text_x, 150)

announce = turtle.Turtle()
announce.hideturtle()
announce.penup()
announce.goto(text_x, 100)

bet_display = turtle.Turtle()
bet_display.hideturtle()
bet_display.penup()
bet_display.goto(0, 250)

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

deck = []
triggered_penalties = []

def update_bet_display():
    bet_display.clear()
    if player_bet:
        bet_display.write(f"당신의 선택: {player_bet}", align="center", font=("Arial", 23, "bold"))
    else:
        bet_display.write("거북이를 클릭하여 선택하세요", align="center", font=("Arial", 23, "bold"))

def clear_name_labels():
    for label in name_labels:
        label.clear()
        label.hideturtle()
    name_labels.clear()

def input_horse_names():
    global horse_names
    horse_names.clear()
    for i, sym in enumerate(symbols):
        name = screen.textinput("거북이 이름 짓기", f"거북이 {sym}의 이름을 입력하세요 (기본은 심볼):")
        if name is None or name.strip() == "":
            name = sym
        horse_names.append(name)

def draw_card(x, y):
    global deck, triggered_penalties, game_over, betting_mode

    if not (-100 < x < 100 and -220 < y < -180):
        return

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

    symbol = deck.pop()
    card_display.clear()
    card_display.write(f"뽑은 카드: {symbol}\n", align="left", font=("Arial", 18, "bold"))

    if symbol in symbols:
        idx = symbols.index(symbol)
        pos_m = (horses[idx].xcor() - start_x - left_shift) / pixels_per_meter
        distance = 15 if abs(pos_m - 0) < 0.001 else 10
        horses[idx].forward(distance * pixels_per_meter)

        if horses[idx].xcor() >= finish_line:
            announce.clear()
            winner_name = horse_names[idx]
            if player_bet == winner_name:
                announce.write(f"{winner_name} 거북이가 우승했습니다!\n축하합니다! 우승에 성공했습니다!", align="left", font=("Arial", 20, "bold"))
            else:
                announce.write(f"{winner_name} 거북이가 우승했습니다!\n아쉽지만 우승에 실패했습니다.", align="left", font=("Arial", 20, "bold"))
            game_over = True
            return

    for penalty_m in penalty_trigger_distances:
        if penalty_m in triggered_penalties:
            continue
        penalty_x = start_x + left_shift + (penalty_m * pixels_per_meter)
        if all(horse.xcor() >= penalty_x for horse in horses):
            triggered_penalties.append(penalty_m)
            if deck:
                penalty_symbol = deck.pop()
                card_display.clear()
                card_display.write(f"페널티 카드: {penalty_symbol}", align="left", font=("Arial", 15, "bold"))
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
    global player_bet, betting_mode
    if not betting_mode:
        return
    for i, horse in enumerate(horses):
        hx, hy = horse.position()
        if hx - 20 < x < hx + 20 and hy - 20 < y < hy + 20:
            player_bet = horse_names[i]
            update_bet_display()
            announce.clear()
            announce.write(f"{player_bet} 거북이에 선택하셨습니다.\n\n'카드 뽑기'를 눌러 게임을 시작하세요!", align="left", font=("Arial", 16, "bold"))
            betting_mode = False
            return

def restart_game(x, y):
    global deck, triggered_penalties, game_over, betting_mode, player_bet

    if not (-90 < x < 90 and -280 < y < -240) and (x != 0 or y != 0):
        return

    input_horse_names()
    deck = symbols * 10
    random.shuffle(deck)

    for i, horse in enumerate(horses):
        horse.goto(start_x + left_shift, start_y - (i * 100))

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
    place_bet(x, y)
    draw_card(x, y)
    restart_game(x, y)

update_bet_display()
screen.onclick(handle_click)
restart_game(0, 0)
screen.mainloop()
