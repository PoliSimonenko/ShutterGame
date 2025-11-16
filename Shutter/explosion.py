import pygame
import os

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, all_sprites, sound_manager, images_dir):
        super().__init__(all_sprites)
        # Загрузка кадров взрыва или создание простой анимации
        self.frames = []
        for i in range(1, 4):
            try:
                image_path = os.path.join(images_dir, f'explosion{i}.png')
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
            pygame.draw.circle(frame, (255, 255, 0), (30, 30), 30)
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
        # Анимация взрыва 3 кадра
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