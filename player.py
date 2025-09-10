class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 10
        self.max_hp = 10
        self.strength = 1
        self.perception = 1
        self.endurance = 1
        self.charisma = 1
        self.intelligence = 1
        self.agility = 1
        self.luck = 1
        self.defense = 1
        self.attack = 1
        self.level = 1
        self.xp = 1
        self.xp_to_next = 100  # XP needed for next level
        self.inventory = ["Potion", "Sword"]
        self.equipment = {
            "Head": None,
            "Body": None,
            "Weapon": None,
            "Shield": None,
        }

    def add_xp(self, amount):
        self.xp += amount
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * 2.5)  # Increase XP needed for next level
            print(f"You leveled up! Now level {self.level}")

def display_inventory(player):
    lines = ["Inventory:"]
    if player.inventory:
        for item in player.inventory:
            lines.append(f"- {item}")
    else:
        lines.append(" (empty)")
    return "\n".join(lines)

def display_stats(player):
    return (
        f"Stats:\n"
        f"HP: {player.hp}/{player.max_hp}\n"
        f"Level: {player.level}\n"
        
        f"Strength: {player.strength}\n"
        f"Perception: {player.perception}\n"
        f"Endurance: {player.endurance}\n"
        f"Charisma: {player.charisma}\n"
        f"Intelligence: {player.intelligence}\n"
        f"Agility: {player.agility}\n"
        f"Luck: {player.luck}\n"
        f"Attack: {player.attack}\n"
        f"Defense: {player.defense}\n"
        f"Equipment:\n" +
        "\n".join([f"{slot}: {item if item else 'None'}" for slot, item in player.equipment.items()])
    )