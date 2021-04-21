import pygame


class CheckBox:
    def __init__(self, x, y, width=35, height=35, color_back=(255, 255, 255), color_cross=(0, 0, 0), default=False):
        self.value = default
        self.color_back = color_back
        self.color_cross = color_cross

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self, screen: pygame.Surface):
        screen.fill(self.color_back, (self.x, self.y, self.width, self.height))
        if self.value:
            cross = pygame.font.SysFont("Calibri", 35).render("X", False, self.color_cross)
            screen.blit(cross, (self.x + cross.get_size()[0] / 2, self.y + cross.get_size()[1] / 8))

    def get_value(self):
        return self.value

    def click(self):
        self.value = not self.value

    def do_hover(self, mouse):
        return self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height
