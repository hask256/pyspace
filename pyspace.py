import pygame
from pygame import sprite
import time
from random import randint

from collections import namedtuple
Point = namedtuple('Point', 'x y')
Size = namedtuple('Size', 'w h')
Color = namedtuple('Color', 'red green blue')

black = Color(0,   0,    0)
white = Color(255,255, 255)
blue  = Color(0,   0,  255)
green = Color(0, 140,    0)


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

        x = self.rect.x
        y = self.rect.y
        w = screen_size.w - self.rect.w
        h = screen_size.h - self.rect.h

        if x > w: self.rect.x = w
        if x < 0: self.rect.x = 0

        if y > h: self.rect.y = h
        if y < 0: self.rect.y = 0

    def move_to_pos(self, pos):
        self.rect.x = pos.x
        self.rect.y = pos.y

class Alien(pygame.sprite.Sprite):

    def __init__(self, point):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("alien.png").convert()

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = point
    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


class Fire(pygame.sprite.Sprite):

    def __init__(self, point, image):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image).convert()

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = point

    def on_board(self, w, h):
        return (0 < self.rect.x < w) and (0 < self.rect.y < h)

        

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
        self.rect.x += randint(-3, 3)
        self.rect.y -= 5



class Bonus(pygame.sprite.Sprite):

    def __init__(self, point):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("bonus.png").convert()

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = point

class Map(object):
    def __init__(self, alien, bonus):
        self.alien = alien
        self.bonus = bonus
        
    
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


fire_keys = {pygame.K_z: LaserFire,
             pygame.K_x: PlasmaFire,
             pygame.K_c: RandFire}

pygame.key.set_repeat(5, 5)


fires = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bonus = pygame.sprite.Group()



points = 0
killed = 0
points = 0
life = 5
start_time = time.time()

def set_labels():

    myfont = pygame.font.SysFont("", 25)

    title = ["time: %s"    % int(time.time() - start_time),
             "fire: %s"    % len(fires),
             "enemies: %s" % len(aliens),
             "%s : %s"     % (player.rect.x, player.rect.y),
             "killed: %s"  % killed,
             "points: %s"  % points,
             "life:  %s"   % life
            ]

    pos = 0

    for t in title:
        screen.blit(myfont.render(t, 1, green), (0, pos))
        pos += 20

def event_handle():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key in moves:
                mv, x, y = moves[event.key]
                mv(x, y)

            if event.key in fire_keys:
                p1 = Point(player.rect.x, player.rect.y - 5)
                p2 = Point(player.rect.x + 38, player.rect.y - 5)

                left_fire = fire_keys[event.key](p1)

                if event.key == pygame.K_x:
                    right_fire = fire_keys[event.key](p2, False)
                else:
                    right_fire = fire_keys[event.key](p2)

                fires.add(left_fire)
                fires.add(right_fire)
                points = len(fires)
                
            if event.key == pygame.K_q:
                x = randint(100, screen_size.w - 100)
                y = randint(100, screen_size.h - 100)
                aliens.add(Alien(Point(x, y)))

            if event.key == pygame.K_w:
                x = randint(100, screen_size.w - 100)
                y = randint(100, screen_size.h - 100)
                bonus.add(Bonus(Point(x, y)))

    return False

sound = pygame.mixer.Sound("explosion.wav")

while not end:
    clock.tick(30)
    screen.fill(black)

    to_del = []
    for f in fires:
        if not f.on_board(*screen_size):
            to_del.append(f)
        f.move()
        
        if pygame.sprite.spritecollide(f, aliens, True):
            to_del.append(f)
            killed += 1
            sound.play()

    
    if pygame.sprite.spritecollide(player, bonus, True):
        points += 100

    if pygame.sprite.spritecollide(player, aliens, False):
        life -= 1
        player.move_to_pos(Point(300, 500))

            

    for d in to_del:
        fires.remove(d)

    end = event_handle()

    for s in sprites, fires, aliens, bonus:
        s.draw(screen)
    
    set_labels()

    pygame.display.flip()

pygame.quit()

