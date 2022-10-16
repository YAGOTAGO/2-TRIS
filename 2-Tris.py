from random import randint
import pygame

#GAME CONSTANTS
WIDTH  = 400
HEIGHT = 650
FPS = 60
game = None

#initializes the pygame engine
pygame.init()


#player movement
p2MoveUp = False
p2MoveDown = False

#player movement
p1MoveLeft = False
p1MoveRight = False

#shooting
UpBulletShoot = False
sideBulletShoot = False

#player swapping sides
playerIsRight = True
playerTriggerSwitch = False

#var
playerSpeed = 4

#display vars
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2-Tris")
pygame.display.set_icon(pygame.image.load("img\Dandy_Icon.png").convert_alpha())

#background
backgroundImg = pygame.image.load("img\Game Board Window.png").convert_alpha()
boardImg = pygame.image.load("img\Tetris Board (300 × 600 px).png").convert_alpha()

#main menu player movememt
pLeft = False
pUp = False
pDown = False
pRight = False

p2Left = False
p2Up = False
p2Down = False
p2Right = False

#Main Menu background images
mainMenuBG = pygame.image.load("img\MainMenuBG.png").convert_alpha()
playButtonImg = pygame.image.load("img\MainMenu\PlayButton.png").convert_alpha()
playButtonRect = playButtonImg.get_rect(center = (WIDTH/2,300))

quitButton = pygame.image.load("img\MainMenu\QuitButton.png").convert_alpha()
quitButtonRect = quitButton.get_rect(center = (WIDTH/2, 500))

creditsButton = pygame.image.load("img\MainMenu\CreditsButton.png").convert_alpha()
creditsButtonRect = creditsButton.get_rect(center = (WIDTH/2, 400))

titleImg = pygame.image.load("img\MainMenu\Title.png").convert_alpha()
titleRect = titleImg.get_rect(center = (WIDTH/2, 100))

helpButton = pygame.image.load("img\MainMenu\HelpButton.png").convert_alpha()
helpButtonRect = helpButton.get_rect(center = (WIDTH-50, 50))

#help menu
HowToPlayImg = pygame.image.load("img\HelpMenu\HowToPlay.png")
HowToPlayRect = HowToPlayImg.get_rect(topleft = (0,0))

#back button help menu
backButHelp = pygame.image.load("img\HelpMenu\X.png")
backButHelpRect = backButHelp.get_rect(center = (WIDTH-50,50))

#Credits
creditsBG = pygame.image.load("img\Credits.png")
creditsRect = creditsBG.get_rect(topleft = (0,0))

#Main menu sprite groups
p1MenuGroup = pygame.sprite.GroupSingle()
p2MenuGroup = pygame.sprite.GroupSingle()

#Restart
RestartImg = pygame.image.load("img\Restart.png").convert_alpha()
RestartRect = RestartImg.get_rect(center = (WIDTH/2, 650))

#Main Menu Button
MainMenuButton = pygame.image.load("img\MainMenu.png").convert_alpha()
MainMenuRect = MainMenuButton.get_rect(center = (WIDTH/2, 450))

#Game Over vars
gameOverBG = pygame.image.load("img\Game Over.png").convert_alpha()
gameGoing = True

#Bullet groups
UpBulletsGroup = pygame.sprite.Group()
goingLeftBulletGroup = pygame.sprite.Group()
goingRightBulletGroup = pygame.sprite.Group()

#Game player groups
player2Group = pygame.sprite.GroupSingle()
player1Group = pygame.sprite.GroupSingle()

#game engine movement vars
COOLDOWN = 20
moveLeft = False
moveRight = False
turnPiece = False

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

class mainMenuPlayers(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center = (x, y))
        self.speed = playerSpeed


#move using WASD
class MainMenuP1(mainMenuPlayers):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
    
    def move(self):
        if pLeft and self.rect.left>0:
            self.rect.x -= self.speed
        if pRight and self.rect.right<WIDTH:
            self.rect.x += self.speed
        if pDown and self.rect.bottom<HEIGHT:
            self.rect.y += self.speed
        if pUp and self.rect.top>0:
            self.rect.y -= self.speed

    
    def update(self):
        self.move()
    

