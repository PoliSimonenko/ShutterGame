import pygame
import sys
import os

# Импорт классов из отдельных файлов
from bullet import Bullet
from player import Player
from enemy import Enemy
from explosion import Explosion

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Размеры спрайтов
PLAYER_WIDTH = 150
PLAYER_HEIGHT = 150
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
BULLET_WIDTH = 25
BULLET_HEIGHT = 25

# Пути
IMAGES_DIR = 'assets/images'
SOUNDS_DIR = 'assets/sounds'


class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_loaded = False

    def load_sound(self, name, filepath, volume=0.5):
        try:
            if os.path.exists(filepath):
                sound = pygame.mixer.Sound(filepath)
                sound.set_volume(volume)
                self.sounds[name] = sound
                print(f"Звук загружен: {name}")
                return True
            else:
                print(f"Файл не найден: {filepath}")
                return False
        except Exception as e:
            print(f"Ошибка загрузки звука {name}: {e}")
            return False

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def load_music(self, filepath, volume=0.3):
        try:
            if os.path.exists(filepath):
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.set_volume(volume)
                self.music_loaded = True
                print("Фоновая музыка загружена")
                return True
            else:
                print(f"Файл музыки не найден: {filepath}")
                return False
        except Exception as e:
            print(f"Ошибка загрузки музыки: {e}")
            return False

    def play_music(self, loops=-1):
        if self.music_loaded:
            pygame.mixer.music.play(loops)


def draw_game_over(screen, score, font):
    # Отрисовывает экран завершения игры со счетом
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)  # Полупрозрачный черный фон
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    # Заголовок
    game_over_text = font.render("ИГРА ОКОНЧЕНА", True, RED)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
    screen.blit(game_over_text, game_over_rect)
    # Счет
    score_text = font.render(f"Ваш счет: {score}", True, YELLOW)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10))
    screen.blit(score_text, score_rect)
    # Инструкция по перезапуску
    restart_text = font.render("Нажмите R для перезапуска", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
    screen.blit(restart_text, restart_rect)


def load_game_icon():
    # Загружает и устанавливает иконку игры
    try:
        icon_path = os.path.join(IMAGES_DIR, 'icon.jpg')
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
        print("Иконка игры загружена: icon.jpg")
        return True
    except Exception as e:
        print(f"Не удалось загрузить иконку: {e}")
        # Создаем иконку
        try:
            icon_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.polygon(icon_surface, (0, 100, 255), [
                (16, 5), (8, 25), (24, 25)
            ])
            pygame.display.set_icon(icon_surface)
            print("Создана запасная иконка")
            return True
        except:
            print("Не удалось создать иконку")
            return False


def main():
    # Инициализация Pygame
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Цыплячья атака")

    # Установка иконки
    load_game_icon()

    clock = pygame.time.Clock()

    # Загрузка фона
    try:
        background = pygame.image.load(os.path.join(IMAGES_DIR, 'background.jpg')).convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        print("Фоновое изображение загружено")
    except:
        background = None
        print("Фоновое изображение не найдено")

    # Инициализация менеджера звуков
    sound_manager = SoundManager()
    sound_manager.load_sound('shoot', os.path.join(SOUNDS_DIR, 'shoot.wav'), 0.7)
    sound_manager.load_sound('explosion', os.path.join(SOUNDS_DIR, 'explosion.wav'), 0.8)
    sound_manager.load_sound('enemy_spawn', os.path.join(SOUNDS_DIR, 'enemy_spawn.wav'), 0.5)
    sound_manager.load_music(os.path.join(SOUNDS_DIR, 'background.wav'), 0.3)
    sound_manager.play_music()

    # Группы спрайтов
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Создание игрока
    player = Player(all_sprites, bullets, sound_manager, SCREEN_WIDTH, SCREEN_HEIGHT, IMAGES_DIR, PLAYER_WIDTH, PLAYER_HEIGHT)

    # Переменные
    score = 0
    font = pygame.font.Font(None, 36)
    large_font = pygame.font.Font(None, 48)  # Большой шрифт для экрана завершения
    enemy_timer = 0
    game_over = False

    # Главный игровой цикл
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    # Перезапуск игры
                    all_sprites.empty()
                    bullets.empty()
                    enemies.empty()
                    player = Player(all_sprites, bullets, sound_manager, SCREEN_WIDTH, SCREEN_HEIGHT, IMAGES_DIR, PLAYER_WIDTH, PLAYER_HEIGHT)
                    score = 0
                    game_over = False
                    sound_manager.play_music()

        if not game_over:
            # Появление врагов с интервалом
            now = pygame.time.get_ticks()
            if now - enemy_timer > 1000:
                Enemy(all_sprites, enemies, sound_manager, SCREEN_WIDTH, SCREEN_HEIGHT, IMAGES_DIR, ENEMY_WIDTH, ENEMY_HEIGHT)
                enemy_timer = now

            # Обновление всех спрайтов
            all_sprites.update()
            bullets.update()

            # Проверка столкновений пуль с врагами
            hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
            for enemy, bullet_list in hits.items():
                for bullet in bullet_list:
                    if enemy.take_damage(bullet.damage):
                        Explosion(enemy.rect.center, all_sprites, sound_manager, IMAGES_DIR)
                        enemy.kill()
                        score += 10

            # Проверка столкновений игрока с врагами
            hits = pygame.sprite.spritecollide(player, enemies, True)
            for hit in hits:
                Explosion(hit.rect.center, all_sprites, sound_manager, IMAGES_DIR)
                player.health -= 10
                if player.health <= 0:
                    game_over = True
                    pygame.mixer.music.stop()

        # Отрисовка
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)

        # Отрисовка всех спрайтов
        all_sprites.draw(screen)
        bullets.draw(screen)

        # Отрисовка счет и здоровье
        score_text = font.render(f"Счет: {score}", True, WHITE)
        health_text = font.render(f"Здоровье: {player.health}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 50))

        # Отрисовка экрана завершения игры
        if game_over:
            draw_game_over(screen, score, large_font)

        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()