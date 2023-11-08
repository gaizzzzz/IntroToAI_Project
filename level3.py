# import pygame
# import random
# import heapq
# import time
#
# # Constants
# GRID_SIZE = 40
# WIDTH, HEIGHT = 400, 400
# GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
# PACMAN_COLOR = (255, 255, 0)
# FOOD_COLOR = (0, 255, 0)  # Change to yellow (255, 255, 0)
# MONSTER_COLOR = (255, 0, 0)  # Change to red (255, 0, 0)
# WALL_COLOR = (0, 0, 255)
# RUNTIME = 100
# MOVE_DELAY = 0.3
#
# # Node class for A* search
# class Node:
#     def __init__(self, x, y, parent=None):
#         self.x = x
#         self.y = y
#         self.parent = parent
#         self.g = 0
#         self.h = 0
#
#     def __lt__(self, other):
#         return (self.g + self.h) < (other.g + other.h)
#
# # A* search algorithm
# def astar_search(start, goal, walls):
#     open_set = []
#     closed_set = set()
#     heapq.heappush(open_set, start)
#
#     while open_set:
#         current = heapq.heappop(open_set)
#         if current.x == goal.x and current.y == goal.y:
#             path = []
#             while current:
#                 path.append((current.x, current.y))
#                 current = current.parent
#             return path[::-1]
#
#         closed_set.add((current.x, current.y))
#
#         for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
#             new_x, new_y = current.x + dx, current.y + dy
#             if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and (new_x, new_y) not in closed_set and (new_x, new_y) not in walls:
#                 neighbor = Node(new_x, new_y, current)
#                 neighbor.g = current.g + 1
#                 neighbor.h = abs(neighbor.x - goal.x) + abs(neighbor.y - goal.y)
#                 heapq.heappush(open_set, neighbor)
#
# # Main function for Level 3
# def main():
#
#     # Initialize pygame
#     pygame.init()
#     screen = pygame.display.set_mode((WIDTH, HEIGHT))
#     pygame.display.set_caption("Pac-Man Level 3")
#
#     # Initial positions
#     pacman_x, pacman_y = 0, 0
#
#     # Generate multiple food coordinates
#     num_food = 5  # Change to the number of food items you want
#     food_coordinates = [(random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)) for _ in range(num_food)]
#     print(food_coordinates)
#
#     # Generate random stationary monster coordinates
#     monster_x, monster_y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
#     while (monster_x, monster_y) in food_coordinates:
#         monster_x, monster_y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
#
#     path = []
#     ticks = 0
#     recompute_path = True
#
#     # Generate random obstacles (walls) when the game starts
#     num_obstacles = random.randint(30, 60)
#     obstacles = set()
#     for _ in range(num_obstacles):
#         while True:
#             x, y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
#             if (x, y) not in food_coordinates and (x, y) != (0, 0) and (x, y) != (monster_x, monster_y):
#                 obstacles.add((x, y))
#                 break
#
#     # Main game loop
#     running = True
#     game_over = False
#     win_message_displayed = False
#     lose_message_displayed = False
#
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#         if not game_over:
#             if recompute_path:
#                 start_node = Node(pacman_x, pacman_y)
#                 nearest_food = find_nearest_food(start_node, food_coordinates, obstacles)
#                 if nearest_food:
#                     goal_node = Node(nearest_food[0], nearest_food[1])
#                     path = astar_search(start_node, goal_node, obstacles)
#                 recompute_path = False
#
#             if not path:  # No path found
#                 game_over = True
#                 lose_message_displayed = True
#             elif ticks < RUNTIME:
#                 pacman_x, pacman_y = path[0]
#                 path = path[1:]
#                 ticks += 1
#                 time.sleep(MOVE_DELAY)
#
#             # Check for collision with the monster
#             if (pacman_x, pacman_y) == (monster_x, monster_y):
#                 game_over = True
#                 lose_message_displayed = True
#
#             if not path and not game_over:
#                 if (pacman_x, pacman_y) in food_coordinates:
#                     food_coordinates.remove((pacman_x, pacman_y))  # Remove the eaten food
#                     recompute_path = True
#
#                 if not food_coordinates:
#                     game_over = True
#                     win_message_displayed = True
#
#             # Move the monster randomly
#             monster_x, monster_y = move_monster_randomly(monster_x, monster_y, obstacles)
#
#         screen.fill((0, 0, 0))
#
#         for x in range(GRID_WIDTH):
#             for y in range(GRID_HEIGHT):
#                 pygame.draw.rect(screen, (255, 255, 255), (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
#
#         for wall in obstacles:
#             x, y = wall[0], wall[1]
#             wall_x, wall_y = x * GRID_SIZE, y * GRID_SIZE
#             # Draw the wall using custom texture
#             pygame.draw.rect(screen, WALL_COLOR, (wall_x, wall_y, GRID_SIZE, GRID_SIZE), 1)
#
#             # Draw diagonal lines on the wall
#             pygame.draw.line(screen, WALL_COLOR, (wall_x, wall_y), (wall_x + GRID_SIZE, wall_y + GRID_SIZE), 2)
#             pygame.draw.line(screen, WALL_COLOR, (wall_x + GRID_SIZE, wall_y), (wall_x, wall_y + GRID_SIZE), 2)
#
#         for food_x, food_y in food_coordinates:
#             pygame.draw.rect(screen, FOOD_COLOR, (food_x * GRID_SIZE, food_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
#
#         pygame.draw.circle(screen, PACMAN_COLOR,
#                            (pacman_x * GRID_SIZE + GRID_SIZE // 2, pacman_y * GRID_SIZE + GRID_SIZE // 2),
#                            GRID_SIZE // 2)
#
#         # Draw the stationary monster
#         pygame.draw.rect(screen, MONSTER_COLOR, (monster_x * GRID_SIZE, monster_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
#
#         if game_over:
#             if win_message_displayed:
#                 font = pygame.font.Font(None, 36)
#                 text = font.render("You Win!", True, (0, 255, 0))
#                 text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
#                 screen.blit(text, text_rect)
#             elif lose_message_displayed:
#                 font = pygame.font.Font(None, 36)
#                 text = font.render("You Lose!", True, (255, 0, 0))
#                 text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
#                 screen.blit(text, text_rect)
#
#         pygame.display.flip()
#
#     pygame.quit()
#
# # Helper function to find the nearest food using A* search
# def find_nearest_food(start, food_coordinates, obstacles):
#     if not food_coordinates:
#         return None
#
#     nearest_food = None
#     nearest_distance = float('inf')
#
#     for food_x, food_y in food_coordinates:
#         goal_node = Node(food_x, food_y)
#         path = astar_search(start, goal_node, obstacles)
#
#         if path and len(path) < nearest_distance:
#             nearest_food = (food_x, food_y)
#             nearest_distance = len(path)
#
#     return nearest_food
#
# # Helper function to move the monster randomly
# def move_monster_randomly(monster_x, monster_y, obstacles):
#     possible_moves = [
#         (monster_x - 1, monster_y),
#         (monster_x + 1, monster_y),
#         (monster_x, monster_y - 1),
#         (monster_x, monster_y + 1)
#     ]
#     # Filter out moves that hit obstacles or go out of bounds
#     valid_moves = [(x, y) for x, y in possible_moves if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and (x, y) not in obstacles]
#     if valid_moves:
#         return random.choice(valid_moves)
#     return monster_x, monster_y
#
# if __name__ == "__main__":
#     main()

