import pygame
import random

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * GRID_WIDTH
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, RED, GREEN, BLUE, ORANGE]

class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def create_grid(locked_positions={}):
    grid = [[BLACK for x in range(GRID_WIDTH)] for x in range(GRID_HEIGHT)]
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

def draw_grid(surface, row, grid):
    sx = top_left_x
    sy = top_left_y
    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))  # vertical lines

def draw_tetromino(surface, tetromino):
    for i, row in enumerate(tetromino.shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, tetromino.color,
                                 ((tetromino.x + j) * BLOCK_SIZE,
                                  (tetromino.y + i) * BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE), 0)

def valid_move(tetromino, grid):
    for i, row in enumerate(tetromino.shape):
        for j, cell in enumerate(row):
            if cell:
                if (tetromino.x + j < 0 or tetromino.x + j >= GRID_WIDTH or
                    tetromino.y + i >= GRID_HEIGHT or
                    grid[tetromino.y + i][tetromino.x + j] != BLACK):
                    return False
    return True

def lock_tetromino(tetromino, grid):
    for i, row in enumerate(tetromino.shape):
        for j, cell in enumerate(row):
            if cell:
                grid[tetromino.y + i][tetromino.x + j] = tetromino.color
    return grid

def clear_rows(grid):
    full_rows = []
    for i in range(GRID_HEIGHT):
        if BLACK not in grid[i]:
            full_rows.append(i)
    for row in full_rows:
        del grid[row]
        grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
    return len(full_rows)

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (SCREEN_WIDTH/2 - (label.get_width()/2), SCREEN_HEIGHT/2 - (label.get_height()/2)))

def draw_score(surface, score):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render(f'Score: {score}', 1, WHITE)
    surface.blit(label, (SCREEN_WIDTH - 200, 10))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    grid = create_grid()
    current_piece = Tetromino(GRID_WIDTH // 2 - 1, 0, random.choice(SHAPES))
    next_piece = Tetromino(GRID_WIDTH // 2 - 1, 0, random.choice(SHAPES))

    fall_time = 0
    fall_speed = 0.5
    score = 0

    running = True
    game_over = False

    while running:
        if game_over:
            screen.fill(BLACK)
            draw_text_middle(screen, "Game Over", 40, WHITE)
            draw_score(screen, score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        main()
            continue

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_move(current_piece, grid):
                current_piece.y -= 1
                grid = lock_tetromino(current_piece, grid)
                score += clear_rows(grid) * 100
                current_piece = next_piece
                next_piece = Tetromino(GRID_WIDTH // 2 - 1, 0, random.choice(SHAPES))
                if not valid_move(current_piece, grid):
                    game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_move(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_move(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_move(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP or event.key == pygame.K_r:
                    current_piece.rotate()
                    if not valid_move(current_piece, grid):
                        current_piece.rotate()
                        current_piece.rotate()
                        current_piece.rotate()

        screen.fill(BLACK)
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                pygame.draw.rect(screen, grid[i][j], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
        for i in range(GRID_HEIGHT):
            pygame.draw.line(screen, WHITE, (0, i * BLOCK_SIZE), (SCREEN_WIDTH, i * BLOCK_SIZE))
        for j in range(GRID_WIDTH):
            pygame.draw.line(screen, WHITE, (j * BLOCK_SIZE, 0), (j * BLOCK_SIZE, SCREEN_HEIGHT))
        draw_tetromino(screen, current_piece)
        draw_score(screen, score)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
