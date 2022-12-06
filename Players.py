import pygame
import BulletLogic
from BulletLogic import SidewaysBullet, UpBullet

#all players speed
playerSpeed = 4

#in game player movement
p2MoveUp = False
p2MoveDown = False
p1MoveLeft = False
p1MoveRight = False

#player swapping sides
playerIsRight = True
playerTriggerSwitch = False

#main menu player movememt
pLeft = False
pUp = False
pDown = False
pRight = False

p2Left = False
p2Up = False
p2Down = False
p2Right = False

WIDTH = 400
HEIGHT = 650


class mainMenuPlayers(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center = (x, y))
        self.speed = playerSpeed

#Extends the MainMenu Player Class/ Moves using wasd
class MainMenuP1(mainMenuPlayers):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
    
    #move using WASD
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

#Extends the MainMenu Player Classmove using arrows
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
     
#Logic for player 2 (side player)
class sidePlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img\player2.png").convert_alpha()
        self.rect = self.image.get_rect(center = (WIDTH/2 + 163, 100))
        self.maxCD = 20
        self.shootCD = self.maxCD
        self.dir = -1
        self.flipAmount = 325

    def move(self):
        if(p2MoveUp and self.rect.y >= 5):
            self.rect.y -= playerSpeed

        if (p2MoveDown and self.rect.y <= 550):
            self.rect.y += playerSpeed

    def switchSides(self):
        global playerIsRight, playerTriggerSwitch
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
        if BulletLogic.sideBulletShoot and self.shootCD<0:
            bullet = SidewaysBullet(self.rect.centerx, self.rect.centery, self.dir)
            if self.dir == -1:
                BulletLogic.goingLeftBulletGroup.add(bullet)
            else:
                BulletLogic.goingRightBulletGroup.add(bullet)

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
        self.maxShootCD = 20
        self.shootCD = self.maxShootCD

    def move(self):
        if(p1MoveLeft and self.rect.x >= (WIDTH / 2) - 155):
            self.rect.x -= playerSpeed

        if(p1MoveRight and self.rect.x <= (WIDTH / 2) + 115):
            self.rect.x += playerSpeed

    def shoot(self):
        self.shootCD -= 1
        if BulletLogic.UpBulletShoot and self.shootCD<0:
            self.shootCD = self.maxShootCD
            bullet = UpBullet(self.rect.centerx, self.rect.centery)
            BulletLogic.UpBulletsGroup.add(bullet)

    def update(self):
        self.shoot()
        self.move()
     


