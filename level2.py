import pygame
from pygame.locals import *
import time
import heapq

# Constants for ingame objects
PACMAN_COLOR = (255, 255, 0)
FOOD_COLOR = (0, 255, 0)  # Change to yellow (255, 255, 0)
MONSTER_COLOR = (255, 0, 0)  # Change to red (255, 0, 0)
WALL_COLOR = (0, 0, 255)
RUNTIME = 100
MOVE_DELAY = 0.3

# Node class


class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = 0
        self.h = 0

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)


class Map:
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()
        if contents.count('P') != 1:
            raise Exception('The game has only 1 Pac-man')
        contents = contents.splitlines()
        area = contents[0].split(' ')
        contents = contents[1:]
        self.height = int(area[0])
        self.width = int(area[1])

        pacman_position = contents[-1].split(' ')
        contents = contents[:-1]

        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == 'P':
                        self.pacman = (
                            int(pacman_position[0]), int(pacman_position[1]))
                        row.append(False)
                    elif contents[i][j] == '2':
                        self.food = (i, j)
                        row.append(False)
                    elif contents[i][j] == '0':
                        row.append(False)
                    elif contents[i][j] == '1':
                        row.append(True)
                    elif contents[i][j] == '3':
                        self.monster = (i, j)
                        row.append(False)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution = None

    def neighbor(self, state):
        row, col = state

        candidates = [
            ('up', (row - 1, col)),
            ('down', (row + 1, col)),
            ('left', (row, col - 1)),
            ('right', (row, col + 1))]
        results = []
        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c] and (r, c) != self.monster:
                    results.append((action, (r, c)))
            except IndexError:
                continue
        return results

    def solve_BFS(self):
        self.num_explored = 0
        start = Node(state=self.pacman, parent=None, action=None)

        self.explored = set()
        frontier = []

        heapq.heappush(frontier, start)

        while frontier:
            current = heapq.heappop(frontier)
            self.num_explored += 1

            if current.state == self.food:
                actions = []
                cells = []

                while current.parent is not None:
                    actions.append(current.action)
                    cells.append(current.state)
                    current = current.parent

                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            self.explored.add(current.state)

            for action, state in self.neighbor(current.state):
                isExist = False
                for node in frontier:
                    if node.state == state:
                        isExist = True
                        break
                if not isExist and state not in self.explored:
                    child = Node(state=state, parent=current, action=action)
                    heapq.heappush(frontier, child)

    def solve_astar(self):
        self.num_explored = 0
        start = Node(state=self.pacman, parent=None, action=None)

        self.explored = set()
        frontier = []
        heapq.heappush(frontier, start)

        while frontier:
            current = heapq.heappop(frontier)
            self.num_explored += 1

            if current.state == self.food:
                actions = []
                cells = []

                while current.parent is not None:
                    actions.append(current.action)
                    cells.append(current.state)
                    current = current.parent

                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            self.explored.add(current.state)

            for action, state in self.neighbor(current.state):
                isExist = False
                for node in frontier:
                    if node.state == state:
                        isExist = True
                        break
                if not isExist and state not in self.explored:
                    child = Node(state=state, parent=current, action=action)
                    child.g = current.g + 1
                    child.h = abs(
                        child.state[0] - self.food[0]) + abs(child.state[1] - self.food[1])
                    heapq.heappush(frontier, child)

    def solve_GBFS(self):
        self.num_explored = 0
        start = Node(state=self.pacman, parent=None, action=None)

        self.explored = set()
        frontier = []
        heapq.heappush(frontier, start)

        while frontier:
            current = heapq.heappop(frontier)
            self.num_explored += 1

            if current.state == self.food:
                actions = []
                cells = []

                while current.parent is not None:
                    actions.append(current.action)
                    cells.append(current.state)
                    current = current.parent

                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            self.explored.add(current.state)

            for action, state in self.neighbor(current.state):
                isExist = False
                for node in frontier:
                    if node.state == state:
                        isExist = True
                        break
                if not isExist and state not in self.explored:
                    child = Node(state=state, parent=current, action=action)
                    child.h = abs(
                        child.state[0] - self.food[0]) + abs(child.state[1] - self.food[1])
                    heapq.heappush(frontier, child)
# solve map


