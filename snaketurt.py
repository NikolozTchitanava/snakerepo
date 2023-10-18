import turtle
import random
import time

screen = turtle.Screen()
screen.title("Random Color Snake Game")
screen.bgcolor("black")
screen.setup(width=600, height=600)

def random_color():
    color = [random.random() for _ in range(3)]
    return tuple(color)

head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color(random_color())
head.penup()
head.goto(0, 0)
head.direction = "stop"

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

score = 0

score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")

def eat_food():
    if head.distance(food) < 20:
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)
        global score
        score += 1
        update_score_display()
        add_segment() 

def add_segment():
    segment = turtle.Turtle()
    segment.speed(0)
    segment.shape("square")
    segment.color(random_color())
    segment.penup()
    segments.append(segment)

def check_collision():
    if (
        head.xcor() > 290
        or head.xcor() < -290
        or head.ycor() > 290
        or head.ycor() < -290
    ):
        return True

    for segment in segments:
        if head.distance(segment) < 20:
            return True

    return False

def update_screen():
    global score, high_score
    if check_collision():
        if score > high_score:
            high_score = score
            update_high_score_display()
            save_high_score(high_score)
        score_display.clear()
        score_display.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))
        head.goto(0, 0)
        head.direction = "stop"
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()
        time.sleep(2)
        start_new_game()

    for i in range(len(segments) - 1, 0, -1):
        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()
        segments[i].goto(x, y)

    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    eat_food()
    screen.update()
    move()
    time.sleep(0.1)

def update_score_display():
    score_display.clear()
    score_display.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

def start_new_game():
    global score
    score = 0
    update_score_display()
    head.color(random_color())
    food.color("red")

def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

high_score = load_high_score()

high_score_display = turtle.Turtle()
high_score_display.speed(0)
high_score_display.color("white")
high_score_display.penup()
high_score_display.hideturtle()
high_score_display.goto(-280, 260)

def update_high_score_display():
    high_score_display.clear()
    high_score_display.write(f"High Score: {high_score}", align="left", font=("Courier", 12, "normal"))

update_high_score_display()

while True:
    screen.update()
    update_screen()

turtle.done()
