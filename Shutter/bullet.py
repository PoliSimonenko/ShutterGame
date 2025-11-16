import pygame
import os

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, images_dir, bullet_width=25, bullet_height=25):
        super().__init__()
        # Загрузка изображения пули или создание простого спрайта
        try:
            image_path = os.path.join(images_dir, 'bullet.png')
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (bullet_width, bullet_height))
        except:
            self.image = pygame.Surface((bullet_width, bullet_height), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (0, 255, 0), (0, 0, bullet_width, bullet_height))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 7
        self.damage = 1

    def update(self):
        # Движение пули вверх
        self.rect.y -= self.speed
        # Удаление пули, если она вышла за пределы экрана
        if self.rect.bottom < 0:
            self.kill()