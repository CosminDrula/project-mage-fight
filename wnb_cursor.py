import pygame

class Cursor:
    def __init__(self, speed=5):
        self.speed = speed  # Sensitivity multiplier
        self.pos = pygame.Vector2(pygame.mouse.get_pos())  # Start at actual mouse pos
        self.rect = pygame.Rect(self.pos.x, self.pos.y, 16, 16)
        self.active = False
        self.state = [ pygame.image.load(r'GUI\cursor_0.png').convert_alpha() ,
                       pygame.image.load(r'GUI\cursor_1.png').convert_alpha()]
        self.icon= self.state[0]
        pygame.event.set_grab(True)  # Lock the mouse to the window
        pygame.mouse.set_visible(False)

    def update(self):
        # Get relative mouse movement since last frame
        dx, dy = pygame.mouse.get_rel()
        self.pos.x += dx * self.speed * 0.1  # 0.1 smooths the scale a bit
        self.pos.y += dy * self.speed * 0.1

        # Clamp to screen boundaries
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.pos.x = max(0, min(self.pos.x, screen_width - self.rect.width))
        self.pos.y = max(0, min(self.pos.y, screen_height - self.rect.height))

        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.active = pygame.mouse.get_pressed()[0]

    def check_collision(self, target_rect):
        return self.active and self.rect.colliderect(target_rect)

    def draw(self, surface):
        self.icon = self.state[1] if self.active else self.state[0]
        surface.blit(self.icon, self.rect)
    def get_pos(self):
        return self.pos.x, self.pos.y