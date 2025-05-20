import pickle
import os
import pygame
import numpy as np
import sys


CELL_SIZE = 10
GRID_WIDTH = 80
GRID_HEIGHT = 60
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10
SAVE_FILE = "savegame.pkl"



WHITE = (255, 255, 255)
DEAD_COLOR = (30, 30, 30)
ALIVE_COLOR = (0, 255, 0)
GRID_COLOR = (50, 50, 50)
BG_COLOR = (40, 40, 40)
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER = (0, 150, 0)


pygame.init()
FONT = pygame.font.Font("fonts/PressStart2P.ttf", 32)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50


class Button:
    def __init__(self, text, x, y, w, h, callback, bg_color=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.callback = callback
        self.bg_color = bg_color  

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.bg_color:
            color = self.bg_color
        else:
            color = BUTTON_HOVER if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR

        pygame.draw.rect(surface, color, self.rect)

        if self.text:
            txt = font.render(self.text, True, WHITE)
            txt_rect = txt.get_rect(center=self.rect.center)
            surface.blit(txt, txt_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()



def save_grid(grid):
    with open(SAVE_FILE, "wb") as f:
        pickle.dump(grid, f)
    print("Game saved.")

def load_grid():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "rb") as f:
            return pickle.load(f)
    return np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)



def run_game(grid=None):
    grid = grid if grid is not None else np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
    paused = False
    running = True
    show_menu = False
    toggled_cells = set()

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
            Button("Save", WINDOW_WIDTH//2 - 100, 300, 200, 60, lambda: save_grid(grid)),
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
        paused = True
        show_menu = False
        return

    def exit_to_main_menu():
        main_menu()

    while running:
        screen.fill(DEAD_COLOR)
        draw_grid()
        pygame.display.flip()

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
            elif paused and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                
                toggled_cells.clear()
                mx, my = event.pos
                x, y = mx // CELL_SIZE, my // CELL_SIZE
                if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                    grid[y][x] = not grid[y][x]
                    toggled_cells.add((x, y))
            elif paused and event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                mx, my = event.pos
                x, y = mx // CELL_SIZE, my // CELL_SIZE
                if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                    if (x, y) not in toggled_cells:
                        grid[y][x] = not grid[y][x]
                        toggled_cells.add((x, y))

        if not paused:
            grid = update_grid(grid)

        clock.tick(FPS)


def show_settings():
    global ALIVE_COLOR, DEAD_COLOR

    
    color_options = [
        (0, 255, 0),     
        (255, 0, 0),     
        (0, 200, 200),   
        (255, 255, 0),   
        (255, 105, 180), 
        (160, 32, 240),  
        (255, 165, 0),   
        (200, 200, 200), 
    ]

    
    alive_index = color_options.index(ALIVE_COLOR) if ALIVE_COLOR in color_options else 0
    dead_index = color_options.index(DEAD_COLOR) if DEAD_COLOR in color_options else 0

    def set_alive(index):
        nonlocal alive_index
        alive_index = index

    def set_dead(index):
        nonlocal dead_index
        dead_index = index

    def apply_settings():
        global ALIVE_COLOR, DEAD_COLOR
        ALIVE_COLOR = color_options[alive_index]
        DEAD_COLOR = color_options[dead_index]
        main_menu()

    def back():
        main_menu()

    
    alive_buttons = [
        Button("", 80 + i * 90, 200, 60, 60, lambda i=i: set_alive(i), bg_color=color_options[i])
        for i in range(len(color_options))
    ]
    dead_buttons = [
        Button("", 80 + i * 90, 320, 60, 60, lambda i=i: set_dead(i), bg_color=color_options[i])
        for i in range(len(color_options))
    ]

    apply_button = Button("Apply", 250, 450, 130, 60, apply_settings)
    back_button = Button("Back", 420, 450, 130, 60, back)

    while True:
        screen.fill(BG_COLOR)

        
        screen.blit(font.render("Settings", True, WHITE), (WINDOW_WIDTH // 2 - 70, 100))
        screen.blit(font.render("Alive Cell Color:", True, WHITE), (80, 160))
        screen.blit(font.render("Dead Cell Color:", True, WHITE), (80, 280))

        
        for i, btn in enumerate(alive_buttons):
            pygame.draw.rect(screen, color_options[i], btn.rect)
            if i == alive_index:
                pygame.draw.rect(screen, WHITE, btn.rect, 3)
            btn.draw(screen)

        for i, btn in enumerate(dead_buttons):
            pygame.draw.rect(screen, color_options[i], btn.rect)
            if i == dead_index:
                pygame.draw.rect(screen, WHITE, btn.rect, 3)
            btn.draw(screen)

        apply_button.draw(screen)
        back_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in alive_buttons + dead_buttons + [apply_button, back_button]:
                    btn.check_click(event.pos)

        pygame.display.flip()
        clock.tick(60)



def quit_game():
    pygame.quit()
    sys.exit()



def main_menu():
    def load_and_run():
        run_game(load_grid())

    def choose_pattern_menu():
        pattern_dir = "static_patterns"
        files = [
            f for f in os.listdir(pattern_dir)
            if f.endswith(".pkl") and f != "savegame.pkl"
        ]
        buttons = []
        for i, fname in enumerate(files):
            name = fname[:-4]  
            path = os.path.join(pattern_dir, fname)
            buttons.append(Button(name, WINDOW_WIDTH//2 - 100, 150 + i*80, 200, 60,
                                  lambda p=path: run_game(load_pattern(p))))



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

    def load_pattern(path):
        with open(path, "rb") as f:
            return pickle.load(f)



    buttons = [
        Button("Start", WINDOW_WIDTH//2 - 100, 150, BUTTON_WIDTH, BUTTON_HEIGHT, run_game),
        Button("Load Save", WINDOW_WIDTH//2 - 100, 230, BUTTON_WIDTH, BUTTON_HEIGHT, load_and_run),
        Button("Choose Pattern", WINDOW_WIDTH//2 - 100, 310, BUTTON_WIDTH, BUTTON_HEIGHT, choose_pattern_menu),
        Button("Settings", WINDOW_WIDTH//2 - 100, 390, BUTTON_WIDTH, BUTTON_HEIGHT, show_settings),
        Button("Quit", WINDOW_WIDTH//2 - 100, 470, BUTTON_WIDTH, BUTTON_HEIGHT, quit_game),
    ]

    title_text = FONT.render("Game of Life", True, WHITE)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 80))

    while True:
        screen.fill(BG_COLOR)
        screen.blit(title_text, title_rect)
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
