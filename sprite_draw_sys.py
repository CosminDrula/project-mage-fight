import pygame

class SpriteAnimator:
    def __init__(self, spritesheet, frame_width, frame_height, columns, rows, x, y, frame_delay=100):
        self.frames = []
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.x = x
        self.y = y
        self.frame_delay = frame_delay
        self.current_frame = 0
        self.frame_timer = 0
        self.layers = {}  # Dictionary to store layers and their corresponding surfaces
        self.default_layer = 1  # Default layer is 1 (AI object layer)

        self._load_frames(spritesheet, columns, rows)

    def get_rect(self):
        """Return the rectangle that represents the current frame position."""
        return pygame.Rect(self.x - self.frame_width // 2, self.y - self.frame_height // 2, self.frame_width, self.frame_height)

    def _load_frames(self, spritesheet, columns, rows):
        """Load frames from the spritesheet."""
        for row in range(rows):
            for col in range(columns):
                frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
                frame.blit(
                    spritesheet,
                    (0, 0),
                    pygame.Rect(col * self.frame_width, row * self.frame_height, self.frame_width, self.frame_height)
                )
                self.frames.append(frame)

    def update(self, dt):
        """Update the animation based on delta time."""
        self.frame_timer += dt
        if self.frame_timer >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_timer = 0

    def draw(self, surface, layer=None):
        """Draw the current frame on the given surface at the specified layer."""
        if layer is None:
            layer = self.default_layer  # Use the default layer if no layer is specified

        # Create a surface for the specified layer if not already created
        if layer not in self.layers:
            self.layers[layer] = pygame.Surface(surface.get_size(), pygame.SRCALPHA)

        # Clear the layer surface (optional, based on your needs)
        self.layers[layer].fill((0, 0, 0, 0))  # Clear the layer to transparent

        # Draw the current frame to the specified layer surface
        frame = self.frames[self.current_frame]
        rect = self.get_rect()  # Get the current frame's position
        self.layers[layer].blit(frame, rect)  # Draw frame on the layer surface

        # Now blit the layer onto the main surface
        surface.blit(self.layers[layer], (0, 0))
