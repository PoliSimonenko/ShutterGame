import pygame
import sys
from .config import *
from player import Player
from game_manager import GameManager


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_manager = GameManager()
        self.player = Player(
            [self.game_manager.all_sprites],
            self.game_manager.bullets)
        try:
            pygame.mixer.music.load(os.path.join(SOUNDS_DIR, 'background.mp3'))
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except:
            print("Фоновая музыка не найдена")

    def handle_events(self):
        # Цикл обработки событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_manager.game_over:
                    self.restart_game()
                elif event.key == pygame.K_SPACE and not self.game_manager.game_over:
                    self.player.shoot()
        return True

    def update(self):
        if not self.game_manager.game_over:
            now = pygame.time.get_ticks()
            if now - self.game_manager.enemy_spawn_timer > ENEMY_SPAWN_DELAY:
                self.game_manager.spawn_enemy()
                self.game_manager.enemy_spawn_timer = now

            self.game_manager.all_sprites.update()
            self.game_manager.bullets.update()
            self.game_manager.check_collisions(self.player)

    def draw(self):
        self.screen.fill(BLACK)
        self.game_manager.all_sprites.draw(self.screen)
        self.game_manager.bullets.draw(self.screen)
        self.game_manager.draw_ui(self.screen)
        pygame.display.flip()

    def restart_game(self):
        self.game_manager.reset_game()
        self.player = Player(
            [self.game_manager.all_sprites],
            self.game_manager.bullets
        )

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()