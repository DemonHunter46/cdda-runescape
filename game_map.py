SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

def create_map():
    """Create a simple bordered map."""
    return [
        ["#" if x == 0 or x == SCREEN_WIDTH - 1 or y == 0 or y == SCREEN_HEIGHT - 1 else "."
         for x in range(SCREEN_WIDTH)]
        for y in range(SCREEN_HEIGHT)
    ]