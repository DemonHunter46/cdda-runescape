
import tcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45

PLAYER_CHAR = '@'
PLAYER_COLOR = (255, 255, 255)

class Player:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.level = 1
		self.inventory = []
		# Add more player stats as needed

	def move(self, dx, dy, game_map):
		new_x = self.x + dx
		new_y = self.y + dy
		if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
			if not game_map[new_y][new_x]:  # 0 = walkable
				self.x = new_x
				self.y = new_y

class Game:
	def __init__(self):
		self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
		self.game_map = self.initialize_map()
		# Placeholders for mechanics
		self.farming_tiles = set()
		self.buildings = []
		self.crafting_recipes = {}

	def initialize_map(self):
		# 0 = walkable, 1 = wall
		return [[0 for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

	def render(self, console):
		console.clear()
		# Draw map (walls)
		for y in range(MAP_HEIGHT):
			for x in range(MAP_WIDTH):
				if self.game_map[y][x]:
					console.print(x, y, '#', fg=(100, 100, 100))
		# Draw player
		console.print(self.player.x, self.player.y, PLAYER_CHAR, fg=PLAYER_COLOR)
		# Draw farming/building/crafting info (placeholder)
		console.print(1, SCREEN_HEIGHT - 2, f'Level: {self.player.level}', fg=(200, 200, 50))
		console.print(1, SCREEN_HEIGHT - 1, 'Inventory: ' + ', '.join(self.player.inventory), fg=(200, 200, 200))

	def handle_keys(self, key):
		if key.vk == tcod.event.K_UP:
			self.player.move(0, -1, self.game_map)
		elif key.vk == tcod.event.K_DOWN:
			self.player.move(0, 1, self.game_map)
		elif key.vk == tcod.event.K_LEFT:
			self.player.move(-1, 0, self.game_map)
		elif key.vk == tcod.event.K_RIGHT:
			self.player.move(1, 0, self.game_map)
		# Add more key handling for mechanics here


def main():
	tcod.console_set_custom_font(
		'dejavu10x10_gs_tc.png', tcod.FONT_LAYOUT_ASCII_INROW
	)
	with tcod.console_init_root(
		SCREEN_WIDTH, SCREEN_HEIGHT, order="F", title="Survival Roguelike", vsync=True
	) as root_console:
		game = Game()
		while True:
			game.render(root_console)
			tcod.console_flush()
			for event in tcod.event.wait():
				if event.type == "QUIT":
					raise SystemExit()
				if event.type == "KEYDOWN":
					game.handle_keys(event)

if __name__ == "__main__":
	main()
