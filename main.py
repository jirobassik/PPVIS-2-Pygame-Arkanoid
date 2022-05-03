import pygame
import random
import pygame_menu
import sys

WHITE = (255, 255, 255)

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
        if color == 4:
            self.image = pygame.image.load("sprites/Brick_blue.png")
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
        self.size_x = 70
        self.image = pygame.image.load("sprites/Bar_image.png")
        self.image = pygame.transform.scale(self.image, (self.size_x, 20))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.power_time = pygame.time.get_ticks()

    def update(self):
        if (self.size_x == 90 or self.size_x == 50) and pygame.time.get_ticks() - self.power_time > 10000:
            self.size_x = 70
            self.image = pygame.transform.scale(self.image, (self.size_x, 20))
            self.power_time = pygame.time.get_ticks()
            powerup_sound_done.play()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.borders_map()

    def borders_map(self):
        if self.x < 2:
            self.x = 2
        if self.x > 430:
            self.x = 430

    def big_bar(self):
        self.size_x = 90
        self.image = pygame.transform.scale(self.image, (self.size_x, 20))
        self.power_time = pygame.time.get_ticks()

    def small_bar(self):
        self.size_x = 50
        self.image = pygame.transform.scale(self.image, (self.size_x, 20))
        self.power_time = pygame.time.get_ticks()

    def reset(self):
        self.x = 215
        self.y = 480
        self.size_x = 70
        self.image = pygame.transform.scale(self.image, (self.size_x, 20))

class Ball(pygame.sprite.Sprite):
    """Draw Ball"""
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = 2
        self.image = pygame.image.load("sprites/ball.png")
        self.image = pygame.transform.scale(self.image, (12, 12)).convert_alpha()
        self.rect = self.image.get_rect()
        self.moving = False
        self.power_time = pygame.time.get_ticks()

    def update(self):
        """The ball moves"""
        global ball
        global ball_x, ball_y
        if (self.speed == 4 or self.speed == 1) and pygame.time.get_ticks() - self.power_time > 10000:
            self.speed = 2
            self.power_time = pygame.time.get_ticks()
            powerup_sound_done.play()

        if not self.moving:
            self.x = bar.rect.centerx - 4
        else:
            if ball_x == "left":
                ball.x -= self.speed
                if ball.x < 3:
                    ball_x = "right"
                    pong_bar_sound.play()
            if ball_y == 'down':
                ball.y += self.speed
            if ball_y == 'up':
                ball.y -= self.speed
                if ball.y < 3:
                    ball_y = 'down'
                    pong_bar_sound.play()
            if ball_x == "right":
                ball.x += self.speed
                if ball.x > 490:
                    ball_x = "left"
                    pong_bar_sound.play()
        #gfxdraw.filled_circle(screen, ball.x, ball.y, 5, GREEN)
        #self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.rect = self.image.get_rect()
        self.rect.x = ball.x
        self.rect.y = ball.y

    def start(self):
        self.moving = True

    def get_self_moving(self):
        return self.moving

    def get_speed(self):
        return self.speed

    def move_faster(self):
        self.speed = 4
        self.power_time = pygame.time.get_ticks()

    def move_slover(self):
        self.speed = 1
        self.power_time = pygame.time.get_ticks()

    def reset(self):
        self.x = 25
        self.y = 471
        self.speed = 2
        self.moving = False

class Pow(pygame.sprite.Sprite):
    """Power ups"""
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['slower', 'faster', 'big_bar', 'small_bar', 'x2'])
        self.image = powerup_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > 500:
            self.kill()

class Score:
    def __init__(self):
        self.score = 0
        self.plus_score = 20
        self.power_time = pygame.time.get_ticks()

    def get_score(self):
        return self.score

    def plus(self):
        self.score += self.plus_score

    def double_score(self):
        self.plus_score = 40
        self.power_time = pygame.time.get_ticks()

    def check_time(self):
        if self.plus_score == 40 and pygame.time.get_ticks() - self.power_time > 10000:
            self.plus_score = 20
            self.power_time = pygame.time.get_ticks()
            powerup_sound_done.play()

