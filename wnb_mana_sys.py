import pygame

class MagicGUI:
    def __init__(self, screen, cursor, grid_size=3, radius=10, margin=50):
        self.screen = screen
        self.cursor = cursor
        self.grid_size = grid_size
        self.radius = radius
        self.margin = margin
        screen_width, screen_height = self.screen.get_size()
        self.dot_centers = []
        self.dot_rects = []
        self.selected = []
        self.dragging = False
        self._setup_dots()
        self.is_active = False
        self.stencils = {
            1 : [6,3,0,4,2,5,8],
            2 : [2,1,3,7,8,5],
            3 : [1,3,4,5,7]
        }
        self.loaded_spell=4
        self.circle_images= [   pygame.image.load(r'GUI\chanting_ring_F0.png').convert_alpha(),
                                pygame.image.load(r'GUI\chanting_ring_F1.png').convert_alpha(),
                                pygame.image.load(r'GUI\chanting_ring_F2.png').convert_alpha(),
                                pygame.image.load(r'GUI\chanting_ring_F3.png').convert_alpha()
                                ]
        self.magic_circle= self.circle_images[0]
        self.magic_circle_rect=self.magic_circle.get_rect()
        self.magic_circle_rect.center = (screen_width // 2, screen_height // 2)
        self.last_update_time = 0
        self.current_time=0
        self.frame_index=0

    def _setup_dots(self):
        screen_w, screen_h = self.screen.get_size()

        # Define the area: 1/3 width and 1/3 height in the center (middle 9th of the screen)
        area_w = screen_w // 3
        area_h = screen_h // 3
        area_x = (screen_w - area_w) // 2
        area_y = (screen_h - area_h) // 2

        # Padding inside the area to prevent dots from touching edges
        padding = min(area_w, area_h) // 10

        usable_w = area_w - 2 * padding
        usable_h = area_h - 2 * padding

        spacing_x = usable_w // (self.grid_size - 1)
        spacing_y = usable_h // (self.grid_size - 1)

        self.dot_centers.clear()
        self.dot_rects.clear()
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x = area_x + padding + j * spacing_x
                y = area_y + padding + i * spacing_y
                self.dot_centers.append((x, y))
                rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
                self.dot_rects.append(rect)

    def update(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_update_time >= 300:
            self.last_update_time = self.current_time
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 0
            self.magic_circle = self.circle_images[self.frame_index]
        if self.cursor.active and self.is_active:
            for index, rect in enumerate(self.dot_rects):
                if index not in self.selected and self.cursor.check_collision(rect):
                    self.selected.append(index)
                    # print(index)
                    self.dragging = True
        elif self.dragging and not self.cursor.active and self.is_active:
            # print("Pattern:", self.selected)
            self.loaded_spell = self.compare(self.selected)
            self.dragging = False
            self.selected.clear()


    def compare(self, pattern):
        for key, stencil_pattern in self.stencils.items():
            print(f"Checking stencil {key}: {stencil_pattern}")
            if pattern == stencil_pattern:
                return key  # Return the matching stencil's key (ID)
        return 4  # No match

    def draw(self):
        self.screen.blit (self.magic_circle,self.magic_circle_rect)
        # Draw lines between selected dots
        if len(self.selected) >= 1:
            for i in range(len(self.selected) - 1):
                pygame.draw.line(self.screen, (128, 255, 255), self.dot_centers[self.selected[i]],
                                    self.dot_centers[self.selected[i + 1]], 5)
            if self.dragging:
                pygame.draw.line(self.screen, (128, 255, 255), self.dot_centers[self.selected[-1]],
                                     self.cursor.get_pos(), 2)
            # Draw dots
        for i, center in enumerate(self.dot_centers):
            if i in self.selected:
                pygame.draw.circle(self.screen, (0, 255, 255), center, self.radius)
            else:
                pygame.draw.circle(self.screen, (128, 128, 255), center, self.radius, 3)
