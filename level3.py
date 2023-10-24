import pygame
import random
import heapq
import time

# Constants
GRID_SIZE = 40
WIDTH, HEIGHT = 400, 400
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
PACMAN_COLOR = (255, 255, 0)
FOOD_COLOR = (0, 255, 0)  # Change to yellow (255, 255, 0)
MONSTER_COLOR = (255, 0, 0)  # Change to red (255, 0, 0)
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

# Main function for Level 2
def main():

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man Level 3")

    # Initial positions
    pacman_x, pacman_y = 0, 0

    # Generate multiple food coordinates
    num_food = 5  # Change to the number of food items you want
    food_coordinates = [(random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)) for _ in range(num_food)]

    # Generate random stationary monster coordinates
    monster_x, monster_y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
    while (monster_x, monster_y) in food_coordinates:
        monster_x, monster_y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)

    path = []
    ticks = 0
    recompute_path = True

    # Generate random obstacles (walls) when the game starts
    num_obstacles = random.randint(30, 60)
    obstacles = set()
    for _ in range(num_obstacles):
        while True:
            x, y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in food_coordinates and (x, y) != (0, 0) and (x, y) != (monster_x, monster_y):
                obstacles.add((x, y))
                break

    # Main game loop
    running = True
    game_over = False
    win_message_displayed = False
    lose_message_displayed = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            if recompute_path:
                start_node = Node(pacman_x, pacman_y)
                nearest_food = find_nearest_food(start_node, food_coordinates, obstacles)
                if nearest_food:
                    goal_node = Node(nearest_food[0], nearest_food[1])
                    path = astar_search(start_node, goal_node, obstacles)
                recompute_path = False

            if not path:  # No path found
                game_over = True
                lose_message_displayed = True
            elif ticks < RUNTIME:
                pacman_x, pacman_y = path[0]
                path = path[1:]
                ticks += 1
                time.sleep(MOVE_DELAY)

            # Check for collision with the monster
            if (pacman_x, pacman_y) == (monster_x, monster_y):
                game_over = True
                lose_message_displayed = True

            if not path and not game_over:
                if (pacman_x, pacman_y) in food_coordinates:
                    food_coordinates.remove((pacman_x, pacman_y))  # Remove the eaten food
                    recompute_path = True

                if not food_coordinates:
                    game_over = True
                    win_message_displayed = True

            # Move the monster randomly
            monster_x, monster_y = move_monster_randomly(monster_x, monster_y, obstacles)

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

        for food_x, food_y in food_coordinates:
            pygame.draw.rect(screen, FOOD_COLOR, (food_x * GRID_SIZE, food_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        pygame.draw.circle(screen, PACMAN_COLOR,
                           (pacman_x * GRID_SIZE + GRID_SIZE // 2, pacman_y * GRID_SIZE + GRID_SIZE // 2),
                           GRID_SIZE // 2)

        # Draw the stationary monster
        pygame.draw.rect(screen, MONSTER_COLOR, (monster_x * GRID_SIZE, monster_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

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

# Helper function to find the nearest food using A* search
def find_nearest_food(start, food_coordinates, obstacles):
    if not food_coordinates:
        return None

    nearest_food = None
    nearest_distance = float('inf')

    for food_x, food_y in food_coordinates:
        goal_node = Node(food_x, food_y)
        path = astar_search(start, goal_node, obstacles)

        if path and len(path) < nearest_distance:
            nearest_food = (food_x, food_y)
            nearest_distance = len(path)

    return nearest_food

# Helper function to move the monster randomly
def move_monster_randomly(monster_x, monster_y, obstacles):
    possible_moves = [
        (monster_x - 1, monster_y),
        (monster_x + 1, monster_y),
        (monster_x, monster_y - 1),
        (monster_x, monster_y + 1)
    ]
    # Filter out moves that hit obstacles or go out of bounds
    valid_moves = [(x, y) for x, y in possible_moves if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and (x, y) not in obstacles]
    if valid_moves:
        return random.choice(valid_moves)
    return monster_x, monster_y

if __name__ == "__main__":
    main()
