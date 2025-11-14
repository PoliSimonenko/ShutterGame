import pygame
from .config import *


class GameManager:
    def __init__(self):
        self.score = 0
        self.game_over = False
        self.enemy_spawn_timer = 0

        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self.font = pygame.font.Font(None, 36)
        self.health = 100

    def spawn_enemy(self):
        from enemy import Enemy
        Enemy([self.all_sprites, self.enemies])

    def check_collisions(self, player):
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, False, True)
        for enemy, bullets in hits.items():
            for bullet in bullets:
                if enemy.take_damage(bullet.damage):
                    from explosion import Explosion
                    Explosion(enemy.rect.center, [self.all_sprites, self.explosions])
                    self.score += 10

        hits = pygame.sprite.spritecollide(player, self.enemies, True)
        for hit in hits:
            from explosion import Explosion
            Explosion(hit.rect.center, [self.all_sprites, self.explosions])
            if player.take_damage(10):
                self.game_over = True
        self.health = player.health

    def draw_ui(self, screen):
        score_text = self.font.render(f"Счет: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        health_text = self.font.render(f"Здоровье: {self.health}", True, WHITE)
        screen.blit(health_text, (10, 50))

        if self.game_over:
            game_over_text = self.font.render("ИГРА ОКОНЧЕНА! Нажмите R для перезапуска", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)

    def reset_game(self):
        self.__init__()