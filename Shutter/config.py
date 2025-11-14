import os

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Пути к ресурсам
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')

# РАЗМЕРЫ СПРАЙТОВ
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 150
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
BULLET_WIDTH = 10
BULLET_HEIGHT = 25

# Настройки игрока
PLAYER_SPEED = 5
PLAYER_SHOOT_DELAY = 200

# Настройки врагов
ENEMY_SPAWN_DELAY = 1000
ENEMY_SPEED = 2
ENEMY_HEALTH = 1

# Настройки пуль
BULLET_SPEED = 7
BULLET_DAMAGE = 1