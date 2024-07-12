"""
graphics engine for 2D games
"""
import os
import numpy as np
import cv2
from pygame import mixer
from game import (
    start_game,
    move_player,
    update_fast,
    update_super,
    check_teleporters,
    use_items,
    check_switch,
    player_attack,
    respawn_box,
    x_max,
    y_max,
)


# title of the game window
GAME_TITLE = "Dungeon Explorer"

# map keyboard keys to move commands
MOVES = {
    "a": "left",
    "d": "right",
    "w": "up",
    "s": "down",
    "e": "use",
    "r": "respawn"
    }

# map the symbols to the tile name
SYMBOLS = {
    ".": "floor",
    "#": "wall",
    "&": "fountain",
    "x": "stairs_down",
    "c": "coin",
    "!": "trap",
    "s": "statue",
    "$": "chest",
    "?": "key",
    "D": "closed_door",
    "|": "open_door",
    "{": "pressure_plate",
    "h": "ruby_new",
    "t": "transparent"
}

#
# constants measured in pixels
#
SCREEN_SIZE_X, SCREEN_SIZE_Y = (x_max * 64 + 150), (y_max * 64)
TILE_SIZE = 64

mixer.init()

def mouse_clicked(event, x, y, flags, params):
    """Returns the position of the mouse when clicked"""
    if event == cv2.EVENT_LBUTTONDOWN:
        player_attack(game, x=x, y=y)


def read_image(filename: str) -> np.ndarray:
    """
    Reads an image from the given filename and doubles its size.
    If the image file does not exist, an error is created.
    """
    img = cv2.imread(filename)  # sometimes returns None
    if img is None:
        raise IOError(f"Image not found: '{filename}'")
    # double image size
    img = np.kron(img, np.ones((2, 2, 1), dtype=img.dtype))
    return img


def read_images():
    return {
        filename[:-4]: read_image(os.path.join("tiles", filename))
        for filename in os.listdir("tiles")
        if filename.endswith(".png")
    }


def draw_tile(frame, x, y, image, xbase=0, ybase=0):
    # calculate screen position in pixels
    xpos = xbase + x * TILE_SIZE
    ypos = ybase + y * TILE_SIZE
    # copy the image to the screen
    frame[ypos:ypos + TILE_SIZE, xpos:xpos + TILE_SIZE] = image


def write_text(frame, text, position, color):
    """Writes text to be put on the screen"""
    cv2.putText(
        frame,
        str(text),
        org=position,
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=1.5,
        color=color,
        thickness=3,
    )


def cutscene(name, color, text, extension):
    """Plays cutscenes for the start and end of the game"""
    play_music(name, extension)
    img = cv2.imread(f"images/{name}.png")
    img[-100:] = 0
    write_text(frame=img, text=text, position=(500, 720), color=color)
    cv2.imshow("Cutscene", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    mixer.music.stop()


def play_music(music_name, extension):
    """Plays music for the game"""
    mixer.music.load(f"music/{music_name}{extension}")
    mixer.music.play(loops=-1)


def draw(game, images):
    # initialize screen
    frame = np.zeros((SCREEN_SIZE_Y, SCREEN_SIZE_X, 3), np.uint8)
    # draw tiles for the level
    for y, row in enumerate(game.current_level.level):
        for x, tile in enumerate(row):
            draw_tile(frame, x=x, y=y, image=images[SYMBOLS[tile]])
    # draw switches
    for switch in game.current_level.switches:
        draw_tile(frame, x=switch.x, y=switch.y, image=images["switch"])
    # draw player
    draw_tile(frame, x=game.x, y=game.y, image=images["player"])
    # draws the sprites that move around
    sprites = [
        ["box", game.current_level.boxes],
        ["teleporter", game.current_level.teleporters],
        ["fireball", game.current_level.fireballs],
        ["skeleton", game.current_level.skeletons],
        ["rat", game.current_level.rats],
        ["fireball", game.current_level.bullets],
        ["deep_elf_knight_new", game.current_level.bosses],
    ]
    for image_name, elements in sprites:
        for t in elements:
            draw_tile(frame, x=t.x, y=t.y, image=images[image_name])
    # coin counter
    draw_tile(frame, x=21, y=0, image=images["coin"], xbase=10, ybase=30)
    write_text(frame, text=game.coins, position=(1429, 76), color=(0, 215, 255))
    # draw damage icons
    for dmg in game.damages:
        if dmg.counter > 0:
            dmg.counter -= 1
            cv2.putText(
                frame,
                str(dmg.damage),
                org=(dmg.x * 64, dmg.y * 64 + dmg.counter),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=dmg.color,
                thickness=2,
            )
        else:
            game.damages.remove(dmg)
    # draw attack damage
    draw_tile(frame, x=21, y=1, image=images["fighting"], xbase=10, ybase=30)
    write_text(
        frame, text=game.player_damage, position=(1429, 140), color=(255, 0, 255)
    )
    # draw armor
    draw_tile(frame, x=21, y=2, image=images["armor_icon"], xbase=10, ybase=30)
    write_text(frame, text=game.player_armor, position=(1429, 204), color=(255, 0, 0))
    # draw health bar
    draw_tile(frame, x=21, y=3, image=images["heart"], xbase=10, ybase=50)
    frame[313:513, 1359:1410] = (50, 50, 50)
    frame[313:313 + game.health, 1359:1410] = (0, 0, 255)
    # draw items
    for i, item in enumerate(game.items):
        y = i + 4
        if i > 1:
            y = i // 2 + 5
            x = i % 2
            draw_tile(frame, x=x + 21, y=y, image=images[item], xbase=15, ybase=134)
        else:
            draw_tile(frame, x=22, y=y, image=images[item], xbase=15, ybase=134)
    # draw pickups
    for p in game.current_level.pickups:
        draw_tile(frame, x=p.x, y=p.y, image=images[p.item])
    for i, item in enumerate(game.inventory):
        y = i + 2
        draw_tile(frame, x=22, y=y, image=images[item], xbase=15, ybase=114)
    # draw boss bar
    for b in game.current_level.bosses:
        frame[3:67, 140:1140] = (50, 50, 50)
        frame[3:67, 140:140 + b.health] = (0, 255, 255)
        cv2.putText(
            frame,
            str("Elf King"),
            org=(500, 50),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=2,
            color=(0, 0, 0),
            thickness=3,
        )
    # display complete image
    cv2.imshow(GAME_TITLE, frame)


def handle_keyboard(game):
    """keys are mapped to move commands"""
    key = chr(cv2.waitKey(1) & 0xFF)
    if key == "q":
        game.status = "exited"
    if key in MOVES:
        move_player(game, MOVES[key])
        use_items(game, MOVES[key])
        respawn_box(game, MOVES[key])


# game starts
cutscene("title", color=(255, 255, 255), text="Enter the Dungeon", extension=".mp3")
images = read_images()
game = start_game()

cv2.namedWindow(GAME_TITLE)
cv2.setMouseCallback(GAME_TITLE, mouse_clicked)

counter = 0
while game.status == "running":
    counter += 1
    draw(game, images)
    check_teleporters(game)
    check_switch(game)
    handle_keyboard(game)
    if counter % 100 == 0:
        update_fast(game)
    if counter % 50 == 0:
        update_super(game)
cv2.destroyAllWindows()

if game.status == "you lose":
    cutscene("game_over", color=(0, 0, 255), text="You Died", extension=".mp3")
elif game.status == "you win":
    cutscene("victory", color=(0, 215, 255), text="Victory!!", extension=".ogg")
cv2.destroyAllWindows()
