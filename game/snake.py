import pygame

class Snake:
    def __init__(self, x, y, cell_size):
        self.cell_size = cell_size
        # body is a list of (x, y) grid-cell positions, head is body[0]
        self.body = [(x, y), (x - 1, y), (x - 2, y)]
        self.direction = (1, 0)  # moving right
        self.next_directions = []
        self.grow_pending = False

    def set_direction(self, dx, dy):
        if dx == 0 and dy == 0:
            return

        # Determine reference direction to check against (the last queued direction or current movement direction)
        ref_dir = self.next_directions[-1] if self.next_directions else self.direction

        # Ignore 180-degree reversals (opposite of reference direction)
        if dx == -ref_dir[0] and dy == -ref_dir[1]:
            return

        # Ignore redundant duplicate direction changes
        if (dx, dy) == ref_dir:
            return

        # Queue up to 2 direction changes for responsive and safe key presses
        if len(self.next_directions) < 2:
            self.next_directions.append((dx, dy))

    def move(self):
        if self.next_directions:
            self.direction = self.next_directions.pop(0)

        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)
        if self.grow_pending:
            self.grow_pending = False
        else:
            self.body.pop()

    def grow(self):
        self.grow_pending = True

    def head_rect(self):
        x, y = self.body[0]
        return pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

    def segment_rects(self):
        return [
            pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
            for (x, y) in self.body
        ]

    def collides_with_self(self):
        head = self.body[0]
        return head in self.body[1:]

    def collides_with_wall(self, grid_width, grid_height):
        x, y = self.body[0]
        return x < 0 or y < 0 or x >= grid_width or y >= grid_height
