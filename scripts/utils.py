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

    def copy(self):
        return Animation(self.images, self.frame_rate, self.loop)

    def update(self):
        if self.loop:
            self.current_frame = (self.current_frame + 1) % (self.img_duration / len(self.images))
        else:
            self.current_frame = min(self.current_frame + 1, self.img_duration / len(self.images)-1)
            if self.current_frame >= self.img_duration / len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.current_frame / self.frame_rate)]
    



    