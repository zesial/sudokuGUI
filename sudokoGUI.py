import pygame
import time

board = [  # use of this grid
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

FPS = 10  # screen refresh rate
width = 540  # this is screen width
height = 600  # height
WHITE = (255, 255, 255)  # colours
BLACK = (0, 0, 0,)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
startTime = time.time()  # this is used to store game starting time


def format_time(secs):  # this function convert sec in to min and round up sec
    sec = secs % 60
    minute = secs // 60
    mat = " " + str(minute) + ":" + str(sec)
    return mat


def drawClock():
    pygame.draw.line(screen, BLACK, (0, width), (width, width))
    font = pygame.font.Font('freesansbold.ttf', 40)
    timeInSec = round(time.time() - startTime)
    TIME = font.render("Time :" + format_time(timeInSec), True, BLACK)
    screen.blit(TIME, (325, 555))


def drawGrid():                                              # draw all grid and clock
    cellSize = int(width / 9)                                # cell 1/9 0f width
    blockSize = int(540 / 3)                                 # block
    for x in range(0, width, cellSize):                      # light gray lines are drawn
        pygame.draw.line(screen, GRAY, (x, 0), (x, width))   # draw method is used
    for x in range(0, width, blockSize):                     # line where to draw , colour,
        pygame.draw.line(screen, BLACK, (x, 0), (x, width))  # staring coordinates,end coordinates
    for y in range(0, width, cellSize):
        pygame.draw.line(screen, GRAY, (0, y), (width, y))
    for y in range(0, width, blockSize):
        pygame.draw.line(screen, BLACK, (0, y), (width, y))
    drawClock()
    fillBoard(board)


def fillBoard(grid):  # this function fills board with number in our board matrix
    font = pygame.font.Font('freesansbold.ttf',62)  # here a method font is used to use to make a variable ( it is just syntax thing )
    blank = '  '                                    # here this is used to put a space at places where there is nothing (zero)
    for i in range(len(grid)):                      # standard double loop
        for j in range(len(grid[0])):
            num = str(grid[i][j])                   # here converting int into str because a method render and blit only take str
            if grid[i][j] == 0:                     # checking if it is zero than putting blank
                num = blank
            text = font.render(num, True, BLACK)    # rendering num str into required "image" format
            x = j * 60 + 10                         # this coordinate are of upper left corner and extra 10 is added for cosmetic reasons
            y = i * 60
            pos = (x, y)                            # making it list kind of useless step
            screen.blit(text, pos)                  # method blit is used to draw image "text"


def cellNumFinder(pos):                  # this method is used to convert position of mouse in to cell num in matrix
    if pos[1] < 540:                     # check that mouse is not clicked on lower clock region
        x = pos[1] // 60                 # // represent integer division
        y = pos[0] // 60                 #
        return x, y                      #
    else:                                #
        return None                    # returning None to specify that mouse clicked on wrong place


def makeItRed(cell_num,key):                                # mark the selected cell with red border and fill temp key
    if board[cell_num[0]][cell_num[1]] == 0:                # only cell with zero in it are selected
        x1 = cell_num[1] * 60                               # marking upper left and lower right coordinates
        x2 = x1 + 60
        y1 = cell_num[0] * 60
        y2 = y1 + 60
        pygame.draw.line(screen, RED, (x1, y1), (x1, y2))
        pygame.draw.line(screen, RED, (x1, y1), (x2, y1))
        pygame.draw.line(screen, RED, (x1, y2), (x2, y2))
        pygame.draw.line(screen, RED, (x2, y1), (x2, y2))

        if key:
            font = pygame.font.Font('freesansbold.ttf', 62)
            text = font.render( str(key), True, GRAY)
            screen.blit(text, (x1+10, y1))


# below is backtracking implementation of sudoko solver


def solver(bo):                          # recursive solution of problem
    find = findZero(bo)                  # find zero and return them in to find tuple
    if find is None:                     # if none then we have find solution
        return True
    for k in range(1, 10):               # checking what can be filled
        if isValid(bo, k, find):         # is this move valid
            bo[find[0]][find[1]] = k     # filling that number
            if solver(bo):               # if this give solution then it okay
                return True
            bo[find[0]][find[1]] = 0     # otherwise try it again

    return False                         # return that no solution exit


def solverSpecial(grid, position, key):       # driver function to check that a num at a position will give solution
    rows, cols = (9, 9)                       # making new matrix
    arr = []
    for i in range(cols):
        col = []
        for j in range(rows):
            col.append(0)
        arr.append(col)

    for i in range(0, 9):
        for j in range(0, 9):
            arr[i][j] = grid[i][j]            # copying original matrix

    arr[position[0]][position[1]] = key       # putting key

    return solver(arr)                        # returning if solution exit


def findZero(bo):                       # find zero in matrix
    for rowZ in range(0, 9):
        for colZ in range(0, 9):
            if bo[rowZ][colZ] == 0:
                return rowZ, colZ
    return None


def isValid(bo, num, pos):               # check that it is valid to put num at this pos
    row = pos[0]
    col = pos[1]
    if bo[row][col] != 0:
        return False

    for i in range(0, 9):
        if bo[i][col] == num:
            return False

    for j in range(0, 9):
        if bo[row][j] == num:
            return False

    row = row - row % 3                  # now check that no same element is in box
    col = col - col % 3                  # getting the upper left coordinates of box

    for i in range(0, 3):
        for j in range(0, 3):
            if num == bo[i + row][j + col]: # checking in it
                return False

    return True


def specialEffect():
    solver(board)

def main():
    global fps    # variable used to access refresh rate of screen
    global screen # variable used to access screen

    pygame.init()                                       # used to initialise pygame lib
    fps = pygame.time.Clock()                           # method to access the required functionality
    screen = pygame.display.set_mode((width, height))   # method use to set screen size
    pygame.display.set_caption('Sudoko')

    run = True                                          # show that game is running
    isItRed = False                                     # show that cell is selected
    cellNum = None                                      # selected cell coordinates
    key = 0                                             # value of that cell

    while run:                                          # most imp loop which make screen stable
        screen.fill(WHITE)                              # fill color on screen
        drawGrid()
        for event in pygame.event.get():                # checking input or whatever is happening
            if event.type == pygame.QUIT:               # check if ordered to quit
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:    # mouse is clicked
                pos = pygame.mouse.get_pos()
                cellNum = cellNumFinder(pos)
                isItRed = False
                if cellNum and board[cellNum[0]][cellNum[1]] == 0:
                    isItRed = True

            if event.type == pygame.KEYDOWN:            # any button is pressed
                if event.key == pygame.K_SPACE:         # this will solve board instantaneously
                    specialEffect()
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9

                if event.key == pygame.K_RETURN:                 # make an entry of key
                    if isItRed and key:                          # check valid cell is selected and a key is given
                        if solverSpecial(board, cellNum, key):   # solve the matrix
                            board[cellNum[0]][cellNum[1]] = key  # if it is solvable with this entry
                            printBoard(board)
                        else:
                            print('test')                        # used for debugging
                    key = None

        if isItRed:
            makeItRed(cellNum, key)

        pygame.display.update()  # update display
        fps.tick(FPS)


def printBoard(boi):  # used as debugging tool, has no purpose in code
    print('')
    for i in range(0, 9):
        for j in range(0, 9):
            print(boi[i][j], end=' ')
        print('')


if __name__ == '__main__':
    main()
