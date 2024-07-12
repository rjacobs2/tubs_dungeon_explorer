from model import Teleporter, Switch, Box, Fireball, Skeleton, Rat, Armory, Level, Boss


def parse_level(level):
    """Changes the data structure level"""
    return [list(row) for row in level]


LEVEL_ONE = Level(
    level=parse_level(
        [
            "#####################",
            "#s.&.&.#.?#?D.......#",
            "#x.....D..####D#..?s#",
            "#s.&.&.#....#?!######",
            "#########D###.......#",
            "#...........#.......#",
            "#.....!.....#.......#",
            "#?h.....!...#####D###",
            "#...........DDD.#...#",
            "############.###?...#",
            "#..!.......D...?#...#",
            "#.....!...!.##..##D##",
            "#...........#......&#",
            "#####################",
        ]
    ),
    teleporters=[Teleporter(x=15, y=8, target_x=5, target_y=2)],
    switches=[
        Switch(x=11, y=1, spawn_x=[14], spawn_y=[3], change_object="h"),
        Switch(x=8, y=11, spawn_x=[7, 8], spawn_y=[12, 12], change_object="h", uses=2),
        Switch(
            x=4,
            y=12,
            spawn_x=[1, 6, 11],
            spawn_y=[11, 10, 12],
            change_object="?",
            uses=3,
        ),
        Switch(
            x=1, y=8, spawn_x=[5, 5, 5], spawn_y=[6, 7, 8], change_object="#", uses=3
        ),
    ],
    fireballs=[
        Fireball(x=16, y=4, direction="right"),
        Fireball(x=17, y=6, direction="left"),
        Fireball(x=18, y=12, direction="right"),
        Fireball(x=1, y=8, direction="up"),
        Fireball(x=3, y=5, direction="down"),
        Fireball(x=6, y=7, direction="right"),
    ],
    skeletons=[
        Skeleton(x=17, y=9),
        Skeleton(x=4, y=12),
        Skeleton(x=6, y=12),
        Skeleton(x=5, y=8),
    ],
)

LEVEL_TWO = Level(
    level=parse_level(
        [
            "#####################",
            "#!hh#.#.c...#...cc.x#",
            "#..?#$#..!..D..!..###",
            "##D######c..#......?#",
            "#.......#####....!..#",
            "#...#...#?...#....###",
            "#...#...##...##D##.h#",
            "#...#...#!..........#",
            "#.......#.!...#####.#",
            "#######D####..#...###",
            "#{..........#D#####h#",
            "#...........#....?#.#",
            "#{.....#cccc#.....#$#",
            "#####################",
        ]
    ),
    fireballs=[
        Fireball(x=5, y=12, direction="right"),
        Fireball(x=12, y=7, direction="up"),
        Fireball(x=15, y=7, direction="left"),
        Fireball(x=15, y=4, direction="right"),
        Fireball(x=14, y=3, direction="down"),
        Fireball(x=16, y=4, direction="up"),
        Fireball(x=17, y=2, direction="down"),
    ],
    switches=[
        Switch(x=7, y=4, spawn_x=[1], spawn_y=[5], change_object="?"),
        Switch(x=1, y=10, spawn_x=[4], spawn_y=[12], change_object="#", kind="heavy"),
        Switch(
            x=1,
            y=12,
            spawn_x=[12],
            spawn_y=[11],
            change_object=".",
            kind="heavy",
            before="#",
        ),
        Switch(
            x=5,
            y=1,
            spawn_x=[18, 17, 14],
            spawn_y=[12, 8, 9],
            change_object=".",
            uses=3,
        ),
        Switch(
            x=19,
            y=8,
            spawn_x=[6],
            spawn_y=[1],
            change_object=".",
            kind="heavy",
            before="#",
        ),
    ],
    rats=[
        Rat(x=3, y=5),
        Rat(x=3, y=7),
        Rat(x=5, y=8),
        Rat(x=5, y=5),
        Rat(x=17, y=9),
        Rat(x=17, y=9),
        Rat(x=17, y=9),
        Rat(x=9, y=1),
        Rat(x=10, y=2),
        Rat(x=9, y=2),
        Rat(x=10, y=3),
    ],
    skeletons=[
        Skeleton(x=17, y=9),
        Skeleton(x=17, y=9),
        Skeleton(x=17, y=9),
        Skeleton(x=10, y=6),
    ],
    boxes=[Box(x=5, y=11), Box(x=7, y=11), Box(x=13, y=8)],
    backups=[Box(x=5, y=11), Box(x=7, y=11), Box(x=13, y=8)],
    pickups=[
        Armory(
            x=14, y=12, item="short_sword", damage=20, armor=0, reach=2, type="weapon"
        ),
        Armory(x=19, y=11, item="armor", damage=0, armor=15, reach=0, type="armor"),
    ],
)