import heapq
import pygame
import time
from pygame.locals import *

RUNTIME = 100
MOVE_DELAY = 0.3
WALL_COLOR = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = 0
        self.h = 0

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)


def find_neighbor(node, matrix):
    row, col = node.state

    candidates = [
        ('up', (row - 1, col)),
        ('down', (row + 1, col)),
        ('left', (row, col - 1)),
        ('right', (row, col + 1))]

    n = len(matrix)
    m = len(matrix[0])
    results = []
    for action, (r, c) in candidates:
        if 0 <= r < n and 0 <= c < m and matrix[r][c] != 1 and matrix[r][c] != 3:
            results.append((action, (r, c)))

    return results


def find_monster_neighbor(monster_state, matrix):
    row = monster_state[0]
    col = monster_state[1]

    candidates = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

    n = len(matrix)
    m = len(matrix[0])
    results = []
    for (r, c) in candidates:
        if 0 <= r < n and 0 <= c < m and matrix[r][c] != 1:
            results.append((r, c))

    return results


def find_pacman_vision(state, map_matrix):
    r = len(map_matrix)
    c = len(map_matrix[0])

    rs = state[0] - 3
    re = state[0] + 4
    cs = state[1] - 3
    ce = state[1] + 4

    if rs < 0:
        rs = 0
    if re > r:
        re = r
    if cs < 0:
        cs = 0
    if ce > c:
        ce = c

    return rs, re, cs, ce


