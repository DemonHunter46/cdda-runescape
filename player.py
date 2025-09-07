class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None
        self.equipped_trinket = None
        self.max_health = 20
        self.health = 20
        self.max_mana = 10
        self.mana = 10
        self.skills = {
            "Attack": 1,
            "Defense": 1,
            "Magic": 1,
            "Mining": 1,
            "Woodcutting": 1,
            "Fishing": 1,
        }

    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy
        if game_map[new_y][new_x] != "#":
            self.x = new_x
            self.y = new_y