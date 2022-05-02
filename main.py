import pygame
import pygame_menu
import sys


class Brick(pygame.sprite.Sprite):
    """Draw Brick"""
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        if color == 1:
            self.image = pygame.image.load("sprites/Brick_green.png")
        if color == 2:
            self.image = pygame.image.load("sprites/Brick_red.png")
        if color == 3:
            self.image = pygame.image.load("sprites/Brick_yellow.png")
        self.image = pygame.transform.scale(self.image, (70, 30)).convert_alpha()
        self.rect = self.image.get_rect()
        #self.rect = pygame.Rect(self.x, self.y, 60, 20)
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        #pygame.draw.rect(screen, GREEN, (self.x, self.y, 60, 20))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Bar(pygame.sprite.Sprite):
    """Draw Player 2"""
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load("sprites/Bar_image.png")
        self.image = pygame.transform.scale(self.image, (70, 20))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        #self.rect = self.image.get_rect()
        #pygame.draw.rect(screen, RED, (self.x, self.y, 60, 10))
        #self.rect = pygame.Rect(self.x, self.y, 60, 10)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.borders_map()

    def borders_map(self):
        if self.x < 2:
            self.x = 2
        if self.x > 430:
            self.x = 430

class Ball(pygame.sprite.Sprite):
    """Draw Ball"""
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pygame.image.load("sprites/ball.png")
        self.image = pygame.transform.scale(self.image, (12, 12))
        self.rect = self.image.get_rect()
        self.moving = False

    def update(self):
        "The ball moves"
        global ball
        global ball_x, ball_y

        if not self.moving:
            self.x = bar.rect.centerx - 4
        else:
            if ball_x == "left":
                ball.x -= vel_bal
                if ball.x < 3:
                    ball_x = "right"
            if ball_y == 'down':
                ball.y += vel_bal
            if ball_y == 'up':
                ball.y -= vel_bal
                if ball.y < 3:
                    ball_y = 'down'
            if ball_x == "right":
                ball.x += vel_bal
                if ball.x > 490:
                    ball_x = "left"
        #gfxdraw.filled_circle(screen, ball.x, ball.y, 5, GREEN)
        #self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.rect = self.image.get_rect()
        self.rect.x = ball.x
        self.rect.y = ball.y

    def start(self):
        self.moving = True

def collision():
    global ball, bar, ball_y, ball_x

    if ball.rect.colliderect(bar):
        #print("Collision detected")
        ball_y = "up"
        #print(ball_y)
        #print(ball.y)
        #speed_up()

    for n, brick in enumerate(bricks):
        if ball.rect.colliderect(brick):
            print("You hit a brick")
            if ball_y == "up":
                if ball.y == (brick.y + 20 - vel_bal):
                    ball_y = "down"
                else:
                    if ball_x == "left":
                        ball_x = "right"
                    else:
                        ball_x = "left"
            else:
                if ball.y <= brick.y:
                    ball_y = "up"
                else:
                    if ball_x == "left":
                        ball_x = "right"
                    else:
                        ball_x = "left"
            bricks.pop(n)
            brick.kill()
            if bricks == []:
                pygame.quit()
                sys.exit()

    if ball.y > 500:
        ball.xb, ball.y = 500, 300


def exit_game(event):
    global loop
    if event.type == pygame.QUIT:
        loop = 0
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_ESCAPE:
            loop = 0
    return loop


'''def speed_up():
    global bar, vel_bal
    bar.x = pygame.mouse.get_pos()[0]
    if (startx - bar.x) > 0:
        ball_x = "right"
    else:
        ball_x = "left"
        # vel_bal = 3
        # print("Speed up")'''


def create_bricks():
    with open('levels/lvl1', 'r') as f:
        file_blocks = f.read().splitlines()[0:]
    bricks = []
    h = 30
    w = 0
    for line in file_blocks:
        for brick in line:
            if brick == "1":
                bricks.append(Brick(20 + w * 100, h, 1))
            elif brick == "2":
                bricks.append(Brick(20 + w * 100, h, 2))
            elif brick == "3":
                bricks.append(Brick(20 + w * 100, h, 3))
            w += 1
            if w == 5:
                w = 0
                h += 50
    return bricks


def show_bricks():
    for brick in bricks:
        brick.update()

all_sprites = pygame.sprite.Group()
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ball_x = 'left'
ball_y = 'down'
scorep1 = 0
scorep2 = 0
vel_bal = 2
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Game")
startx = 0
bar = Bar(10, 480)
ball = Ball(25, 471)
bricks = create_bricks()
all_sprites.add(bricks, ball, bar)
background = pygame.image.load("background/space.jpg")
pygame.mouse.set_visible(False)
loop = 1
while loop:
    screen.blit(background, (0, 0))
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        loop = exit_game(event)
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_a]:
        bar.x -= 8
    if keystate[pygame.K_d]:
        bar.x += 8
    if keystate[pygame.K_SPACE]:
        ball.start()
    bar.update()
    ball.update()
    collision()
    #startx = bar.x
    show_bricks()
    all_sprites.draw(screen)
    pygame.display.update()
    clock.tick(120)

pygame.quit()

