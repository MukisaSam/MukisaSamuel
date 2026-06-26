import random

class Entity:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol


class Player(Entity):
    MOVES = {
        "w": (0, -1),
        "s": (0, 1),
        "a": (-1, 0),
        "d": (1, 0),
    }

    def __init__(self, x, y):
        super().__init__(x, y, "@")
        self._health = 3

    @property
    def health(self):
        return self._health

    def take_damage(self, amount):
        self._health -= amount

    def is_alive(self):
        return self._health > 0

    def move(self, direction, grid_size):
        dx, dy = self.MOVES.get(direction, (0, 0))
        new_x = max(0, min(grid_size - 1, self.x + dx))
        new_y = max(0, min(grid_size - 1, self.y + dy))
        self.x, self.y = new_x, new_y


class Trap(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "X")

    def trigger(self, player):
        player.take_damage(1)


class Treasure(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "T")



class Game:
    GRID_SIZE = 5

    def __init__(self):
        self.player = Player(0, 0)
        self.treasure = self._place_random(exclude=[(0, 0)])
        self.treasure = Treasure(*self.treasure)
        self.traps = self._place_traps()
        self.game_over = False
        self.message = ""

    def _place_random(self, exclude):
        while True:
            pos = (random.randint(0, self.GRID_SIZE - 1), random.randint(0, self.GRID_SIZE - 1))
            if pos not in exclude:
                return pos

    def _place_traps(self, count=4):
        occupied = [(0, 0), (self.treasure.x, self.treasure.y)]
        traps = []
        for _ in range(count):
            pos = self._place_random(exclude=occupied)
            occupied.append(pos)
            traps.append(Trap(*pos))
        return traps

    def render(self):
        grid = [["." for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        grid[self.treasure.y][self.treasure.x] = self.treasure.symbol
        for trap in self.traps:
            grid[trap.y][trap.x] = trap.symbol
        grid[self.player.y][self.player.x] = self.player.symbol

        print("\n" + "  ".join(str(i) for i in range(self.GRID_SIZE)))
        for row in grid:
            print(" ".join(row))
        print(f"Health: {self.player.health}")
        if self.message:
            print(self.message)

    def check_collisions(self):
        self.message = ""
        for trap in self.traps:
            if (trap.x, trap.y) == (self.player.x, self.player.y):
                trap.trigger(self.player)
                self.traps.remove(trap)
                self.message = "You hit a trap! -1 health"
                if not self.player.is_alive():
                    self.message = "You ran out of health. Game over!"
                    self.game_over = True
                break

        if (self.treasure.x, self.treasure.y) == (self.player.x, self.player.y):
            self.message = "You found the treasure! You win!"
            self.game_over = True

    def run(self):
        print("=== Memory Labyrinth ===")
        print("Find the treasure (T), avoid the traps (X). Move with W/A/S/D, Q to quit.")
        while not self.game_over:
            self.render()
            move = input("Move (w/a/s/d, q to quit): ").strip().lower()
            if move == "q":
                print("Thanks for playing!")
                return
            if move not in Player.MOVES:
                print("Invalid move. Use w, a, s, or d.")
                continue
            self.player.move(move, self.GRID_SIZE)
            self.check_collisions()

        self.render()


if __name__ == "__main__":
    Game().run()
