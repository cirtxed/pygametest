import pygame

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

        touching = False


        if self.touch_tile(tiles):
            #self.speed_x *= -1.0
            touching = True
            pass
        else:
            self.speed_x *= 0.7

        if self.x >= center_x + 10 and self.scroll_x > 0:
            if touching:
                self.scroll_x += self.speed_x * -1
                self.speed_x = 0
                #self.scroll_x += self.speed_x
            else:
                self.scroll_x += self.speed_x
        else:
            self.scroll_x = 0.1
            if touching:
                self.x += self.speed_x * -1
                self.speed_x = 0
                #self.x += self.speed_x
            else:
                self.x += self.speed_x
            print(self.speed_x)

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
        pygame.draw.rect(self.display, (50, 255, 50), self.get_rect())
