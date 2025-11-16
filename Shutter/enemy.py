import pygame
import random

try:
    from .config import *
except ImportError:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    RED = (255, 0, 0)
    ENEMY_SPEED = 2
    ENEMY_HEALTH = 1
    IMAGES_DIR = 'assets/images'


class Enemy(pygame.sprite.Sprite):
    def __init__(self, all_sprites, enemies, sound_manager):
        super().__init__(all_sprites)
        # Загрузка изображения
        try:
            image_path = os.path.join(IMAGES_DIR, 'enemy.png')
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (35, 35))
        except Exception as e:
            print(f"Ошибка загрузки изображения врага: {e}")
            self.image = pygame.Surface((35, 35), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, RED, [(0, 0), (35, 0), (17, 35)])

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.uniform(ENEMY_SPEED * 0.5, ENEMY_SPEED * 1.5)
        self.health = ENEMY_HEALTH
        enemies.add(self)
        self.sound_manager = sound_manager
        self.sound_manager.play_sound('enemy_spawn')

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True
        return False