import pygame
import os
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, bullets, sound_manager, screen_width, screen_height, images_dir, player_width=150, player_height=150):
        super().__init__(all_sprites)
        # Загрузка изображения игрока или создание простого спрайта
        try:
            image_path = os.path.join(images_dir, 'player.png')
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (player_width, player_height))
        except:
            # Создаем объект
            self.image = pygame.Surface((player_width, player_height), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, (0, 0, 255), [
                (player_width // 2, 0), (player_width // 5, player_height * 2 // 3),
                (player_width * 4 // 5, player_height * 2 // 3)
            ])
            pygame.draw.rect(self.image, (0, 150, 255),
                           (player_width // 3, player_height * 2 // 3, player_width // 3, player_height // 3))
            pygame.draw.rect(self.image, (255, 200, 0),
                           (player_width // 3 + 5, player_height * 2 // 3 + 20, 10, 20))
            pygame.draw.rect(self.image, (255, 200, 0),
                           (player_width * 2 // 3 - 15, player_height * 2 // 3 + 20, 10, 20))
            pygame.draw.circle(self.image, (100, 200, 255),
                             (player_width // 2, player_height // 3), 15)

        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10  # Поднимаем от нижнего края

        self.speed = 5
        self.last_shot = 0
        self.shoot_delay = 200
        self.health = 100
        self.bullets = bullets
        self.sound_manager = sound_manager
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        # Обработка управления игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Ограничение движения в пределах экрана
        self.rect.clamp_ip(pygame.Rect(0, 0, self.screen_width, self.screen_height))

        # Стрельба с задержкой
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now - self.last_shot > self.shoot_delay:
            self.shoot()
            self.last_shot = now

    def shoot(self):
        # Создание пули и добавление в группу
        bullet = Bullet(self.rect.centerx, self.rect.top + 20, 'assets/images', 25, 25)
        self.bullets.add(bullet)
        self.sound_manager.play_sound('shoot')