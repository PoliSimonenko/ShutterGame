import pygame
import numpy as np
import os


def generate_sound(frequency=440, duration=0.5, volume=0.5):
    """Генерирует простой звуковой сигнал"""
    sample_rate = 44100
    n_samples = int(round(duration * sample_rate))

    # Создаем буфер для звука
    buf = np.zeros((n_samples, 2), dtype=np.int16)
    max_amplitude = np.iinfo(np.int16).max * volume

    for i in range(n_samples):
        t = float(i) / sample_rate
        # Синусоидальная волна
        sample = max_amplitude * np.sin(2 * np.pi * frequency * t)
        buf[i][0] = int(sample)  # Левый канал
        buf[i][1] = int(sample)  # Правый канал

    return pygame.sndarray.make_sound(buf)


def create_all_sounds():
    """Создает все необходимые звуковые файлы"""
    pygame.mixer.init()

    # Создаем папку если её нет
    sounds_dir = 'assets/sounds'
    if not os.path.exists(sounds_dir):
        os.makedirs(sounds_dir)
        print(f"Создана папка: {sounds_dir}")

    # Создаем звуки
    sounds = {
        'shoot.wav': (800, 0.1, 0.7),  # Высокий короткий звук
        'explosion.wav': (150, 0.4, 0.8),  # Низкий длинный звук
        'enemy_spawn.wav': (400, 0.2, 0.5),  # Средний звук
        'background.wav': (300, 1.0, 0.3)  # Фоновая музыка
    }

    for filename, (freq, duration, volume) in sounds.items():
        try:
            sound = generate_sound(freq, duration, volume)
            filepath = os.path.join(sounds_dir, filename)
            pygame.mixer.Sound.save(sound, filepath)
            print(f"Создан: {filepath}")
        except Exception as e:
            print(f"Ошибка создания {filename}: {e}")

    print("Все тестовые звуки созданы!")


if __name__ == "__main__":
    create_all_sounds()