def find_heuristic(state, explores, foods_visible, monster_state):
    if state in foods_visible:
        return -1
    if monster_state is not None:
        row, col = monster_state
        if state in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1), (row, col)]:
            return 100
    if len(foods_visible) != 0:
        heu = []
        for food in foods_visible:
            h = abs(state[0] - food[0]) + abs(state[1] - food[1])
            heu.append(int(h))
        return min(heu)
    return 0

def find_path(map_matrix, pacman_state, foods, monster_state):
    start_node = Node(state=pacman_state, parent=None, action=None)
    monster_node = Node(state=monster_state, parent=None, action=None)
    frontiers = []  # chứa các Node được đi đến
    explores = []  # chứa các Node đã đươc khám phá
    heapq.heappush(frontiers, start_node)
    actions = []
    path = []
    node = None
    while frontiers:
        current_node = heapq.heappop(frontiers)
        # print(current_node.state)
        explores.append(current_node.state)

        if current_node.state in foods:
            map_matrix[current_node.state[0]][current_node.state[1]] = 0
            foods.remove(current_node.state)
            if len(foods) == 0:
                while current_node.parent is not None:
                    actions.append(current_node.action)
                    path.append(current_node.state)
                    current_node = current_node.parent
                actions.reverse()
                path.reverse()
                break
        if current_node.state == monster_node.state:
            break

        rs, re, cs, ce = find_pacman_vision(current_node.state, map_matrix)
        # find foods
        foods_visible = []
        monster_visible = None
        for i in range(rs, re):
            for j in range(cs, ce):
                if map_matrix[i][j] == 2:
                    foods_visible.append((i, j))
        if rs <= monster_node.state[0] < re and cs <= monster_node.state[1] < ce:
            monster_visible = monster_state
        # update heuristic cho cac frontier
        for node in frontiers:
            node.g = find_heuristic(node.state, explores, foods_visible, monster_visible)
        # find neighbor phai tinh theo node trong
        neighbours = find_neighbor(current_node, map_matrix)
        for action, state in neighbours:
            next_node = Node(state=state, parent=current_node, action=action)
            next_node.g = current_node.g + 1
            next_node.h = find_heuristic(state, explores, foods_visible, monster_visible)
            heapq.heappush(frontiers, next_node)

    return path


def find_full_path(map_matrix, pacman_state, foods, monster_state):
    foods_save = foods[:]
    path = find_path(map_matrix, pacman_state, foods, monster_state)
    while True:
        for i in path:
            if i in foods_save:
                foods_save.remove(i)
        if len(foods_save) == 0:
            break

        # Khôi phục map_matrix
        for food in foods_save:
            map_matrix[food[0]][food[1]] = 2

        new_start_state = path[len(path) - 1]
        foods_save_temp = foods_save[:]
        new_path = find_path(map_matrix, new_start_state, foods_save_temp, monster_state)
        path += new_path

    return path

