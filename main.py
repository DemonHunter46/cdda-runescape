import tcod
from game_map import SCREEN_WIDTH, SCREEN_HEIGHT, create_map
from player import Player
from item import Item

# (Unused) Function to draw a bar (e.g., for health/mana bars)
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
        Item(10, 10, "Sword", "!", "weapon", {"attack": 2}),           # Equipable weapon
        Item(15, 5, "Apple", "%", "misc"),                             # Not equipable
        Item(12, 8, "Leather Armor", "[", "armor", {"defense": 1}),    # Equipable armor
        Item(18, 12, "Lucky Charm", "*", "trinket", {"luck": 5}),      # Equipable trinket
    ]

    inventory_open = False  # Tracks if the inventory panel is open

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

            # Draw the map (walls as "#")
            for y in range(SCREEN_HEIGHT):
                for x in range(SCREEN_WIDTH):
                    if game_map[y][x] == "#":
                        console.print(x, y, "#", fg=(255, 255, 255))

            # Draw all items on the map
            for item in items:
                console.print(item.x, item.y, item.symbol, fg=(255, 255, 0))

            # Draw stats (health/mana) above the player, centered
            stats_text = f"H:{player.health} M:{player.mana}"
            stats_y = max(0, player.y - 1)  # Prevent drawing off the top edge
            stats_x = max(0, player.x - len(stats_text) // 2)
            console.print(stats_x, stats_y, stats_text, fg=(255, 255, 255))

            # Draw the player character
            console.print(player.x, player.y, "@", fg=(255, 255, 255))

            # Draw inventory panel if open
            if inventory_open:
                inv_x = SCREEN_WIDTH - 20  # Inventory panel starts 20 columns from the right
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

                    # If inventory is open, handle equipping items
                    if inventory_open:
                        # Number keys 1-5 to equip items in inventory
                        if event.sym in (ord("1"), ord("2"), ord("3"), ord("4"), ord("5")):
                            idx = event.sym - ord("1")
                            if 0 <= idx < len(player.inventory):
                                item = player.inventory[idx]
                                # Equip item in the correct slot based on type
                                if item.item_type == "weapon":
                                    player.equipped_weapon = item
                                elif item.item_type == "armor":
                                    player.equipped_armor = item
                                elif item.item_type == "trinket":
                                    player.equipped_trinket = item
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

                        # Move the player if possible
                        player.move(dx, dy, game_map)
                        # Check if player is on an item to pick up
                        for item in items:
                            if player.x == item.x and player.y == item.y:
                                player.inventory.append(item)
                                items.remove(item)
                                print(f"Picked Up {item.name}!")
                                break  # Only pick up one item per move

if __name__ == "__main__":
    main()