# Game Option / Settings
title = 'Jumpy!'
screen_width = 480
screen_height = 600
FPS = 60
font_name = 'arial'
hs_file = 'highscore.txt'
spritesheet = 'spritesheet_jumper.png'

# player properties
player_acc = 0.5
player_gravity = 0.5
player_friction = -0.10
player_jump = 20

# Starting platforms
platform_list = [(0, screen_height - 40),
                 (screen_width / 2 - 50, screen_height * 3 / 4),
                 (125, screen_height - 350),
                 (350, 200), (175, 100)]

# define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
lightblue = (0, 155, 155)
green = (0, 255, 0)
