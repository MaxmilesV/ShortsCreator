import argparse
from moviepy.editor import *
import os
import random


# Парсинг аргументов из командной строки
def parse_namespace() -> argparse.Namespace:
    # Инициализация
    parser = argparse.ArgumentParser()

    # Добавление аргументов
    parser.add_argument('-f1', nargs='?', default=None)
    parser.add_argument('-f2', nargs='?', default=None)
    parser.add_argument('-m', nargs='?', default=None)

    # Сам парсинг
    namespace = parser.parse_args(sys.argv[1:])

    return namespace


# Излечение и обрезка видео
def cut_video(path: str) -> VideoFileClip:
    # Выбор случайного файла и получение его пути
    filename = random.choice(os.listdir(path))
    path_to_file = os.path.join(path, filename)

    # Чтение файла
    video = VideoFileClip(path_to_file)

    # Удаление аудио и обрезка
    video = video.without_audio()
    video = video.subclip(0, 2)

    return video


def read_music(path: str) -> AudioFileClip:
    # Выбор случайного файла и получение его пути
    filename = random.choice(os.listdir(path))
    path_to_file = os.path.join(path, filename)

    # Чтение файла
    audio = AudioFileClip(path_to_file)

    return audio


# Сама программа
def main():
    # Извлечение аргументов
    namespace = parse_namespace()

    # Обработка музыки
    music = read_music(namespace.m)

    # Чтение видео файлов
    video_1 = cut_video(namespace.f1)
    video_2 = cut_video(namespace.f2)

    # Объединение двух видеофайлов
    video_final = concatenate_videoclips([video_1, video_2], method='compose')

    # Повторное обрезание видеоклипа ввиду того, что аудиофайл не ограничен 4 секундами
    video_final.audio = music
    video_final = video_final.subclip(0, 4)

    # Сохранение в файл
    video_final.write_videofile('output.mp4')


if __name__ == '__main__':
    main()
