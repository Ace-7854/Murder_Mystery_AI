import pygame
from button import Button

class InputBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (200, 200, 200)
        self.text = text
        self.font = pygame.font.Font(None, 40)
        self.text_surface = self.font.render(text, True, (0, 0, 0))
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

        self.text_surface = self.font.render(self.text, True, (0, 0, 0))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        screen.blit(self.text_surface, (self.rect.x + 10, self.rect.y + 10))

class Settings:
    def __init__(self, application, screen, go_back, game_settings):
        self.screen = screen
        self.bg_color = (50, 50, 50)
        self.go_back = go_back
        self.game_settings = game_settings
        self.application = application

        font = pygame.font.Font(None, 60)
        self.title_text = font.render("Settings", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen.get_width() // 2, 80))

        input_width = 400
        self.phone_input = InputBox(screen.get_width() // 2 - input_width // 2, 300, input_width, 50)

        button_font = pygame.font.Font(None, 40)
        self.back_button = Button(
            x=screen.get_width() // 2 - 75, y=500, width=150, height=50,
            text="Back", font=button_font, color=(150, 0, 0), hover_color=(255, 0, 0),
            action=go_back
        )
        
        self.button_save = Button(x=screen.get_width() // 2 - 75, y=400, width=150, height=50, 
            text="Save", font=button_font, color=(0, 150, 0), 
            hover_color=(0, 255, 0), action=self.save_ph_num
        )

    def save_ph_num(self):
        self.application.game_settings["phone_num"] = self.phone_input.text
        
    def run(self):
        running = True
        while running:
            self.screen.fill(self.bg_color)
            self.screen.blit(self.title_text, self.title_rect)
            self.phone_input.draw(self.screen)
            self.back_button.draw(self.screen)
            self.button_save.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.phone_input.handle_event(event)
                self.button_save.handle_event(event)
                self.back_button.handle_event(event)

            pygame.display.flip()
