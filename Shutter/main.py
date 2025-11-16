import pygame
import random
import sys
import os

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


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Загрузка изображения пули или создание простого спрайта
        try:
            image_path = os.path.join(IMAGES_DIR, 'bullet.png')
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (BULLET_WIDTH, BULLET_HEIGHT))
        except:
            self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(self.image, GREEN, (0, 0, BULLET_WIDTH, BULLET_HEIGHT))

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


class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, bullets, sound_manager):
        super().__init__(all_sprites)
        # Загрузка изображения игрока или создание простого спрайта
        try:
            image_path = os.path.join(IMAGES_DIR, 'player.png')
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        except:
            # Создаем большой корабль 100x150
            self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, (0, 0, 255), [
                (50, 0), (20, 100), (80, 100)
            ])
            pygame.draw.rect(self.image, (0, 150, 255), (30, 100, 40, 50))
            pygame.draw.rect(self.image, (255, 200, 0), (35, 120, 10, 20))
            pygame.draw.rect(self.image, (255, 200, 0), (55, 120, 10, 20))
            pygame.draw.circle(self.image, (100, 200, 255), (50, 40), 15)

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10  # Поднимаем от нижнего края

        self.speed = 5
        self.last_shot = 0
        self.shoot_delay = 200
        self.health = 100
        self.bullets = bullets
        self.sound_manager = sound_manager

    def update(self):
        # Обработка управления игроком
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Ограничение движения в пределах экрана
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        # Стрельба с задержкой
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now - self.last_shot > self.shoot_delay:
            self.shoot()
            self.last_shot = now

    def shoot(self):
        # Создание пули и добавление в группу
        bullet = Bullet(self.rect.centerx, self.rect.top + 20)
        self.bullets.add(bullet)
        self.sound_manager.play_sound('shoot')


class Enemy(pygame.sprite.Sprite):
    def __init__(self, all_sprites, enemies, sound_manager):
        super().__init__(all_sprites)
        # Загрузка изображения врага или создание простого спрайта
        try:
            image_path = os.path.join(IMAGES_DIR, 'enemy.png')
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (ENEMY_WIDTH, ENEMY_HEIGHT))
        except:
            self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, RED, [(0, 0), (ENEMY_WIDTH, 0), (ENEMY_WIDTH // 2, ENEMY_HEIGHT)])

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)

        self.speed = random.uniform(1, 3)
        self.health = 1
        enemies.add(self)
        self.sound_manager = sound_manager
        self.sound_manager.play_sound('enemy_spawn')

    def update(self):
        # Движение врага вниз
        self.rect.y += self.speed
        # Удаление врага, если он вышел за пределы экрана
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def take_damage(self, damage):
        # Обработка получения урона
        self.health -= damage
        if self.health <= 0:
            return True
        return False


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, all_sprites, sound_manager):
        super().__init__(all_sprites)
        # Загрузка кадров взрыва или создание простой анимации
        self.frames = []
        for i in range(1, 4):
            try:
                image_path = os.path.join(IMAGES_DIR, f'explosion{i}.png')
                frame = pygame.image.load(image_path).convert_alpha()
                frame = pygame.transform.scale(frame, (60 + i * 20, 60 + i * 20))
                self.frames.append(frame)
            except:
                frame = pygame.Surface((60 + i * 20, 60 + i * 20), pygame.SRCALPHA)
                color = (255, 200 - i * 50, 0)
                pygame.draw.circle(frame, color, (frame.get_width() // 2, frame.get_height() // 2),
                                   frame.get_width() // 2)
                self.frames.append(frame)

        # Если не удалось загрузить кадры, создаем простой взрыв
        if not self.frames:
            frame = pygame.Surface((60, 60), pygame.SRCALPHA)
            pygame.draw.circle(frame, YELLOW, (30, 30), 30)
            self.frames = [frame, frame, frame]

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.sound_manager = sound_manager
        self.sound_manager.play_sound('explosion')

    def update(self):
        # Анимация взрыва
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame < len(self.frames):
                old_center = self.rect.center
                self.image = self.frames[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = old_center
            else:
                self.kill()


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
        # Создаем простую иконку программно
        try:
            icon_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.polygon(icon_surface, (0, 100, 255), [
                (16, 5), (8, 25), (24, 25)
            ])
            pygame.display.set_icon(icon_surface)
            print("Создана простая иконка")
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
    player = Player(all_sprites, bullets, sound_manager)

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
                    player = Player(all_sprites, bullets, sound_manager)
                    score = 0
                    game_over = False
                    sound_manager.play_music()

        if not game_over:
            # Появление врагов с интервалом
            now = pygame.time.get_ticks()
            if now - enemy_timer > 1000:
                Enemy(all_sprites, enemies, sound_manager)
                enemy_timer = now

            # Обновление всех спрайтов
            all_sprites.update()
            bullets.update()

            # Проверка столкновений пуль с врагами
            hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
            for enemy, bullet_list in hits.items():
                for bullet in bullet_list:
                    if enemy.take_damage(bullet.damage):
                        Explosion(enemy.rect.center, all_sprites, sound_manager)
                        enemy.kill()
                        score += 10

            # Проверка столкновений игрока с врагами
            hits = pygame.sprite.spritecollide(player, enemies, True)
            for hit in hits:
                Explosion(hit.rect.center, all_sprites, sound_manager)
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