import turtle as t
import random, time

WIDTH = 500
HEIGHT = 400
TILE_WIDTH = 60
BLUE = (33, 150, 243)
RED = (183, 28, 28)
ASSETS = "assets/"

# Initializing graphic elements

win = t.Screen()
win.title("Bridge-it Bob")
win.colormode(255)
win.bgcolor(BLUE)
win.setup(WIDTH, HEIGHT)
win.tracer(0)

win.register_shape(ASSETS + 'game_title.gif')
win.register_shape(ASSETS + 'game_over.gif')
win.register_shape(ASSETS + 'bob.gif')
win.register_shape(ASSETS + 'bob1.gif')
win.register_shape(ASSETS + 'tile.gif')
win.register_shape(ASSETS + 'cloud.gif')

title = t.Turtle()
title.shape(ASSETS + 'game_title.gif')
title.penup()
title.goto(0, 100)

player = t.Turtle()
player.shape(ASSETS + 'bob.gif')
player.speed(3)
player.setheading(-90)
player.penup()
player.hideturtle()

Tile = t.Turtle()
Tile.shape(ASSETS + 'tile.gif')
Tile.color('black')
Tile.speed(3)
Tile.setheading(180)
Tile.penup()
Tile.hideturtle()

tile1 = Tile.clone()
tile2 = Tile.clone()
tile3 = Tile.clone()
tile4 = Tile.clone()

bridge = t.Turtle()
bridge.shape('square')
bridge.color(RED)
bridge.speed(3)
bridge.penup()
bridge.hideturtle()

Text = t.Turtle()
Text.color('white')
Text.speed(0)
Text.penup()
Text.hideturtle()

score_text = Text.clone()
score_text.goto(-WIDTH / 2 + 20, HEIGHT / 2 - 40)

hiscore_text = Text.clone()
hiscore_text.goto(WIDTH / 2 - 120, HEIGHT / 2 - 40)

status_text = Text.clone()
status_text.goto(0, -50)

cloud = t.Turtle()
cloud.shape(ASSETS + 'cloud.gif')
cloud.speed(3)
cloud.penup()
cloud.goto(300, 120)
cloud.setheading(180)

cloud2 = cloud.clone()
cloud2.goto(cloud.xcor() + 200, cloud.ycor() - 20)

# Game variables

hi_score = 0
score = 0
running = False


def playGame(speed: float = 0.5):
    """Main game mechanics	

	Args:
	    speed (float, optional): Animation speed
	"""
    global running, hi_score, score
    global tile1, tile2, tile3, tile4
    global costume

    # If game is not running, exit function
    if not running:
        return

    rotateBridge()
    moved_distance = 0
    to_move = bridge_length / 2 + player.distance(bridge)
    crossable = tile1.distance(
        tile2) - TILE_WIDTH < bridge_length < tile1.distance(tile2)
    costume = 0

    if crossable:
        # If bridge length is perfect for crossing
        # play crossing animation
        while moved_distance <= to_move:
            scrollBg(speed)
            moved_distance += speed
            if moved_distance % 20 == 0:
                walk()
            win.update()
        player.shape(ASSETS + 'bob.gif')
        # Changing scores
        score += 1
        if score > hi_score:
            hi_score = score
        updateScore()
        # Preparing for next stage
        resetBridge()
        tile1.hideturtle()
        # Replacing tiles
        temp_tile = tile1
        tile1 = tile2
        tile2 = tile3
        tile3 = tile4
        tile4 = temp_tile
        placeTile(tile4)
    else:
        # If bridge is too short or too long
        # move to edge of bridge
        while moved_distance <= to_move + 10:
            scrollBg(speed)
            moved_distance += speed
            if moved_distance % 20 == 0:
                walk()
            win.update()
        player.shape(ASSETS + 'bob.gif')
        # fall to the ground
        while player.ycor() >= -t.window_height() / 2 - 20:
            player.forward(speed * 1.5)
            win.update()
        # Game Over
        time.sleep(0.3)
        running = False
        title.shape(ASSETS + 'game_over.gif')
        title.showturtle()
        title.goto(0, 50)
        displayStatus("Press 's' to restart")
        win.update()


