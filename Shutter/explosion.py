import pygame

try:
    from .config import *
except ImportError:
    YELLOW = (255, 255, 0)
    IMAGES_DIR = 'assets/images'


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, all_sprites, sound_manager):
        super().__init__(all_sprites)
        self.frames = []
        # Загрузка кадров анимации
        for i in range(1, 4):
            try:
                image_path = os.path.join(IMAGES_DIR, f'explosion{i}.png')
                frame = pygame.image.load(image_path).convert_alpha()
                frame = pygame.transform.scale(frame, (40 + i * 10, 40 + i * 10))
                self.frames.append(frame)
            except Exception as e:
                print(f"Ошибка загрузки изображения взрыва {i}: {e}")
                # Запасной вариант
                frame = pygame.Surface((30 + i * 10, 30 + i * 10), pygame.SRCALPHA)
                color = (255, 200 - i * 50, 0)
                pygame.draw.circle(frame, color, (frame.get_width() // 2, frame.get_height() // 2),
                                   frame.get_width() // 2)
                self.frames.append(frame)

        if not self.frames:
            # Запасной вариант
            frame = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(frame, YELLOW, (15, 15), 15)
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