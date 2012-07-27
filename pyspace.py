import pygame
from random import randint

from collections import namedtuple
Point = namedtuple('Point', 'x y')
Size = namedtuple('Size', 'w h')
Color = namedtuple('Color', 'red green blue')

black = Color(0,   0,    0)
white = Color(255,255, 255)
blue  = Color(0,   0,  255)


screen_size = Size(800, 600)

class Spaceship(pygame.sprite.Sprite):

    def __init__(self, point):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("spaceship.png").convert()

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = point
    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_to_pos(self, pos):
        self.rect.x = pos.x 

class Fire(pygame.sprite.Sprite):

    def __init__(self, point, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image).convert()

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = point

        

class LaserFire(Fire):
    def __init__(self, point):
        super(LaserFire, self).__init__(point, "fire.png")

    def move(self):
        self.rect.y -= 5


class PlasmaFire(Fire):
    def __init__(self, point, left=True):
        self.left = left
        super(PlasmaFire, self).__init__(point, "fire.png")

    def move(self):
        if self.left:
            self.rect.x -= 1
        else:
            self.rect.x += 1
        self.rect.y -= 5


class RandFire(Fire):
    def __init__(self, point):
        super(RandFire, self).__init__(point, "fire.png")

    def move(self):
        self.rect.x += randint(-2, 2)
        self.rect.y -= 5




def random_color():
    return Color(randint(0, 255), randint(0, 255), randint(0, 255))



pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('pyrace')



clock = pygame.time.Clock()

end = False

player = Spaceship(Point(300, 500))

sprites = pygame.sprite.RenderPlain()
sprites.add(player)

pygame.mouse.set_visible(0)


moves = {pygame.K_LEFT: (player.move, -10, 0),
         pygame.K_RIGHT: (player.move, 10, 0),
         pygame.K_UP: (player.move, 0, -10),
         pygame.K_DOWN: (player.move, 0, 10)
         }

pygame.key.set_repeat(5, 5)


fires = pygame.sprite.RenderPlain()

while not end:
    clock.tick(30)
    screen.fill(black)


    for f in fires:
        f.move()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
        if event.type == pygame.KEYDOWN:
            if event.key in moves:
                mv, x, y = moves[event.key]
                mv(x, y)
            elif event.key == pygame.K_SPACE:
                left_fire  = LaserFire(Point(player.rect.x, player.rect.y - 5))
                right_fire = LaserFire(Point(player.rect.x + 38, player.rect.y - 5))
                fires.add(left_fire)
                fires.add(right_fire)

            elif event.key == pygame.K_z:
                left_fire  = PlasmaFire(Point(player.rect.x, player.rect.y - 5))
                right_fire = PlasmaFire(Point(player.rect.x + 38, player.rect.y - 5), False)
                fires.add(left_fire)
                fires.add(right_fire)
        
            elif event.key == pygame.K_x:
                left_fire  = RandFire(Point(player.rect.x, player.rect.y - 5))
                right_fire = RandFire(Point(player.rect.x + 38, player.rect.y - 5))
                fires.add(left_fire)
                fires.add(right_fire)
            


    sprites.draw(screen)
    fires.draw(screen)
    pygame.display.flip()

pygame.quit()

