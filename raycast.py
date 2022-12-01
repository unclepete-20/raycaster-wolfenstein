
# -*- coding: utf-8 -*- 
#----------------------------------------------------------------------------
# Creado por: Pedro Pablo Arriola Jimenez (20188)   
# Fecha de creación: 30/11/2022
# version ='1.0'
# ---------------------------------------------------------------------------
""" Proyecto 3: Raycaster that lets you play CASTLE WOLFENSTEIN""" 
# ---------------------------------------------------------------------------

# Imports
import pygame
from math import pi, cos, sin, atan2


class Raycaster (object):
    def __init__(self):
        
        pygame.init()
        
        self.gameDisplay = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption('CASTLE WOLFENSTEIN')
        _, _, self.width, self.height = self.gameDisplay.get_rect()
        self.blocksize = 50
        self.map = []
        self.zbuffer = [-float('inf') for z in range(0, 500)]
        self.player = {
			"x": self.blocksize + 20,
			"y": self.blocksize + 20,
			"a": 0,
			"fov": pi/3
		}
        
        self.wall1 = pygame.image.load('./sprites/wall1.png').convert()
        self.wall2 = pygame.image.load('./sprites/wall3.png').convert()
        self.wall3 = pygame.image.load('./sprites/wall4.png').convert()
        self.enemy = pygame.image.load('./sprites/enemy.png').convert()
        self.player_perspective = pygame.image.load('./sprites/player.png').convert()
        
        self.textures = {
            "1": self.wall1,
            "2": self.wall2,
            "3": self.wall3,
        }
        
        self.enemies = [
            {
                "x": 100,
                "y": 150,
                "texture": self.enemy
            }
        ]
        
        self.clock = pygame.time.Clock()
        
        # COLOR CONSTANTS
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.STEELBLUE = (70, 130, 180)
        self.BLUE = (0, 0, 255)
        self.LOSE = (255, 0, 0)
        self.BACKGROUND = (54, 35, 18)
        self.WIN = (0, 255, 0)

        # CONSTANTS FOR PLAYER INTERACTION
        self.PLAYER_SIZE = 0.125
        self.CAST_SIZE = 2.56
        self.PI_20 = 0.157

    def point(self, x, y, c=None):
        self.gameDisplay.set_at((x, y), c)

    def draw_rectangle(self, x, y, texture, size):
        for cx in range(x, x + size):
            for cy in range(y, y + size):
                tx = int((cx - x) * 12.8)
                ty = int((cy - y) * 12.8)
                c = texture.get_at((tx, ty))
                self.point(cx, cy, c)

    def draw_player(self, xi, yi, element, w=256, h=256):
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * self.PLAYER_SIZE)
                ty = int((y - yi) * self.PLAYER_SIZE)
                c = element.get_at((tx, ty))
                if c != (152, 0, 136, 255):
                    self.point(x, y, c)

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def cast_ray(self, a):
        d = 0
        cosa = cos(a)
        sina = sin(a)
        while True:
            x = int(self.player["x"] + d * cosa)
            y = int(self.player["y"] + d * sina)

            i = int(x / self.blocksize)
            j = int(y / self.blocksize)

            if self.map[j][i] != ' ':
                hitx = x - i * 50
                hity = y - j * 50
                if 1 < hitx < 49:
                    maxhit = hitx
                else:
                    maxhit = hity
                tx = int(maxhit * self.CAST_SIZE)
                return d, self.map[j][i], tx
            d += 1

    def draw_stake(self, x, h, tx, texture):
        h_half = h/2
        start = int(250 - h_half)
        end = int(250 + h_half)
        end_start_pro = 128 / (end - start)
        for y in range(start, end):
            ty = int((y - start) * end_start_pro)
            c = texture.get_at((tx, ty))
            self.point(x, y, c)

    def draw_sprite(self, sprite):
        sprite_a = atan2((sprite["y"] - self.player["y"]),
						 (sprite["x"] - self.player["x"]))
        sprite_d = ((self.player["x"] - sprite["x"]) ** 2 +
					(self.player["y"] - sprite["y"]) ** 2) ** 0.5
        sprite_size_half = int(250/sprite_d * 70)
        sprite_size = sprite_size_half * 2
        sprite_x = int(500 + (sprite_a - self.player["a"]) * 477.46 +
					   250 - sprite_size_half)
        sprite_y = int(250 - sprite_size_half)

        sprite_size_pro = 128/sprite_size
        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                if 500 < x < 1000 and self.zbuffer[x - 500] <= sprite_d:
                    tx = int((x - sprite_x) * sprite_size_pro)
                    ty = int((y - sprite_y) * sprite_size_pro)
                    c = sprite["texture"].get_at((tx, ty))
                    if c != (152, 0, 136, 255):
                        self.point(x, y, c)
                        self.zbuffer[x - 500] = sprite_d

    def render(self):
        for i in range(0, 1000):
            try:
                a = self.player["a"] - self.player["fov"] / \
                    2 + (i * 0.00105)
                d, m, tx = self.cast_ray(a)
                x = i
                h = (500 / (d * cos(a - self.player["a"]))) * 50
                self.draw_stake(x, h, tx, self.textures[m])
            except:
                self.player["x"] = 70
                self.player["y"] = 70
                self.game_over()

        for enemy in self.enemies:
            self.point(enemy["x"], enemy["y"], self.BLACK)
            self.draw_sprite(enemy)
		
        for x in range(0, 100, 10):
            for y in range(0, 100, 10):
                i = int(x * 0.1)
                j = int(y * 0.1)
                if self.map[j][i] != ' ':
                    y = 500 + y
                    x1 = 900 + x
                    self.draw_rectangle(x1, y, self.textures[self.map[j][i]], 10)

        self.point(int(self.player["x"] * 0.2) + 900, int(self.player["y"] * 0.2) + 500, self.LOSE)
		
        self.draw_player(400, 350, self.player_perspective)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, self.WHITE)
        return textSurface, textSurface.get_rect()
    
    def start_game(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        intro = False
                        self.game_start()
            
            self.gameDisplay.fill(self.BLUE)
            
            largeText = pygame.font.Font('./fonts/wolfenstein.ttf', 100)
            mediumText = pygame.font.Font('./fonts/wolfenstein.ttf', 50)
            smallText = pygame.font.Font('./fonts/wolfenstein.ttf', 30)
            
            TextSurf, TextRect = self.text_objects(
	        	"CASTLE WOLFENSTEIN", largeText)
            TextRect.center = (500, 250)
            self.gameDisplay.blit(TextSurf, TextRect)
            
            TextSurf, TextRect = self.text_objects(
				"PRESS SPACE TO ENTER THE GAME!", mediumText)
            TextRect.center = (500, 350)
            self.gameDisplay.blit(TextSurf, TextRect)
            
            TextSurf, TextRect = self.text_objects(
				"PRESS ESC IF YOU ARE NOT INTERESTED...", smallText)
            TextRect.center = (500, 450)
            self.gameDisplay.blit(TextSurf, TextRect)
            
            pygame.display.update()

    def game_over(self):
        lose_sound = pygame.mixer.Sound('./music/defeat.wav')
        pygame.mixer.Sound.play(lose_sound)
        pygame.mixer.music.stop()
		
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        intro = False
                        self.game_start()

            self.gameDisplay.fill(self.LOSE)
            
            largeText = pygame.font.Font('./fonts/wolfenstein.ttf', 100)
            mediumText = pygame.font.Font('./fonts/wolfenstein.ttf', 50)
            smallText = pygame.font.Font('./fonts/wolfenstein.ttf', 30)
            
            TextSurf, TextRect = self.text_objects(
	        	"YOU DIED", largeText)
            TextRect.center = (500, 250)
            self.gameDisplay.blit(TextSurf, TextRect)
            
            TextSurf, TextRect = self.text_objects(
				"PRESS R IF YOU DARE", mediumText)
            TextRect.center = (500, 350)
            self.gameDisplay.blit(TextSurf, TextRect)
            
            TextSurf, TextRect = self.text_objects(
				"PRESS ESC TO EXIT THE GAME", smallText)
            TextRect.center = (500, 450)
            self.gameDisplay.blit(TextSurf, TextRect)
            
            pygame.display.update()
			

    def game_win(self):
        win_sound = pygame.mixer.Sound('./music/victory.mp3')
        pygame.mixer.Sound.play(win_sound)
        pygame.mixer.music.stop()
		
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        intro = False
                        self.game_intro()

            self.gameDisplay.fill(self.WIN)
            
            largeText = pygame.font.Font('./fonts/wolfenstein.ttf', 100)
            mediumText = pygame.font.Font('./fonts/wolfenstein.ttf', 50)
            smallText = pygame.font.Font('./fonts/wolfenstein.ttf', 30)
            
            TextSurf, TextRect = self.text_objects(
	        	"YOU WON!", largeText)
            
            TextRect.center = (500, 250)
            self.gameDisplay.blit(TextSurf, TextRect)
            
            TextSurf, TextRect = self.text_objects(
				"PRESS R TO RESTART THE GAME", mediumText)
            TextRect.center = (500, 350)
            self.gameDisplay.blit(TextSurf, TextRect)
            
            TextSurf, TextRect = self.text_objects(
				"PRESS ESC TO EXIT THE GAME", smallText)
            TextRect.center = (500, 450)
            self.gameDisplay.blit(TextSurf, TextRect)
            
            pygame.display.update()
			

    def background_music(self):
        pygame.mixer.music.load('./music/wolfenstein.mp3')
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)

    def update(self):
        font = pygame.font.Font('./fonts/wolfenstein.ttf', 30)
        fps_counter = "FPS: " + str(round(self.clock.get_fps(), 3))
        text = font.render(fps_counter, True, self.STEELBLUE)
        return text


    def game_start(self):
        paused = False
        running = True
        d = 10
        self.background_music()
        while running:
            self.gameDisplay.fill(self.BACKGROUND)
            if not paused:
                self.gameDisplay.blit(self.update(), [100, 550])
                if (self.player["x"] >= 400 and self.player["x"] <= 420) and (self.player["y"] >= 250 and self.player["y"] <= 265):
                    self.game_win()
                self.render()
                pygame.display.flip()
                self.clock.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    running = False
                    exit(0)
                if e.type == pygame.KEYDOWN:
                    if not paused:
                        if e.key == pygame.K_LEFT:
                            self.player["a"] -= self.PI_20
                        if e.key == pygame.K_RIGHT:
                            self.player["a"] += self.PI_20
                        if e.key == pygame.K_UP:
                            self.player["x"] += int(d * cos(self.player["a"]))
                            self.player["y"] += int(d * sin(self.player["a"]))
                        if e.key == pygame.K_DOWN:
                            self.player["x"] -= int(d * cos(self.player["a"]))
                            self.player["y"] -= int(d * sin(self.player["a"]))
                    if e.key == pygame.K_SPACE:
                        paused = not paused
                if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:
                    if not paused:
                        if e.button == 4:
                            self.player['a'] -= self.PI_20
                        if e.button == 5:
                            self.player['a'] += self.PI_20
			
			



