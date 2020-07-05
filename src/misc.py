from src.util import *


class Spritesheet:
    def __init__(self, filename, colorkey=None):
        self.sheet = load_image(filename, colorkey)
        self.colorkey = colorkey

    def _convert(self, img):
        if self.colorkey is not None:
            return img.convert_alpha()
        else:
            return img.convert()

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=None):
        """Loads image from x,y,x+offset,y+offset"""
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey=None):
        """Loads multiple images, supply a list of coordinates"""
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey=None):
        """Loads a strip of images and returns them as a list"""
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


class Animation(pg.sprite.Sprite):
    """A class that conveniently switches frames by a call."""

    def __init__(self, anim_tuple, *args):
        """args include: 'loop', 'reverse' (WIP)"""
        super().__init__()
        self.image = anim_tuple[0][0]  # current image, begin with the first frame
        self.frames = anim_tuple[0]  # images
        self.timings = anim_tuple[1]
        self.rect = self.image.get_rect()
        self._i = 0  # animation counter
        self._cur = 1  # animation frame (skip the first)
        self.looped = 'loop' in args  # detect if the animation is looped
        self.ended = False

    def restart(self):
        self._i = 0
        self._cur = 1
        self.image = self.frames[self._cur]
        self.ended = False

    def tick(self, *args):
        """Tick every frame"""
        if self.ended:
            raise RuntimeError("Called tick after the animation ended")
        if self._cur >= len(self.frames):
            if self.looped:
                self.restart()
                return True
            else:
                self.ended = True
                return False
        self._i += 1
        if self._i == self.timings[self._cur]:  # if the counter reached the value in the next position in the list
            self.image = self.frames[self._cur]  # set the new frame
            self._cur += 1  # begin waiting for the next frame
            return True  # indicate the change NOTE: For the time being, will be removed
        else:
            return False  # indicate no change


class RotatingAnim(pg.sprite.Sprite):
    """Animation that rotates the sprite"""

    def __init__(self, image, d_alpha, to_alpha=360, *args):
        """args include: 'loop', 'reverse', ... (WIP)"""
        super().__init__(*args)
        self.image = image  # current image, begin with the first frame
        self._base_image = image
        self.rect = self.image.get_rect()
        self.d_alpha = d_alpha  # animation counter
        self.to_alpha = to_alpha
        self.alpha = 1  # animation frame (skip the first)
        self.looped = 'loop' in args  # detect if the animation is looped
        self.ended = False

    def restart(self):
        self.alpha = 0
        self.image = self._base_image
        self.ended = False

    def tick(self, *args):
        """Tick every frame"""
        if self.ended:
            raise RuntimeError("Called tick after the animation ended")
        if self.alpha >= self.to_alpha:
            if self.looped:
                self.restart()
                return True
            else:
                self.ended = True
                return False
        self.alpha += self.d_alpha
        print(self.alpha)
        self.image, self.rect = rot_center(self._base_image, self.rect, self.alpha)
        return True  # indicate the change NOTE: For the time being, will be removed


class SoundPack:
    def __init__(self, soundlist):
        self.sounds = soundlist
        self._i = 0

    def _increment(self):
        self._i += 1
        if self._i >= len(self.sounds):
            self._i = 0
        return self._i

    def set_volume(self, vol):
        """From 0.0 to 1.0"""
        for el in self.sounds:
            el.set_volume(vol)

    def get_random(self):
        return self.sounds[randint(0, len(self.sounds) - 1)]

    def get_next(self):
        self._increment()
        return self.sounds[self._i]

    def play_next(self):
        self._increment()
        self.sounds[self._i].play()

    def play_random(self):
        self.sounds[randint(0, len(self.sounds) - 1)].play()
