from src.util import *
from src.data import *
from src.object import *


# Note: Always use .convert() when loading images from the disk
# Note: Scroll by several pixels per update. The flip() method is very slow.
# Note: No cyclic dependencies, no going up hierarchy

# TODO: Set font
# TODO: Add exception handling for files
# TODO: Handle the difficulties with object size etc depending on screen size. Add zoom?
# TODO: Add normal speed config for player


class Game:
    """Main game class"""

    def __init__(self):
        pg.init()
        infos = pg.display.Info()
        self.screen_width, self.screen_height = infos.current_w, infos.current_h
        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        pg.display.set_caption("Ninja")
        pg.display.set_icon(pg.image.load("../res/img/icon.png").convert())
        self.data = Data(self, "settings.json")
        self.bg = 11, 102, 32  # RGB
        self.time = 1.0  # Adjust time speed
        self.player = Player(self.data.player_sprite,
                             0,
                             0,
                             self.data.player_max_hp,
                             self.data.player_defence,
                             7,
                             (self.screen_width, self.screen_height))
        self.view = View(self.player, self.screen)
        self.clock = pg.time.Clock()
        self.mouse_pos = pg.mouse.get_pos()

    def main(self):
        """Run the game"""
        while True:
            self._process_events()
            # After every event

            self._update()
            self._draw()
            self.clock.tick(self.data.fps)  # cap the fps

    def _process_events(self):
        """Handle the event queue"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                try:
                    self.data.keydown_actions[event.key]()  # execute specified keydown actions
                except KeyError:
                    pass
            elif event.type == pg.KEYUP:
                try:
                    self.data.keyup_actions[event.key]()
                except KeyError:
                    pass
            # On every event

    def _draw(self):
        """Draw every object and refresh the screen"""
        self.screen.fill(self.bg)  # blank the screen
        self.screen.blit(self.player.sprite, self.player.rect)
        self.print_text()
        pg.display.flip()

    def _update(self):
        self.mouse_pos = pg.mouse.get_pos()
        self.player.update()
        self.player.rect.x, self.player.rect.y = self.view.update((self.screen_width, self.screen_height),
                                                                  self.mouse_pos,
                                                                  (self.player.rect.x, self.player.rect.y))

    def print_text(self):
        font = pg.font.Font(None, 20)
        text = font.render('player coords ' + str(self.player.x) + '  ' + str(self.player.y), True, (0, 0, 0))
        self.screen.blit(text, (400, 300))


if __name__ == '__main__':
    game = Game()
    game.main()