def solve_map(selected_map):
    filename = f"level3_map{selected_map + 1}.txt"
    f = open(filename)
    pointer = f.readline().split()
    size = (int(pointer[0]), int(pointer[1]))
    map_matrix = []
    for i in range(0, size[0]):
        pointer = list(map(int, f.readline().split()))
        map_matrix.append(pointer)
    pointer = f.readline().split()
    pacman_state = (int(pointer[0]), int(pointer[1]))
    pacman_x, pacman_y = pacman_state
    # print(f"Pacman pos: {pacman_x} {pacman_y}")
    f.close()

    walls = []
    foods = []
    foods_copy = []
    monster_state = None
    for i in range(0, size[0]):
        for j in range(0, size[1]):
            if map_matrix[i][j] == 1:
                walls.append((i, j))
            elif map_matrix[i][j] == 2:
                foods.append((i, j))
                foods_copy.append((i, j))
            elif map_matrix[i][j] == 3:
                monster_state = (i, j)
    monster_x, monster_y = monster_state

    path = find_full_path(map_matrix, pacman_state, foods, monster_state)

    GRID_SIZE = 60
    pygame.init()
    pygame.display.set_caption(f"Pac-Man Level 3 - Map {selected_map + 1}")
    height, width = size[0] * GRID_SIZE, size[1] * GRID_SIZE
    GRID_WIDTH, GRID_HEIGHT = width // GRID_SIZE, height // GRID_SIZE
    screen = pygame.display.set_mode((width, height))

    ticks = 0
    running = True
    game_over = False
    win_message_displayed = False
    lose_message_displayed = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            if not path:  # No path found
                game_over = True
                lose_message_displayed = True
            elif ticks < RUNTIME:
                pacman_x, pacman_y = path[0]
                # print(f"Pacman: {pacman_x} {pacman_y}")
                path = path[1:]
                # print(f"Path: {path}")
                ticks += 1
                time.sleep(MOVE_DELAY)

            # Check for collision with the monster
            if (pacman_x, pacman_y) == (monster_x, monster_y):
                game_over = True
                lose_message_displayed = True

            if len(path) >= 0 and not game_over:
                if (pacman_x, pacman_y) in foods_copy:
                    # print(f"Food in {pacman_x} {pacman_y}")
                    foods_copy.remove((pacman_x, pacman_y))  # Remove the eaten food

                if len(foods_copy) == 0:
                    game_over = True
                    win_message_displayed = True

        # draw map
        screen.fill((0, 0, 0))

        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pygame.draw.rect(screen, (255, 255, 255), (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

        for wall_x, wall_y in walls:
            pygame.draw.rect(screen, (0, 0, 255), (wall_y * GRID_SIZE, wall_x * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, (255, 255, 255), (wall_y * GRID_SIZE, wall_x * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
            pygame.draw.line(screen, (0, 0, 0), (wall_y * GRID_SIZE, wall_x * GRID_SIZE),
                             (wall_y * GRID_SIZE + GRID_SIZE, wall_x * GRID_SIZE + GRID_SIZE), 3)
            pygame.draw.line(screen, (0, 0, 0), (wall_y * GRID_SIZE, wall_x * GRID_SIZE + GRID_SIZE),
                             (wall_y * GRID_SIZE + GRID_SIZE, wall_x * GRID_SIZE), 3)

        for food_x, food_y in foods_copy:
            pygame.draw.circle(screen, (255, 255, 255),
                               (food_y * GRID_SIZE + GRID_SIZE // 2, food_x * GRID_SIZE + GRID_SIZE // 2),
                               GRID_SIZE // 5)
            pygame.draw.rect(screen, (255, 255, 255), (food_y * GRID_SIZE, food_x * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

        # draw_monster
        pygame.draw.rect(screen, (255, 0, 0), (monster_y * GRID_SIZE, monster_x * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, (255, 255, 255), (monster_y * GRID_SIZE, monster_x * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                         1)

        pygame.draw.circle(screen, (255, 255, 0),
                           (pacman_y * GRID_SIZE + GRID_SIZE // 2, pacman_x * GRID_SIZE + GRID_SIZE // 2),
                           GRID_SIZE // 2)

        if game_over:
            if win_message_displayed:
                font = pygame.font.Font(None, 36)
                text = font.render("You Win!", True, (0, 255, 0))
                text_rect = text.get_rect(center=(width // 2, height // 2))
                screen.blit(text, text_rect)
            elif lose_message_displayed:
                font = pygame.font.Font(None, 36)
                text = font.render("You Lose!", True, (255, 0, 0))
                text_rect = text.get_rect(center=(width // 2, height // 2))
                screen.blit(text, text_rect)

        pygame.display.flip()

# Đọc map
def main():
    # filename = input("Input file map (level3_map<>.txt): ")

    # Create menu maps
    pygame.init()

    # Create the display surface
    screen_menu = pygame.display.set_mode((700, 400))
    pygame.display.set_caption("Menu Maps")

    # Create font
    FONT = pygame.font.Font(None, 36)

    # Menu options
    options = ["Map 1", "Map 2"]

    # Position for menu items
    menu_rects = [FONT.render("   " + option, True, WHITE).
                  get_rect(center=(200, 100 + index * 50)) for index, option in enumerate(options)]

    # Game loop
    selected_map = 0
    running_menu = True

    def draw_menu():
        screen_menu.fill((0, 0, 0))
        for index, rect in enumerate(menu_rects):
            color = YELLOW if index == selected_map else WHITE
            text = FONT.render(
                "-> " + options[index] if index == selected_map else "   " + options[index], True, color)
            screen_menu.blit(text, rect)

    while running_menu:
        for event in pygame.event.get():
            if event.type == QUIT:
                running_menu = False

            if event.type == MOUSEBUTTONDOWN:
                for index, rect in enumerate(menu_rects):
                    if rect.collidepoint(event.pos):
                        selected_map = index

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    selected_map = (selected_map - 1) % len(options)
                elif event.key == K_DOWN:
                    selected_map = (selected_map + 1) % len(options)
                elif event.key == K_RETURN:
                    if selected_map == 0:  # Start Map 1
                        solve_map(selected_map)
                    elif selected_map == 1:  # Start Map 2
                        solve_map(selected_map)

        draw_menu()
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()