import pygame

#color definition
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0 , 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0) 
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

COLORS=[RED, ORANGE, YELLOW, GREEN, BLUE]

#screen dimension
screen = 0
screen_width, screen_height = 365, 500

#entities
player = ""
ball = ""
block = ""
line = ""

#lists
blocks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

#score var
score = 0

#text related variables
score_text = ""
font = ""
testo_continua = "Premi spazio per continuare"
testo_defeat = "Punteggio negativo, hai perso!"
testo_win = "Hai vinto, complimenti!"

#game settings
running = True
paused = False
timer = 1000
clock = pygame.time.Clock()

#ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, radius, vel):

        super().__init__()

        self.changing = False
        self.vel = vel
        self.width = self.height = radius * 2
        self.facing = 'right'
        self.radius = radius

        self.image = pygame.Surface([radius * 2, radius * 2])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.circle(self.image, color, [radius, radius], radius)

        self.rect = self.image.get_rect()

    def move(self):
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]

#player
class Player(pygame.sprite.Sprite):

    def __init__(self, velocity, color, width, height):
        
        super().__init__()

        self.velocity = velocity
        self.width = width
        self.height = height
        self.facing = 'right'

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()


    def moveRight(self, vel):
        self.rect.x += vel
        self.facing = 'right'

    def moveLeft(self, vel):
        self.rect.x -= vel
        self.facing = 'left'

#blocks
class Block(pygame.sprite.Sprite):

    def __init__(self, color, width, height):

        super().__init__()

        self.width = width
        self.height = height

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()

#trajectory
class Line(pygame.sprite.Sprite):

    def __init__(self, start, end, color, thickness = 1):
        
        super().__init__()

        self.color = color
        self.thickness = thickness
        self.width = end[0] - start[0]
        self.height = end[1] - start[1]

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.line(self.image, self.color, (0,0), (self.width, self.height))

        self.rect = self.image.get_rect()


def screen_init():

    global screen_width, screen_height, screen

    pygame.init()
    screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.set_caption("Breakout")


def create_ball():

    global ball, all_sprites

    ball = Ball(PURPLE, 9, [4, 4])
    ball.rect.x = 250
    ball.rect.y = 250
    all_sprites.add(ball)


def create_player():

    global player

    player = Player(5, WHITE, 60, 10)
    player.rect.x = 250
    player.rect.y = 450
    all_sprites.add(player)

def create_blocks():

    global block, blocks

    num_blocks = 44
    i = 0
    j = 0
    h = 0
    bheight, bwidth = 20, 40
    for i in range(num_blocks):
        block = Block(COLORS[h], bwidth, bheight)
        if 5 + 45*j + 40 <= screen_width:
            block.rect.x = 5 + 45*j
            j += 1
        else:
            j = 0
            block.rect.x = 5
            h += 1    
        block.rect.y = 5 + (bheight + 5)*h
        blocks.add(block)
        all_sprites.add(block)


def create_trajectory():

    global line

    line = Line([260, 260], [screen_width, 370], RED)
    line.rect.x = line.rect.y = 260


def create_text():

    global font, score, score_text

    font = pygame.font.SysFont("lucida console", 15)
    score = 0
    score_text = font.render("Score: {}".format(score), True, WHITE)

def init_scene():
    screen_init()
    create_ball()
    create_player()
    create_blocks()
    create_trajectory()
    create_text()



#mainloop
init_scene()

#ciclo del gioco
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #ritorno testo bianco
    score_text = font.render("Score: {}".format(score), True, WHITE)

    #controllo tasti premuti
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        if player.rect.x + player.width < screen_width:
            player.moveRight(player.velocity)

    if keys[pygame.K_LEFT]:
        if player.rect.x > 0:
            player.moveLeft(player.velocity)

    if not(paused):
        ball.move()
        #controllo collisione pallina con blocchi
        ball.changing = False
        for block in blocks:
            if pygame.sprite.collide_mask(ball, block) and (ball.rect.right >= block.rect.left or ball.rect.left <= block.rect.right) and ball.rect.y - ball.vel[1] < block.rect.bottom :
                if not(ball.changing):
                    ball.changing = True
                    ball.vel[0] = -ball.vel[0]
                    score += 5
                    score_text = font.render("Score: {}".format(score), True, WHITE)
                blocks.remove(block)
                all_sprites.remove(block)

            elif pygame.sprite.collide_mask(ball, block):
                if not(ball.changing):
                    ball.changing = True
                    ball.vel[1] = -ball.vel[1]
                    score += 5
                    score_text = font.render("Score: {}".format(score), True, WHITE)
                blocks.remove(block)
                all_sprites.remove(block)


        #controllo collisioni pallina con lo schermo
        if ball.rect.x + ball.width + ball.vel[0] > screen_width or ball.rect.x < 0:
            ball.vel[0] = -ball.vel[0]
            if ball.facing == 'right':
                ball.facing = 'left'
            if ball.facing == 'left':
                ball.facing = 'right'

        if ball.rect.y < 0:
            ball.vel[1] = -ball.vel[1]

        #controllo collisione pallina con giocatore
        if pygame.sprite.collide_mask(ball, player):
            ball.vel[1] = -ball.vel[1]
            if player.facing == ball.facing and ball.vel[0] < 7:
                ball.vel[0] += 1
            if player.facing != ball.facing and ball.vel[0] > 3:
                ball.vel[0] -= 1

        #controllo se la pallina e' caduta
        if ball.rect.y > screen_height:
            score -= 10
            score_text = font.render("Score: {}".format(score), True, RED)
            ball.rect.x = ball.rect.y = 250
            ball.vel = [4, 4]
            paused = True

        #controllo punteggio
        if len(blocks.sprites()) == 0:
            score_text = font.render(testo_win, True, GREEN)
            ball.vel = [0, 0]

    else:
        if score >= 0:
            score_text = font.render(testo_continua, True, RED)
            all_sprites.add(line)
            if keys[pygame.K_SPACE]:
                paused = False
                all_sprites.remove(line)
        else:
            score_text = font.render(testo_defeat, True, RED)

    #aggiornamento dei movimenti
    blocks.update()
    all_sprites.update()

    #disegno dello schermo
    screen.fill(BLACK)
    screen.blit(score_text, [5, 475])
    all_sprites.draw(screen)
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
