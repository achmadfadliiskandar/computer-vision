import pygame
from pygame.locals import *
from random import randint, seed
import time

TILE_SIZE = 50
MAZE_WIDTH = 20
MAZE_HEIGHT = 15
MAX_LEVEL = 10

def generate_maze(level):
    seed(level)
    maze = [[1 for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]
    for y in range(1, MAZE_HEIGHT - 1):
        for x in range(1, MAZE_WIDTH - 1):
            if randint(0, 10) > level + 2:
                maze[y][x] = 0

    x, y = 1, 1
    while x < MAZE_WIDTH - 2 or y < MAZE_HEIGHT - 2:
        maze[y][x] = 0
        if x < MAZE_WIDTH - 2 and randint(0, 1):
            x += 1
        elif y < MAZE_HEIGHT - 2:
            y += 1
    maze[13][18] = 0
    return maze

class CEvent:
    def on_key_down(self, event):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]: return 'keKiri'
        elif keys[K_RIGHT]: return 'keKanan'
        elif keys[K_UP]: return 'keAtas'
        elif keys[K_DOWN]: return 'keBawah'
        elif keys[K_q]: return 'keluar'

class App:
    def __init__(self):
        pygame.init()
        self.event = CEvent()
        self._running = True
        self.size = self.weight, self.height = TILE_SIZE * MAZE_WIDTH, TILE_SIZE * MAZE_HEIGHT
        self._display_surf = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.level = 1
        self.game_over = False
        self.game_win = False
        self.score = 0

        self.pacman = pygame.image.load("pacman.jpeg")
        self.apple = pygame.image.load("apple.jpeg")
        self._pacman_surf = pygame.transform.scale(self.pacman.convert_alpha(), (TILE_SIZE, TILE_SIZE))
        self._apple_surf = pygame.transform.scale(self.apple.convert_alpha(), (TILE_SIZE, TILE_SIZE))

        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.reset_game()

    def reset_game(self):
        if self.level > MAX_LEVEL:
            self.game_win = True
            return

        self.MAZE_MAP = generate_maze(self.level)
        self.pm_posx, self.pm_posy = 1, 1
        self.place_apple()
        self.start_time = time.time()
        self.level_time = 30 - (self.level * 2)

    def place_apple(self):
        self.apple_posx, self.apple_posy = 18, 13
        while self.MAZE_MAP[self.apple_posy][self.apple_posx] == 1:
            self.apple_posx = randint(1, MAZE_WIDTH - 2)
            self.apple_posy = randint(1, MAZE_HEIGHT - 2)

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        elif event.type == KEYDOWN:
            state = self.event.on_key_down(event)
            if state:
                if state == 'keluar':
                    self._running = False
                    return

                if self.game_over or self.game_win:
                    self.level = 1
                    self.score = 0
                    self.game_over = False
                    self.game_win = False
                    self.reset_game()
                    return

                dx, dy = 0, 0
                if state == 'keKiri': dx = -1
                elif state == 'keKanan': dx = 1
                elif state == 'keAtas': dy = -1
                elif state == 'keBawah': dy = 1

                new_x = self.pm_posx + dx
                new_y = self.pm_posy + dy
                if self.MAZE_MAP[new_y][new_x] == 0:
                    self.pm_posx = new_x
                    self.pm_posy = new_y

    def on_loop(self):
        if self.game_over or self.game_win:
            return

        if self.pm_posx == self.apple_posx and self.pm_posy == self.apple_posy:
            self.score += 10
            self.level += 1
            self.reset_game()

        elapsed_time = time.time() - self.start_time
        if elapsed_time > self.level_time:
            self.game_over = True

    def on_render(self):
        self._display_surf.fill((255, 255, 255))
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                if self.MAZE_MAP[y][x] == 1:
                    pygame.draw.rect(self._display_surf, (255, 0, 0), (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))

        if not self.game_win:
            self._display_surf.blit(self._apple_surf, (self.apple_posx*TILE_SIZE, self.apple_posy*TILE_SIZE))
            self._display_surf.blit(self._pacman_surf, (self.pm_posx*TILE_SIZE, self.pm_posy*TILE_SIZE))

        score_text = self.my_font.render(f'Score: {self.score} | Level: {self.level}', True, (0, 0, 0))
        self._display_surf.blit(score_text, (10, 10))

        if not self.game_win:
            time_left = max(0, int(self.level_time - (time.time() - self.start_time)))
            time_text = self.my_font.render(f'Time Left: {time_left}s', True, (0, 0, 0))
            self._display_surf.blit(time_text, (10, 40))

        if self.game_over:
            game_over_text = self.my_font.render(f"Game Over! Final Score: {self.score}", True, (255, 0, 0))
            restart_text = self.my_font.render("Press any arrow key to restart", True, (0, 0, 0))
            self._display_surf.blit(game_over_text, (MAZE_WIDTH * TILE_SIZE // 2 - game_over_text.get_width() // 2, MAZE_HEIGHT * TILE_SIZE // 2 - 30))
            self._display_surf.blit(restart_text, (MAZE_WIDTH * TILE_SIZE // 2 - restart_text.get_width() // 2, MAZE_HEIGHT * TILE_SIZE // 2 + 10))

        elif self.game_win:
            win_text = self.my_font.render(f"You Win! Final Score: {self.score}", True, (0, 128, 0))
            restart_text = self.my_font.render("Press any arrow key to restart", True, (0, 0, 0))
            self._display_surf.blit(win_text, (MAZE_WIDTH * TILE_SIZE // 2 - win_text.get_width() // 2, MAZE_HEIGHT * TILE_SIZE // 2 - 30))
            self._display_surf.blit(restart_text, (MAZE_WIDTH * TILE_SIZE // 2 - restart_text.get_width() // 2, MAZE_HEIGHT * TILE_SIZE // 2 + 10))

        pygame.display.flip()

    def on_execute(self):
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self.clock.tick(10)
        pygame.quit()

if __name__ == "__main__":
    App().on_execute()
