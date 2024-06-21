import turtle
import time
import random

# Set up the screen
wn = turtle.Screen()
wn.title("Breakout Clone")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)  # Turns off screen updates

# Paddle
paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.penup()
paddle.goto(0, -250)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.15
ball.dy = -0.15

# Bricks
bricks = []
colors = ["red", "orange", "yellow", "green", "blue"]
for i in range(5):
    for j in range(8):
        brick = turtle.Turtle()
        brick.speed(0)
        brick.shape("square")
        brick.color(colors[i])
        brick.penup()
        brick.goto(-340 + j * 100, 200 - i * 24)
        bricks.append(brick)

# Pen for scoring
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0", align="center", font=("Courier", 24, "normal"))

# Game over text
game_over_pen = turtle.Turtle()
game_over_pen.speed(0)
game_over_pen.color("white")
game_over_pen.penup()
game_over_pen.hideturtle()
game_over_pen.goto(0, 0)

# Initial score
score = 0

# Paddle movement
def paddle_right():
    x = paddle.xcor()
    if x < 350:
        paddle.setx(x + 20)

def paddle_left():
    x = paddle.xcor()
    if x > -350:
        paddle.setx(x - 20)

# Keyboard bindings
wn.listen()
wn.onkeypress(paddle_right, "Right")
wn.onkeypress(paddle_left, "Left")

# Function to reset the game
def reset_game():
    global score
    ball.goto(0, 0)
    ball.dx = 0.15 * random.choice([-1, 1])
    ball.dy = -0.15
    paddle.goto(0, -250)
    game_over_pen.clear()
    game_over_pen.hideturtle()
    score = 0
    pen.clear()
    pen.write("Score: {}".format(score), align="center", font=("Courier", 24, "normal"))
    # Reset bricks
    for brick in bricks:
        brick.goto(1000, 1000)  # Move brick off screen
    bricks.clear()
    colors = ["red", "orange", "yellow", "green", "blue"]
    for i in range(5):
        for j in range(8):
            brick = turtle.Turtle()
            brick.speed(0)
            brick.shape("square")
            brick.color(colors[i])
            brick.penup()
            brick.goto(-340 + j * 100, 200 - i * 24)
            bricks.append(brick)

# Main game loop
while True:
    wn.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border collision
    if ball.xcor() > 390:
        ball.setx(390)
        ball.dx *= -1
    if ball.xcor() < -390:
        ball.setx(-390)
        ball.dx *= -1
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    # Paddle collision
    if (ball.dy < 0) and (ball.ycor() < -240) and (paddle.xcor() - 50 < ball.xcor() < paddle.xcor() + 50):
        ball.dy *= -1

    # Brick collision
    for brick in bricks:
        if brick.distance(ball) < 20:
            ball.dy *= -1
            bricks.remove(brick)
            brick.goto(1000, 1000)  # Move brick off screen
            score += 10
            pen.clear()
            pen.write("Score: {}".format(score), align="center", font=("Courier", 24, "normal"))

    # Game over if ball falls down
    if ball.ycor() < -290:
        game_over_pen.write("GAME OVER\nPress 'Y' to play again or 'N' to exit", align="center", font=("Courier", 24, "normal"))
        wn.update()
        time.sleep(1)  # Delay to avoid immediate key detection

        # Wait for user input to play again or exit
        while True:
            choice = wn.textinput("Play Again?", "Press 'Y' to play again or 'N' to exit").lower()
            if choice == 'y':
                reset_game()
                break
            elif choice == 'n':
                wn.bye()
                break

# Close the window on click
wn.mainloop()
