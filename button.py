import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = color
        self.hover_color = hover_color
        self.current_color = self.base_color
        self.action = action
        self.hovering = False

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.hovering = True
            self.current_color = self._blend_colors(self.base_color, self.hover_color, 0.2)  # 20% more red
        else:
            self.hovering = False
            self.current_color = self.base_color

        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=8)
        
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def _blend_colors(self, color1, color2, factor):
        """Blends two colors based on a factor (0-1)."""
        return tuple(
            int(color1[i] + (color2[i] - color1[i]) * factor)
            for i in range(3)
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()
