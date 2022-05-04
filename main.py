import pygame
import random
import pygame_menu
import string

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
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Bar(pygame.sprite.Sprite):
    """Draw Player"""

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size_x = 70
        self.check_pow_1 = 0
        self.image = pygame.image.load("sprites/Bar_image.png")
        self.image = pygame.transform.scale(self.image, (self.size_x, 20))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.power_time = pygame.time.get_ticks()

    def update(self):
        if (self.check_pow_1 == 90 or self.check_pow_1 == 50) and pygame.time.get_ticks() - self.power_time > 10000:
            self.check_pow_1 = 0
            self.size_x = 70
            self.image = pygame.image.load("sprites/Bar_image.png")
            self.image = pygame.transform.scale(self.image, (self.size_x, 20))
            self.rect = self.image.get_rect()
            self.power_time = pygame.time.get_ticks()
            powerup_sound_done.play()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.borders_map()

    def borders_map(self):
        if self.rect.x < 2:
            self.x = 2
        if self.rect.x > 430:
            self.x = 430

    def big_bar(self):
        self.check_pow_1 = 90
        self.image = pygame.image.load("sprites/big_bar.png")
        self.image = pygame.transform.scale(self.image, (90, 20))
        self.rect = self.image.get_rect()
        self.power_time = pygame.time.get_ticks()

    def small_bar(self):
        self.check_pow_1 = 50
        self.image = pygame.image.load("sprites/small_bar.png")
        self.image = pygame.transform.scale(self.image, (50, 20))
        self.rect = self.image.get_rect()
        self.power_time = pygame.time.get_ticks()

    def reset(self):
        self.x = 215
        self.y = 480
        self.size_x = 70
        self.image = pygame.transform.scale(self.image, (self.size_x, 20))
        self.rect = self.image.get_rect()


class Ball(pygame.sprite.Sprite):
    """Draw Ball"""

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.ball_x = "left"
        self.ball_y = "up"
        self.speed = 2
        self.image = pygame.image.load("sprites/ball.png")
        self.image = pygame.transform.scale(self.image, (12, 12)).convert_alpha()
        self.rect = self.image.get_rect()
        self.moving = False
        self.power_time = pygame.time.get_ticks()

    def update(self):
        """The ball moves"""
        if (self.speed == 4 or self.speed == 1) and pygame.time.get_ticks() - self.power_time > 10000:
            self.speed = 2
            self.power_time = pygame.time.get_ticks()
            powerup_sound_done.play()

        if not self.moving:
            self.x = bar.rect.centerx - 4
        else:
            if self.ball_x == "left":
                self.x -= self.speed
                if self.x < 3:
                    self.ball_x = "right"
                    pong_bar_sound.play()
            if self.ball_y == 'down':
                self.y += self.speed
            if self.ball_y == 'up':
                self.y -= self.speed
                if self.y < 3:
                    self.ball_y = 'down'
                    pong_bar_sound.play()
            if self.ball_x == "right":
                self.x += self.speed
                if self.x > 490:
                    self.ball_x = "left"
                    pong_bar_sound.play()
        self.rect = self.image.get_rect()
        self.rect.x = ball.x
        self.rect.y = ball.y

    def start(self):
        self.moving = True

    def get_self_moving(self):
        return self.moving

    def get_speed(self):
        return self.speed

    def get_ball_y(self):
        return self.ball_y

    def set_ball_y(self, ball_y):
        self.ball_y = ball_y

    def get_ball_x(self):
        return self.ball_x

    def set_ball_x(self, ball_x):
        self.ball_x = ball_x

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
        self.ball_x = "left"


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

    def reset(self):
        self.score = 0


class Update_sprites:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.brick = None
        self.i = 0
        self.lvls = ['levels/lvl1', 'levels/lvl2', 'levels/lvl3',
                     'levels/lvl4', 'levels/lvl5', 'levels/lvl6',
                     'levels/lvl7', 'levels/lvl8', 'levels/lvl9', 'levels/lvl10']

    def new_lvl(self):
        self.all_sprites = pygame.sprite.Group()
        bar.reset()
        ball.reset()
        self.brick = create_bricks(self.lvls.pop(0))
        self.all_sprites.add(self.brick, ball, bar)
        self.print_new_lvl()

    def print_new_lvl(self):
        self.i += 1

    def print_lvl(self):
        return draw_text(screen, f'Level {self.i}', 18, 90 / 2, 9)

    def get_sprites(self):
        return self.all_sprites

    def get_brick(self):
        return self.brick

    def reset(self):
        self.all_sprites = pygame.sprite.Group()
        self.brick = None
        self.i = 0
        self.lvls = ['levels/lvl1', 'levels/lvl2', 'levels/lvl3',
                     'levels/lvl4', 'levels/lvl5', 'levels/lvl6',
                     'levels/lvl7', 'levels/lvl8', 'levels/lvl9', 'levels/lvl10']

    def get_lvls(self):
        return self.lvls


