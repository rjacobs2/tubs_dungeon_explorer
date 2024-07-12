from pydantic import BaseModel


class DamageIcon(BaseModel):
    x: int
    y: int
    damage: int
    counter: int
    color: tuple[int, int, int]


class Teleporter(BaseModel):
    x: int
    y: int
    target_x: int
    target_y: int


class Switch(BaseModel):
    x: int
    y: int
    spawn_x: list[int]
    spawn_y: list[int]
    change_object: str
    counter: int = 0
    uses: int = 1
    kind: str = "normal"
    before: str = "."
    how_many: int = 0


class Box(BaseModel):
    x: int
    y: int
    status: str = "live"


class Boss(BaseModel):
    x: int
    y: int
    health: int = 1000
    status: str = "live"


class Fireball(BaseModel):
    x: int
    y: int
    direction: str


class Skeleton(BaseModel):
    x: int
    y: int
    health: int = 50
    status: str = "live"


class Rat(BaseModel):
    x: int
    y: int
    health: int = 20
    status: str = "live"


# class Monster(BaseModel):
#     x: int
#     y: int
#     health: int = 20
#     status: str = "live"
#     type: str


class Bullet(BaseModel):
    x: int
    y: int
    direction: str
    tile_range: int = 4
    status: str = "live"


class Armory(BaseModel):
    x: int
    y: int
    item: str
    damage: int
    armor: int
    reach: int
    type: str
    status: str = "live"


class Level(BaseModel):
    level: list[list[str]]
    teleporters: list[Teleporter] = []
    fireballs: list[Fireball] = []
    skeletons: list[Skeleton] = []
    switches: list[Switch] = []
    rats: list[Rat] = []
    boxes: list[Box] = []
    pickups: list[Armory] = []
    bullets: list[Bullet] = []
    bosses: list[Boss] = []
    backups: list[Box] = []


class DungeonGame(BaseModel):
    status: str = "running"
    x: int
    y: int
    coins: int = 0
    health: int = 200
    items: list[str] = []
    inventory: list[str] = ["slot", "slot"]
    current_level: Level
    level_number: int = 0
    # level_cache: Level
    player_damage: int = 5
    player_reach: int = 1
    player_armor: int = 0
    damages: list[DamageIcon] = []
