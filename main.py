import pygame
import numpy as np
import sys

# --- Configuration ---
CELL_SIZE = 10
GRID_WIDTH = 80
GRID_HEIGHT = 60
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10

# --- Colors ---
WHITE = (255, 255, 255)
DEAD_COLOR = (30, 30, 30)
ALIVE_COLOR = (0, 255, 0)
GRID_COLOR = (50, 50, 50)
BG_COLOR = (40, 40, 40)
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER = (0, 150, 0)

# --- Init ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()


# --- Button class ---
class Button:
    def __init__(self, text, x, y, w, h, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.callback = callback

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = BUTTON_HOVER if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)
        txt = font.render(self.text, True, WHITE)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()


# --- Menu actions ---
def run_game():
    grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
    paused = True
    running = True
    show_menu = False

    def count_neighbors(grid, y, x):
        total = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                ny, nx = (y + dy) % GRID_HEIGHT, (x + dx) % GRID_WIDTH
                total += grid[ny][nx]
        return total

    def update_grid(grid):
        new_grid = np.zeros_like(grid)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                neighbors = count_neighbors(grid, y, x)
                if grid[y][x] == 1 and neighbors in [2, 3]:
                    new_grid[y][x] = 1
                elif grid[y][x] == 0 and neighbors == 3:
                    new_grid[y][x] = 1
        return new_grid

    def draw_grid():
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = ALIVE_COLOR if grid[y][x] == 1 else DEAD_COLOR
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)

    def pause_menu():
        nonlocal show_menu
        menu_buttons = [
            Button("Continue", WINDOW_WIDTH//2 - 100, 200, 200, 60, resume_game),
            Button("Save", WINDOW_WIDTH//2 - 100, 300, 200, 60, lambda: print("Save placeholder")),
            Button("Main Menu", WINDOW_WIDTH//2 - 100, 400, 200, 60, exit_to_main_menu),
        ]

        while show_menu:
            screen.fill(BG_COLOR)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in menu_buttons:
                        btn.check_click(event.pos)

            for btn in menu_buttons:
                btn.draw(screen)
            pygame.display.flip()
            clock.tick(60)

    def resume_game():
        nonlocal paused, show_menu
        paused = True  # Go back to paused state, then resume loop
        show_menu = False
        return

    def exit_to_main_menu():
        main_menu()

    while running:
        screen.fill(DEAD_COLOR)
        draw_grid()
        pygame.display.flip()

        if paused:
            mouse_held = pygame.mouse.get_pressed()[0]
            if mouse_held:
                mx, my = pygame.mouse.get_pos()
                x, y = mx // CELL_SIZE, my // CELL_SIZE
                if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                    grid[y][x] = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_c:
                    grid = np.zeros_like(grid)
                elif event.key == pygame.K_p:
                    show_menu = not show_menu
                    pause_menu()

        if not paused:
            grid = update_grid(grid)

        clock.tick(FPS)



def show_settings():
    print("Settings button clicked (not implemented yet).")


def quit_game():
    pygame.quit()
    sys.exit()


# --- Main Menu ---
def main_menu():
    buttons = [
        Button("Start", WINDOW_WIDTH//2 - 100, 200, 200, 60, run_game),
        Button("Settings", WINDOW_WIDTH//2 - 100, 300, 200, 60, show_settings),
        Button("Quit", WINDOW_WIDTH//2 - 100, 400, 200, 60, quit_game),
    ]

    while True:
        screen.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    btn.check_click(event.pos)

        for btn in buttons:
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()
