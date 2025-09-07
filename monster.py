class Monster:
    def __init__(self, x, y, name, symbol, health, attack, defense, experience):
        self.x = x
        self.y = y
        self.name = name
        self.symbol = symbol
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.experience = experience

    def move_towards(self, target_x, target_y, game_map):
        """Simple AI to move towards the player"""
        dx = 0 if self.x == target_x else 1 if self.x < target_x else -1
        dy = 0 if self.y == target_y else 1 if self.y < target_y else -1
        
        # Only move if the path is clear
        if game_map[self.y + dy][self.x + dx] != "#":
            self.x += dx
            self.y += dy