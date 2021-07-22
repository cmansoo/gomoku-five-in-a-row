import pygame


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface) -> None:
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def is_clicked(self) -> bool:
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True

            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False

        return action
