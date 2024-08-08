import pygame
import random

# 初始化Pygame
pygame.init()

# 屏幕大小
screen_width = 450
screen_height = 800
block_size = 40

# 计算游戏区域宽度和高度
play_width = screen_width
play_height = screen_height

# 顶部左上角位置
top_left_x = 0
top_left_y = 0

# 形状格式
shapes = [
    [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']],

    [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']],

    [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']],

    [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']],

    [['.....',
      '.....',
      '..00.',
      '..0..',
      '..0..'],
     ['.....',
      '.000.',
      '..0..',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '.000.',
      '.....',
      '.....']],

    [['.....',
      '.....',
      '.00..',
      '..0..',
      '..0..'],
     ['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....'],
     ['.....',
      '.000.',
      '..0..',
      '.....',
      '.....']],

    [['.....',
      '.....',
      '..0..',
      '.000.',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
]

# 形状颜色
shape_colors = [
    (0, 255, 0),
    (255, 0, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (0, 255, 255),
    (128, 0, 128)
]


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for _ in range(play_width // block_size)] for _ in range(play_height // block_size)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0], pos[1])

    return positions


def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(play_width // block_size) if grid[i][j] == (0, 0, 0)] for i in
                          range(play_height // block_size)]
    accepted_positions = [j for sub in accepted_positions for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    return Piece(play_width // (2 * block_size), 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    label = font.render(text, 1, color)

    surface.blit(label, (
    top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))


def draw_grid(surface, grid):
    pass  # 不再绘制网格线


def clear_rows(grid, locked):
    increment = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            increment += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if increment > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)
    return increment


def draw_next_shape(shape, surface):
    font = pygame.font.Font(pygame.font.get_default_font(), 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100

    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def draw_window(surface, grid, score=0, level=0):
    surface.fill((0, 0, 0))

    font = pygame.font.Font(pygame.font.get_default_font(), 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    font = pygame.font.Font(pygame.font.get_default_font(), 30)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))

    surface.blit(label, (top_left_x + 20, top_left_y + 20))

    label = font.render('Level: ' + str(level), 1, (255, 255, 255))
    surface.blit(label, (top_left_x + 20, top_left_y + 50))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)


def main(level):
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    score = 0
    lines_cleared = 0

    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.27 - (level * 0.02)

        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                if event.key == pygame.K_UP or event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                if event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            lines_cleared += clear_rows(grid, locked_positions)
            score += lines_cleared * 10
            if lines_cleared >= 5:
                level += 1
                lines_cleared = 0

        draw_window(win, grid, score, level)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    draw_text_middle("You Lost", 40, (255, 255, 255), win)
    pygame.display.update()
    pygame.time.delay(2000)


def level_selection():
    run = True
    selected_level = 0
    while run:
        win.fill((0, 0, 0))
        draw_text_middle('Select Level (1-9)', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_level = 1
                elif event.key == pygame.K_2:
                    selected_level = 2
                elif event.key == pygame.K_3:
                    selected_level = 3
                elif event.key == pygame.K_4:
                    selected_level = 4
                elif event.key == pygame.K_5:
                    selected_level = 5
                elif event.key == pygame.K_6:
                    selected_level = 6
                elif event.key == pygame.K_7:
                    selected_level = 7
                elif event.key == pygame.K_8:
                    selected_level = 8
                elif event.key == pygame.K_9:
                    selected_level = 9

                if selected_level > 0:
                    run = False
    return selected_level


def main_menu():
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle('Press Any Key To Play', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                level = level_selection()
                main(level)
    pygame.quit()


win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')
main_menu()
