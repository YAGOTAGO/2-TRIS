from random import randint
import pygame
import Players
from Players import MainMenuP1, MainMenuP2, sidePlayer, bottomPlayer
import BulletLogic

#GAME CONSTANTS
WIDTH  = 400
HEIGHT = 650
FPS = 60
game = None

#Initializes the pygame engine
pygame.init()

#display vars
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2-Tris")
pygame.display.set_icon(pygame.image.load("img\Dandy_Icon.png").convert_alpha())

#background
backgroundImg = pygame.image.load("img\Game Board Window.png").convert_alpha()
boardImg = pygame.image.load("img\TetrisBoard.png").convert_alpha()

#Main Menu background images
mainMenuBG = pygame.image.load("img\MainMenuBG.png").convert_alpha()
playButtonImg = pygame.image.load("img\MainMenu\PlayButton.png").convert_alpha()
playButtonRect = playButtonImg.get_rect(center = (WIDTH/2,300))

#Quit
quitButton = pygame.image.load("img\MainMenu\QuitButton.png").convert_alpha()
quitButtonRect = quitButton.get_rect(center = (WIDTH/2, 500))

#Credits
creditsButton = pygame.image.load("img\MainMenu\CreditsButton.png").convert_alpha()
creditsButtonRect = creditsButton.get_rect(center = (WIDTH/2, 400))

#Title
titleImg = pygame.image.load("img\MainMenu\Title.png").convert_alpha()
titleRect = titleImg.get_rect(center = (WIDTH/2, 100))

#Help
helpButton = pygame.image.load("img\MainMenu\HelpButton.png").convert_alpha()
helpButtonRect = helpButton.get_rect(center = (WIDTH-50, 50))

#help menu
HowToPlayImg = pygame.image.load("img\HelpMenu\HowToPlay.png").convert_alpha()
HowToPlayRect = HowToPlayImg.get_rect(topleft = (0,0))

#back button help menu
backButHelp = pygame.image.load("img\HelpMenu\X.png").convert_alpha()
backButHelpRect = backButHelp.get_rect(center = (WIDTH-50,50))

#Credits
creditsBG = pygame.image.load("img\Credits.png").convert_alpha()
creditsRect = creditsBG.get_rect(topleft = (0,0))

#Restart
RestartImg = pygame.image.load("img\Restart.png").convert_alpha()
RestartRect = RestartImg.get_rect(center = (WIDTH/2, 650))

#Main Menu Button
MainMenuButton = pygame.image.load("img\MainMenu.png").convert_alpha()
MainMenuRect = MainMenuButton.get_rect(center = (WIDTH/2, 450))

#Game Over vars
gameOverBG = pygame.image.load("img\Game Over.png").convert_alpha()
gameGoing = True

#game engine movement vars
COOLDOWN = 30

#piece logic
moveLeft = False
moveRight = False
turnPiece = False

#Player groups for drawing and movement
p1MenuGroup = pygame.sprite.GroupSingle()
p2MenuGroup = pygame.sprite.GroupSingle()
p1Menu = MainMenuP1(150, 200, pygame.image.load("img\player1.png").convert_alpha())
p2Menu = MainMenuP2(250, 200, pygame.image.load("img\player2.png").convert_alpha())
p1MenuGroup.add(p1Menu)
p2MenuGroup.add(p2Menu)
player2Group = pygame.sprite.GroupSingle()
player1Group = pygame.sprite.GroupSingle()

