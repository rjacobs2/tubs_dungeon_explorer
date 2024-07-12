"""
the Dungeon Explorer game logic
"""
import random
from model import DungeonGame, DamageIcon, Skeleton, Bullet, Box
from levels import LEVELS
from pygame import mixer

# TODO do the music

x_max = 22
y_max = 14
walkable = ".$x!c?|{h"


def respawn_box(game, key):
    if key == "respawn":
        new_boxes = []
        for backup in game.current_level.backups:
            new_boxes.append(Box(
                x=backup.x,
                y=backup.y
            ))
        game.current_level.boxes = new_boxes


def get_next_position(x, y, direction):
    """gets the position of where something will move to"""
    if direction == "right":
        x += 1
    elif direction == "left":
        x -= 1
    elif direction == "up":
        y -= 1
    elif direction == "down":
        y += 1
    return x, y


def change_direction(direction):
    """changes the direction of moving tiles"""
    opp_dir = {"right": "left", "left": "right", "up": "down", "down": "up"}
    return opp_dir[direction]


def toward_player(game, monster):
    b = monster
    if b.x > game.x:
        b.x, b.y, direction = monster_movement(game, b.x, b.y, direction="left")
    elif b.y > game.y:
        b.x, b.y, direction = monster_movement(game, b.x, b.y, direction="up")
    elif b.x < game.x:
        b.x, b.y, direction = monster_movement(game, b.x, b.y, direction="right")
    else:
        b.x, b.y, direction = monster_movement(game, b.x, b.y, direction="down")
    return direction


def player_attack(game, x, y):
    x = x // 64
    y = y // 64
    boundary_x = [x + i for i in range(-game.player_reach, game.player_reach + 1)]
    boundary_y = [y + i for i in range(-game.player_reach, game.player_reach + 1)]
    monsters = [
        game.current_level.skeletons,
        game.current_level.rats,
        game.current_level.bosses,
    ]
    for elements in monsters:
        for m in elements:
            if m.x == x and m.y == y and game.x in boundary_x and game.y in boundary_y:
                game.damages.append(
                    DamageIcon(
                        x=m.x,
                        y=m.y,
                        damage=game.player_damage,
                        counter=64,
                        color=(255, 0, 255),
                    )
                )
                m.health -= game.player_damage
                if m.health <= 0:
                    m.status = "dead"


def move_player(game, direction: str) -> None:
    """Things that happen when the player walks on stuff"""
    check_collision_fast(game)
    check_collision_super(game)
    box = move_box(game, direction)
    if box is False:
        return
    x, y = get_next_position(game.x, game.y, direction)
    # changes the level of the game
    if game.current_level.level[y][x] == "x":
        game.level_number += 1
        num_keys = game.items.count("key")
        for i in range(num_keys):
            game.items.remove("key")
        if game.level_number < len(LEVELS):
            # move to next level
            if game.level_number == 3:
                mixer.music.load("music/boss_intro.wav")
                mixer.music.play(loops=1)
                mixer.music.load("music/boss_main.wav")
                mixer.music.play(loops=-1)
            game.current_level = LEVELS[game.level_number]
        else:
            # no more levels left
            game.status = "finished"
    # checks to see if tile is walkable
    if game.current_level.level[y][x] in walkable:
        game.x = x
        game.y = y
    # pickup coins
    if game.current_level.level[y][x] == "c":
        game.coins += 1
        game.current_level.level[y][x] = "."
    # pickup chest
    if game.current_level.level[y][x] == "$":
        game.coins += 10
        game.current_level.level[y][x] = "."
    # pickup key
    if game.current_level.level[y][x] == "?":
        game.items.append("key")
        game.current_level.level[y][x] = "."
    # pickup health potion
    if game.current_level.level[y][x] == "h":
        game.items.append("ruby_new")
        game.current_level.level[y][x] = "."
    # step on trap
    if game.current_level.level[y][x] == "!":
        game.damages.append(
            DamageIcon(x=game.x, y=game.y, damage=50, counter=100, color=(0, 0, 255))
        )
        game.health -= 50
        game.current_level.level[y][x] = "."
    # open doors
    if game.current_level.level[y][x] == "D" and "key" in game.items:
        game.items.remove("key")
        game.current_level.level[y][x] = "|"


