import pygame
import os

try:
    from .config import *
except ImportError:
    # Локальные константы если config не импортируется
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    BLUE = (0, 0, 255)
    PLAYER_SPEED = 5
    PLAYER_SHOOT_DELAY = 200
    IMAGES_DIR = 'assets/images'
    PLAYER_WIDTH = 150
    PLAYER_HEIGHT = 150


class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, bullets, sound_manager):
        super().__init__(all_sprites)

        # Загрузка изображения с размером 100x150
        try:
            image_path = os.path.join(IMAGES_DIR, 'player.PNG')
            self.image = pygame.image.load(image_path).convert_alpha()
            # Масштабируем к нужному размеру
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        except Exception as e:
            print(f"Ошибка загрузки изображения игрока: {e}")
            # Запасной вариант - создаем спрайт 100x150
            self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
            # Рисуем корабль большего размера
            pygame.draw.polygon(self.image, BLUE, [
                (50, 0), (20, 100), (80, 100)  # Нос и крылья
            ])
            pygame.draw.rect(self.image, (0, 150, 255), (30, 100, 40, 50))  # Корпус
            pygame.draw.rect(self.image, (255, 200, 0), (35, 120, 10, 20))  # Двигатель левый
            pygame.draw.rect(self.image, (255, 200, 0), (55, 120, 10, 20))  # Двигатель правый
            pygame.draw.circle(self.image, (100, 200, 255), (50, 40), 15)  # Кабина

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10  # Поднимаем немного от нижнего края

        self.speed = PLAYER_SPEED
        self.last_shot = 0
        self.shoot_delay = PLAYER_SHOOT_DELAY
        self.health = 100
        self.bullets = bullets
        self.sound_manager = sound_manager

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Ограничение движения с учетом нового размера
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now - self.last_shot > self.shoot_delay:
            self.shoot()
            self.last_shot = now

    def shoot(self):
        # Пули вылетают из центра верхней части корабля
        bullet_x = self.rect.centerx
        bullet_y = self.rect.top + 20  # Немного отступаем от верха
        try:
            from bullet import Bullet
            bullet = Bullet(bullet_x, bullet_y)
            self.bullets.add(bullet)
            self.sound_manager.play_sound('shoot')
        except ImportError:
            print("Ошибка импорта Bullet")

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0