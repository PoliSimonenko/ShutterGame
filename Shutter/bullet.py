import pygame
import os

try:
    from .config import *
except ImportError:
    GREEN = (0, 255, 0)
    BULLET_SPEED = 7
    BULLET_DAMAGE = 1
    IMAGES_DIR = 'assets/images'


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Загрузка изображения
        try:
            image_path = os.path.join(IMAGES_DIR, 'bullet.png')
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (25, 25))
        except Exception as e:
            print(f"Ошибка загрузки изображения пули: {e}")
            self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
            pygame.draw.rect(self.image, GREEN, (0, 0, 25, 25))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.speed = BULLET_SPEED
        self.damage = BULLET_DAMAGE

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()