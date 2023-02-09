import sys, pygame, random
from subprocess import Popen
from pygame.locals import * 
pygame.init()
 
fps = 60
clock = pygame.time.Clock()
 
width, height = 350, 500
win = pygame.display.set_mode((width, height))

pygame.mixer.init()

jumpSound = pygame.mixer.Sound('assets/sound/jump.wav')
hurtSound = pygame.mixer.Sound('assets/sound/hitHurt.wav')
scoreSound = pygame.mixer.Sound('assets/sound/pickupCoin.wav')
selectSound = pygame.mixer.Sound('assets/sound/blipSelect.wav')

pygame.mixer.music.load('assets/sound/noble.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

def playSound(sfx):
    pygame.mixer.Sound.play(sfx)

def draw_text(text, font, color, surface, y):
    # Draws Text centered in screen
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(win.get_width()/2, y))
    #textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.x = 10 
        self.y = 100
        self.pos = (self.x, self.y)

        self.y_vel = 0
        self.gravity = 0.5 
        self.jumpHeight = 7

        self.image = pygame.image.load('assets/revStand.png').convert_alpha()
        size = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, (size[0]/4, size[1]/4))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.isJumping = False
        
    def update(self):
        self.y_vel += self.gravity
        self.rect.y += self.y_vel

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def jump(self):
        playSound(jumpSound)
        self.y_vel = -10

class Tower(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.x_vel = -4

        self.imageBot=pygame.image.load('assets/watertower.png')
        size = self.imageBot.get_rect().size
        self.imageBot = pygame.transform.scale(self.imageBot, (size[0]/1.5, size[1]/1.5))
        self.imageTop = pygame.transform.flip(self.imageBot, False, True)
        self.rectBot = self.imageBot.get_rect()
        self.rectTop = self.imageTop.get_rect()
        self.rectTop.left = 350
        self.rectTop.bottom = random.randint(100, 300)
        self.rectBot.left = 350
        self.rectBot.top = self.rectTop.bottom + 175

    def update(self):
        self.rectTop.x += self.x_vel
        self.rectBot.x += self.x_vel
        if(self.rectTop.right < 0):
            self.kill()

    def draw(self, screen):
        screen.blit(self.imageBot, self.rectBot)
        screen.blit(self.imageTop, self.rectTop)

    def collide(self, player):
        if(pygame.Rect.colliderect(player.rect, self.rectTop) or pygame.Rect.colliderect(player.rect, self.rectBot)):
            return True
        return False

class Ground():
    def __init__(self):
        self.image = pygame.image.load('assets/ground.png')
        size = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, (size[0]/2, size[1]/2))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.x1 = 0
        self.x2 = self.width
        self.y = 450

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
        self.image = pygame.image.load('assets/sky.png')
        size = self.image.get_rect().size
        self.image = pygame.transform.scale(self.image, (size[0]/2, size[1]/2))
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.x1 = 0
        self.x2 = self.width
        self.y = 0

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
    
    draw_text("FlappyRev!", bigfont,(80,0,0), win, 120)
    draw_text("Help Reveille fly,", font, (0,0,0), win, 165)
    draw_text("But watch out for The", font, (0,0,0), win, 195)
    draw_text("Watertowers!", font, (0,0,0), win, 225)
    draw_text("Jump with space or Arrowkeys", font, (0,0,0), win, 255)
    draw_text("Press Any Key to Continue", font, (80,0,0), win, 285)

    pygame.display.flip()

rev = Player()
ground = Ground()
background = Back()
tower_group = pygame.sprite.Group()
tower_group.add(Tower())
# Game loop.
count = 0
alive = True
score = 0
while True:
    win.fill((0, 0, 0))
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                rev.jump()
            if event.key == K_q and not alive:
                Popen(['python3', 'menu.py'])
                quit()
            if event.key == K_r and not alive:
                alive = True
                rev.rect.y = 100
                rev.jump()
                score = 0
                count = 0
                tower_group.empty()
               
    if alive:

        ground.update(4)
        background.update(2.5)
        
        count += 1
        if(count % 150 == 0):
            tower = Tower()
            tower_group.add(tower)

        # Update.
        rev.update()

        if rev.rect.bottom >= 500 or rev.rect.bottom <= 0:
                playSound(hurtSound)
                alive = False

        for tower in tower_group:
            tower.update()
            if(rev.rect.x == tower.rectTop.x):
                playSound(scoreSound)
                score += 1

            if tower.collide(rev):
                playSound(hurtSound)
                alive = False


    background.draw(win)
    ground.draw(win)

    scoreout = 'Score = '+str(score)
    text = font.render(scoreout, True, (0,0,0))
    win.blit(text, (10,0))

    for tower in tower_group:
        tower.draw(win)
    rev.draw(win)

    if not alive:
        pygame.draw.rect(win, (214,210,196), (0, 80, 380, 85))
        draw_text('GAME OVER', bigfont, (80,0,0), win, 100)
        draw_text(scoreout, medfont, (0,0,0), win, 130)
        draw_text('Return to menu: Q / Restart: R', font, (0,0,0), win, 153)

    pygame.display.flip()
    clock.tick(fps)
