import pygame
import random
import os

class Enemy(pygame.sprite.Sprite):
    def __init__(self, all_sprites, enemies, sound_manager, screen_width, screen_height, images_dir, enemy_width=50, enemy_height=50):
        super().__init__(all_sprites)
        # Загрузка изображения врага или создание простого спрайта
        try:
            image_path = os.path.join(images_dir, 'enemy.png')
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (enemy_width, enemy_height))
        except:
            self.image = pygame.Surface((enemy_width, enemy_height), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, (255, 0, 0),
                              [(0, 0), (enemy_width, 0), (enemy_width // 2, enemy_height)])

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)

        self.speed = random.uniform(1, 3)
        self.health = 1
        enemies.add(self)
        self.sound_manager = sound_manager
        self.screen_height = screen_height
        self.sound_manager.play_sound('enemy_spawn')

    def update(self):
        # Движение врага вниз
        self.rect.y += self.speed
        # Удаление врага, если он вышел за пределы экрана
        if self.rect.top > self.screen_height:
            self.kill()

    def take_damage(self, damage):
        # Обработка получения урона
        self.health -= damage
        if self.health <= 0:
            return True
        return False