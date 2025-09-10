import tcod
from player import Player, display_stats, display_inventory
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 60

def show_message(console, message, x=1, y=1, color=(255, 255, 0)):
    for i, line in enumerate(message.splitlines()):
        console.print(x, y + i, line, fg=color)

def display_inventory(player):
    lines = ["Inventory:"]
    if hasattr(player, "inventory") and player.inventory:
        for item in player.inventory:
            lines.append(f"- {item}")
    else:
        lines.append(" (empty)")
    return "\n".join(lines)

def draw_popup(console, message, width=30, height=18):
    x = 0
    y = 0
    # Draw box background
    for dx in range(width):
        for dy in range(height):
            console.print(x + dx, y + dy, " ", bg=(30, 30, 30))
    # Draw border
    for dx in range(width):
        console.print(x + dx, y, "-", fg=(255, 255, 0))
        console.print(x + dx, y + height - 1, "-", fg=(255, 255, 0))
    for dy in range(height):
        console.print(x, y + dy, "|", fg=(255, 255, 0))
        console.print(x + width - 1, y + dy, "|", fg=(255, 255, 0))
    # Print message inside box
    lines = message.splitlines()
    for i, line in enumerate(lines[:height-2]):
        console.print(x + 2, y + 1 + i, line, fg=(255, 255, 255))

# Redjack17 tileset mapping (CP437 and graphical)
TILES = {
    "floor": 32,        # Space character (CP437)
    "wall": 219,        # Solid block (CP437)
    "player": 1,        # '@' symbol (CP437)
    "door": 43,         # '+' symbol (CP437)
    "stairs_up": 94,    # '^' symbol (CP437)
    "stairs_down": 118, # 'v' symbol (CP437)
    "chest": 240,       # Graphical chest (bottom row, column 0)
    "grass": 0,         # Top-left tile (graphical grass)
    "water": 16,        # Second row, first column (graphical water)
    "brick": 32,        # Third row, first column (graphical brick)
    "tree": 48,         # Fourth row, first column (graphical tree)
    "mountain": 64,     # Fifth row, first column (graphical mountain)
    "road": 80,         # Sixth row, first column (graphical road)
    "bridge": 96,       # Seventh row, first column (graphical bridge)
    "trap": 112,        # Eighth row, first column (graphical trap)
    "key": 128,         # Ninth row, first column (graphical key)
    "potion": 144,      # Tenth row, first column (graphical potion)
    "sword": 160,       # Eleventh row, first column (graphical sword)
    "shield": 176,      # Twelfth row, first column (graphical shield)
    "crown": 192,       # Thirteenth row, first column (graphical crown)
    "skull": 208,       # Fourteenth row, first column (graphical skull)
    "book": 224,        # Fifteenth row, first column (graphical book)
    "gem": 240,         # Sixteenth row, first column (graphical gem)
    # Add more as you identify them!
}

def main():
    # Load a tileset (font)
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    showing_info = None  # Variable to track if inventory or stats are being shown

    # Create a window/context
    with tcod.context.new_terminal(
        SCREEN_WIDTH, SCREEN_HEIGHT, tileset=tileset, title="Roguelike"
    ) as context:
        # Create a console to draw on
        console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")

        player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        while True:
            console.clear()
            # Draw the map and player
            console.print(player.x, player.y, "@", fg=(255, 255, 255))

            # Show inventory or stats if requested
            if showing_info == "inventory":
                draw_popup(console, display_inventory(player))
            elif showing_info == "stats":
                draw_popup(console, display_stats(player))

            # Show everything on the screen
            context.present(console)

            # Handle input
            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()
                elif event.type == "KEYDOWN":
                    if event.sym == ord("i"):
                        showing_info = "inventory"
                    elif event.sym == ord("s"):
                        showing_info = "stats"
                    elif event.sym == tcod.event.KeySym.ESCAPE:
                        showing_info = None
                    elif event.sym == tcod.event.KeySym.UP:
                        player.y -= 1
                    elif event.sym == tcod.event.KeySym.DOWN:
                        player.y += 1
                    elif event.sym == tcod.event.KeySym.LEFT:
                        player.x -= 1
                    elif event.sym == tcod.event.KeySym.RIGHT:
                        player.x += 1

if __name__ == "__main__":
    main()


