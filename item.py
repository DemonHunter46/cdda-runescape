class Item:
    def __init__(self, x, y, name, symbol="!", item_type="misc", bonus=None):
        self.x = x
        self.y = y
        self.name = name
        self.symbol = symbol
        self.item_type = item_type  # "weapon", "armor", "trinket", etc.
        self.bonus = bonus or {}    # e.g., {"attack": 2}