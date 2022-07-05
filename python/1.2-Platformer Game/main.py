# Jumpy!(a platform game)
import pygame as pg
import random
from settings import *
from sprites import *
from os import path


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        # for sounds
        pg.mixer.init()
        self.screen = pg.display.set_mode((screen_width, screen_height))
        pg.display.set_caption(title)
        # controls the speed of the game
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(font_name)
        self.load_data()

    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'images')
        with open(path.join(self.dir, hs_file), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        # load spritesheet images
        self.spritesheet = Spritesheet(path.join(img_dir, spritesheet))

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in platform_list:
            p = Platform(self, *plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game loop - update
        self.all_sprites.update()
        # check if player hits the platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.y < lowest.rect.centery:
                    self.player.pos.y = lowest.rect.top + 1
                    self.player.vel.y = 0
                    self.player.jumping = False

        # if player reaches top 1/4 of screen_width
        if self.player.rect.top <= screen_height / 4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= screen_height:
                    plat.kill()
                    self.score += 1
        # if self.player.rect.x <= 50:
        #     self.player.pos.x += abs(self.player.vel.x)
        #     for plat in self.platforms:
        #         plat.rect.x += abs(self.player.vel.x)
        # if self.player.rect.x >= screen_width -50:
        #     self.player.pos.x -= abs(self.player.vel.x)
        #     for plat in self.platforms:
        #         plat.rect.x -= abs(self.player.vel.x)

        # if die - Part 6
        if self.player.rect.bottom > screen_height:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # spawn new platforms to keep some average number
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            p = Platform(self, random.randrange(0, screen_width - width),
                         random.randrange(-75, -30))
            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        # Game loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # Game loop - drawing
        self.screen.fill(lightblue)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text('Score: ' + str(self.score),
                       22, white, screen_width/2, 15)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game start screen
        self.screen.fill(lightblue)
        self.draw_text(title, 48, black, screen_width/2, screen_height/4)
        self.draw_text('ARROW TO MOVE AND SPACE TO JUMP', 22,
                       black, screen_width/2, screen_height/2)
        self.draw_text('Press ENTER to play', 18, black,
                       screen_width/2, screen_height*3/4)
        self.draw_text('High Score:' + str(self.highscore),
                       22, white, screen_width/2, 18)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        if not self.running:
            return
        # game over screen
        self.screen.fill(lightblue)
        self.draw_text('GAME OVER', 48, black, screen_width/2, screen_height/4)
        self.draw_text('Score: ' + str(self.score), 30,
                       black, screen_width/2, screen_height/2)
        self.draw_text('Press ENTER to play', 18, black,
                       screen_width/2, screen_height*3/4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text('NEW HIGH SCORE!', 22, white,
                           screen_width/2, screen_height/2 + 40)
            with open(path.join(self.dir, hs_file), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text('High Score: ' + str(self.highscore),
                           22, white, screen_width/2, screen_height/2 + 40)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
