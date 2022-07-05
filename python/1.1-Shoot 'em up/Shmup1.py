#  Shmup Game
import pygame as pg
import random
from os import path

image_folder = path.join(path.dirname(__file__), 'images')
sound_folder = path.join(path.dirname(__file__), 'sounds')

screen_width = 480
screen_height = 600
FPS = 60

# define colors
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
cyan = (0, 255, 255)

# initialize game and create display screen
pg.init()
# for sounds
pg.mixer.init()
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('GAME')
clock = pg.time.Clock()

# to define score in game
font_name = pg.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# to define spawn new mob


def new_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 10
    fill = (pct / 100) * bar_length
    outline_rect = pg.Rect(x, y, bar_length, bar_height)
    fill_rect = pg.Rect(x, y, fill, bar_height)
    pg.draw.rect(surf, green, fill_rect)
    pg.draw.rect(surf, white, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "FIGHTER GAME", 60, screen_width/2, screen_height/4)
    draw_text(screen, 'Arrow Keys To Move And SpaceBar To Shoot',
              23, screen_width/2, screen_height/2)
    draw_text(screen, 'Press A Key To Begin', 18, screen_width/2, screen_height*3/4)
    pg.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYUP:
                waiting = False


# for player
class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        # for circle
        self.radius = 20
        # pg.draw.circle(self.image, yellow, self.rect.center, self.radius)
        self.rect.centerx = screen_width / 2
        self.rect.bottom = screen_height - 10
        self.speedx = 0
        self.shield = 100
        # self.shoot_delay = 250
        # self.last_shot = pg.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()

    def update(self):
        # check if time to unhide
        if self.hidden and pg.time.get_ticks() - self.hide_timer > 6000:
            self.hidden = False
            self.rect.centerx = screen_width / 2
            self.rect.bottom = screen_height - 10
        self.speedx = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_a] or keystate[pg.K_LEFT]:
            self.speedx = -8
        if keystate[pg.K_d] or keystate[pg.K_RIGHT]:
            self.speedx = 8
        # if keystate[pg.K_SPACE]:
        #     self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        # now = pg.time.get_ticks()
        # if now - self.last_shot > self.shoot_delay:
        #     self.last_shot = now
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

    def hide(self):
        # hides the player temporarily
        self.hidden = True
        self.hide_timer - pg.time.get_ticks()
        self.rect.center = (screen_width / 2, screen_height + 200)


# for enemies
class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_original = random.choice(meteor_images)
        self.image_original.set_colorkey(black)
        # to avoid the lag
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pg.draw.circle(self.image, yellow, self.rect.center, self.radius)
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-2, 2)
        # to rotate the meteor
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pg.time.get_ticks()

    # to rotate the mob
    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_original, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > screen_height + 10 or self.rect.left < -10 or self.rect.right > screen_width + 10:
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)


# for bullets
class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of screen
        if self.rect.bottom < 0:
            self.kill()


# for powerups
class PowerUps(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the bottom of screen
        if self.rect.top > screen_height:
            self.kill()


# for explosions
class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animations[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_animations[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animations[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Load all game graphics
background = pg.image.load(path.join(image_folder, 'bg_1_1.png')).convert()
background_rect = background.get_rect()
player_img = pg.image.load(path.join(image_folder, 'playerShip1_red.png')).convert()
player_mini_img = pg.transform.scale(player_img, (25, 15))
player_mini_img.set_colorkey(black)
bullet_img = pg.image.load(path.join(image_folder, 'laserRed16.png')).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png',
               'meteorBrown_big3.png', 'meteorBrown_med1.png', 'meteorBrown_small1.png',
               'meteorBrown_small2.png', 'meteorBrown_tiny2.png']
for img in meteor_list:
    meteor_images.append(pg.image.load(path.join(image_folder, img)).convert())
explosion_animations = {}
explosion_animations['large'] = []
explosion_animations['small'] = []
explosion_animations['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pg.image.load(path.join(image_folder, filename)).convert()
    img.set_colorkey(black)
    img_lg = pg.transform.scale(img, (75, 75))
    explosion_animations['large'].append(img_lg)
    img_sm = pg.transform.scale(img, (32, 32))
    explosion_animations['small'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    player_expl_img = pg.image.load(path.join(image_folder, filename)).convert()
    player_expl_img.set_colorkey(black)
    explosion_animations['player'].append(player_expl_img)
powerup_images = {}
powerup_images['shield'] = pg.image.load(path.join(image_folder, 'shield_gold.png')).convert()
powerup_images['gun'] = pg.image.load(path.join(image_folder, 'bolt_gold.png')).convert()

# Load all game sounds
shoot_sound = pg.mixer.Sound(path.join(sound_folder, 'sfx_laser1.ogg'))
explosion_sound = []
for sound in ['Explosion2.wav', 'Explosion4.wav']:
    explosion_sound.append(pg.mixer.Sound(path.join(sound_folder, sound)))
pg.mixer.music.load(path.join(sound_folder, 'tgfcoder-FrozenJam-SeamlessLoop (1).ogg'))
pg.mixer.music.set_volume(0.6)
player_die_sound = pg.mixer.Sound(path.join(sound_folder, 'rumble1.ogg'))


pg.mixer.music.play(loops=-1)

# Game Loop
running = True
game_over = True
while game_over:
    if running:
        show_go_screen()
        running = False
        all_sprites = pg.sprite.Group()
        mobs = pg.sprite.Group()
        bullets = pg.sprite.Group()
        powerups = pg.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            new_mob()

        score = 0
    # keep loop running in right speed
    clock.tick(FPS)

    # Process input(events)
    for event in pg.event.get():

        # check for closing window
        if event.type == pg.QUIT:
            game_over = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # check to see if a bullet hit the mob
    hits = pg.sprite.groupcollide(mobs, bullets, True, True)
    # for looping the enemy
    for hit in hits:
        score += 50
        random.choice(explosion_sound).play()
        expl = Explosion(hit.rect.center, 'large')
        all_sprites.add(expl)
        if random.random() > 0.8:
            power = PowerUps(hit.rect.center)
            all_sprites.add(power)
            powerups.add(power)
        new_mob()

    # check to see if a mob hit the player
    hits = pg.sprite.spritecollide(
        player, mobs, True, pg.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'large')
        all_sprites.add(expl)
        new_mob()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # check to see if a player hits the powerup
    hits = pg.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 20)
            if player.shield >= 100:
                player.shield = 100

    # if player died and the explosion has finished playing
    if player.lives == 0 and not death_explosion.alive():
        running = True

    # Draw / Render
    screen.fill(black)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, 'Score: ' + str(score), 20, screen_width/2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, screen_width - 100, 5, player.lives, player_mini_img)

    # *after* drawing everything, flip the display
    pg.display.flip()

pg.quit()
