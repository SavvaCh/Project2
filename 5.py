import time

import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size,
                                  self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def on_click(self, cell, board, screen):
        pass

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos, board, screen):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell, board, screen)


class Lines(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.selected_cell = None

    def has_path(self, x1, y1, x2, y2):
        d = {(x1, y1): 0}
        v = [(x1, y1)]
        while len(v) > 0:
            x, y = v.pop(0)
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx * dy != 0:
                        continue
                    if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                        continue
                    if self.board[y + dy][x + dx] == 0:
                        dn = d.get((x + dx, y + dy), -1)
                        if dn == -1:
                            d[(x + dx, y + dy)] = d.get((x, y), -1) + 1
                            v.append((x + dx, y + dy))
        dist = d.get((x2, y2), -1)
        return dist >= 0

    def show_way(self, x1, y1, x2, y2, board, screen):
        all_ways = [[[x1, y1]]]
        bad_pixels = [[x1, y1]]
        right_way = []
        a1 = True

        while a1:
            del_this = []
            for way in all_ways:
                del_this.append(way)
                x, y = way[-1]
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dx * dy != 0:
                            continue
                        if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                            continue
                        if [x + dx, y + dy] == [x2, y2]:
                            right_way = way + [[x + dx, y + dy]]
                            a1 = False
                            break
                        if self.board[y + dy][x + dx] == 0 and [x + dx, y + dy] not in bad_pixels:
                            bad_pixels.append([x + dx, y + dy])
                            all_ways.append(way + [[x + dx, y + dy]])
            for i in del_this:
                del all_ways[all_ways.index(i)]

        for i in right_way:
            x, y = i
            screen.fill((0, 0, 0))
            board.render(screen)
            pygame.draw.ellipse(screen, "red",
                                        (x * self.cell_size + self.left,
                                         y * self.cell_size + self.top, self.cell_size,
                                         self.cell_size))
            pygame.display.flip()
            time.sleep(0.1)

    def on_click(self, cell, board, screen):
        x = cell[0]
        y = cell[1]
        if self.selected_cell is None:

            if self.board[y][x] == 1:
                self.selected_cell = x, y
            else:
                self.board[y][x] = 1

        else:
            if self.selected_cell == (x, y):
                self.selected_cell = None
                return

            x2 = self.selected_cell[0]
            y2 = self.selected_cell[1]
            if self.has_path(x2, y2, x, y):
                self.board[y][x] = 1
                self.board[y2][x2] = 0
                self.selected_cell = None
                self.show_way(x2, y2, x, y, board, screen)

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):

                if self.board[y][x] == 1:
                    color = pygame.Color("blue")
                    if self.selected_cell == (x, y):
                        color = pygame.Color("red")
                    pygame.draw.ellipse(screen, color,
                                        (x * self.cell_size + self.left,
                                         y * self.cell_size + self.top, self.cell_size,
                                         self.cell_size))

                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top,
                                  self.cell_size,
                                  self.cell_size), 1)


def main():
    pygame.init()
    size = 420, 420
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Линеечки')

    board = Lines(10, 10)
    board.set_view(10, 10, 40)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos, board, screen)

        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()


if __name__ == '__main__':
    main()