LEVEL_THREE = Level(
    level=parse_level(
        [
            "#####################",
            "#x.&s&cc#?!###..#!h.#",
            "#.....c.#.......D.?.#",
            "####D####..#...######",
            "#?......#......#....#",
            "##......########.!.h#",
            "#.#####Dc##?##.D....#",
            "#...!#..#......######",
            "#.#.....?#D##..#hc.$#",
            "#D#######h..##.######",
            "#?............#.....#",
            "#h............#.....#",
            "#.............#....h#",
            "#####################",
        ]
    ),
    fireballs=[
        Fireball(x=8, y=2, direction="right"),
        Fireball(x=12, y=3, direction="up"),
        Fireball(x=10, y=3, direction="down"),
        Fireball(x=14, y=7, direction="up"),
        Fireball(x=11, y=7, direction="right"),
        Fireball(x=3, y=11, direction="up"),
        Fireball(x=4, y=10, direction="up"),
        Fireball(x=5, y=11, direction="down"),
        Fireball(x=6, y=12, direction="down"),
        Fireball(x=6, y=7, direction="right"),
        Fireball(x=1, y=7, direction="down"),
        Fireball(x=1, y=4, direction="right"),
        Fireball(x=3, y=5, direction="right"),
    ],
    boxes=[Box(x=13, y=3), Box(x=8, y=11)],
    backups=[Box(x=13, y=3), Box(x=8, y=11)],
    switches=[
        Switch(x=9, y=4, spawn_x=[15], spawn_y=[4], change_object=".", kind="heavy", before="#"),
        Switch(x=1, y=12, spawn_x=[16], spawn_y=[9], change_object=".", kind="heavy", before="#"),
        Switch(x=3, y=12, spawn_x=[14, 14, 14], spawn_y=[10, 11, 12], change_object=".", uses=3),
        Switch(x=1, y=8, spawn_x=[5], spawn_y=[7], change_object="."),
    ],
    rats=[
        Rat(x=17, y=5),
        Rat(x=18, y=5),
        Rat(x=17, y=6),
        Rat(x=17, y=10),
        Rat(x=17, y=11),
        Rat(x=17, y=12),
        Rat(x=3, y=5),
        Rat(x=4, y=5),
    ],
    skeletons=[
        Skeleton(x=12, y=7),
        Skeleton(x=18, y=10),
        Skeleton(x=18, y=11),
        Skeleton(x=18, y=12),
        Skeleton(x=4, y=8),
        Skeleton(x=3, y=5),
    ],
    pickups=[
        Armory(
            x=4, y=2, item="long_sword", damage=50, armor=0, reach=3, type="weapon"
        ),
        # Armory(x=3, y=2, item="gold_armor", damage=0, armor=30, reach=0, type="armor"),
        Armory(x=18, y=8, item="gold_armor", damage=0, armor=30, reach=0, type="armor"),
    ],
    teleporters=[
        Teleporter(x=2, y=10, target_x=8, target_y=11)
    ],
)

LEVEL_FOUR = Level(
    level=parse_level(
        [
            "#####################",
            "#...................#",
            "#.tttttttt.tttttttt.#",
            "#.t...............t.#",
            "#.t.ttttttttttttt.t.#",
            "#.t.t...........t.t.#",
            "#.t.t.tttt.tttt.t.t.#",
            "#.t.............t.t.#",
            "#.t.t.tttt.tttt.t.t.#",
            "#.t.t...........t.t.#",
            "#.t.tttttt.tttttt.t.#",
            "#.t.t...t...t...t.t.#",
            "#.....t...t...t.....#",
            "#####################",
        ]
    ),
    bosses=[
        Boss(x=8, y=8),
    ],
    # pickups=[
    #     Armory(
    #         x=18, y=1, item="long_sword", damage=50, armor=0, reach=3, type="weapon"
    #     ),
    #     Armory(x=17, y=1, item="gold_armor", damage=0, armor=30, reach=0, type="armor"),
    # ],
)

LEVELS = [LEVEL_ONE, LEVEL_TWO, LEVEL_THREE, LEVEL_FOUR]
