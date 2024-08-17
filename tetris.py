import pygame
import random

'Initializes all imported game modules'
pygame.init()

'Global Variables'

gameOverImage = pygame.image.load("GameOverScreen.jpeg")
countClear = 0

'Define colors'
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 100, 100)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

'This sets the WIDTH and HEIGHT of each grid location'
WIDTH = 20
HEIGHT = 20

'This sets the margin between each cell'
MARGIN = 1

'''
These 2d lists represents the Tetromino pieces in their basic state.
Since we're using an array backed list, we need to have data that
can be modified. All the 1's are the Tetromino pieces represented as strings.
Inspired by other Tetris examples: https://www.thepythoncode.com/article/create-a-tetris-game-with-pygame-in-python,  https://www.techwithtim.net/tutorials/game-development-with-python/tetris-pygame/tutorial-3
'
'''
S = [['.....',
    '......',
    '..OO..',
    '.OO...',
    '.....'],
    ['.....',
    '..O..',
    '..OO.',
    '...O.',
    '.....']]

Z = [['.....',
    '.....',
    '.OO..',
    '..OO.',
    '.....'],
    ['.....',
    '..O..',
    '.OO..',
    '.O...',
    '.....']]

I = [['..O..',
    '..O..',
    '..O..',
    '..O..',
    '.....'],
    ['.....',
    'OOOO.',
    '.....',
    '.....',
    '.....']]

O = [['.....',
    '.....',
    '.OO..',
    '.OO..',
    '.....']]

J = [['.....',
    '.O...',
    '.OOO.',
    '.....',
    '.....'],
    ['.....',
    '..OO.',
    '..O..',
    '..O..',
    '.....'],
    ['.....',
    '.....',
    '.OOO.',
    '...O.',
    '.....'],
    ['.....',
    '..O..',
    '..O..',
    '.OO..',
    '.....']]

L = [['.....',
    '...O.',
    '.OOO.',
    '.....',
    '.....'],
    ['.....',
    '..O..',
    '..O..',
    '..OO.',
    '.....'],
    ['.....',
    '.....',
    '.OOO.',
    '.O...',
    '.....'],
    ['.....',
    '.OO..',
    '..O..',
    '..O..',
    '.....']]

T = [['.....',
    '..O..',
    '.OOO.',
    '.....',
    '.....'],
    ['.....',
    '..O..',
    '..OO.',
    '..O..',
    '.....'],
    ['.....',
    '.....',
    '.OOO.',
    '..O..',
    '.....'],
    ['.....',
    '..O..',
    '.OO..',
    '..O..',
    '.....']]

'Creates a list of shapes along with the color associated with them.'
shapes = [S, Z, I, O, J, L, T]
shapeColors = [GREEN, RED, CYAN, YELLOW, ORANGE, BLUE, PURPLE]

'''
The Tetromino class stores all the data in a piece.
'''
class Tetromino:
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shapeColors[shapes.index(shape)]
        self.rotation = 0

