import tcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

def main():
    with tcod.context.new(
        columns=SCREEN_WIDTH,
        rows=SCREEN_HEIGHT,
        tileset=tcod.tileset.load_tilesheet(
            "cdda-runescape/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
        ),
        title="CDDA Runescape",
        vsync=True,
    ) as context:
        console = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT, order="F")
        while True:
            console.clear()
            console.print(
                SCREEN_WIDTH // 2 - 14,
                SCREEN_HEIGHT // 2,
                "Hello, Cataclysm: Dark Days Ahead!",
                fg=(255, 255, 255),
            )
            context.present(console)  # <-- Use the context object here

            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()

if __name__ == "__main__":
    main()