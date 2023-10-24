import pygame
import heapq
import time
import random

# Constants
GRID_SIZE = 30
WIDTH, HEIGHT = 400, 400
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
PACMAN_COLOR = (255, 255, 0)
FOOD_COLOR = (0, 255, 0)
WALL_COLOR = (0, 0, 255)
RUNTIME = 100
MOVE_DELAY = 0.3

# Node class for A* search
class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0
        self.h = 0

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

# A* search algorithm
def astar_search(start, goal, walls):
    open_set = []
    closed_set = set()
    heapq.heappush(open_set, start)

    while open_set:
        current = heapq.heappop(open_set)
        if current.x == goal.x and current.y == goal.y:
            path = []
            while current:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1]

        closed_set.add((current.x, current.y))

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_x, new_y = current.x + dx, current.y + dy
            if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and (new_x, new_y) not in closed_set and (new_x, new_y) not in walls:
                neighbor = Node(new_x, new_y, current)
                neighbor.g = current.g + 1
                neighbor.h = abs(neighbor.x - goal.x) + abs(neighbor.y - goal.y)
                heapq.heappush(open_set, neighbor)
# Main function for Level 1
def main():
    # ... (Your Level 1 code)
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man")

    # Initial positions
    pacman_x, pacman_y = 0, 0

    # Generate random food coordinates
    food_x, food_y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)

    path = []
    ticks = 0
    visited_cells = set()

    # Generate random obstacles (walls) when the game starts
    num_obstacles = random.randint(30, 60)
    obstacles = set()
    for _ in range(num_obstacles):
        while True:
            x, y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
            if (x, y) != (0, 0) and (x, y) != (food_x, food_y):
                obstacles.add((x, y))
                break


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
                start_node = Node(pacman_x, pacman_y)
                goal_node = Node(food_x, food_y)
                path = astar_search(start_node, goal_node, obstacles)
                path_calculated = True

            if path and ticks < RUNTIME:
                pacman_x, pacman_y = path[0]
                visited_cells.add((pacman_x, pacman_y))
                path = path[1:]
                ticks += 1
                time.sleep(MOVE_DELAY)

            if (pacman_x, pacman_y) == (food_x, food_y):
                game_over = True
                win_message_displayed = True

            if not path and not game_over and not path_traced:
                game_over = True
                lose_message_displayed = True

        screen.fill((0, 0, 0))

        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pygame.draw.rect(screen, (255, 255, 255), (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

        for wall in obstacles:
            x, y = wall[0], wall[1]
            wall_x, wall_y = x * GRID_SIZE, y * GRID_SIZE
            # Draw the wall using custom texture
            pygame.draw.rect(screen, WALL_COLOR, (wall_x, wall_y, GRID_SIZE, GRID_SIZE), 1)

            # Draw diagonal lines on the wall
            pygame.draw.line(screen, WALL_COLOR, (wall_x, wall_y), (wall_x + GRID_SIZE, wall_y + GRID_SIZE), 2)
            pygame.draw.line(screen, WALL_COLOR, (wall_x + GRID_SIZE, wall_y), (wall_x, wall_y + GRID_SIZE), 2)

        pygame.draw.rect(screen, FOOD_COLOR, (food_x * GRID_SIZE, food_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.circle(screen, PACMAN_COLOR,
                           (pacman_x * GRID_SIZE + GRID_SIZE // 2, pacman_y * GRID_SIZE + GRID_SIZE // 2),
                           GRID_SIZE // 2)

        if path_traced:
            for cell in visited_cells:
                pygame.draw.rect(screen, (200, 200, 200),
                                 (cell[0] * GRID_SIZE, cell[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            for cell in visited_cells:
                pygame.draw.rect(screen, (0, 255, 0), (cell[0] * GRID_SIZE, cell[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                                 2)

        if not path and not path_traced:
            path_traced = True

        if game_over:
            if win_message_displayed:
                font = pygame.font.Font(None, 36)
                text = font.render("You Win!", True, (0, 255, 0))
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(text, text_rect)
            elif lose_message_displayed:
                font = pygame.font.Font(None, 36)
                text = font.render("You Lose!", True, (255, 0, 0))
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(text, text_rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
