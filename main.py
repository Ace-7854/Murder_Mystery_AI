import pygame
from menu import Menu
from game import Game
from settings import Settings

class Application:
    def __init__(self):
        """Initialize the game application."""
        pygame.init()
        
        # Sound mixer stuff
        pygame.mixer.init()
        self.menu_music = "assets/menu.mp3"  # Replace with your file
        self.game_music = "assets/clock.mp3"  # Replace with your file
        self._play_music(self.menu_music)

        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        pygame.display.set_caption("Murder Mystery")

        # Store game settings in a dictionary
        self.game_settings = {"phone_num": ""}

        # Initialize menu with callbacks
        self.menu = Menu(self.screen, self.start_game, self.open_settings)

    def _play_music(self, track):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(track)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def start_game(self):
        """Start the main game."""
        self._play_music(self.game_music)
        game = Game(self.screen, self)
        game.run()

    def open_settings(self):
        """Open the settings menu."""
        settings = Settings(self, self.screen, self.run, self.game_settings)
        settings.run()

    def run(self):
        self.menu.run()


# Run the application
if __name__ == "__main__":
    app = Application()
    app.run()