def resetBridge():
    """Init a new bridge after crossing
	"""
    global bridge_height, bridge_length

    bridge.clear()
    bridge_height = 1  # scale (perpendicular)
    bridge_length = 0  # pixel (horizontal)
    bridge.shapesize(bridge_height, 0.3)
    bridge.setheading(0)
    bridge.hideturtle()


def drawBridge():
    """Construct a bridge upright from the ground
	"""
    global bridge_height, bridge_length

    if not running:
        return

    start_pos = tile1.xcor() + 25, -52
    bridge.shapesize(bridge_height, 0.3)
    bridge.goto(start_pos)
    bridge.showturtle()
    bridge_height += 0.2
    bridge_length = abs(bridge.get_shapepoly()[0][0]) * 2
    bridge.sety(bridge.ycor() + bridge_length / 2)


def rotateBridge():
    """Change bridge orientation to horizontal
	"""
    bridge.right(90)
    bridge.goto(bridge.xcor() + bridge_length / 2, -52)


def scrollBg(spd: float):
    """Scroll background with parallax clouds

	Args:
	    spd (float): Animation speed
	"""
    tile1.forward(spd)
    tile2.forward(spd)
    tile3.forward(spd)
    tile4.forward(spd)
    bridge.setx(bridge.xcor() - spd)
    # Parallax clouds
    cloud.forward(spd * 0.3)
    cloud2.forward(spd * 0.3)
    if cloud.xcor() < -WIDTH / 2 - 50:
        cloud.setx(WIDTH + 100)
    if cloud2.xcor() < -WIDTH / 2 - 50:
        cloud2.setx(WIDTH + 100)


def walk():
    """Player walking animation
	"""
    global costume
    if costume == 1:
        costume = 0
        player.shape(ASSETS + 'bob1.gif')
    else:
        costume = 1
        player.shape(ASSETS + 'bob.gif')


def placeTile(tile: t.Turtle):
    """Generate new tile at the right

    Args:
        tile (t.Turtle): Tile image
    """
    x = random.randint(300, 350)
    tile.setx(x)
    if tile.distance(tile3) < TILE_WIDTH + 50:
        tile.setx(tile.xcor() + TILE_WIDTH)
    tile.showturtle()


def updateScore():
    """Updating score text
    """
    score_text.clear()
    score_text.penup()
    score_text.write(f'Score: {score}', font='Arial 20 bold')
    hiscore_text.clear()
    hiscore_text.penup()
    hiscore_text.write(f'Best: {hi_score}', font='Arial 20 bold')


def displayStatus(msg: str = ""):
    """Updating game status

    Args:
        msg (str, optional): Message to display
    """
    status_text.clear()
    status_text.write(msg, align='Center', font=('Arial', 20, 'bold'))


def startGame():
    """Go to start state from main menu
    """
    global running, score
    global tile1, tile2, tile3, tile4

    if not running:
        running = True

        # Initialize game screen
        score = 0
        updateScore()
        displayStatus()
        resetBridge()

        title.hideturtle()
        player.goto(-200, -35)
        player.showturtle()
        tile1.goto(-200, -130)
        tile2.goto(0, -130)
        tile3.goto(200, -130)
        tile4.goto(400, -130)
        tile1.showturtle()
        tile2.showturtle()
        tile3.showturtle()
        tile4.showturtle()
        while running:
            win.update()


title.showturtle()
displayStatus("Press 's' to start")
win.update()

win.onkeypress(startGame, 's')
win.onkeypress(drawBridge, 'space')
win.onkeyrelease(playGame, 'space')
win.listen()
win.mainloop()