def check_teleporters(game):
    """Teleports player if on teleporter"""
    for t in game.current_level.teleporters:
        if game.x == t.x and game.y == t.y:
            game.x = t.target_x
            game.y = t.target_y


def check_switch(game):
    """What happens when stepping on a switch"""
    for switch in game.current_level.switches:
        if switch.kind == "normal":
            if game.x == switch.x and game.y == switch.y:
                if switch.how_many < switch.uses:
                    x = switch.spawn_x[switch.how_many]
                    y = switch.spawn_y[switch.how_many]
                    game.current_level.level[y][x] = switch.change_object
                switch.how_many += 1
        else:
            for b in game.current_level.boxes:
                x = switch.spawn_x[0]
                y = switch.spawn_y[0]
                if b.x == switch.x and b.y == switch.y:
                    switch.counter = 10
                    game.current_level.level[y][x] = switch.change_object
                else:
                    if switch.counter > 0:
                        switch.counter -= 1
                        game.current_level.level[y][x] = switch.change_object
                    else:
                        game.current_level.level[y][x] = switch.before


def pickup_inventory_item(game, item):
    """changes the status according to picked up item"""
    item.status = "dead"
    if item.type == "weapon":
        game.inventory[0] = item.item
        game.player_damage = item.damage
        game.player_armor += item.armor
        game.player_reach = item.reach
    else:
        game.inventory[1] = item.item
        game.player_damage += item.damage
        game.player_armor = item.armor
        game.player_reach += item.reach


def check_collision_fast(game):
    """checks if player runs into something"""
    for p in game.current_level.pickups:
        if p.x == game.x and p.y == game.y:
            pickup_inventory_item(game, p)
    monsters = [[game.current_level.skeletons, 75], [game.current_level.bosses, 100]]
    for elements, damage in monsters:
        for m in elements:
            if m.x == game.x and m.y == game.y:
                game.damages.append(
                    DamageIcon(
                        x=game.x,
                        y=game.y,
                        damage=damage - game.player_armor,
                        counter=100,
                        color=(0, 0, 255),
                    )
                )
                game.health -= damage - game.player_armor


def check_collision_super(game):
    monsters = [
        [game.current_level.rats, 25],
        [game.current_level.fireballs, 50],
        [game.current_level.bullets, 80],
    ]
    for elements, damage in monsters:
        for m in elements:
            if m.x == game.x and m.y == game.y:
                game.damages.append(
                    DamageIcon(
                        x=game.x,
                        y=game.y,
                        damage=damage - game.player_armor,
                        counter=100,
                        color=(0, 0, 255),
                    )
                )
                game.health -= damage - game.player_armor


def move_box(game, direction):
    """box logic"""
    x, y = get_next_position(game.x, game.y, direction)
    behind_x, behind_y = get_next_position(x, y, direction)
    for b in game.current_level.boxes:
        if b.x == x and b.y == y:
            if game.current_level.level[behind_y][behind_x] in walkable:
                b.x = behind_x
                b.y = behind_y
                return True
            else:
                return False
    return True


def monster_movement(game, x, y, direction):
    """logic for monster movement"""
    monster_walkable = walkable + "t"
    is_move_possible = True
    new_x, new_y = get_next_position(x, y, direction)
    for b in game.current_level.boxes:
        if new_x == b.x and new_y == b.y:
            is_move_possible = False
    if game.current_level.level[new_y][new_x] not in monster_walkable:
        is_move_possible = False
    if is_move_possible:
        return new_x, new_y, direction
    else:
        direction = change_direction(direction)
        return x, y, direction


def move_fireball(game):
    """Handles the fireball movement"""
    for f in game.current_level.fireballs:
        new_x, new_y = get_next_position(f.x, f.y, f.direction)
        for b in game.current_level.boxes:
            if (new_x == b.x and new_y == b.y) or (f.x == b.x and f.y == b.y):
                b.status = "dead"
        if game.current_level.level[new_y][new_x] in walkable:
            f.x, f.y = new_x, new_y
        else:
            f.direction = change_direction(f.direction)
            f.x, f.y = get_next_position(f.x, f.y, f.direction)


def move_skeleton(game):
    """Handles the skeleton movement"""
    for s in game.current_level.skeletons:
        direction = random.choice(["up", "down", "left", "right"])
        s.x, s.y, direction = monster_movement(game, s.x, s.y, direction)


