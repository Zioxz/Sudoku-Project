import pygame
from sudoku_generator import *
from Board import Board


class GameUI:
    """Handles rendering and interaction for game screens."""

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 30)

    def draw_start_screen(self):
        """Draws the game start screen with difficulty buttons."""
        self.screen.fill("white")
        title = self.font.render("Welcome to Sudoku!", True, "black")
        self.screen.blit(title, (150, 50))

        difficulties = ["Easy", "Medium", "Hard"]
        for idx, difficulty in enumerate(difficulties):
            btn = pygame.Rect(200, 150 + idx * 100, 200, 50)
            pygame.draw.rect(self.screen, "blue", btn)
            text = self.font.render(difficulty, True, "white")
            self.screen.blit(text, (btn.x + 50, btn.y + 10))

        pygame.display.update()
        return difficulties

    def draw_end_screen(self, message):
        """Displays the end screen with a message."""
        self.screen.fill("white")
        text = self.font.render(message, True, "black")
        self.screen.blit(text, (150, 50))
        #pygame.time.wait(3000)
        if message == "You Win!":
            end_btn = pygame.Rect(200, 150, 200, 50)
            pygame.draw.rect(self.screen, "blue", end_btn)
            text = self.font.render("Exit", True, "white")
            self.screen.blit(text, (end_btn.x + 50, end_btn.y + 10))

        else:
            btn = pygame.Rect(200, 150, 200, 50)
            pygame.draw.rect(self.screen, "blue", btn)
            text = self.font.render("Restart", True, "white")
            self.screen.blit(text, (btn.x + 50, btn.y + 10))
        pygame.display.update()


    def draw_ui_buttons(self):
        """Draws the buttons below the board."""
        buttons = {"Reset": (50, 620), "Restart": (250, 620), "Exit": (450, 620)}
        for text, (x, y) in buttons.items():
            btn = pygame.Rect(x, y, 120, 40)
            pygame.draw.rect(self.screen, "gray", btn)
            label = self.button_font.render(text, True, "white")
            self.screen.blit(label, (x + 20, y + 10))

        pygame.display.update()
        return buttons


def main():
    pygame.init()
    screen = pygame.display.set_mode((603, 700))  # Extra space for buttons
    pygame.display.set_caption("Sudoku Game")
    clock = pygame.time.Clock()
    ui = GameUI(screen)
    running = True
    difficulty = None

    # Game start screen
    while running:
        difficulties = ui.draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                for idx, level in enumerate(difficulties):
                    btn = pygame.Rect(200, 150 + idx * 100, 200, 50)
                    if btn.collidepoint(event.pos):
                        difficulty = level.lower()
                        running = False

    # Start game
    board = Board(603, 603, screen, difficulty)
    #print("asnwer",board.answer)
    screen.fill("white")  # Clear start screen before showing the board
    play_game(board, screen, ui, difficulty)


def play_game(board, screen, ui, difficulty):
    """Main gameplay loop."""
    running = True
    sketch = False
    ui.draw_ui_buttons()

    board.draw()
    board.fill_board()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y > 603:  # Check if clicking buttons below the board
                    if 50 <= x <= 170 and 620 <= y <= 660:  # Reset button
                        board.reset_to_original()
                        board.draw()
                        ui.draw_ui_buttons()
                    elif 250 <= x <= 370 and 620 <= y <= 660:  # Restart button
                        main()  # Restart the game
                    elif 450 <= x <= 570 and 620 <= y <= 660:  # Exit button
                        pygame.quit()
                        return
                #elif board.original_board[y // 67][x // 67] == 0:
                #    board.select(x // 67, y // 67)
                else:
                    board.select(x // 67, y // 67)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and board.check_original(board.row,board.col) and board.sketch_list[board.col][board.row] != 0:
                    board.place_number(board.sketch_list[board.col][board.row])
                if event.key == pygame.K_c and board.check_original(board.row,board.col):
                    board.clear()
                if event.key == pygame.K_s:
                    sketch = True
                if pygame.K_1 <= event.key <= pygame.K_9:
                    num = event.key - pygame.K_0
                    if board.check_original(board.row,board.col):
                        board.sketch(num)
                    '''
                    if sketch and board.check_original(board.row,board.col):
                        board.sketch(num)
                        sketch = False
                    elif board.check_original(board.row,board.col):
                        board.place_number(num)
                    '''
                if event.key == pygame.K_f:
                    selection = board.find_empty()
                    board.select(selection[0],selection[1])
                if event.key == pygame.K_RIGHT:
                    if board.row == 8:
                        board.row = 0
                    else:
                        board.row += 1
                    board.select(board.row,board.col)
                if event.key == pygame.K_UP:
                    if board.col == 0:
                        board.col = 8
                    else:
                        board.col -= 1
                    board.select(board.row, board.col)
                if event.key == pygame.K_DOWN:
                    if board.col == 8:
                        board.col = 0
                    else:
                        board.col += 1
                    board.select(board.row, board.col)
                if event.key == pygame.K_LEFT:
                    if board.row == 0:
                        board.row = 8
                    else:
                        board.row -= 1
                    board.select(board.row, board.col)
        if board.is_full():
            if board.check_board():
                #main()
                #ui.draw_end_screen("You Win!")
                end_screen("You Win!",screen,ui)
            else:
                #main()
                #ui.draw_end_screen("Game Over :(")
                end_screen("Game Over :(", screen,ui)
            #return

        pygame.display.update()

def end_screen(message,screen,ui):
    running = True
    screen.fill("white")
    ui.draw_end_screen(message)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn = pygame.Rect(200, 150, 200, 50)
                if btn.collidepoint(event.pos):
                    if message == "You Win!":
                        pygame.quit()
                        running  = False
                    else:
                        main()
                        running = False



if __name__ == "__main__":
    main()