'''
The Tetris class is the game itself, all of the functions in the game
are in this class.
'''
class Tetris:

    '''
    Initializes the game, sets the columns and rows, and gets a shape, the next shape and gameOver status.
    Initializes a dictionary. The purpose of the dictionary is to assign gridboxes
    to the color of the shape.
    '''
    def __init__(self):
        self.lockedPosition = {}
        self.x = 10
        self.y = 20
        self.grid = self.createBoard()
        self.currentShape = self.getShape()
        self.nextShape = self.getShape()
        self.gameOver = False

    "Gives a random shape and spawns it at the top of the board."
    def getShape(self):
            return Tetromino(3, 0, random.choice(shapes))

    '''
    Creates an array-backed grid, so this array will have a list of 20 lists and
    have 10 elements within those lists.
    Locked position is a dictionary that allows elements on a board to have an assigned color.
    Code from: http://programarcadegames.com/index.php?lang=en&chapter=array_backed_grids
    '''
    def createBoard(self):
        grid = []
        for row in range(20):
            # Add an empty array that will hold each cell
            # in this row
            grid.append([])
            for column in range(10):
                grid[row].append(0)  # Append a cell

        return grid
    
    '''
    Draws the all the gridboxes.
    '''
    def drawBoard(self, screen):
        for row in range(20):
            for column in range(10):
                color = WHITE
                if (column, row) in self.lockedPosition:
                    color = self.lockedPosition[(column, row)]
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])
    
    '''
    Draws the shape on the board based on the shape list.
    Help from Tom Finzell.
    '''
    def drawShape(self, screen):
            pattern = self.currentShape.shape[self.currentShape.rotation % len(self.currentShape.shape)]
            for i in range(len(pattern)):
                rowPattern = pattern[i]

                for j, letter in enumerate(rowPattern):
                    if letter == 'O':
                         pygame.draw.rect(screen, self.currentShape.color, [(MARGIN + WIDTH) * (j + self.currentShape.x) + MARGIN,
                               (MARGIN + HEIGHT) * (i + self.currentShape.y) + MARGIN,
                               WIDTH, HEIGHT])
                         
    "Draws next shape on the screen."
    def drawNextShape(self, screen):
        font = pygame.font.SysFont('Georgia', 15)
        nextShapeText = font.render("Next Shape:", True, WHITE)
        nextShape = self.nextShape.shape[self.nextShape.rotation % len(self.nextShape.shape)]
        for i in range(len(nextShape)):
            rowPattern = nextShape[i]
            for j, letter in enumerate(rowPattern):
                if letter == 'O':
                     pygame.draw.rect(screen, self.nextShape.color, [(MARGIN + WIDTH) * (j + self.nextShape.x) + 160,
                            (MARGIN + HEIGHT) * (i + self.nextShape.y) + 60,
                            WIDTH, HEIGHT])

        screen.blit(nextShapeText, [225,40])

    '''
    Checks if a piece can move into the space. Returns a boolean.
    Inspired from: https://www.thepythoncode.com/article/create-a-tetris-game-with-pygame-in-python
    '''
    def openSpace(self, piece, x, y, rotation):
        for i, row in enumerate(piece.shape[(piece.rotation + rotation) % len(piece.shape)]):
            for j, column in enumerate(row):
                try:
                    if column == 'O':
                        new_x = piece.x + j + x
                        new_y = piece.y + i + y
                        if not (0 <= new_x < 10 and 0 <= new_y < 20):
                            return False
                        if self.grid[new_y][new_x] != 0:
                            return False
                except IndexError:
                    return False
        return True
    
    '''
    If there isn't a valid place, we change the color of the grid box which "locks" the piece in.
    Inspired from: https://www.thepythoncode.com/article/create-a-tetris-game-with-pygame-in-python
    '''
    def lockPiece(self, piece):
            for i, row in enumerate(piece.shape[piece.rotation % len(piece.shape)]):
                for j, cell in enumerate(row):
                    if cell == 'O':
                        newX = piece.x + j
                        newY = piece.y + i
                        self.lockedPosition[(newX,newY)] = piece.color
                        self.grid[newY][newX] = piece.color  # Update the grid with the locked piece color

    '''
    Clears the lines if a row is filled.
    Recieved help from Kaitlyn Peterson and classmates.
    '''
    def clearLine(self):
        maxRow = -1
        linesToClear = []
        global countClear
        for row in range(20):
            allFilled = True
            for cell in self.grid[row]:
                if cell == 0:
                    allFilled = False
            if allFilled:
                if row > maxRow:
                    maxRow = row
                linesToClear.append(row)
                for row in sorted(linesToClear, reverse=True):
                    del self.grid[row]
                    countClear+=1

                for _ in range(len(linesToClear)):
                    self.grid.insert(0, [0] * 10)

                new_locked_position = {}
                for col in range(10):
                    for row in range(20):
                        if (col, row) in self.lockedPosition:
                            if row not in linesToClear and maxRow > row:
                                new_locked_position[(col, row + len(linesToClear))] = self.lockedPosition[(col, row)]
                            elif row not in linesToClear and maxRow < row:
                                new_locked_position[(col, row)] = self.lockedPosition[(col, row)]

                self.lockedPosition = new_locked_position

    '''
    Updates the status of the game
    Moves the pieces down, locks pieces, updates shapes, clears lines, 
    and checking if the game is over
    '''
    def updateShape(self):
        if not self.gameOver:
            if self.openSpace(self.currentShape,0,1,0):
                self.currentShape.y += 1
            else:
                self.lockPiece(self.currentShape)
                self.currentShape = self.nextShape
                self.nextShape = self.getShape()
            self.clearLine()
        if not self.openSpace(self.currentShape, 0,0,0):
                self.gameOver = True

    

