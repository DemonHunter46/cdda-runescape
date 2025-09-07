import random

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

def create_map():
    """Create a village map with buildings and resources."""
    # Start with an empty map of grass (.)
    game_map = [["." for x in range(SCREEN_WIDTH)] for y in range(SCREEN_HEIGHT)]
    
    # Add border walls
    for x in range(SCREEN_WIDTH):
        game_map[0][x] = "#"  # Top wall
        game_map[SCREEN_HEIGHT-1][x] = "#"  # Bottom wall
    
    for y in range(SCREEN_HEIGHT):
        game_map[y][0] = "#"  # Left wall
        game_map[y][SCREEN_WIDTH-1] = "#"  # Right wall
    
    # Create village center with a plaza
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    for y in range(center_y-5, center_y+6):
        for x in range(center_x-10, center_x+11):
            if 0 < x < SCREEN_WIDTH-1 and 0 < y < SCREEN_HEIGHT-1:
                game_map[y][x] = " "  # Clear space for plaza
    
    # Add paths from center to edges
    for x in range(center_x-2, center_x+3):
        for y in range(5, SCREEN_HEIGHT-6):
            game_map[y][x] = " "  # Vertical path
    for y in range(center_y-2, center_y+3):
        for x in range(5, SCREEN_WIDTH-6):
            game_map[y][x] = " "  # Horizontal path
    
    # Add buildings around the plaza
    
    # Blacksmith (top-left of plaza)
    for y in range(center_y-8, center_y-3):
        for x in range(center_x-15, center_x-10):
            if 0 < x < SCREEN_WIDTH-1 and 0 < y < SCREEN_HEIGHT-1:
                game_map[y][x] = "#"  # Building walls
    game_map[center_y-6][center_x-13] = "+"  # Door
    
    # General Store (top-right of plaza)
    for y in range(center_y-8, center_y-3):
        for x in range(center_x+10, center_x+15):
            if 0 < x < SCREEN_WIDTH-1 and 0 < y < SCREEN_HEIGHT-1:
                game_map[y][x] = "#"
    game_map[center_y-6][center_x+13] = "+"  # Door
    
    # Inn (bottom-left of plaza)
    for y in range(center_y+3, center_y+8):
        for x in range(center_x-15, center_x-10):
            if 0 < x < SCREEN_WIDTH-1 and 0 < y < SCREEN_HEIGHT-1:
                game_map[y][x] = "#"
    game_map[center_y+5][center_x-13] = "+"  # Door
    
    # Bank (bottom-right of plaza)
    for y in range(center_y+3, center_y+8):
        for x in range(center_x+10, center_x+15):
            if 0 < x < SCREEN_WIDTH-1 and 0 < y < SCREEN_HEIGHT-1:
                game_map[y][x] = "#"
    game_map[center_y+5][center_x+13] = "+"  # Door
    
    # Add resource areas
    
    # Forest area (top of map)
    for y in range(5, 15):
        for x in range(20, 60):
            if random.random() < 0.3 and game_map[y][x] == ".":
                game_map[y][x] = "T"  # Trees
    
    # Mine area (bottom of map)
    for y in range(SCREEN_HEIGHT-15, SCREEN_HEIGHT-5):
        for x in range(20, 60):
            if random.random() < 0.4 and game_map[y][x] == ".":
                game_map[y][x] = "#"  # Rocks
    
    # Fishing pond (left of map)
    for y in range(20, 30):
        for x in range(10, 20):
            if game_map[y][x] == ".":
                game_map[y][x] = "~"  # Water
    
    # Farming area (right of map)
    for y in range(20, 30):
        for x in range(60, 70):
            if game_map[y][x] == ".":
                game_map[y][x] = ","  # Farmland
    
    return game_map