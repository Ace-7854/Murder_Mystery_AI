import pygame
from button import Button
from game import Game
from settings import Settings

class Menu:
    def __init__(self, screen, start_game, open_settings):
        self.screen = screen
        self.bg_image = pygame.image.load("assets/menu_background.jpg")
        self.bg_image = pygame.transform.scale(self.bg_image, self.screen.get_size())

        font = pygame.font.Font(None, 80)
        self.title_text = font.render("Murder Mystery", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen.get_width() // 2, 100))

        button_font = pygame.font.Font(None, 50)
        self.play_button = Button(
            x=screen.get_width() // 2 - 125, y=250, width=250, height=60,
            text="PLAY", font=button_font, color=(200, 0, 0), hover_color=(255, 125, 0),
            action=start_game
        )

        self.settings_button = Button(
            x=screen.get_width() // 2 - 125, y=350, width=250, height=60,
            text="SETTINGS", font=button_font, color=(50, 50, 150), hover_color=(100, 100, 255),
            action=open_settings
        )

    def run(self):
        running = True
        while running:
            self.screen.blit(self.bg_image, (0, 0))
            self.screen.blit(self.title_text, self.title_rect)
            self.play_button.draw(self.screen)
            self.settings_button.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.play_button.handle_event(event)
                self.settings_button.handle_event(event)

            pygame.display.flip()
