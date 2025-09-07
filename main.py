import tcod
import random
from game_map import SCREEN_WIDTH, SCREEN_HEIGHT, create_map
from player import Player
from item import Item
from monster import Monster

# Function to draw a bar (e.g., for health/mana bars)
def draw_bar(console, x, y, width, current, maximum, bar_color, back_color, label):
    bar_width = int(float(current) / maximum * width)
    # Draw background
    console.draw_rect(x, y, width, 1, ord(" "), bg=back_color)
    # Draw bar
    if bar_width > 0:
        console.draw_rect(x, y, bar_width, 1, ord(" "), bg=bar_color)
    # Print label
    console.print(x + 1, y, f"{label}: {current}/{maximum}", fg=(255,255,255), bg=None)

def main():
    # Create the player at the center of the map
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    # Generate the map (2D list of characters)
    game_map = create_map()
    
    # List of items placed on the map
    items = [
        Item(SCREEN_WIDTH // 2 - 5, SCREEN_HEIGHT // 2, "Beginner Sword", "!", "weapon", {"attack": 1}),
        Item(SCREEN_WIDTH // 2 + 5, SCREEN_HEIGHT // 2, "Leather Armor", "[", "armor", {"defense": 1}),
        Item(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 5, "Health Potion", "!", "potion", {"heal": 5}),
    ]

    # List of monsters on the map (outside the village)
    monsters = [
        Monster(20, 10, "Forest Goblin", "g", 10, 3, 1, 25),
        Monster(25, 12, "Forest Goblin", "g", 10, 3, 1, 25),
        Monster(30, 8, "Forest Goblin", "g", 10, 3, 1, 25),
        Monster(25, SCREEN_HEIGHT-10, "Cave Rat", "r", 8, 2, 0, 15),
        Monster(30, SCREEN_HEIGHT-12, "Cave Rat", "r", 8, 2, 0, 15),
    ]

    inventory_open = False  # Tracks if the inventory panel is open
    message_log = ["Welcome to the village! Explore and develop your skills."]

    # Set up the tcod context (window, tileset, etc.)
    with tcod.context.new(
        columns=SCREEN_WIDTH,
        rows=SCREEN_HEIGHT,
        tileset=tcod.tileset.load_tilesheet(
            "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
        ),
        title="CDDA Runescape",
        vsync=True,
    ) as context:
        # Create the console (where everything is drawn)
        console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
        while True:
            console.clear()  # Clear the screen each frame

            # --- DRAWING SECTION ---

            # Draw the map with different colors for different elements
            for y in range(SCREEN_HEIGHT):
                for x in range(SCREEN_WIDTH):
                    char = game_map[y][x]
                    if char == "#":  # Walls and rocks
                        console.print(x, y, "#", fg=(150, 150, 150))
                    elif char == "T":  # Trees
                        console.print(x, y, "T", fg=(0, 150, 0))
                    elif char == "~":  # Water
                        console.print(x, y, "~", fg=(0, 0, 200))
                    elif char == ",":  # Farmland
                        console.print(x, y, ",", fg=(150, 100, 0))
                    elif char == "+":  # Doors
                        console.print(x, y, "+", fg=(150, 75, 0))
                    elif char == " ":  # Paths
                        console.print(x, y, " ", fg=(200, 200, 200))
                    else:  # Grass and other
                        console.print(x, y, char, fg=(100, 200, 100))

            # Draw all items on the map
            for item in items:
                console.print(item.x, item.y, item.symbol, fg=(255, 255, 0))

            # Draw all monsters on the map
            for monster in monsters:
                console.print(monster.x, monster.y, monster.symbol, fg=(255, 0, 0))

            # Draw stats (health/mana) above the player, centered
            stats_text = f"H:{player.health}/{player.max_health} M:{player.mana}/{player.max_mana}"
            stats_y = max(0, player.y - 1)  # Prevent drawing off the top edge
            stats_x = max(0, player.x - len(stats_text) // 2)
            console.print(stats_x, stats_y, stats_text, fg=(255, 255, 255))

            # Draw the player character
            console.print(player.x, player.y, "@", fg=(255, 255, 255))

            # Draw message log at the bottom
            for i, message in enumerate(message_log[-5:]):  # Show last 5 messages
                console.print(1, SCREEN_HEIGHT - 6 + i, message, fg=(255, 255, 255))

            # Draw inventory panel if open
            if inventory_open:
                inv_x = SCREEN_WIDTH - 20  # Inventory panel starts 20 columns from the right
                console.draw_rect(inv_x, 0, 20, SCREEN_HEIGHT, ord(" "), bg=(0, 0, 50))
                console.print(inv_x, 1, "Inventory:", fg=(255, 255, 255))
                # List each item in inventory, marking equipable and equipped items
                for idx, item in enumerate(player.inventory):
                    equipped = ""
                    if item == player.equipped_weapon or item == player.equipped_armor or item == player.equipped_trinket:
                        equipped = " (E)"  # Mark as equipped
                    equipable = ""
                    if item.item_type in ("weapon", "armor", "trinket"):
                        equipable = " *"  # Mark as equipable
                    console.print(
                        inv_x, 3 + idx,
                        f"{idx+1}. {item.name}{equipable}{equipped}",
                        fg=(255, 255, 0)
                    )
                # Show skills below inventory
                skills_start_y = 5 + len(player.inventory)
                console.print(inv_x, skills_start_y, "Skills:", fg=(255, 255, 255))
                for i, (skill, level) in enumerate(player.skills.items()):
                    console.print(inv_x, skills_start_y + 1 + i, f"{skill}: {level}", fg=(200, 200, 255))
                # Show equipped items at the bottom of the panel
                eq_y = SCREEN_HEIGHT - 6
                console.print(inv_x, eq_y, "Equipped:", fg=(255, 255, 255))
                console.print(inv_x, eq_y + 1, f"Weapon: {player.equipped_weapon.name if player.equipped_weapon else 'None'}", fg=(200, 200, 255))
                console.print(inv_x, eq_y + 2, f"Armor: {player.equipped_armor.name if player.equipped_armor else 'None'}", fg=(200, 255, 200))
                console.print(inv_x, eq_y + 3, f"Trinket: {player.equipped_trinket.name if player.equipped_trinket else 'None'}", fg=(255, 200, 200))

            # Present everything drawn to the window
            context.present(console)

            # --- EVENT HANDLING SECTION ---
            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()  # Exit the game if the window is closed
                if event.type == "KEYDOWN":
                    # Toggle inventory panel with 'i'
                    if event.sym == ord("i"):
                        inventory_open = not inventory_open
                        continue  # Skip movement if toggling inventory

                    # If inventory is open, handle equipping items and using potions
                    if inventory_open:
                        # Number keys 1-9 to interact with items in inventory
                        if event.sym in (ord("1"), ord("2"), ord("3"), ord("4"), ord("5"), 
                                        ord("6"), ord("7"), ord("8"), ord("9")):
                            idx = event.sym - ord("1")
                            if 0 <= idx < len(player.inventory):
                                item = player.inventory[idx]
                                # Equip item in the correct slot based on type
                                if item.item_type == "weapon":
                                    player.equipped_weapon = item
                                    message_log.append(f"Equipped {item.name}.")
                                elif item.item_type == "armor":
                                    player.equipped_armor = item
                                    message_log.append(f"Equipped {item.name}.")
                                elif item.item_type == "trinket":
                                    player.equipped_trinket = item
                                    message_log.append(f"Equipped {item.name}.")
                                elif item.item_type == "potion" and "heal" in item.bonus:
                                    player.health = min(player.max_health, player.health + item.bonus["heal"])
                                    player.inventory.remove(item)
                                    message_log.append(f"Used {item.name}. Healed {item.bonus['heal']} HP.")
                    else:
                        # Handle player movement with arrow keys
                        dx, dy = 0, 0
                        if event.sym == tcod.event.K_UP:
                            dy = -1
                        elif event.sym == tcod.event.K_DOWN:
                            dy = 1
                        elif event.sym == tcod.event.K_LEFT:
                            dx = -1
                        elif event.sym == tcod.event.K_RIGHT:
                            dx = 1
                        elif event.sym == ord(" "):  # Space bar to interact with environment
                            # Check what's around the player
                            for y in range(player.y-1, player.y+2):
                                for x in range(player.x-1, player.x+2):
                                    if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                                        tile = game_map[y][x]
                                        if tile == "T":  # Tree - woodcutting
                                            player.skills["Woodcutting"] += 0.1
                                            message_log.append("You chop at the tree. Woodcutting +0.1")
                                        elif tile == "#" and y > SCREEN_HEIGHT-15:  # Rock in mine area - mining
                                            player.skills["Mining"] += 0.1
                                            message_log.append("You mine the rock. Mining +0.1")
                                        elif tile == "~":  # Water - fishing
                                            player.skills["Fishing"] += 0.1
                                            # Chance to catch a fish
                                            if random.random() < 0.2:
                                                fish = Item(x, y, "Fish", "%", "food", {"heal": 2})
                                                items.append(fish)
                                                message_log.append("You caught a fish!")
                                            else:
                                                message_log.append("You fish in the pond. Fishing +0.1")
                                        elif tile == ",":  # Farmland - farming
                                            player.skills["Farming"] += 0.1
                                            message_log.append("You tend to the crops. Farming +0.1")
                                        elif tile == "+":  # Door - enter building
                                            message_log.append("You enter the building.")

                        # Only process movement if there's actual movement
                        if dx != 0 or dy != 0:
                            # Move the player if possible
                            if player.move(dx, dy, game_map):
                                # Check if player is on an item to pick up
                                for item in items[:]:  # Use a slice copy to safely remove items
                                    if player.x == item.x and player.y == item.y:
                                        player.inventory.append(item)
                                        items.remove(item)
                                        message_log.append(f"Picked up {item.name}!")
                                        break  # Only pick up one item per move
                                
                                # Check for combat with monsters
                                for monster in monsters[:]:  # Use a slice copy to safely remove monsters
                                    if player.x == monster.x and player.y == monster.y:
                                        # Combat happens here
                                        player_attack, player_defense = player.calculate_stats()
                                        damage = max(1, player_attack - monster.defense)
                                        monster.health -= damage
                                        message_log.append(f"You hit the {monster.name} for {damage} damage!")
                                        player.skills["Attack"] += 0.2
                                        
                                        if monster.health <= 0:
                                            message_log.append(f"You killed the {monster.name}!")
                                            player.gain_experience("Attack", monster.experience)
                                            monsters.remove(monster)
                                        else:
                                            # Monster attacks back
                                            damage = max(1, monster.attack - player_defense)
                                            player.health -= damage
                                            message_log.append(f"The {monster.name} hits you for {damage} damage!")
                                            player.skills["Defense"] += 0.1
                                            
                                            if player.health <= 0:
                                                message_log.append("You have died!")
                                                raise SystemExit()
                                        break  # Only fight one monster at a time

if __name__ == "__main__":
    main()