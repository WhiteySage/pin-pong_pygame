import os
import random
import sys

import pygame

os.environ['SDL_VIDEO_CENTERED'] = '1'


class Game:
    def __init__(self, WIDTH_screen, HEIGHT_screen):
        pygame.init()
        self.WIDTH_screen = WIDTH_screen
        self.HEIGHT_screen = HEIGHT_screen
        self.window = pygame.display.set_mode((self.WIDTH_screen, self.HEIGHT_screen))
        self.font_score = pygame.font.SysFont('arial', int(self.WIDTH_screen / 20))
        self.font_text = pygame.font.SysFont('arial', 15)
        pygame.display.set_caption("Pin-Pong")

        self.clock = pygame.time.Clock()
        self.running = True

        # Create game objects

        self.player = pygame.Rect(self.WIDTH_screen - 50, self.HEIGHT_screen / 2 - 50, 10, 100)
        self.opponent = pygame.Rect(50, self.HEIGHT_screen / 2 - 50, 10, 100)
        self.player_score, self.opponent_score = 0, 0
        self.ball = pygame.Rect(self.WIDTH_screen / 2, self.HEIGHT_screen / 2 - 10, 20, 20)
        self.x_speed, self.y_speed = 2, 2

    def processInput(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP]:
            if self.player.top > 0:
                self.player.top -= 4
        if key_pressed[pygame.K_DOWN]:
            if self.player.bottom < self.HEIGHT_screen:
                self.player.bottom += 4
        if key_pressed[pygame.K_r]:
            self.player_score, self.opponent_score = 0, 0
            self.ball.center = (self.WIDTH_screen / 2, self.HEIGHT_screen / 2)
            self.player = pygame.Rect(self.WIDTH_screen - 50, self.HEIGHT_screen / 2 - 50, 10, 100)
            self.opponent = pygame.Rect(50, self.HEIGHT_screen / 2 - 50, 10, 100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def game_logic(self):

        self.ball.x += self.x_speed * 2
        self.ball.y += self.y_speed * 2

        if self.ball.y >= self.HEIGHT_screen:
            self.y_speed = -2
        if self.ball.y <= 0:
            self.y_speed = 2
        if self.ball.x <= 0:
            self.player_score += 1
            self.ball.center = (self.WIDTH_screen / 2, self.HEIGHT_screen / 2)
            self.x_speed, self.y_speed = random.choice([2, -2]), random.choice([2, -2])
        if self.ball.x >= self.WIDTH_screen:
            self.opponent_score += 1
            self.ball.center = (self.WIDTH_screen / 2, self.HEIGHT_screen / 2)
            self.x_speed, self.y_speed = random.choice([2, -2]), random.choice([2, -2])

        if self.player.x - self.ball.width <= self.ball.x <= self.player.x and self.ball.y in range(
                self.player.top - self.ball.width,
                self.player.bottom + self.ball.width):
            self.x_speed = -2
        if self.opponent.x - self.ball.width <= self.ball.x <= self.opponent.x and self.ball.y in range(
                self.opponent.top - self.ball.width,
                self.opponent.bottom + self.ball.width):
            self.x_speed = 2

        # opponent logic
        opponent_speed = random.choice([3.3, 3.5, 3.7])

        if self.opponent.y < self.ball.y:
            self.opponent.top += opponent_speed
        if self.opponent.bottom > self.ball.y:
            self.opponent.bottom -= opponent_speed

    def update(self):
        pass

    def render(self):

        # Text fields
        player_score_text = self.font_score.render(str(self.player_score), True, 'white')
        opponent_score_text = self.font_score.render(str(self.opponent_score), True, 'white')
        restart_text = self.font_text.render(str('press R for restart game'), True, 'white')

        self.window.fill('black')
        pygame.draw.circle(self.window, 'white', self.ball.center, 10)
        pygame.draw.rect(self.window, 'red', self.player)
        pygame.draw.rect(self.window, 'green', self.opponent)
        self.window.blit(player_score_text, (self.WIDTH_screen / 2 + 50, 50))
        self.window.blit(opponent_score_text, (self.WIDTH_screen / 2 - 50, 50))
        self.window.blit(restart_text, (900, 75))
        pygame.display.update()

    def run(self):
        while self.running:
            self.processInput()
            self.game_logic()
            self.update()
            self.render()
            self.clock.tick(60)


game = Game(1280, 768)
game.run()
