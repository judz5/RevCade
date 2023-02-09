import sys
 
import pygame, random
from subprocess import Popen
from pygame.locals import *
 
pygame.init()
 
fps = 60
clock = pygame.time.Clock()
 
width, height = 640, 480
win = pygame.display.set_mode((width, height))
 
hurtSound = pygame.mixer.Sound('assets/sound/hitHurt.wav')
scoreSound = pygame.mixer.Sound('assets/sound/pickupCoin.wav')
selectSound = pygame.mixer.Sound('assets/sound/blipSelect.wav')

pygame.mixer.music.load('assets/sound/spirit.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

def playSound(sfx):
    pygame.mixer.Sound.play(sfx)

def draw_text(text, font, color, surface, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(win.get_width()/2, y))
    #textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

class Rev(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.x = 100
        self.x_vel = 0
        self.y = 480
        self.pos = (self.x, self.y)
        
        self.image = pygame.image.load('assets/revStand.png')
        size = self.image.get_rect().size
        self.imageR = pygame.transform.scale(self.image, (size[0]/2.5, size[1]/2.5))
        self.rect = self.imageR.get_rect()
        self.rect.x = self.x
        self.rect.bottom = self.y

        self.imageL = pygame.transform.flip(self.imageR, True, False)

    def update(self):
        self.rect.x += self.x_vel
        if(self.rect.right < 0):
           self.rect.left = 640
        elif(self.rect.left > 640):
            self.rect.right = 0

    def draw(self, screen, imgnum):
        if imgnum == 0:
            img = self.imageR
        elif imgnum == 1:
            img = self.imageL
        try:
            screen.blit(img, self.rect)
        except:
            screen.blit(self.imageR, self.rect)

class Treat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.y = 0
        self.x = random.randint(50, 580)

        self.y_vel = 10

        self.image = pygame.image.load('assets/treat.png').convert_alpha()
        size = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, (size[0]/25, size[1]/25))
        self.rect = self.image.get_rect()
        

        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self):
        self.rect.y += self.y_vel
        if(self.rect.top > 480):
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Bevo(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.y_vel = 10
        self.x = random.randint(50,580)

        self.image = pygame.image.load('assets/bevo.png').convert_alpha()
        size = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, (size[0]/20, size[1]/20))
        # self.image = pygame.transform.flip(self.image, False, True)  # Enables Upside down horn
        self.rect = self.image.get_rect()

        self.rect.bottom = 0
        self.rect.x = self.x

    def update(self):
        self.rect.y += self.y_vel
        if(self.rect.top > 480):
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Game loop.

font = pygame.font.Font('assets/pixelfont.ttf' , 18)
bigfont = pygame.font.Font('assets/Pixelfont.ttf', 45)
medfont = pygame.font.Font('assets/Pixelfont.ttf', 25)

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
    
    draw_text("RevCatch!", bigfont,(80,0,0), win, 140)
    draw_text("Help Reveille Catch Falling Treats,", medfont, (0,0,0), win, 180)
    draw_text("But watch out for falling Bevos!", medfont, (0,0,0), win, 210)
    draw_text("Move with A/D or Arrowkeys", medfont, (0,0,0), win, 240)
    draw_text("Press Any Key to Continue", font, (80,0,0), win, 270)


    pygame.display.flip()


rev = Rev()
treat_group = pygame.sprite.Group()
tu_group = pygame.sprite.Group()

bg0 = pygame.image.load('assets/ground.png') 
bg1 = pygame.image.load('assets/trees.png')
bg1 = pygame.transform.scale(bg1, (640, 480))
bg2 = pygame.image.load('assets/sky.png')
bg2 = pygame.transform.scale(bg2, (640, 480))

img = 0
count = 0
spawn_rate = 100
score = 0
alive = True
while True:
    win.fill((0,0,0))
    win.blit(bg2, (0,0))
    win.blit(bg1, (0,50))
    win.blit(bg0, (0, 425))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_a:
                rev.x_vel = -10
                img = 1
            if event.key == K_d:
                rev.x_vel = 10
                img = 0
            if event.key == K_q and not alive:
                Popen(['python3', 'menu.py'])
                quit()
            if event.key == K_r and not alive:
                alive = True
                score = 0
                spawn_rate = 100
                count = 0
                img = 0
                treat_group.empty()
                tu_group.empty()

        if event.type == KEYUP:
            if event.key == K_a or event.key == K_d:
                rev.x_vel = 0
   
    scoreout = 'Score = '+str(score)
    text = font.render(scoreout, True, (0,0,0))
    win.blit(text, (10,0))

    if alive:

        rev.update()

        count += 1
        if count % int(spawn_rate) == 0:
            new_treat = Treat()
            treat_group.add(new_treat)
        if count % int(spawn_rate+50) == 0:
            new_bevo = Bevo()
            tu_group.add(new_bevo)
        if count % 500 == 0:
            spawn_rate -= 2
            print(f'New spawn rate: {spawn_rate}')

        for treat in treat_group:
            if pygame.sprite.collide_rect(rev, treat):
                playSound(scoreSound)
                score += 1
                treat.kill()

        for bevo in tu_group:
            if pygame.sprite.collide_rect(rev, bevo):
                playSound(hurtSound)
                alive = False

  # Update.
    if alive:

        for treat in treat_group:
            treat.update()
        
        for bevo in tu_group:
            bevo.update()

    rev.draw(win, img)
    treat_group.draw(win)
    tu_group.draw(win)

    if not alive:
        pygame.draw.rect(win, (214,210,196), (130, 80, 380, 85))
        draw_text('GAME OVER', bigfont, (80,0,0), win, 100)
        draw_text(scoreout, medfont, (0,0,0), win, 130)
        draw_text('Return to menu: Q / Restart: R', font, (0,0,0), win, 153)

    pygame.display.flip()
    clock.tick(fps)