def solve_map(selected_option):
    # Initialize map
    filename = f'map{selected_option + 1}.txt'
    gameplay = Map(filename)

    # Constants
    GRID_SIZE = 50
    WIDTH, HEIGHT = gameplay.width * 50, gameplay.height * 50
    GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"Pac-Man Level 2 - Map {selected_option + 1}")

    # Initialize positions
    pacman_y, pacman_x = gameplay.pacman

    # Generate food coordinates
    food_y, food_x = gameplay.food

    # Generate stationary monster coordinates
    monster_y, monster_x = gameplay.monster

    path = []
    ticks = 0
    visited_cells = set()

    # Generate walls
    walls = gameplay.walls

    # Main game loop
    running = True
    path_calculated = False
    path_traced = False
    game_over = False
    win_message_displayed = False
    lose_message_displayed = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            if not path_calculated:
                gameplay.solve_GBFS()
                path = gameplay.solution[1]
                path_calculated = True

            if path and ticks < RUNTIME:
                pacman_y, pacman_x = path[0]
                visited_cells.add((pacman_x, pacman_y))
                path = path[1:]
                ticks += 1
                time.sleep(MOVE_DELAY)

            if (pacman_x, pacman_y) == (food_x, food_y):
                game_over = True
                win_message_displayed = True

            # Check for collision with the monster
            if (pacman_x, pacman_y) == (monster_x, monster_y):
                game_over = True
                lose_message_displayed = True

            if not path and not game_over and not path_traced:
                game_over = True
                lose_message_displayed = True

        screen.fill((0, 0, 0))

        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pygame.draw.rect(screen, (255, 255, 255),
                                 (x * GRID_SIZE, y * GRID_SIZE,
                                  GRID_SIZE, GRID_SIZE), 1)

        for y, row in enumerate(walls):
            for x, col in enumerate(row):
                if col:
                    wall_x, wall_y = x * GRID_SIZE, y * GRID_SIZE
                    # Draw the wall using custom texture
                    pygame.draw.rect(screen, WALL_COLOR,
                                     (wall_x, wall_y, GRID_SIZE, GRID_SIZE), 1)

                    # Draw diagonal lines on the wall
                    pygame.draw.line(screen, WALL_COLOR, (wall_x, wall_y),
                                     (wall_x + GRID_SIZE, wall_y + GRID_SIZE), 2)
                    pygame.draw.line(
                        screen, WALL_COLOR, (wall_x + GRID_SIZE, wall_y), (wall_x, wall_y + GRID_SIZE), 2)

        pygame.draw.rect(screen, FOOD_COLOR,
                         (food_x * GRID_SIZE, food_y * GRID_SIZE,
                          GRID_SIZE, GRID_SIZE))
        pygame.draw.circle(screen, PACMAN_COLOR,
                           (pacman_x * GRID_SIZE + GRID_SIZE // 2,
                            pacman_y * GRID_SIZE + GRID_SIZE // 2),
                           GRID_SIZE // 2)

        # Draw the stationary monster
        pygame.draw.rect(screen, MONSTER_COLOR,
                         (monster_x * GRID_SIZE, monster_y * GRID_SIZE,
                          GRID_SIZE, GRID_SIZE))

        if path_traced:
            for cell in visited_cells:
                pygame.draw.rect(screen, (200, 200, 200),
                                 (cell[0] * GRID_SIZE, cell[1] * GRID_SIZE,
                                  GRID_SIZE, GRID_SIZE))
            for cell in visited_cells:
                pygame.draw.rect(screen, (0, 255, 0),
                                 (cell[0] * GRID_SIZE, cell[1] * GRID_SIZE,
                                  GRID_SIZE, GRID_SIZE), 2)

        if not path and not path_traced:
            path_traced = True

        if game_over:
            if win_message_displayed:
                FONT = pygame.font.Font(None, 36)
                text = FONT.render("You Win!", True, (0, 255, 0))
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(text, text_rect)
            elif lose_message_displayed:
                FONT = pygame.font.Font(None, 36)
                text = FONT.render("You Lose!", True, (255, 0, 0))
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(text, text_rect)

        pygame.display.flip()

# Main function for Level 2
def main():
    # Create menu maps
    pygame.init()

    # Create the display surface
    screen_menu = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Menu Maps")

    # Set up colors and fonts
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    FONT = pygame.font.Font(None, 36)

    # Menu options
    options = ["Map 1", "Map 2"]

    # Position for menu items
    menu_rects = [FONT.render("   " + option, True, WHITE).
                  get_rect(center=(200, 100 + index * 50)) for index, option in enumerate(options)]

    # Game loop
    selected_option = 0
    running_menu = True

    def draw_menu():
        screen_menu.fill((0, 0, 0))
        for index, rect in enumerate(menu_rects):
            color = YELLOW if index == selected_option else WHITE
            text = FONT.render(
                "-> " + options[index] if index == selected_option else "   " + options[index], True, color)
            screen_menu.blit(text, rect)

    while running_menu:
        for event in pygame.event.get():
            if event.type == QUIT:
                running_menu = False

            if event.type == MOUSEBUTTONDOWN:
                for index, rect in enumerate(menu_rects):
                    if rect.collidepoint(event.pos):
                        selected_option = index

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == K_RETURN:
                    if selected_option == 0:  # Start Map 1
                        solve_map(selected_option)
                    elif selected_option == 1:  # Start Map 2
                        solve_map(selected_option)

        draw_menu()
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
