from game import move_player, DungeonGame, parse_level, Box


def test_move_box():
    x = 0
    y = 1
    level = ["....", "....", "....", "...."]
    boxes = [Box(x=1, y=1)]
    move_player("right")
    for b in boxes:
        assert b.x == 2
        assert b.y == 1
