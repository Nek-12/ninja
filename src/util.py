import pygame as pg
import platform
import os
import sys

SAFEZONE_MULTIPLIER = 3  # the MINIMUM amount the object
# can fit into the distance between it and newly spawned object
DEFAULT_TIMING = 3  # The time between frames in animations
TIMINGS_FILENAME = 'timings.txt'
IMG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'res', 'img')) + os.path.sep
SFX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'res', 'sfx')) + os.path.sep
print(IMG_PATH + '\n' + SFX_PATH)


def load_image(fname, colorkey=None):
    try:
        image = pg.image.load(IMG_PATH+fname)
    except pg.error as message:
        print('Cannot load image:', fname)
        raise SystemExit(message)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
            image = image.convert_alpha()
    else:
        image = image.convert()
    return image


def load_sound(fname):
    try:
        sound = pg.mixer.Sound(SFX_PATH + fname)
    except pg.error as message:
        raise SystemExit(message)
    return sound


def toggle_fullscreen():
    """Supported only on linux"""
    if platform.system() == 'Linux':
        pg.display.toggle_fullscreen()


def rot_center(image, rect, angle):
    """rotate an image while keeping its center
    returns an image and its rectangle"""
    rot_image = pg.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


def get_timings(path, amount, fname=TIMINGS_FILENAME):
    try:
        f = open(f'{path}/{fname}')  # try to get the file
        timings_text = f.read().split(';')
        f.close()
        timings = tuple(int(i) for i in timings_text)  # convert to numeric list
        if len(timings) != amount:
            raise IndexError(f"Timings don't match images in {path}")
    except FileNotFoundError:  # If not found, use default
        print(f"Haven't found timings in {path} , using default")
        timings = tuple([DEFAULT_TIMING] * amount)  # create a default timings list
    return timings


def load_anim(folder, colorkey=None, timings_fname=TIMINGS_FILENAME):
    """Loads images from the specified folder and returns a list of pygame image objects and their timings
    returns a tuple of images and timings"""
    path = IMG_PATH+folder
    filenames = os.listdir(path)
    if timings_fname in filenames:
        filenames.pop(filenames.index(timings_fname))
    frames_cnt = len(filenames)
    timings = get_timings(path, frames_cnt, timings_fname)
    imgs = []
    for fname in filenames:
        imgs.append(load_image(f'{folder}{os.path.sep}{fname}', colorkey))
    return imgs, timings


def upscale_image(img, coefficient):
    """returns image"""
    if coefficient % 2 == 0:
        while coefficient != 1:
            coefficient //= 2
            img = pg.transform.scale2x(img)
    else:
        base_rect = img.get_rect()
        img = pg.transform.smoothscale(img, (base_rect.width * coefficient, base_rect.height * coefficient))
    return img


def upscale_anim(sprite_list, coefficient):
    """returns a list of images and their rectangles
    anim_list is a list of pygame.sprites"""
    for i in range(len(sprite_list)):
        sprite_list[i] = upscale_image(sprite_list[i], coefficient)
    return sprite_list


def load_soundlist(folder):
    """loads a list of sounds and returns it"""
    path = SFX_PATH+folder
    filenames = os.listdir(path)
    ret = []
    for name in filenames:
        ret.append(load_sound(f"{folder}{os.path.sep}{name}"))
    return ret


def collision_test(obj, targets):
    """Test collistion"""
    collided_objects = []
    for o in targets:
        if o.rect.colliderect(obj):
            collided_objects.append(o)
    return collided_objects
