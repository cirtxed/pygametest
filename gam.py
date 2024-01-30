import pygame

pygame.init()

SCREEN_SIZE = pygame.Vector2(1200, 950)
SCREEN_CENTER = SCREEN_SIZE * 0.5
display = pygame.display.set_mode(SCREEN_SIZE)

clock = pygame.time.Clock()

CAMERA_POSITION = pygame.Vector2()
player_speed = 250  # px/s

def world_to_screen(world_coordinate: pygame.Vector2) -> pygame.Vector2:
    return world_coordinate - CAMERA_POSITION + SCREEN_CENTER


tiles: list[pygame.Rect] = []
with open("level") as f:
    lines = f.readlines()
    tiles.clear()

    for y, row in enumerate(lines):
        for x, item in enumerate(row):

            item = item.strip().lower()
            if item == "x":
                tiles.append(pygame.Rect(x * 80, y * 80, 80, 80))

class Player:
    def __init__(self, position, speed, force, gravity_jump):
        self.position = position
        self.velocity = pygame.Vector2()
        self.speed = speed
        self.force = force
        self.gravity_jump = gravity_jump

    def move(self, delta, tiles):
        self.gravity(tiles)
        move_vec = pygame.Vector2()
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_d]:
            move_vec.x += 1
            self.velocity.x += 1
        if pressed_keys[pygame.K_a]:
            move_vec.x -= 1
            self.velocity.x -= 1
        if pressed_keys[pygame.K_s]:
            move_vec.y += 1
        if pressed_keys[pygame.K_w]:
            move_vec.y -= 1

        move_vec = move_vec.normalize() if move_vec.magnitude_squared() != 0 else move_vec
        player_position_new = self.position + move_vec * self.speed * delta

        if not self.touch_tile(tiles):
            self.position = player_position_new

    def gravity(self, tiles):
        self.position.y -= self.force

        if self.touch_tile(tiles):
            self.position.y -= self.force
            self.force = 0

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.force += self.gravity_jump
        else:
            self.force -= 0.2

    def touch_tile(self, tiles):
        rect = pygame.Rect(self.position.x, self.position.y, 30, 30)
        return rect.collidelistall(tiles)

    def draw(self, display):
        player_screen_coordinate = world_to_screen(self.position)
        pygame.draw.rect(display, (255, 50, 255), (self.position.x, self.position.y, 30, 30))


# Initialize player with gravity-related parameters
player_position = pygame.Vector2(100, 50)
player_speed = 250
player_force = 1
player_gravity_jump = 20
player = Player(player_position, player_speed, player_force, player_gravity_jump)

CAMERA_POSITION.x = 600
CAMERA_POSITION.y = 475

running = True
while running:
    delta = clock.tick(60) / 1000.0
    display.fill((100, 100, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player
    player.move(delta, tiles)

    # Match camera to player's position
    if player.position.x >= 600:
        CAMERA_POSITION.x = player.position.x

    # Draw tiles
    for tile in tiles:
        updated_rect = pygame.Rect(world_to_screen(tile.topleft), tile.size)
        pygame.draw.rect(display, (255, 0, 0), updated_rect)

    player.draw(display)

    pygame.display.flip()

pygame.quit()
