import tcod
from game_map import SCREEN_WIDTH, SCREEN_HEIGHT, create_map
from player import Player
from item import Item

def main():
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    game_map = create_map()
    
    items = [
        Item(10, 10, "Sword", "!", "weapon", {"attack": 2}),
        Item(15, 5, "Apple", "%", "misc"),
        Item(12, 8, "Leather Armor", "[", "armor", {"defense": 1}),
        Item(18, 12, "Lucky Charm", "*", "trinket", {"luck": 5}),
    ]

    inventory_open = False  # Add this line before the game loop

    with tcod.context.new(
        columns=SCREEN_WIDTH,
        rows=SCREEN_HEIGHT,
        tileset=tcod.tileset.load_tilesheet(
            "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
        ),
        title="CDDA Runescape",
        vsync=True,
    ) as context:
        console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
        while True:
            console.clear()

            # Display health and mana at the top
            console.print(1, 0, f"HP: {player.health}/{player.max_health}", fg=(255, 80, 80))
            console.print(20, 0, f"MP: {player.mana}/{player.max_mana}", fg=(80, 80, 255))

            # Draw map
            for y in range(SCREEN_HEIGHT):
                for x in range(SCREEN_WIDTH):
                    if game_map[y][x] == "#":
                        console.print(x, y, "#", fg=(255, 255, 255))
            # Draw items
            for item in items:
                console.print(item.x, item.y, item.symbol, fg=(255, 255, 0))
            # Draw player
            console.print(player.x, player.y, "@", fg=(255, 255, 255))

            # Draw inventory panel if open
            if inventory_open:
                inv_x = SCREEN_WIDTH - 20  # Inventory panel starts 20 columns from the right
                console.print(inv_x, 1, "Inventory:", fg=(255, 255, 255))
                for idx, item in enumerate(player.inventory):
                    console.print(inv_x, 3 + idx, f"{idx+1}. {item.name}", fg=(255, 255, 0))
                # Show equipped items
                console.print(inv_x, SCREEN_HEIGHT - 6, "Equipped:", fg=(255, 255, 255))
                console.print(inv_x, SCREEN_HEIGHT - 5, f"Weapon: {player.equipped_weapon.name if player.equipped_weapon else 'None'}", fg=(200, 200, 255))
                console.print(inv_x, SCREEN_HEIGHT - 4, f"Armor: {player.equipped_armor.name if player.equipped_armor else 'None'}", fg=(200, 255, 200))
                console.print(inv_x, SCREEN_HEIGHT - 3, f"Trinket: {player.equipped_trinket.name if player.equipped_trinket else 'None'}", fg=(255, 200, 200))

            context.present(console)

            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()
                if event.type == "KEYDOWN":
                    if event.sym == ord("i"):
                        inventory_open = not inventory_open
                        continue  # Skip movement if toggling inventory

                    if inventory_open:
                        if event.sym in (ord("1"), ord("2"), ord("3"), ord("4"), ord("5")):
                            idx = event.sym - ord("1")
                            if 0 <= idx < len(player.inventory):
                                item = player.inventory[idx]
                                if item.item_type == "weapon":
                                    player.equipped_weapon = item
                                elif item.item_type == "armor":
                                    player.equipped_armor = item
                                elif item.item_type == "trinket":
                                    player.equipped_trinket = item
                    else:
                        dx, dy = 0, 0
                        if event.sym == tcod.event.K_UP:
                            dy = -1
                        elif event.sym == tcod.event.K_DOWN:
                            dy = 1
                        elif event.sym == tcod.event.K_LEFT:
                            dx = -1
                        elif event.sym == tcod.event.K_RIGHT:
                            dx = 1

                        player.move(dx, dy, game_map)
                        for item in items:
                            if player.x == item.x and player.y == item.y:
                                player.inventory.append(item)
                                items.remove(item)
                                print(f"Picked Up {item.name}!")
                                break  # Only pick up one item per move

if __name__ == "__main__":
    main()