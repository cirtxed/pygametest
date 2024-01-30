import pygame

pygame.font.init()

font_size = 30
font = pygame.font.Font('freesansbold.ttf', 30)

def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)


class Player:
    def __init__(self, pos, display):
        self.x = pos.x
        self.y = pos.y
        self.display = display
        self.scroll_x = 0
        self.speed_x = 0
        self.force = 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)
    
    def movement(self, tiles):
        center_x = 600
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.speed_x += 1
        elif keys[pygame.K_a]:
            self.speed_x -= 1 

        if self.x >= center_x + 10 and self.scroll_x > 0:
            self.scroll_x += self.speed_x
        else:
            self.scroll_x = 0.1
            self.x += self.speed_x

        if self.touch_tile(tiles):
            if self.x >= center_x + 10 and self.scroll_x > 0:
                self.speed_x *= -1
                self.scroll_x += self.speed_x
                self.speed_x = 0
            else:
                self.scroll_x = 0.1
                self.speed_x *= -1
                self.x += self.speed_x
                self.speed_x = 0
        else:
            self.speed_x *= 0.7

        

    def gravity(self, tiles):  #, tiles
        self.y -= self.force
        
        if self.touch_tile(tiles): 

            self.y -= self.force * -1
            self.force = 0 
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.force += 20 #we can change this maybe?
        else:
            self.force -= 1

    def touch_tile(self, tiles):
        rect = self.get_rect()
        for tile in tiles:
            if rect.colliderect(tile):
                return True

    def update(self, tiles):
        self.gravity(tiles)
        self.movement(tiles)
        draw_text(self.display, f'{self.speed_x}', font, (255, 55, 50), 600, 75)
        pygame.draw.rect(self.display, (50, 255, 50), self.get_rect())
