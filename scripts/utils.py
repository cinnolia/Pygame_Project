import pygame

import os

BASE_IMG_PATH = 'assets/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + '/' + img_name))
    return images

class Animation:
    def __init__(self, images, frame_rate = 10, loop = True):
        self.images = images
        self.frame_rate = frame_rate
        self.loop = loop
        self.current_frame = 0
        self.done = False

    