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

    def on_board(self, w, h):
        return (0 < self.rect.x < w) and (0 < self.rect.y < h)


class Fire(pygame.sprite.Sprite):

    def __init__(self, point, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert()

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = point

    def on_board(self, w, h):
        return (0 < self.rect.x < w) and (0 < self.rect.y < h)

        

class LaserFire(Fire):
    def __init__(self, point, back=False):
        super(LaserFire, self).__init__(point, "fire.png")
        self.back = back

    def move(self):
        if self.back:
            self.rect.y += 5
        else:
            self.rect.y -= 5


class PlasmaFire(Fire):
    def __init__(self, point, left=True, back=False):
        super(PlasmaFire, self).__init__(point, "fire.png")

        self.left = left
        self.back = back

    def move(self):
        if self.left:
            self.rect.x -= 1
        else:
            self.rect.x += 1

        if self.back:
            self.rect.y += 5
        else:
            self.rect.y -= 5


class RandFire(Fire):
    def __init__(self, point, back=False):
        super(RandFire, self).__init__(point, "fire.png")
        self.back = back

    def move(self):
        self.rect.x += randint(-3, 3)
        if self.back:
            self.rect.y += 5
        else:
            self.rect.y -= 5

class BackRandFire(RandFire):
    def __init__(self, point):
        super(BackRandFire, self).__init__((point.x, point.y + 40), back=True)

class SideFire(Fire):
    def __init__(self, point, left=True, back=False):
        super(SideFire, self).__init__((point.x - 20, point.y), "fire.png")
        self.left = left

    def move(self):
        if self.left:
            self.rect.x -= 5
        else:
            self.rect.x += 5



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
pygame.display.set_caption('space')



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
             pygame.K_c: RandFire,
             pygame.K_v: BackRandFire,
             pygame.K_b: SideFire}

pygame.key.set_repeat(5, 5)


fires = pygame.sprite.Group()
alien_fires = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bonus = pygame.sprite.Group()



points = 0
killed = 0
points = 0
life = 5
start_time = time.time()
ammo = 20
cycles = 0



def set_labels():

    myfont = pygame.font.SysFont("", 21)

    title = ["cycles: %s"  % cycles,
             "time: %s"    % int(time.time() - start_time),
             "fire: %s"    % len(fires),
             "enemies: %s" % len(aliens),
             "%s : %s"     % (player.rect.x, player.rect.y),
             "killed: %s"  % killed,
             "points: %s"  % points,
             "life:  %s"   % life,
             "ammo: %s"    % ammo,
            ]

    pos = 0

    for t in title:
        screen.blit(myfont.render(t, 1, green), (0, pos))
        pos += 20

def event_handle():

    global ammo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key in moves:
                mv, x, y = moves[event.key]
                mv(x, y)

            if event.key in fire_keys:
                if ammo <= 0:
                    continue
                ammo -= 2

                p1 = Point(player.rect.x, player.rect.y - 5)
                p2 = Point(player.rect.x + 38, player.rect.y - 5)

                left_fire = fire_keys[event.key](p1)

                if event.key == pygame.K_x or event.key == pygame.K_b:
                    right_fire = fire_keys[event.key](p2, left=False)
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

game_map = Map([(50, 200), (150, 200), (250, 200), (350, 200), (450, 200),
                (550, 200), (650, 200)],
               [(400, 400), (500, 400)]
              )


def init_enemy(enemy_list):
    for e in enemy_list:
        aliens.add(Alien(e))

def init_bonus(bonus_list):
    for b in bonus_list:
        bonus.add(Bonus(b))

init_enemy(game_map.alien)
init_bonus(game_map.bonus)

while not end:
    cycles += 1
    clock.tick(30)
    screen.fill(black)

    if randint(1, 8) == 1:
        if ammo <= 18:
            ammo += 2

    to_del = []
    for f in fires:
        if not f.on_board(*screen_size):
            to_del.append(f)
        f.move()
        
        if pygame.sprite.spritecollide(f, aliens, True):
            to_del.append(f)
            killed += 1
            sound.play()

    for d in to_del:
        fires.remove(d)

    to_del = []
    for af in alien_fires:
        if not af.on_board(*screen_size):
            to_del.append(af)
        af.move()

        if sprite.spritecollide(af, sprites, False):
            to_del.append(af)
            life -= 1
            sound.play()

            player.move_to_pos(Point(300, 500))

    for d in to_del:
        alien_fires.remove(d)

    
    if pygame.sprite.spritecollide(player, bonus, True):
        points += 100

    if pygame.sprite.spritecollide(player, aliens, False):
        life -= 1
        player.move_to_pos(Point(300, 500))
        sound.play()

    for a in aliens:
        if randint(1, 2) == 1:
            x1 = randint(-5, 5)
            y1 = randint(-5, 5)
            a.move(x1, y1)
            if not a.on_board(*screen_size):
                a.move(-x1, -y1)

        if randint(1, 100) == 1:

                p1 = Point(a.rect.x,            a.rect.y + a.rect.w + 5)
                p2 = Point(a.rect.x + a.rect.w - 10, a.rect.y + a.rect.w + 5)

                left_fire = RandFire(p1, back=True)
                right_fire = RandFire(p2, back=True)

                alien_fires.add(left_fire)
                alien_fires.add(right_fire)


    end = event_handle()

    for s in sprites, fires, aliens, bonus, alien_fires:
        s.draw(screen)
    
    set_labels()

    pygame.display.flip()

pygame.quit()

