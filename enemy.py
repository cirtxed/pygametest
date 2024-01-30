import pygame

class Enemy:
    def __init__(self, pos, display):
        self.x = pos.x
        self.y = pos.y
        self.display = display
        self.last_scroll_x = 0

    def movement(self):
        self.x -= 1

    def update(self, scroll_x):
        self.movement()
        scroll_diff = scroll_x - self.last_scroll_x
        self.x -= scroll_diff
        self.last_scroll_x = scroll_x
        pygame.draw.rect(self.display, (255, 255, 50), (self.x, self.y, 30, 30))
        
        pass
