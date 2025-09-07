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
        self.experience = 0
        self.level = 1

    def move(self, dx, dy, game_map):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < len(game_map[0]) and 0 <= new_y < len(game_map):
            if game_map[new_y][new_x] != "#":
                self.x = new_x
                self.y = new_y
                return True
        return False

    def calculate_stats(self):
        """Calculate player stats based on equipment and skills"""
        attack = self.skills["Attack"]
        defense = self.skills["Defense"]
        
        # Apply equipment bonuses
        if self.equipped_weapon and "attack" in self.equipped_weapon.bonus:
            attack += self.equipped_weapon.bonus["attack"]
        if self.equipped_armor and "defense" in self.equipped_armor.bonus:
            defense += self.equipped_armor.bonus["defense"]
            
        return attack, defense

    def gain_experience(self, skill, amount):
        """Gain experience in a skill"""
        self.experience += amount
        # Check for level up (simplified)
        if self.experience >= self.level * 100:
            self.level_up()
            
    def level_up(self):
        """Handle level up"""
        self.level += 1
        self.max_health += 5
        self.health = self.max_health
        self.max_mana += 2
        self.mana = self.max_mana
        self.experience = 0
        print(f"Level up! You are now level {self.level}")