'''
Creates the scoring system.
'''
def gameScore(screen):
    totalGameScore = countClear*100
    font = pygame.font.SysFont('Georgia', 30)
    totalScore = str(totalGameScore)
    scoreText = font.render("Score", True, WHITE)
    scoreNum = font.render(totalScore, True, WHITE)
    screen.blit(scoreText,[230,160])
    screen.blit(scoreNum, [230,200])

'''
Creates the game over screen.
'''
def gameOver(screen):
        font = pygame.font.SysFont('Georgia', 30)
        text = font.render('Game Over!', True, WHITE)
        font = pygame.font.SysFont('Georgia', 20)
        startOverText = font.render('Press Spacebar To Start Over!', True, RED)
        screen.blit(gameOverImage,(-50,0))
        screen.blit(text, (85, 180))
        screen.blit(startOverText, (37, 225))
        pygame.mixer.music.stop()

'''
Starts the game again.
'''
def startOver():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        main()

'Driver function that includes the game loop and creates the frontend aspects of the game'
def main():
    global countClear
    countClear = 0
    pygame.mixer.music.load('01. Title.wav')
    pygame.mixer.music.play(-1)
    'Creates an instance of Tetris'
    game = Tetris()
    'Set the HEIGHT and WIDTH of the screen'
    WINDOW_SIZE = [320, 420]

    screen = pygame.display.set_mode(WINDOW_SIZE)
    # Set title of screen
    pygame.display.set_caption("Tetris")
    fallTime = 0
    fallSpeed = 100

    # Loop until the user clicks the close button.
    running = True

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while running:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                running = False  # Flag that we are done so we exit this loop
                pygame.quit()
                quit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                if game.openSpace(game.currentShape, 1, 0, 0):
                    game.currentShape.x += 1
            if keys[pygame.K_LEFT]:
                if game.openSpace(game.currentShape, -1, 0, 0):
                    game.currentShape.x -= 1
            if keys[pygame.K_DOWN]:
                if game.openSpace(game.currentShape, 0, 1, 0):
                    game.currentShape.y += 1
            if keys[pygame.K_UP]:
                if game.openSpace(game.currentShape, 0, 0 ,1):
                    game.currentShape.rotation += 1

        '''
        Copied code from: https://www.thepythoncode.com/article/create-a-tetris-game-with-pygame-in-python
        to create the fall time and fall speed of the blocks
        '''
        # Get the number of milliseconds since the last frame
        deltaTime = clock.get_rawtime()
        # Add the delta time to the fall time
        fallTime += deltaTime
        if fallTime >= fallSpeed:
            # Move the piece down
            game.updateShape()
            # Reset the fall time
            fallTime = 0
        # Set the screen background
        screen.fill(BLACK)
        '# Draws all of the frontend aspects of the game while it runs'
        game.drawBoard(screen)
        game.drawNextShape(screen)
        game.drawShape(screen)
        gameScore(screen)
        'Always checking for a game over and starts over when spacebar is pressed'
        if game.gameOver:
            gameOver(screen)
            startOver()
        pygame.display.flip()

        'Sets the frames'
        clock.tick(60)

"Runs the game."
main()