def collision():
    global ball, bar, ball_y, ball_x

    if ball.rect.colliderect(bar):
        ball_y = "up"
        if ball.get_self_moving():
            pong_bar_sound.play()

    for n, brick in enumerate(spr.get_brick()):
        if ball.rect.colliderect(brick):
            score.plus()
            pong_sound.play()
            if random.random() > 0.7:
                pow = Pow(brick.rect.center)
                spr.get_sprites().add(pow)
                powerups.add(pow)
            if ball_y == "up":
                if ball.y == (brick.y + 20 - ball.get_speed()):
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
            spr.get_brick().pop(n)
            brick.kill()
            if not spr.get_brick():
                #pygame.quit()
                #sys.exit()
                spr.new_lvl()

    if ball.y > 500:
        ball.xb, ball.y = 500, 300

def collision_powerups():
    hits = pygame.sprite.spritecollide(bar, powerups, True)
    for hit in hits:
        if hit.type == 'faster':
            ball.move_faster()
            powerup_sound.play()
        if hit.type == 'slower':
            ball.move_slover()
            powerup_sound.play()
        if hit.type == 'big_bar':
            bar.big_bar()
            powerup_sound.play()
        if hit.type == 'small_bar':
            bar.small_bar()
            powerup_sound.play()
        if hit.type == 'x2':
            score.double_score()
            powerup_sound.play()


font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

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


def create_bricks(name_lvl):
    with open(name_lvl, 'r') as f:
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
            elif brick == "4":
                bricks.append(Brick(20 + w * 100, h, 4))
            w += 1
            if w == 5:
                w = 0
                h += 50
    return bricks


def show_bricks():
    for brick in spr.get_brick():
        brick.update()

class Update_sprites:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()

    def new_lvl(self):
        self.all_sprites = pygame.sprite.Group()
        bar.reset()
        ball.reset()
        self.brick = create_bricks(lvls.pop(0))
        self.all_sprites.add(self.brick, ball, bar)

    def get_sprites(self):
        return self.all_sprites

    def get_brick(self):
        return self.brick


lvls = ['levels/lvl1', 'levels/lvl2']

#all_sprites = pygame.sprite.Group()
powerups = pygame.sprite.Group()
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ball_x = 'left'
ball_y = 'down'
vel_bal = 2
score = Score()
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Game")
spr = Update_sprites()
startx = 0
bar = Bar(215, 480)
ball = Ball(25, 471)
spr.new_lvl()


"""Images"""
background = pygame.image.load("background/space.jpg")
image_1 = pygame.image.load("sprites/slower.png")
image_2 = pygame.image.load("sprites/faster.png")
image_3 = pygame.image.load("sprites/Bar_image.png")
image_4 = pygame.image.load("sprites/Bar_image.png")
image_5 = pygame.image.load("sprites/x2.png")

powerup_images = {'slower': pygame.transform.scale(image_1, (25, 25)).convert_alpha(),
                  'faster': pygame.transform.scale(image_2, (25, 25)).convert_alpha(),
                  'big_bar': pygame.transform.scale(image_3, (50, 10)).convert_alpha(),
                  'small_bar': pygame.transform.scale(image_4, (20, 10)).convert_alpha(),
                  'x2': pygame.transform.scale(image_5, (25, 25)).convert_alpha()}
"""Images"""

"""Sounds"""
pong_sound = pygame.mixer.Sound('sound/pong.wav')
pong_bar_sound = pygame.mixer.Sound('sound/pong_bar.wav')
powerup_sound = pygame.mixer.Sound('sound/powerup.wav')
powerup_sound_done = pygame.mixer.Sound('sound/powerup_done.wav')
pygame.mixer.music.load('sound/music.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)
"""Sounds"""

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
    powerups.update()
    score.check_time()
    collision()
    #startx = bar.x
    show_bricks()
    collision_powerups()
    spr.get_sprites().draw(screen)
    draw_text(screen, str(score.get_score()), 18, 510 / 2, 10)
    pygame.display.update()
    clock.tick(120)

pygame.quit()
