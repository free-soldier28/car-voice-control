import os
import pygame
import logging

pygame.mixer.init()

def _play(filename):
    try:
        path = os.path.join("sounds", filename)
        sound = pygame.mixer.Sound(path)
        sound.play()
    except Exception as e:
        logging.warning(f"⚠️ Failed to play sound '{filename}': {e}")

def play_activation():
    _play("activation.wav")

def play_deactivation():
    _play("deactivation.wav")

def play_custom(filename):
    _play(filename)
