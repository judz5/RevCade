import pygame, sys, random
from pygame.locals import *

pygame.init()

win = pygame.display.set_mode((500,700))

main_Font = pygame.font.Font('assets/Pixelfont.ttf', 75)
button_Font = pygame.font.Font('assets/Pixelfont.ttf', 30)
small_Font = pygame.font.Font('assets/Pixelfont.ttf', 20)


pygame.mixer.init()

songs = ['assets/sound/noble.mp3', 'assets/sound/hymn.mp3', 'assets/sound/spirit.mp3']
song = songs[random.randint(0,2)]

pygame.mixer.music.load(song)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

def playSound(sfx):
    pygame.mixer.Sound.play(sfx)

selectSound = pygame.mixer.Sound('assets/sound/blipSelect.wav')

class Button():

    def __init__(self, height, width, y, text):
        self.height = height
        self.width = width
        self.y = y
        self.rect = pygame.Rect(250-(self.width/2), self.y, self.width, self.height)
        self.text = text
        self.color = (0,0,0)

    def draw_button(self):
        pygame.draw.rect(win, self.color, self.rect)

    def add_text(self):
        draw_text(self.text, button_Font, (214,210,196), win, self.rect.centery)

def draw_text(text, font, color, surface, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(win.get_width()/2, y))
    #textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def check_hover(sel):
    # for button in buttons:
    #     if(button.rect.collidepoint(pos)):
    #         button.color = color.breaking_color
    #     else:
    #         button.color = color.platform_color
    buttons[sel].color = (32,32,32)

fps = 60
clock = pygame.time.Clock()

buttons = []

revrun = Button(75, 225, 225, 'RevRun')
flappyrev = Button(75, 225, 325, 'FlappyRev')
revcatch = Button(75, 225, 425, 'RevCatch')
stop = Button(75, 225, 525, 'Quit')

buttons.append(revrun)
buttons.append(flappyrev)
buttons.append(revcatch)
buttons.append(stop)

check = ''
selected = 0
while True:
    win.fill((214,210,196))

    draw_text('RevCade!', main_Font, (80,0,0), win, 100)
    draw_text('By: Judson Salinas', small_Font, (0,0,0), win, 150)

    for button in buttons:
        button.color = (62,62,62)
    check_hover(selected)

    if(check == 'RevRun'):
        import RevRun
    elif(check == 'FlappyRev'):
        import FlappyRev
    elif(check == 'RevCatch'):
        import RevCatch
    elif(check == 'Quit'):
        playSound(selectSound)
        pygame.quit()
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == KEYDOWN:
            if event.key == K_w:
                if(selected>0):
                    selected -= 1
                else:
                    selected = 3
            if event.key == K_s:
                if(selected<3):
                    selected += 1
                else:
                    selected = 0
            if event.key == K_DOWN:
                if(selected<3):
                    selected += 1
                else:
                    selected = 0
            if event.key == K_UP:
                if(selected>0):
                    selected -= 1
                else:
                    selected = 3
            if event.key == K_RETURN:
                playSound(selectSound)
                check = buttons[selected].text


    for button in buttons:
        button.draw_button()
        button.add_text()

    pygame.display.flip()
    clock.tick(fps)
