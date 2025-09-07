import tcod
from game_map import SCREEN_WIDTH, SCREEN_HEIGHT, create_map
from player import Player
from item import Item

def main():
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    game_map = create_map()
    
    items = [
        Item(10, 10, "Sword", "!"),
        Item(15, 5, "Apple", "%"),
    ]



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
            
            for y in range(SCREEN_HEIGHT):
                for x in range(SCREEN_WIDTH):
                    if game_map[y][x] == "#":
                        console.print(x, y, "#", fg=(255, 255, 255))
            
            for item in items:
                console.print(item.x, item.y, item.symbol, fg=(255, 255, 0))
            
            console.print(player.x, player.y, "@", fg=(255, 255, 255))
            context.present(console)


            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()
                
                if event.type == "KEYDOWN":
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

if __name__ == "__main__":
    main()