def collision():
    if ball.rect.colliderect(bar):
        if ball.y <= bar.y:
            ball.set_ball_y("up")
        else:
            if ball.get_ball_x() == "left":
                ball.set_ball_x("right")
            else:
                ball.set_ball_x("left")
        if ball.get_self_moving():
            pong_bar_sound.play()

    for n, brick in enumerate(spr.get_brick()):
        if ball.rect.colliderect(brick):
            score.plus()
            pong_sound.play()
            if random.random() > 0.8:
                pow = Pow(brick.rect.center)
                spr.get_sprites().add(pow)
                powerups.add(pow)
            if ball.get_ball_y() == "up":
                if ball.y >= (brick.y + 20):
                    ball.set_ball_y("down")
                else:
                    if ball.get_ball_x() == "left":
                        ball.set_ball_x("right")
                    else:
                        ball.set_ball_x("left")
            else:
                if ball.y <= brick.y:
                    ball.set_ball_y("up")
                else:
                    if ball.get_ball_x() == "left":
                        ball.set_ball_x("right")
                    else:
                        ball.set_ball_x("left")
            spr.get_brick().pop(n)
            brick.kill()
            if not spr.get_brick():
                if len(spr.get_lvls()) > 0:
                    spr.new_lvl()
                else:
                    input_leaderboard()

    if ball.y > 500:
        input_leaderboard()


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


def exit_game(even, loo):
    if even.type == pygame.QUIT:
        loo = 0
    if even.type == pygame.KEYUP:
        if even.key == pygame.K_ESCAPE:
            loo = 0
    return loo


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


def reset_data():
    ball.reset()
    bar.reset()
    spr.reset()
    score.reset()


font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


num = 0
powerups = pygame.sprite.Group()
score = Score()
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Game")
spr = Update_sprites()
bar = Bar(215, 480)
ball = Ball(25, 471)

"""Images"""
background_grey = pygame.image.load("background/grey.jpg")
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

def reference():
    def disable():
        menu.disable()
    menu = pygame_menu.Menu('Справка', 500, 500, theme=pygame_menu.themes.THEME_DARK)
    menu.add.label("Добро пожаловать в игру Arkanoid. \nДля управления платформой "
                   "\nнажимайте клавиши A и D, для \nзапуска шарика нажмите пробел.\n"
                   "Чтобы победить надо пройти все уровни. \nА так же набирайте больше очков,\n"
                   "чтобы быть в топе лидеров", max_char=-1, font_size=17)
    menu.add.button("Назад", disable)
    menu.mainloop(screen)

def leaderboard():
    menu = pygame_menu.Menu('Таблица лидеров', 500, 500, theme=pygame_menu.themes.THEME_DARK)
    table = menu.add.table(table_id='my_table', font_size=30)
    table.default_cell_padding = 5
    table.default_row_background_color = 'red'
    table.add_row(['Никнейм', 'Счет'], cell_font=pygame_menu.font.FONT_OPEN_SANS_BOLD)

    def disable():
        menu.disable()

    with open("data", 'r') as f:
        file_blocks = f.read().splitlines()[0:]

    def add_row(list_data):
        data_dict = dict()
        for item in list_data:
            key = item.split(" ")[0]
            value = item.split(" ")[1]
            data_dict[key] = int(value)
        a = (sorted(data_dict.items(), reverse=True, key=lambda kv: (kv[1], kv[0])))
        for key, value in a:
            mas = [key, value]
            table.add_row(mas)

    add_row(file_blocks)
    menu.add.button("Назад", disable)
    menu.mainloop(screen)

def input_leaderboard():
    menu = pygame_menu.Menu('Ввод данных', 500, 500, theme=pygame_menu.themes.THEME_DARK)
    check = False

    def disable():
        menu.disable()
        start_menu()

    def contains_whitespace(s):
        return True in [c in s for c in string.whitespace]

    def check_name(value):
        if not value.strip() or contains_whitespace(value):
            warning()
        else:
            file = open("data", "a")
            file.write(f"\n{value} {score.get_score()}")
            file.close()
            disable()
    if check:
        warning()
    menu.add.text_input('Никнейм: ', maxchar=10, input_underline='_', onreturn=check_name)
    menu.add.button("Назад", disable)
    menu.mainloop(screen)

def warning():
    def disable():
        input_leaderboard()
    menu = pygame_menu.Menu('Предупреждение', 500, 500, theme=pygame_menu.themes.THEME_DARK)
    menu.add.label("Ник содержит пробелы, уберите их", font_size=30)
    menu.add.button("Назад", disable)
    menu.mainloop(screen)

def start_game():
    pygame.mouse.set_visible(False)
    reset_data()
    spr.new_lvl()
    loop = 1
    while loop:
        screen.blit(background, (0, 0))
        keystate = pygame.key.get_pressed()
        for event in pygame.event.get():
            loop = exit_game(event, loop)
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
        show_bricks()
        collision_powerups()
        spr.get_sprites().draw(screen)
        draw_text(screen, str(score.get_score()), 18, 510 / 2, 10)
        spr.print_lvl()
        pygame.display.update()
        clock.tick(120)

def start_menu():
    menu_main = pygame_menu.Menu('Добро пожаловать', 500, 500, theme=pygame_menu.themes.THEME_DARK)
    menu_main.add.button('Начать игру', start_game)
    menu_main.add.button('Таблица лидеров', leaderboard)
    menu_main.add.button('Справка', reference)
    menu_main.add.button('Выход', pygame_menu.events.EXIT)
    menu_main.mainloop(screen)


start_menu()
