import pygame

#shooting
UpBulletShoot = False
sideBulletShoot = False

#Game Vars
WIDTH = 400
HEIGHT = 650

#Bullet groups
UpBulletsGroup = pygame.sprite.Group()
goingLeftBulletGroup = pygame.sprite.Group()
goingRightBulletGroup = pygame.sprite.Group()

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
   