#Board array and tile mappings
boardArr = [[-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
             [1,1,1,1,1,1,1,1,1,1,1,1]]

#Arrays for pieces and orienations
longPiece  = [[2, 6, 10, 14], [4, 5, 6, 7]]
cube = [[0,1,4,5]]
tPiece = [[2, 5, 6,10], [5, 6, 7, 10], [2, 6, 10, 7], [2, 5, 6, 7]]
lPiece = [[1, 5, 9, 10], [6, 8, 9, 10], [0, 1, 5,9], [4, 5, 6, 8]]
sPiece = [[1, 5, 6, 10], [8, 9, 5, 6]]

#Array holding all tiles and rotations
pieceArray = [longPiece, cube, tPiece, lPiece, sPiece]

def ResetBoard():
    global boardArr
    boardArr = [[-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
            [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1],
             [1,1,1,1,1,1,1,1,1,1,1,1]]


#returns img from 0 - 20
def randBlockImage(i):
    if i ==0:
        return pygame.image.load("Tetris Cubes Final\Blue_Cat.png").convert_alpha()
    elif i ==1:
        return pygame.image.load("Tetris Cubes Final\Blue_Dandy.png").convert_alpha()
    elif i == 2:
        return pygame.image.load("Tetris Cubes Final\Blue_Dog.png").convert_alpha()
    elif i ==3:
        return pygame.image.load("Tetris Cubes Final\Cyan_Cat.png").convert_alpha()
    elif i ==4:
        return pygame.image.load("Tetris Cubes Final\Cyan_Dandy.png").convert_alpha()
    elif i ==5:
        return pygame.image.load("Tetris Cubes Final\Cyan_Dog.png").convert_alpha()
    elif i ==6:
        return pygame.image.load("Tetris Cubes Final\Green_Cat.png").convert_alpha()
    elif i ==7:
        return pygame.image.load("Tetris Cubes Final\Green_Dandy.png").convert_alpha()
    elif i == 8:
        return pygame.image.load("Tetris Cubes Final\Green_Dog.png").convert_alpha()
    elif i ==9:
        return pygame.image.load("Tetris Cubes Final\Orange_Cat.png").convert_alpha()
    elif i ==10:
        return pygame.image.load("Tetris Cubes Final\Orange_Dandy.png").convert_alpha()
    elif i ==11:
        return pygame.image.load("Tetris Cubes Final\Orange_Dog.png").convert_alpha()
    elif i ==12:
        return pygame.image.load("Tetris Cubes Final\Pink_Cat.png").convert_alpha()
    elif i ==13:
        return pygame.image.load("Tetris Cubes Final\Pink_Dandy.png").convert_alpha()
    elif i ==14:
        return pygame.image.load("Tetris Cubes Final\Pink_Dog.png").convert_alpha()
    elif i ==15:
        return pygame.image.load("Tetris Cubes Final\Red_Cat.png").convert_alpha()
    elif i ==16:
        return pygame.image.load("Tetris Cubes Final\Red_Dandy.png").convert_alpha()
    elif i ==17:
        return pygame.image.load("Tetris Cubes Final\Red_Dog.png").convert_alpha()
    elif i==18:
        return pygame.image.load("Tetris Cubes Final\Yellow_Cat.png").convert_alpha()
    elif i ==19:
        return pygame.image.load("Tetris Cubes Final\Yellow_Dandy.png").convert_alpha()
    elif i ==20:
        return pygame.image.load("Tetris Cubes Final\Yellow_Dog.png").convert_alpha()


def GameOverEventLoop():
    
    if pygame.Rect.colliderect(p1Menu.rect, MainMenuRect):
        if pygame.Rect.colliderect(p2Menu.rect, MainMenuRect):
            p1Menu.rect.y = 100
            p2Menu.rect.y = 100
            pygame.mixer.music.stop()
            pygame.mixer.music.load('music\MenuMusic.mp3')
            pygame.mixer.music.play(-1)
            MainMenu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            exit()
        if event.type == pygame.KEYDOWN:
            
            #move using wasd
            if event.key == pygame.K_w:
                Players.pUp = True
                
            if event.key == pygame.K_s:
                Players.pDown = True
            
            if event.key == pygame.K_a:
                Players.pLeft = True
            
            if event.key == pygame.K_d:
                Players.pRight = True

            #move using arrow keys
            if event.key == pygame.K_UP:
                Players.p2Up = True
            
            if event.key == pygame.K_DOWN:
                Players.p2Down = True
            
            if event.key == pygame.K_LEFT:
                Players.p2Left = True
            
            if event.key == pygame.K_RIGHT:
                Players.p2Right = True

        if event.type == pygame.KEYUP:
            #move using wasd
            if event.key == pygame.K_w:
                Players.pUp = False
            if event.key == pygame.K_s:
                Players.pDown = False
            if event.key == pygame.K_a:
                Players.pLeft = False
            if event.key == pygame.K_d:
                Players.pRight = False

            #move using arrow keys
            if event.key == pygame.K_UP:
                Players.p2Up = False
            if event.key == pygame.K_DOWN:
                Players.p2Down = False
            if event.key == pygame.K_LEFT:
               Players.p2Left = False
            if event.key == pygame.K_RIGHT:
                Players.p2Right = False
    
#Function to trigger game over screen
def GameOver():
    global game
    del game

    while True:
        GameOverEventLoop()

        screen.blit(gameOverBG, (0,0))

        screen.blit(MainMenuButton, MainMenuRect)

        p1MenuGroup.update()
        p1MenuGroup.draw(screen)
    
        p2MenuGroup.update()
        p2MenuGroup.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

#Creates a piece class for the current falling piece
class Piece():
    global boardArr, COOLDOWN
    def __init__(self):

        #pos
        self.col = 4
        self.row = 0
        
        #rand img and color
        self.color = randint(0,20)
        self.sprite = randBlockImage(randint(0,20))
        
        self.type = randint(0, 4)
        self.shape = pieceArray[self.type]
        self.rotation = randint(0, len(self.shape) - 1)
        self.shape = pieceArray[self.type][self.rotation]
        self.img = []
        self.rect = []
        self.movePiece()
    
    def ReturnTuple(self):
        return pieceArray[self.type][self.rotation]

    #Creates new images and rects based on cur position
    def movePiece(self):
        self.img = []
        self.rect = []
        self.pixelArr = []

        index = 0
        for width in range(4):
            for height in range(4):
                if(width * 4 + height in self.shape):  
                    self.img.append(self.sprite)
                    self.rect.append(self.img[index].get_rect(topleft = (20 + (30 * height + 30 * self.col), (30 * width + 30 * self.row))))
                    self.pixelArr.append(Pixel(self.img[index], self.rect[index]))
                    index += 1
                    
    #Update function for self
    def update(self):
        self.movePiece()

#Class for storing individual square data
class Pixel():
    #Holds image and rect data for a single square
    def __init__(self, image, rect):
        self.rect = rect
        self.image = image

    def drawPixel(self):
        screen.blit(self.image, self.rect) 
       
#Class that manages the 2-tris game logic
class GameEngine():

    def __init__(self):
        self.curPiece = Piece()
        ResetBoard()
        self.board = boardArr
        self.collide()
        self.rightMoveCD = 15
        self.leftMoveCD = self.rightMoveCD
        self.upMoveCD = self.rightMoveCD


    #Gets a new random piece after the current piece has been placed
    def nextPiece(self):
        self.curPiece = Piece()

    #Checks for collisions with the current piece
    def collide(self):
        for width in range(4):
            for height in range(4):
                if(width * 4 + height in self.curPiece.ReturnTuple()):  #get tiles in the cur piece array
                    if(self.board[self.curPiece.row + width][self.curPiece.col + height] != ' ' and self.board[self.curPiece.row + width][self.curPiece.col + height] != -1):
                        return True #there is a collision
        return False

    #Alters the entries in the board at the current pieces location to the given char
    def changeBoardAtPiece(self, char):
        for width in range(4):
            for height in range(4):
                if(width * 4 + height in self.curPiece.ReturnTuple()):  
                    self.board[self.curPiece.row + width][self.curPiece.col + height] = char

    #Clears any full rows and updates the boardArr
    def clearRows(self):
        global COOLDOWN
        rowsRemoved = 0
        rowIndex = 0
        size = 19   #Number of rows - 1
        while rowIndex <= size:
            tmp = 0
            #Count how many non-int elements are in the row
            for elem in self.board[rowIndex]:
                if(isinstance(elem, int)):
                    tmp+= 1

            #If there are 12 numbers (row is full and should be cleared)
            if tmp == 12:
                if(COOLDOWN >= 10):
                    COOLDOWN -= 2
                self.board.pop(rowIndex)
                rowIndex-= 1
                size-=1
                rowsRemoved += 1

            rowIndex += 1

        #Adds back a copy of a clean row for the number of removed rows
        for i in range(rowsRemoved):
            self.board.insert(0, [-1,' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',-1])
            
    #Updates the position of the falling tile based on an outside call in the game loop
    def fall(self):

        global gameGoing, game
        #Reset past location with 0's to clear the board
        self.changeBoardAtPiece(' ')

        #Try advancing by one row
        self.curPiece.row += 1

        #If the piece collides with the bottom or another piece, turn it to 1's and get a new piece
        if(self.collide()):
            self.curPiece.row -= 1
            self.changeBoardAtPiece(self.curPiece.color)
            self.nextPiece()

            #call function for clearing rows here
            self.clearRows()
            if(self.collide()):
                gameGoing = False
                
                
        #Update the current falling pieces representation on the board with 'x'
        self.changeBoardAtPiece('x')
        self.curPiece.update()
    
    #Moves the falling tile based on user input in the game loop
    def moveTile(self):
        global moveLeft, moveRight

        modList = []
        for num in self.curPiece.shape:
            modList.append(num%4)

        #Side buffers to offset the shape logic
        maxElem = max(modList)
        minElem = min(modList)

        #detects bullet
        self.rightMoveCD -=1
        self.leftMoveCD -=1
        for pixels in self.curPiece.pixelArr:
            if(pygame.sprite.spritecollideany(pixels, BulletLogic.goingRightBulletGroup) and self.rightMoveCD <= 0):
                moveRight = True
                self.rightMoveCD = 15
            elif(pygame.sprite.spritecollideany(pixels, BulletLogic.goingLeftBulletGroup) and self.leftMoveCD <= 0):
                moveLeft = True
                self.leftMoveCD = 15

        #Detects if move is still in bounds
        if(moveLeft and self.curPiece.col > 1 - minElem):
            self.changeBoardAtPiece(' ')
            self.curPiece.col -= 1
            if(self.collide()):
                self.curPiece.col += 1
            moveLeft = False

        if(moveRight and self.curPiece.col < 10 - maxElem):
            self.changeBoardAtPiece(' ')
            self.curPiece.col += 1
            if(self.collide()):
                self.curPiece.col -= 1
            moveRight = False

        self.curPiece.update()

    #Rotates the falling tile based on user input in the game loop
    def rotate(self): 
        global turnPiece
        self.upMoveCD -= 1

        #Detects collision
        for pixels in self.curPiece.pixelArr:
            if(pygame.sprite.spritecollideany(pixels, BulletLogic.UpBulletsGroup) and self.upMoveCD <= 0):
                turnPiece = True
                self.upMoveCD = 15


        #Rotates the piece to the next orientation
        if(turnPiece):
            turnPiece = False
            self.changeBoardAtPiece(' ')
            self.curPiece.rotation += 1
            self.curPiece.rotation = self.curPiece.rotation  % len(pieceArray[self.curPiece.type])
            self.curPiece.shape = pieceArray[self.curPiece.type][self.curPiece.rotation]

            modList = []
            for num in self.curPiece.shape:
                modList.append(num%4)

            #Side buffers to offset the shape logic
            maxElem = max(modList)
            minElem = min(modList)

            #These two while loops keep tile in bound
            while(self.curPiece.col + maxElem > 10):
                self.curPiece.col -= 1

            while(self.curPiece.col + minElem < 1):
                self.curPiece.col += 1

            #Reverts orientation if tile is colliding
            if(self.collide()):
                self.curPiece.rotation -= 1
                self.curPiece.rotation = self.curPiece.rotation  % len(pieceArray[self.curPiece.type])
                self.curPiece.shape = pieceArray[self.curPiece.type][self.curPiece.rotation]

        self.curPiece.update()

    #Draws the static tiles (that have been placed) based on boardArr entries
    def drawStatic(self):
        for r in range(len(boardArr)):
            for c in range(len(boardArr[r])):
                if(randBlockImage(boardArr[r][c]) != None and r <= 19):
                    img = (randBlockImage(boardArr[r][c]))
                    rect = img.get_rect(topleft = (20 + (30 * c),  30 * r))
                    screen.blit(img, rect)

    #Updates self
    def update(self):
        self.moveTile()
        self.rotate()
        self.drawStatic()
      
player2 = sidePlayer()
player2Group.add(player2)

player1 = bottomPlayer()
player1Group.add(player1)

def eventLoop():
    global moveLeft, moveRight, turnPiece
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            exit()

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_w:
                BulletLogic.UpBulletShoot = True
            
            #move up
            if event.key == pygame.K_UP:
                Players.p2MoveUp = True
           
            #move down
            if event.key == pygame.K_DOWN:
                Players.p2MoveDown = True
                
            #move left
            if event.key == pygame.K_a:
                Players.p1MoveLeft = True

            #move right
            if event.key == pygame.K_d:
                Players.p1MoveRight = True

            #switch player side
            if event.key == pygame.K_SPACE:
                Players.playerTriggerSwitch = True
            
            #shoot Horizontally
            if event.key == pygame.K_LEFT:
                BulletLogic.sideBulletShoot = True

            if event.key == pygame.K_RIGHT:
                BulletLogic.sideBulletShoot = True

            
        if event.type == pygame.KEYUP:

            #Upwards bullets shooting
            if event.key == pygame.K_w:
                BulletLogic.UpBulletShoot = False

            if event.key == pygame.K_UP:
                Players.p2MoveUp = False

            if event.key == pygame.K_DOWN:
                Players.p2MoveDown = False

            #move left
            if event.key == pygame.K_a:
                Players.p1MoveLeft = False
            #move right
            if event.key == pygame.K_d:
                Players.p1MoveRight = False

            #shoot horizontally
            if event.key == pygame.K_LEFT:
                BulletLogic.sideBulletShoot = False
            
            if event.key == pygame.K_RIGHT:
                BulletLogic.sideBulletShoot = False

def mainMenuEventLoop():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            exit()

        if event.type == pygame.KEYDOWN:
            
            #move using wasd
            if event.key == pygame.K_w:
                Players.pUp = True
            
            if event.key == pygame.K_s:
                Players.pDown = True
            
            if event.key == pygame.K_a:
                Players.pLeft = True
            
            if event.key == pygame.K_d:
                Players.pRight = True


            #move using arrow keys
            if event.key == pygame.K_UP:
                Players.p2Up = True
            
            if event.key == pygame.K_DOWN:
                Players.p2Down = True
            
            if event.key == pygame.K_LEFT:
                Players.p2Left = True
            
            if event.key == pygame.K_RIGHT:
                Players.p2Right = True

        if event.type == pygame.KEYUP:
            
            #move using wasd
            if event.key == pygame.K_w:
                Players.pUp = False
            if event.key == pygame.K_s:
                Players.pDown = False
            if event.key == pygame.K_a:
                Players.pLeft = False
            if event.key == pygame.K_d:
                Players.pRight = False

            #move using arrow keys
            if event.key == pygame.K_UP:
                Players.p2Up = False
            if event.key == pygame.K_DOWN:
                Players.p2Down = False
            if event.key == pygame.K_LEFT:
                Players.p2Left = False
            if event.key == pygame.K_RIGHT:
                Players.p2Right = False

    if pygame.Rect.colliderect(p1Menu.rect, helpButtonRect):
        if pygame.Rect.colliderect(p2Menu.rect, helpButtonRect):
            p2Menu.rect.x = WIDTH - 80
            p2Menu.rect.y = HEIGHT - 220
            p1Menu.rect.x = 50
            p1Menu.rect.y = 250
            HelpMenu()

    if pygame.Rect.colliderect(p1Menu.rect, playButtonRect):
        if pygame.Rect.colliderect(p2Menu.rect, playButtonRect):
            Players.pUp = Players.pDown= Players.pLeft= Players.pRight= Players.p2Up = Players.p2Down = Players.p2Left = Players.p2Right= False
            GameLoop()
    
    if pygame.Rect.colliderect(p1Menu.rect, creditsButtonRect):
        if pygame.Rect.colliderect(p2Menu.rect, creditsButtonRect):
            Credits()

    if pygame.Rect.colliderect(p1Menu.rect, quitButtonRect):
        if pygame.Rect.colliderect(p2Menu.rect, quitButtonRect):
              exit()        

def HelpMenuEventLoop():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            exit()
        if event.type == pygame.KEYDOWN:
            
            #move using wasd
            if event.key == pygame.K_w:
                Players.pUp = True
                
            if event.key == pygame.K_s:
                Players.pDown = True
            
            if event.key == pygame.K_a:
                Players.pLeft = True
            
            if event.key == pygame.K_d:
                Players.pRight = True

            #move using arrow keys
            if event.key == pygame.K_UP:
                Players.p2Up = True
            
            if event.key == pygame.K_DOWN:
                Players.p2Down = True
            
            if event.key == pygame.K_LEFT:
                Players.p2Left = True
            
            if event.key == pygame.K_RIGHT:
                Players.p2Right = True

        if event.type == pygame.KEYUP:
        
            #move using wasd
            if event.key == pygame.K_w:
                Players.pUp = False
            if event.key == pygame.K_s:
                Players.pDown = False
            if event.key == pygame.K_a:
                Players.pLeft = False
            if event.key == pygame.K_d:
                Players.pRight = False

            #move using arrow keys
            if event.key == pygame.K_UP:
                Players.p2Up = False
            if event.key == pygame.K_DOWN:
                Players.p2Down = False
            if event.key == pygame.K_LEFT:
                Players.p2Left = False
            if event.key == pygame.K_RIGHT:
                Players.p2Right = False

    if pygame.Rect.colliderect(p1Menu.rect, backButHelpRect):
        if pygame.Rect.colliderect(p2Menu.rect, backButHelpRect):
            p2Menu.rect.x = WIDTH/2
            p1Menu.rect.x = WIDTH/2
            MainMenu()

def HelpMenu():
    
    while True:
        HelpMenuEventLoop()

        screen.blit(HowToPlayImg, HowToPlayRect)
        
        screen.blit(backButHelp, backButHelpRect)

        p1MenuGroup.update()
        p1MenuGroup.draw(screen)
        
        p2MenuGroup.update()
        p2MenuGroup.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

def MainMenu():
    
    while True:
        mainMenuEventLoop()

        screen.blit(mainMenuBG, (0,0))

        #play button
        screen.blit(playButtonImg, playButtonRect)

        #credits
        screen.blit(creditsButton, creditsButtonRect)

        #quit button
        screen.blit(quitButton, quitButtonRect)

        #title
        screen.blit(titleImg, titleRect)

        #help button
        screen.blit(helpButton, helpButtonRect)
    
        
        p1MenuGroup.update()
        p1MenuGroup.draw(screen)
        
        p2MenuGroup.update()
        p2MenuGroup.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

def CreditsEventLoop():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            exit()
        if event.type == pygame.KEYDOWN:
            
            #move using wasd
            if event.key == pygame.K_w:
                Players.pUp = True
                
            
            if event.key == pygame.K_s:
                Players.pDown = True
            
            if event.key == pygame.K_a:
                Players.pLeft = True
            
            if event.key == pygame.K_d:
                Players.pRight = True

            #move using arrow keys
            if event.key == pygame.K_UP:
                Players.p2Up = True
            
            if event.key == pygame.K_DOWN:
                Players.p2Down = True
            
            if event.key == pygame.K_LEFT:
                Players.p2Left = True
            
            if event.key == pygame.K_RIGHT:
                Players.p2Right = True

        if event.type == pygame.KEYUP:
            #move using wasd
            if event.key == pygame.K_w:
                Players.pUp = False
            if event.key == pygame.K_s:
                Players.pDown = False
            if event.key == pygame.K_a:
                Players.pLeft = False
            if event.key == pygame.K_d:
                Players.pRight = False

            #move using arrow keys
            if event.key == pygame.K_UP:
                Players.p2Up = False
            if event.key == pygame.K_DOWN:
                Players.p2Down = False
            if event.key == pygame.K_LEFT:
                Players.p2Left = False
            if event.key == pygame.K_RIGHT:
                Players.p2Right = False

    if pygame.Rect.colliderect(p1Menu.rect, backButHelpRect):
        if pygame.Rect.colliderect(p2Menu.rect, backButHelpRect):
            p2Menu.rect.x = WIDTH/2
            p1Menu.rect.x = WIDTH/2
            MainMenu()

def Credits():
    while True:
        CreditsEventLoop()

        screen.blit(creditsBG, creditsRect)

        screen.blit(backButHelp, backButHelpRect)

        p1MenuGroup.update()
        p1MenuGroup.draw(screen)
        
        p2MenuGroup.update()
        p2MenuGroup.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

cd = COOLDOWN
def fallUpdate(game):
    global cd
    for i in range (len(game.curPiece.img)):
            screen.blit(game.curPiece.img[i], game.curPiece.rect[i]) 
    if cd ==0:
        game.fall()
        cd = COOLDOWN
    
    cd-=1

def GameLoop():
    global game, gameGoing

    game = GameEngine()

    pygame.mixer.music.stop()
    pygame.mixer.music.load('music\GameMusic.mp3')
    pygame.mixer.music.play(-1)

    while True:
        if(not gameGoing):
            break

        eventLoop()  

        #background
        screen.blit(backgroundImg, (0,0))

        #board
        screen.blit(boardImg, (50,0))

        game.update()
        fallUpdate(game)

        #Update player 1 position
        player1Group.update()
        player1Group.draw(screen)

        #Update player 2 position
        player2Group.update()
        player2Group.draw(screen)

        BulletLogic.UpBulletsGroup.update()
        BulletLogic.UpBulletsGroup.draw(screen)

        BulletLogic.goingLeftBulletGroup.update()
        BulletLogic.goingLeftBulletGroup.draw(screen)

        BulletLogic.goingRightBulletGroup.update()
        BulletLogic.goingRightBulletGroup.draw(screen)

        pygame.display.update()
        clock.tick(FPS)
    gameGoing = True
    pygame.mixer.music.stop()
    pygame.mixer.music.load('music\GameOverMusic.mp3')
    pygame.mixer.music.play(-1)
    GameOver()
    
#Starts the program
pygame.mixer.music.load('music\MenuMusic.mp3')
pygame.mixer.music.play(-1)
MainMenu()