#move using arrows
class MainMenuP2(mainMenuPlayers):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
    
    def move(self):
        if p2Left and self.rect.left>0:
            self.rect.x -= self.speed
        if p2Right and self.rect.right<WIDTH:
            self.rect.x += self.speed
        if p2Down and self.rect.bottom<HEIGHT:
            self.rect.y += self.speed
        if p2Up and self.rect.top>0:
            self.rect.y -= self.speed
    
    def update(self):
        self.move()
     

#instantiate and add to group
p1Menu = MainMenuP1(150, 200, pygame.image.load("img\player1.png").convert_alpha())
p2Menu = MainMenuP2(250, 200, pygame.image.load("img\player2.png").convert_alpha())
p1MenuGroup.add(p1Menu)
p2MenuGroup.add(p2Menu)


def GameOverEventLoop():
    global pUp, pDown, pLeft, pRight, p2Up, p2Down, p2Left, p2Right

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
                pUp = True
                
            
            if event.key == pygame.K_s:
                pDown = True
            
            if event.key == pygame.K_a:
                pLeft = True
            
            if event.key == pygame.K_d:
                pRight = True

            #move using arrow keys
            if event.key == pygame.K_UP:
                p2Up = True
            
            if event.key == pygame.K_DOWN:
                p2Down = True
            
            if event.key == pygame.K_LEFT:
                p2Left = True
            
            if event.key == pygame.K_RIGHT:
                p2Right = True

        if event.type == pygame.KEYUP:
            #move using wasd
            if event.key == pygame.K_w:
                pUp = False
            if event.key == pygame.K_s:
                pDown = False
            if event.key == pygame.K_a:
                pLeft = False
            if event.key == pygame.K_d:
                pRight = False

            #move using arrow keys
            if event.key == pygame.K_UP:
                p2Up = False
            if event.key == pygame.K_DOWN:
                p2Down = False
            if event.key == pygame.K_LEFT:
                p2Left = False
            if event.key == pygame.K_RIGHT:
                p2Right = False
    
    


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
            if(pygame.sprite.spritecollideany(pixels, goingRightBulletGroup) and self.rightMoveCD <= 0):
                moveRight = True
                self.rightMoveCD = 15
            elif(pygame.sprite.spritecollideany(pixels, goingLeftBulletGroup) and self.leftMoveCD <= 0):
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
            if(pygame.sprite.spritecollideany(pixels, UpBulletsGroup) and self.upMoveCD <= 0):
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
      


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.speed = 10
        self.image = pygame.image.load("img\Flowerproj.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    
    #destroys out of bounds bullets
    def OutOfBoundsKill(self):
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.top<0 or self.rect.top >HEIGHT:
            self.kill()
       
#defines the bullet that moves up
class UpBullet(Bullet):

    def __init__(self, x, y):
        super().__init__(x, y)

    def update(self):
        self.rect.y -= self.speed
        self.OutOfBoundsKill()

#defines bullets that move horizontally
class SidewaysBullet(Bullet):

    def __init__(self, x, y, dir):
        super().__init__(x, y)
        self.direction = dir

    def update(self):
        self.rect.x += (self.direction * self.speed)
        self.OutOfBoundsKill()

#Logic for player 2 (side player)
class sidePlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img\player2.png").convert_alpha()
        self.rect = self.image.get_rect(center = (WIDTH/2 + 163, 100))
        self.maxCD = 30
        self.shootCD = self.maxCD
        self.dir = -1
        self.flipAmount = 325

    def move(self):
        if(p2MoveUp and self.rect.y >= 5):
            self.rect.y -= playerSpeed

        if (p2MoveDown and self.rect.y <= 550):
            self.rect.y += playerSpeed

    def switchSides(self):
        global playerTriggerSwitch, playerIsRight
        if playerTriggerSwitch:
            self.image = pygame.transform.flip(self.image, True, False)
            if(playerIsRight):
                self.rect.x -= self.flipAmount
                playerIsRight = False
                self.dir = 1
            else:
                self.rect.x += self.flipAmount
                playerIsRight = True
                self.dir = -1

            playerTriggerSwitch = False

    def shoot(self):
        self.shootCD -= 1
        if sideBulletShoot and self.shootCD<0:
            bullet = SidewaysBullet(self.rect.centerx, self.rect.centery, self.dir)
            if self.dir == -1:
                goingLeftBulletGroup.add(bullet)
            else:
                goingRightBulletGroup.add(bullet)

            self.shootCD = self.maxCD

    def update(self):
        self.switchSides()
        self.shoot()
        self.move()

#Logic for player 1 (bottom player)
class bottomPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img\player1.png").convert_alpha()
        self.rect = self.image.get_rect(center = (WIDTH / 2, HEIGHT-40))
        self.maxShootCD = 30
        self.shootCD = self.maxShootCD

    def move(self):
        if(p1MoveLeft and self.rect.x >= (WIDTH / 2) - 155):
            self.rect.x -= playerSpeed

        if(p1MoveRight and self.rect.x <= (WIDTH / 2) + 115):
            self.rect.x += playerSpeed

    def shoot(self):
        self.shootCD -= 1
        if UpBulletShoot and self.shootCD<0:
            self.shootCD = self.maxShootCD
            bullet = UpBullet(self.rect.centerx, self.rect.centery)
            UpBulletsGroup.add(bullet)

    def update(self):
        self.shoot()
        self.move()
        

player2 = sidePlayer()
player2Group.add(player2)

player1 = bottomPlayer()
player1Group.add(player1)


def eventLoop():
    global p2MoveUp, p2MoveDown, p1MoveLeft, p1MoveRight, playerTriggerSwitch, UpBulletShoot, sideBulletShoot, moveLeft, moveRight, turnPiece
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            exit()

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_w:
                UpBulletShoot = True
            
            #move up
            if event.key == pygame.K_UP:
                p2MoveUp = True
           
            #move down
            if event.key == pygame.K_DOWN:
                p2MoveDown = True
                
            #move left
            if event.key == pygame.K_a:
                p1MoveLeft = True

            #move right
            if event.key == pygame.K_d:
                p1MoveRight = True

            #switch player side
            if event.key == pygame.K_SPACE:
                playerTriggerSwitch = True
            
            #shoot Horizontally
            if event.key == pygame.K_LEFT:
                sideBulletShoot = True

            if event.key == pygame.K_RIGHT:
                sideBulletShoot = True

            
        if event.type == pygame.KEYUP:

            #Upwards bullets shooting
            if event.key == pygame.K_w:
                UpBulletShoot = False

            if event.key == pygame.K_UP:
                p2MoveUp = False

            if event.key == pygame.K_DOWN:
                p2MoveDown = False

            #move left
            if event.key == pygame.K_a:
                p1MoveLeft = False
            #move right
            if event.key == pygame.K_d:
                p1MoveRight = False

            #shoot horizontally
            if event.key == pygame.K_LEFT:
                sideBulletShoot = False
            
            if event.key == pygame.K_RIGHT:
                sideBulletShoot = False


def mainMenuEventLoop():
    global pUp, pDown, pLeft, pRight, p2Up, p2Down, p2Left, p2Right

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            exit()

        if event.type == pygame.KEYDOWN:
            
            #move using wasd
            if event.key == pygame.K_w:
                pUp = True
            
            if event.key == pygame.K_s:
                pDown = True
            
            if event.key == pygame.K_a:
                pLeft = True
            
            if event.key == pygame.K_d:
                pRight = True


            #move using arrow keys
            if event.key == pygame.K_UP:
                p2Up = True
            
            if event.key == pygame.K_DOWN:
                p2Down = True
            
            if event.key == pygame.K_LEFT:
                p2Left = True
            
            if event.key == pygame.K_RIGHT:
                p2Right = True

        if event.type == pygame.KEYUP:
            
            #move using wasd
            if event.key == pygame.K_w:
                pUp = False
            if event.key == pygame.K_s:
                pDown = False
            if event.key == pygame.K_a:
                pLeft = False
            if event.key == pygame.K_d:
                pRight = False

            #move using arrow keys
            if event.key == pygame.K_UP:
                p2Up = False
            if event.key == pygame.K_DOWN:
                p2Down = False
            if event.key == pygame.K_LEFT:
                p2Left = False
            if event.key == pygame.K_RIGHT:
                p2Right = False

    if pygame.Rect.colliderect(p1Menu.rect, helpButtonRect):
        if pygame.Rect.colliderect(p2Menu.rect, helpButtonRect):
            p2Menu.rect.x = WIDTH - 80
            p2Menu.rect.y = HEIGHT - 220
            p1Menu.rect.x = 50
            p1Menu.rect.y = 250
            HelpMenu()

    if pygame.Rect.colliderect(p1Menu.rect, playButtonRect):
        if pygame.Rect.colliderect(p2Menu.rect, playButtonRect):
            pUp = pDown= pLeft= pRight= p2Up = p2Down = p2Left =p2Right= False
            GameLoop()
    
    if pygame.Rect.colliderect(p1Menu.rect, creditsButtonRect):
        if pygame.Rect.colliderect(p2Menu.rect, creditsButtonRect):
            Credits()

    if pygame.Rect.colliderect(p1Menu.rect, quitButtonRect):
        if pygame.Rect.colliderect(p2Menu.rect, quitButtonRect):
              exit()        

def HelpMenuEventLoop():
    global pUp, pDown, pLeft, pRight, p2Up, p2Down, p2Left, p2Right

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            exit()
        if event.type == pygame.KEYDOWN:
            
            #move using wasd
            if event.key == pygame.K_w:
                pUp = True
                
            
            if event.key == pygame.K_s:
                pDown = True
            
            if event.key == pygame.K_a:
                pLeft = True
            
            if event.key == pygame.K_d:
                pRight = True

            #move using arrow keys
            if event.key == pygame.K_UP:
                p2Up = True
            
            if event.key == pygame.K_DOWN:
                p2Down = True
            
            if event.key == pygame.K_LEFT:
                p2Left = True
            
            if event.key == pygame.K_RIGHT:
                p2Right = True

        if event.type == pygame.KEYUP:
        
            #move using wasd
            if event.key == pygame.K_w:
                pUp = False
            if event.key == pygame.K_s:
                pDown = False
            if event.key == pygame.K_a:
                pLeft = False
            if event.key == pygame.K_d:
                pRight = False

            #move using arrow keys
            if event.key == pygame.K_UP:
                p2Up = False
            if event.key == pygame.K_DOWN:
                p2Down = False
            if event.key == pygame.K_LEFT:
                p2Left = False
            if event.key == pygame.K_RIGHT:
                p2Right = False

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
    global pUp, pDown, pLeft, pRight, p2Up, p2Down, p2Left, p2Right

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            exit()
        if event.type == pygame.KEYDOWN:
            
            #move using wasd
            if event.key == pygame.K_w:
                pUp = True
                
            
            if event.key == pygame.K_s:
                pDown = True
            
            if event.key == pygame.K_a:
                pLeft = True
            
            if event.key == pygame.K_d:
                pRight = True

            #move using arrow keys
            if event.key == pygame.K_UP:
                p2Up = True
            
            if event.key == pygame.K_DOWN:
                p2Down = True
            
            if event.key == pygame.K_LEFT:
                p2Left = True
            
            if event.key == pygame.K_RIGHT:
                p2Right = True

        if event.type == pygame.KEYUP:
            #move using wasd
            if event.key == pygame.K_w:
                pUp = False
            if event.key == pygame.K_s:
                pDown = False
            if event.key == pygame.K_a:
                pLeft = False
            if event.key == pygame.K_d:
                pRight = False

            #move using arrow keys
            if event.key == pygame.K_UP:
                p2Up = False
            if event.key == pygame.K_DOWN:
                p2Down = False
            if event.key == pygame.K_LEFT:
                p2Left = False
            if event.key == pygame.K_RIGHT:
                p2Right = False

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

        UpBulletsGroup.update()
        UpBulletsGroup.draw(screen)

        goingLeftBulletGroup.update()
        goingLeftBulletGroup.draw(screen)

        goingRightBulletGroup.update()
        goingRightBulletGroup.draw(screen)

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