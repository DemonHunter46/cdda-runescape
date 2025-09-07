class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None
        self.equipped_trinket = None

    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy
        if game_map[new_y][new_x] != "#":
            self.x = new_x
            self.y = new_y