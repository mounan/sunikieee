from pygame.locals import *
import pygame
import sys
from pygame import key
import time
from random import randint


class Game_settings:
    step = 30
    legacy = 3
    w = 1000
    h = 700
    size = w, h
    snake_length = 5
    right_head = pygame.image.load("images/head.png")
    horizontal_body = pygame.image.load("images/snake_body.png")
    food_image = pygame.image.load("images/durian.png")
    sleeping_time = 0.005
    gameover_font = "fonts/CHICORY_.TTF"
    score_font = "fonts/04B_03__.TTF"
    bgm_music = "musics/bgm.mp3"
    game_over_music = "musics/gameover.mp3"

    def isDead(self, position):
        if position[0][0] < 0 or position[0][0] > self.w:
            return True
        if position[0][1] < 0 or position[0][1] > self.h:
            return True
        for i in range(1, len(position)):
            if position[0] == position[i]:
                return True
        return False

    def isEaten(self, position, x, y):
        if position[0][0] == x and position[0][1] == y and [x, y] in position:
            return True


class Snake:
    position = []
    step = Game_settings.step
    speed = [step, 0]
    legacy = Game_settings.legacy
    tmp_legacy = 0

    right_head = Game_settings.right_head
    left_head = pygame.transform.flip(right_head, True, False)
    up_head = pygame.transform.rotozoom(right_head, 90, 1)
    down_head = pygame.transform.rotozoom(right_head, -90, 1)
    tmp_head = right_head

    horizontal_body = Game_settings.horizontal_body
    vertical_body = pygame.transform.rotozoom(horizontal_body, 90, 1)
    tmp_body = horizontal_body

    def __init__(self, length):
        self.length = length
        for i in range(0, length):
            self.position.append([self.step * 3 - self.step * i, 300])
        print("len is :", len(self.position))

    def move_right(self):
        if self.speed[0] == 0:
            self.speed[0] = self.step
            self.speed[1] = 0
            self.tmp_head = self.right_head
            self.tmp_body = self.horizontal_body

    def move_left(self):
        if self.speed[0] == 0:
            self.speed[0] = -self.step
            self.speed[1] = 0
            self.tmp_head = self.left_head
            self.tmp_body = self.horizontal_body

    def move_up(self):
        if self.speed[1] == 0:
            self.speed[1] = -self.step
            self.speed[0] = 0
            self.tmp_head = self.up_head
            self.tmp_body = self.vertical_body

    def move_down(self):
        if self.speed[1] == 0:
            self.speed[1] = self.step
            self.speed[0] = 0
            self.tmp_head = self.down_head
            self.tmp_body = self.vertical_body

    def grow(self):
        length = len(self.position)
        self.position.append(
            [self.position[length-1][0]-self.speed[0], self.position[length-1][1]-self.speed[1]])

    def update(self):
        self.tmp_legacy += 1
        if self.tmp_legacy >= self.legacy:
            for i in range(len(self.position) - 1, 0, -1):
                self.position[i][0] = self.position[i-1][0]
                self.position[i][1] = self.position[i-1][1]
            self.position[0][0] += self.speed[0]
            self.position[0][1] += self.speed[1]
            self.tmp_legacy = 0

    def draw(self, surface):

        surface.blit(self.tmp_head, tuple(self.position[0]))
        for i in range(1, len(self.position)):
            surface.blit(self.tmp_body, tuple(self.position[i]))


class Durian:
    durian_image = Game_settings.food_image

    w = Game_settings.w
    h = Game_settings.h
    step = Game_settings.step

    x = 0
    y = 0

    def __init__(self):
        self.update()

    def update(self):
        self.x = randint(1, (self.w // self.step)-1) * self.step
        self.y = randint(1, (self.h // self.step)-1) * self.step

    def draw(self, surface):
        surface.blit(self.durian_image, (self.x, self.y))


class Game:

    black = 0, 0, 0
    white = 255, 255, 255
    new_game = 0
    size = 0
    screen = 0
    length = 0
    snake = 0
    durian = 0

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sunakieee")
        self.new_game = Game_settings()
        pygame.mixer.music.load(self.new_game.bgm_music)
        pygame.mixer.music.play(-1)
        self.size = self.new_game.size
        self.screen = pygame.display.set_mode(self.size)
        self.length = self.new_game.snake_length
        self.snake = Snake(self.length)
        self.durian = Durian()
        self.show_start_count()
        self.game_loop()

    def text_objects(self, text, font):
        textSurface = font.render(text, True, self.white)
        return textSurface, textSurface.get_rect()

    def show_start_count(self):
        clock = 5
        while(clock > 0):
            self.screen.fill(self.black)
            largeText = pygame.font.Font(self.new_game.score_font, 250)
            TextSurf, TextRect = self.text_objects(str(clock), largeText)
            TextRect.center = ((self.new_game.w/2), (self.new_game.h/2))
            self.screen.blit(TextSurf, TextRect)
            pygame.display.update()
            pygame.event.pump()
            clock -= 1
            time.sleep(1)

    def show_length(self, length):
        smallText = pygame.font.Font(self.new_game.score_font, 30)
        TextSurf, TextRect = self.text_objects(
            "length : " + str(length), smallText)
        TextRect.center = ((self.new_game.step*3 + 10),
                           (self.new_game.h-self.new_game.step))
        self.screen.blit(TextSurf, TextRect)
        pygame.display.update()
        pygame.event.pump()

    def game_over(self):
        pygame.mixer.music.load(self.new_game.game_over_music)
        pygame.mixer.music.play(-1)
        largeText = pygame.font.Font(self.new_game.gameover_font, 45)
        TextSurf, TextRect = self.text_objects("GAME OVER", largeText)
        TextRect.center = ((self.new_game.w/2), (self.new_game.h/2))
        self.screen.blit(TextSurf, TextRect)
        pygame.display.update()
        pygame.event.pump()
        self.show_length(self.length)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    def game_loop(self):
        while 1:
            self.show_length(self.length)
            time.sleep(self.new_game.sleeping_time)
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if keys[K_UP]:
                self.snake.move_up()
            if keys[K_DOWN]:
                self.snake.move_down()
            if keys[K_RIGHT]:
                self.snake.move_right()
            if keys[K_LEFT]:
                self.snake.move_left()

            self.snake.update()
            self.screen.fill(self.black)
            self.durian.draw(self.screen)
            self.snake.draw(self.screen)

            if self.new_game.isDead(self.snake.position):
                self.game_over()

            if self.new_game.isEaten(self.snake.position, self.durian.x, self.durian.y):
                self.length += 1
                self.snake.grow()
                self.durian.update()
                self.durian.draw(self.screen)
            pygame.display.flip()


GAME = Game()