def move_rat(game):
    """Handles the rat movement"""
    for r in game.current_level.rats:
        direction = random.choice(["up", "down", "left", "right"])
        r.x, r.y, direction = monster_movement(game, r.x, r.y, direction)


def move_bullet(game):
    """Handles the bullet movement"""
    monster_walkable = walkable + "t"
    for b in game.current_level.bullets:
        if b.tile_range > 0:
            new_x, new_y = get_next_position(b.x, b.y, b.direction)
            if game.current_level.level[new_y][new_x] in monster_walkable:
                b.x, b.y = new_x, new_y
            else:
                b.direction = change_direction(b.direction)
            b.tile_range -= 1
        else:
            b.status = "dead"


def boss_skills(game):
    """Choosed the bosses skills to use"""
    filler = ["" for i in range(5)]
    skills = ["spawn_skeleton", "heal", "bullet", "bullet", "bullet"] + filler
    for b in game.current_level.bosses:
        skill = random.choice(skills)
        if skill == "spawn_skeleton":
            skeleton = Skeleton(x=b.x, y=b.y)
            game.current_level.skeletons.append(skeleton)
        elif skill == "heal" and b.health <= 500:
            b.health += 25
            game.damages.append(
                DamageIcon(x=b.x, y=b.y, damage=25, counter=100, color=(0, 255, 0))
            )
        elif skill == "bullet" and b.health <= 750:
            bullet = Bullet(
                x=b.x, y=b.y, direction=random.choice(["up", "down", "left", "right"])
            )
            game.current_level.bullets.append(bullet)


def move_boss(game):
    """Handles the boss movement"""
    moves = ["toward player", "toward player", "normal"]
    for b in game.current_level.bosses:
        move = random.choice(moves)
        if move == "normal":
            direction = random.choice(["up", "down", "left", "right"])
            b.x, b.y, direction = monster_movement(game, b.x, b.y, direction)
        elif move == "toward player":
            toward_player(game, b)


def use_items(game, key):
    """uses items in players inventory when key is pressed"""
    if key == "use" and "ruby_new" in game.items:
        game.items.remove("ruby_new")
        health_boost = 50
        future_health = game.health + health_boost
        if future_health > 200:
            future_health = future_health % 200
            game.health += health_boost - future_health
            game.damages.append(
                DamageIcon(
                    x=game.x,
                    y=game.y,
                    damage=health_boost - future_health,
                    counter=64,
                    color=(0, 255, 0),
                )
            )
        else:
            game.health += health_boost
            game.damages.append(
                DamageIcon(
                    x=game.x,
                    y=game.y,
                    damage=health_boost,
                    counter=64,
                    color=(0, 255, 0),
                )
            )


def clean_up_element(elements):
    new_items = []
    for p in elements:
        if p.status == "live":
            new_items.append(p)
    return new_items


def update_fast(game):
    check_collision_fast(game)
    boss_skills(game)
    # health check
    if game.health <= 0:
        game.status = "you lose"
    # gets rid of dead rats
    game.current_level.rats = clean_up_element(game.current_level.rats)
    # gets rid of dead skeletons
    game.current_level.skeletons = clean_up_element(game.current_level.skeletons)
    # gets rid of picked up items
    game.current_level.pickups = clean_up_element(game.current_level.pickups)
    # destroys boxes
    game.current_level.boxes = clean_up_element(game.current_level.boxes)
    # gets rid of bullets
    game.current_level.bullets = clean_up_element(game.current_level.bullets)
    # gets rid of bosses and spawns ending stairs
    new_bosses = []
    for b in game.current_level.bosses:
        if b.status == "live":
            new_bosses.append(b)
        elif b.status == "dead":
            game.status = "you win"
            # game.level_number += 1
    game.current_level.bosses = new_bosses

    # moves monsters
    # move_fireball(game)
    move_skeleton(game)
    for b in game.current_level.bosses:
        if b.health > 750:
            move_boss(game)


def update_super(game):
    check_collision_super(game)
    move_fireball(game)
    move_bullet(game)
    move_rat(game)
    for b in game.current_level.bosses:
        if b.health <= 750:
            move_boss(game)


def start_game():
    mixer.music.load("music/action.mp3")
    mixer.music.play(loops=-1)
    return DungeonGame(x=19, y=1, current_level=LEVELS[0])
