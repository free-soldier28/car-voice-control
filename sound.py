import os
import pygame
import logging

pygame.mixer.init()

def _play(file_name: str):
    try:
        path = os.path.join("sounds", file_name)
        sound = pygame.mixer.Sound(path)
        sound.play()
    except Exception as e:
        logging.warning(f"⚠️ Failed to play sound '{file_name}': {e}")

def play_activation():
    _play("activation.wav")

def play_deactivation():
    _play("deactivation.wav")

def play_custom(file_name):
    _play(file_name)
