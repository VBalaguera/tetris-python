import pygame  # first time using pygame, here we go
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS


S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
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

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# index 0 - 6 represent shape


class Piece(object):
    rows = 20
    columns = 10

    """represents different pieces"""

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    """uses two list: one of colors, another"""
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    # creating one list for each row; 20 list with 10 colors each;

    # we have to draw those blocks with locked position in the grid;
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    """every time we rotate each shape, it changes the shape itself too"""
    positions = []
    # base on these positions, we make modifications
    format = shape.shape[shape.rotation % len(shape.shape)]
    # shape index defines which shape we get

    #
    for i, line in enumerate(format):  # todo; study this
        row = list(line)
        for j, column in enumerate(row):
            # looping through every line
            if column == '0':
                # if a 0 exists in any position, we add it to that position, adjusting said position with x and y values
                positions.append((shape.x + j, shape.y + i))
                # however, we need to remove those ... in the shapes, how to?

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
        # with this, we offset ... values, and move everything to the left and up, solving the problem I just wrote above

    return positions


def valid_space(shape, grid):
    """checking the grid if we're moving into a valid space"""
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    # all available positions
    # (0, 0, 0) is an empty position, thus available
    # [(0,1), (2, 3)] => [(0, 1), (2, 3)]
    # converting it to a one dimensional list:
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)
    # a list like [(), ()]

    for pos in formatted:
        # checking if pos exists in valid positions
        if pos not in accepted_pos:
            if pos[1] > -1:  # negative values here equal unvalid pos
                return False
    return True


def check_lost(positions):
    """checking if any of the pos are above the screen, hitting it will result in a game over"""
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    """chooses the next piece to show"""
    return Piece(5, 0, random.choice(shapes))
    # x value is 5, y value is 0


def draw_text_middle(surface, text, size, color, ):
    """draws welcome text in the middle of the screen"""
    font = pygame.font.SysFont('Arial', size, bold=True)  # todo, study this
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width / 2 -
                         (label.get_width() / 2), top_left_y + play_height / 2 -
                         label.get_height() / 2))


def draw_grid(surface, grid):
    """ shows grid structure with grey squares"""
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):  # how many rows?
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        # where/color/starting position/ending position
        for j in range(len(grid[i])):  # how many colums per row?
            # drawing horizontal lines
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))


def clear_rows(grid, locked):  # todo: study this ASAP
    """clears rows"""
    inc = 0  # increment
    for i in range(len(grid) - 1, -1, -1):  # loops through the grid backwards
        row = grid[i]
        if (0, 0, 0) not in row:  # no black squares in the row, complete!
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]  # delete these locked positions!
                except:
                    continue

    # shifting rows positions:
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            # for every key in the list of locked positions based on y value:
            # [(0, 1), (0, 0)]
            # make it look like this:
            # [(0,0) (0,1)]

            x, y = key
            if y < ind:
                # if y is above the current index of the removed row
                # only things above are going to move
                newKey = (x, y + inc)  # getting a new key by adding the inc
                # inc sums 1 when a row is deleted in each loop;
                # deleting one row at a time will add 1, 2 if we deleted 2, and so on
                locked[newKey] = locked.pop(key)  # creating a new key in locked

    return inc  # inc: number of rows to calculate score!


def draw_next_shape(shape, surface):
    """draws next shape"""
    # todo: make this prettier
    # gets all shapes list, turns it into pos
    font = pygame.font.SysFont('Arial', 30)
    label = font.render('next shape', 1, (255, 255, 255))  # 1 is for antialiasing

    sx = top_left_x + play_width + 50  # + 50 moves to the right
    sy = top_left_y + play_height / 2 - 100  # - 100 moves it to the left
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                # draws a static image, nothing else
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * block_size, sy + i * block_size,
                                  block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def update_score(nscore):  # todo: study this!
    """"""
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))
        # .strip() is for removing backslash ends!

def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
        # .strip() is for removing backslash ends!
    return score

def draw_window(surface, grid, score=0, last_score = 0):
    surface.fill((0, 0, 0))  # black
    pygame.font.init()  # setting up font and using it

    font = pygame.font.SysFont('Arial', 50)  # todo: change this into something better
    label = font.render('tetris', 1, (255, 255, 255))  # 1 is for antialiasing

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))  # centering position;

    # drawing the score: todo: make this prettier;
    font = pygame.font.SysFont('Arial', 30)
    label = font.render('score:' + str(score), 1, (255, 255, 255))  # 1 is for antialiasing

    sx = top_left_x + play_width + 50  # + 50 moves to the right
    sy = top_left_y + play_height / 2 - 100  # - 100 moves it to the left

    surface.blit(label, (sx + 10, sy + 120))

    # high score:
    font = pygame.font.SysFont('Arial', 30)
    label = font.render('high score:' + str(last_score), 1, (255, 255, 255))  # 1 is for antialiasing

    sx = top_left_x - 200
    sy = top_left_y + 200

    surface.blit(label, (sx + 10, sy + 120))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size,
                                                   top_left_y + i * block_size,
                                                   block_size, block_size), 0)

    # red rectangule:
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(surface, grid)

    # pygame.display.update()


def main(win):
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    # variables
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    # speed-settings
    fall_speed = 0.27

    # make piece moving faster:
    level_time = 0

    score = 0 # TODO: FIX THIS PROBLEM, EVERY TIME

    while run:

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        # tracks falling position by adding amounts of time while main is running

        level_time += clock.get_rawtime()
        clock.tick()  # ticks each this loop runs, adding time

        if level_time / 1000 > 10:  # every 5 secs we increase speed
            level_time = 0
            if fall_speed > 0.12:  # this number changes playability
                fall_speed -= 0.005  # this can be changed to

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1  # moving pieces automatically
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:  # not at the top os fhte screen
                current_piece.y -= 1
                change_piece = True  # this sets the landing of the shape, locks its position, and throws a new shape

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # CONTROLS here
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1  # on the x axis
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1

                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1  # moving right

                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1

                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    # change rotation means changing shape, how to?
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)  # check all pos when moving down

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:  # not above the screen
                grid[y][x] = current_piece.color  # getting a different color

        if change_piece:  # updating locked_positions
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
                # [(1, 2): (255, 0, 0)] # positions + color with rgb values
                # when we pass locked positions into the grid,
                # we can get each of them in the grid and update their colors;
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            score = clear_rows(grid, locked_positions) * 10
            # this can be personalized

        # draws next shape:

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, 'You lost!', 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(2000)  # after 2 seconds it goes to the main screen
            run = False
            update_score(score)


def main_menu(win):

    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, 'press any key to play', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            # pressing any keys, we go to the game!
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('tetris')
main_menu(win)  # start game
