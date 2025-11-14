import pygame
import os
import random


def create_test_images():
    """Создает тестовые изображения для игры с новыми размерами"""
    pygame.init()

    # Создаем папку если её нет
    images_dir = 'assets/images'
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        print(f"Создана папка: {images_dir}")

    # Игрок (синий корабль) - РАЗМЕР 100x150
    player_surface = pygame.Surface((150, 150), pygame.SRCALPHA)
    # Основной корпус
    pygame.draw.polygon(player_surface, (0, 100, 255), [
        (50, 0), (20, 100), (80, 100)
    ])
    # Нижняя часть
    pygame.draw.rect(player_surface, (0, 150, 255), (30, 100, 40, 50))
    # Двигатели
    pygame.draw.rect(player_surface, (255, 200, 0), (35, 120, 10, 20))
    pygame.draw.rect(player_surface, (255, 200, 0), (55, 120, 10, 20))
    # Кабина
    pygame.draw.circle(player_surface, (100, 200, 255), (50, 40), 15)
    pygame.image.save(player_surface, os.path.join(images_dir, 'player.png'))

    # Враг (красный корабль) - немного больше
    enemy_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.polygon(enemy_surface, (255, 50, 50), [
        (0, 0), (50, 0), (25, 50)
    ])
    pygame.draw.circle(enemy_surface, (255, 100, 100), (25, 15), 8)
    pygame.image.save(enemy_surface, os.path.join(images_dir, 'enemy.png'))

    # Пуля (зеленый луч) - немного больше
    bullet_surface = pygame.Surface((10, 25), pygame.SRCALPHA)
    pygame.draw.rect(bullet_surface, (0, 255, 100), (0, 0, 10, 25))
    pygame.draw.rect(bullet_surface, (100, 255, 150), (2, 2, 6, 21))
    pygame.image.save(bullet_surface, os.path.join(images_dir, 'bullet.png'))

    # Взрывы (анимационные кадры) - больше для нового размера игрока
    for i in range(3):
        size = 60 + i * 20
        explosion_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        color = (255, 200 - i * 50, 0)
        pygame.draw.circle(explosion_surface, color, (size // 2, size // 2), size // 2)
        pygame.draw.circle(explosion_surface, (255, 255, 150),
                           (size // 2, size // 2), size // 3)
        pygame.image.save(explosion_surface,
                          os.path.join(images_dir, f'explosion{i + 1}.png'))

    # Фон (звездное небо)
    bg_surface = pygame.Surface((800, 600))
    bg_surface.fill((10, 10, 40))

    # Рисуем звезды
    for _ in range(100):
        x = random.randint(0, 799)
        y = random.randint(0, 599)
        size = random.choice([1, 1, 1, 2])
        brightness = random.randint(150, 255)
        pygame.draw.circle(bg_surface, (brightness, brightness, brightness),
                           (x, y), size)

    pygame.image.save(bg_surface, os.path.join(images_dir, 'background.jpg'))

    print("Все тестовые изображения созданы с новыми размерами!")
    pygame.quit()


if __name__ == "__main__":
    create_test_images()