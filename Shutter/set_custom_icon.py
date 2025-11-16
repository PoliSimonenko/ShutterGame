import pygame
import os
from PIL import Image


def create_icon_from_photo(photo_path, output_size=(32, 32)):
    #Создает иконку из фотографии
    try:
        # Открываем изображение с помощью PIL
        img = Image.open(photo_path)

        # Конвертируем в RGB если нужно
        if img.mode != 'RGB':
            img = img.convert('RGB')
        # Масштабируем до размера иконки
        img = img.resize(output_size, Image.Resampling.LANCZOS)
        # Сохраняем временный файл
        temp_path = 'temp_icon.png'
        img.save(temp_path)
        # Загружаем в pygame
        icon = pygame.image.load(temp_path)
        # Удаляем временный файл
        os.remove(temp_path)
        print(f"Иконка создана из {photo_path}")
        return icon
    except Exception as e:
        print(f"Ошибка создания иконки: {e}")
        return None


def set_game_icon(photo_path=None):
    # Устанавливает иконку
    pygame.init()

    if photo_path and os.path.exists(photo_path):
        # Пробуем создать иконку из фото
        icon = create_icon_from_photo(photo_path)
        if icon:
            pygame.display.set_icon(icon)
            print("Иконка из фото установлена!")
            return True

    # Если фото не найдено или ошибка, создаем стандартную иконку
    try:
        icon_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
        # Рисуем простую иконку корабля
        pygame.draw.polygon(icon_surface, (0, 100, 255), [
            (16, 5), (8, 25), (24, 25)
        ])
        pygame.draw.rect(icon_surface, (0, 150, 255), (12, 25, 8, 6))
        pygame.display.set_icon(icon_surface)
        print("Установлена стандартная иконка")
        return True
    except:
        print("Не удалось установить иконку")
        return False


if __name__ == "__main__":
    photo_path = "my_photo.jpg"
    set_game_icon(photo_path)