# Rev Run Portion

import pygame, random, sys
from subprocess import Popen
from pygame.locals import *
pygame.init()

win = pygame.display.set_mode([500,250])

clock = pygame.time.Clock()

jumpSound = pygame.mixer.Sound('assets/sound/jump.wav')
hurtSound = pygame.mixer.Sound('assets/sound/hitHurt.wav')
scoreSound = pygame.mixer.Sound('assets/sound/pickupCoin.wav')
selectSound = pygame.mixer.Sound('assets/sound/blipSelect.wav')

pygame.mixer.music.load('assets/sound/hymn.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

def playSound(sfx):
    pygame.mixer.Sound.play(sfx)

def draw_text(text, font, color, surface, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(win.get_width()/2, y))
    #textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
class Ground():
    def __init__(self):
        self.image = pygame.image.load('assets/grass.png')
        size = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, (size[0]/2, size[1]/15))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.x1 = 0
        self.x2 = self.width
        self.y = 225

    def update(self, speed):
        self.x1 -= speed
        self.x2 -= speed

        if self.x1 <= -self.width:
            self.x1 = self.width
        
        if self.x2 <= -self.width:
            self.x2 = self.width

    def draw(self, screen):
        screen.blit(self.image, (self.x1, self.y))
        screen.blit(self.image, (self.x2, self.y))

class Back():
    def __init__(self):
        self.image = pygame.image.load('assets/field.png')
        size = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, (size[0], size[1]))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.x1 = 0
        self.x2 = self.width
        self.y = -130

    def reset(self):
        self.x1 = 0
        self.x2 = self.width

    def update(self, speed):
        self.x1 -= speed/25
        self.x2 -= speed/25

        if self.x1 <= -self.width:
            self.x1 = self.width
        
        if self.x2 <= -self.width:
            self.x2 = self.width

    def draw(self, screen):
        screen.blit(self.image, (self.x1, self.y))
        screen.blit(self.image, (self.x2, self.y))


class Rev(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.x = 20 
        self.y = 250
        self.pos = (self.x, self.y)
        
        self.y_vel = 0 # need a velocity cause we will be jumping
        self.jumping = False
        self.gravity = 1
        self.jumpHeight = 20

        self.image = pygame.image.load('assets/revStand.png').convert_alpha()
        size = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, (size[0]/3, size[1]/3))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
       
    def jump(self):
        if(self.jumping == False):
            playSound(jumpSound)
            self.y_vel = -self.jumpHeight
            self.jumping = True

    def update(self):
        self.y_vel += self.gravity
        if self.y_vel >= self.jumpHeight:
            self.y_vel = self.jumpHeight

        self.rect.y += self.y_vel

        if(self.rect.bottom>250):
            self.jumping = False
            self.rect.bottom = 250

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):

    def __init__(self, type):
        pygame.sprite.Sprite.__init__(self)

        self.x_vel = -7
        if type == 1:
            self.image = pygame.image.load('assets/enemy.png').convert_alpha()
            size = self.image.get_rect().size
            self.image = pygame.transform.scale(self.image, (size[0]/4, size[1]/4))
            self.rect = self.image.get_rect()
            self.rect.left = 500
            self.rect.bottom = 250
        else:
            self.image = pygame.image.load('assets/football.png').convert_alpha()
            size = self.image.get_rect().size
            self.image = pygame.transform.scale(self.image, (size[0]/15, size[1]/15))
            self.rect = self.image.get_rect()
            self.rect.left=500
            self.rect.bottom = 150

    def update(self):
        self.rect.x += self.x_vel
        if(self.rect.right <= 0):
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

font = pygame.font.Font('assets/pixelfont.ttf' , 18)
bigfont = pygame.font.Font('assets/pixelfont.ttf', 45)
medfont = pygame.font.Font('assets/pixelfont.ttf', 25)

tutorial = True
while tutorial:
    win.fill((214,210,196))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            playSound(selectSound)
            tutorial = False
    
    draw_text("RevRun!", bigfont,(80,0,0), win, 40)
    draw_text("Help Reveille score a Touchdown,", font, (0,0,0), win, 80)
    draw_text("But watch out for TU Players!", font, (0,0,0), win, 120)
    draw_text("Jump with space or Arrowkeys", font, (0,0,0), win, 160)
    draw_text("Press Any Key to Continue", font, (0,0,0), win, 200)

    pygame.display.flip()

rev = Rev()
ground = Ground()
background = Back()
enemy_group = pygame.sprite.Group()
running = True

count = 0
enemy_spawn = 100
score = 0
alive = True
speed = 7

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if(alive):
                    rev.jump()
            if event.key == pygame.K_UP:
                if(alive):
                    rev.jump()
            if event.key == pygame.K_q and not alive:
                Popen(['python3', 'menu.py'])
                quit()
            if event.key == pygame.K_r and not alive:
                alive = True
                score = 0
                count = 0
                enemy_spawn = 100
                enemy_group.empty()
                background.reset()

    if alive:
        count += 1
        if count % int(enemy_spawn) == 0:
            if random.randint(1, 100) > 33:
                enemy = Enemy(1)
                enemy_group.add(enemy)
            else:
                enemy = Enemy(2)
                enemy_group.add(enemy)

        if count % 100 == 0:
            #speed += 0.1
            enemy_spawn -= 0.5

        if count % 5 == 0:
            score += 1

    if alive:
        for enemy in enemy_group:
            if pygame.sprite.collide_mask(rev, enemy):
                playSound(hurtSound)
                alive = False

    win.fill((240,240,240))

    if alive:
        ground.update(speed)
        background.update(speed)
    background.draw(win)
    ground.draw(win)
    rev.update()
    rev.draw(win)
    if(alive):
        enemy_group.update()
    enemy_group.draw(win)

    scoreout = 'Score = '+str(score)
    text = font.render(scoreout, True, (0,0,0))
    win.blit(text, (10,0))

    if not alive:
        pygame.draw.rect(win, (214,210,196), (60, 80, 380, 85))
        draw_text('GAME OVER', bigfont, (80,0,0), win, 100)
        draw_text(scoreout, medfont, (0,0,0), win, 130)
        draw_text('Return to menu: Q / Restart: R', font, (0,0,0), win, 153)

    clock.tick(60)
    pygame.display.update()
pygame.quit()
