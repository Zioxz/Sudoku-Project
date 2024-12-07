from sudoku_generator import *
import pygame
class Board:
    '''this should initalize all the variables needed for the board class
    the row and col reprsent the current selected row and col'''
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.row = 0
        self.col = 0
        self.difficulty_dict = {'easy': 30, 'medium': 40, 'hard': 50}
        #
        self.user_sudoku = SudokuGenerator(self.difficulty_dict[difficulty])
        self.user_sudoku.fill_values()
        self.answer = [[],[],[],[],[],[],[],[],[]]
        for i in range(0,9):
            for j in range(0,9):
                self.answer[i].append(self.user_sudoku.get_board()[i][j])
        self.user_sudoku.remove_cells()
        self.original_board = [[],[],[],[],[],[],[],[],[]]
        for i in range(0,9):
            for j in range(0,9):
                self.original_board[i].append(self.user_sudoku.get_board()[i][j])
        self.user_board = self.user_sudoku.get_board()
    def draw(self):
        for i in range(0, 10):
            if i % 3 == 0:
                pygame.draw.line(
                    self.screen,
                    "black",
                    (0, i * 67),
                    (603, i * 67),
                    10)
            else:
                pygame.draw.line(
                    self.screen,
                    "black",
                    (0, i * 67),
                    (603, i * 67),
                    4)

        for i in range(0, 10):
            if i % 3 == 0:
                pygame.draw.line(
                    self.screen,
                    "black",
                    (i * 67, 0),
                    (i * 67, 603),
                    10)
            else:
                pygame.draw.line(
                    self.screen,
                    "black",
                    (i * 67, 0),
                    (i * 67, 603),
                    4)
    def fill_board(self):
        for i in range(0,9):
            for j in range(0,9):
                if self.original_board[i][j] != 0:
                    self.row = j
                    self.col = i
                    self.place_number(self.original_board[i][j],"org")

    def select(self, row, col):
        Board.draw(self)
        self.row = row
        self.col = col
        pygame.draw.rect(self.screen,"red",(row*67,col*67,70,70),3)
    def click(self, row, col):
        return (row // 67,col//67)
    def clear(self):
        pygame.draw.rect(self.screen, "white", (self.row * 67+3, self.col * 67+3, 63, 63))
        self.update_board(0)
    def sketch(self, value):
        sketch_font = pygame.font.Font(None, 20)
        sketch_surf = sketch_font.render(str(value),5,"black")
        sketch_rect = sketch_surf.get_rect(topleft = (self.row * 67 + 10,self.col * 67 +10))
        pygame.draw.rect(self.screen, "white", (self.row * 67 + 10, self.col * 67 + 10, 12, 12))
        screen.blit(sketch_surf,sketch_rect)

    def place_number(self, value,type = "player"):
        if type == "player":
            num_font = pygame.font.Font(None, 60)
            num_surf = num_font.render(str(value),10,"black")
            num_rect = num_surf.get_rect(topleft = (self.row * 67 + 25,self.col * 67 +20))
            pygame.draw.rect(self.screen, "white", (self.row * 67 + 25, self.col * 67 + 20, 30, 40))
            self.screen.blit(num_surf,num_rect)
            self.update_board(value)
        else:
            num_font = pygame.font.Font(None, 60)
            num_surf = num_font.render(str(value), 10, "red")
            num_rect = num_surf.get_rect(topleft=(self.row * 67 + 25, self.col * 67 + 20))
            pygame.draw.rect(self.screen, "white", (self.row * 67 + 25, self.col * 67 + 20, 30, 40))
            self.screen.blit(num_surf, num_rect)
            self.update_board(value)

        #print("user",self.user_board)
    def check_original(self,row,col):
        if self.original_board[col][row] == 0:
            return True
        else:
            return False


    def reset_to_original(self):
        self.screen.fill("white")
        self.draw()
        self.fill_board()

    def is_full(self):
        for i in range(0,9):
            for j in range(0,9):
                if self.user_board[i][j] == 0:
                    return False
        return True
    def update_board(self,value):
        self.user_board[self.col][self.row] = value
    def find_empty(self):
        #if self.col == 0 or self.row == 0:
        for i in range(self.col,9):
            if self.user_board[0][0] == 0 and (self.col != i or self.row != 0):
                return 0,0
            for j in range(self.row,9):
                if self.user_board[i][j] == 0 and (self.col != i or self.row != j):
                    return j,i
            self.row = 0
        for i in range(0,9):
            for j in range(0,9):
                print("check 2")
                if self.user_board[i][j] == 0 and self.col != i and self.row != j:
                    print(j,i)
                    return j,i



    def check_board(self):
        for i in range(0,9):
            for j in range(0,9):
                if self.user_board[i][j] != self.answer[i][j]:
                    return False
        return True
'''
pygame.init()
sketch = False
screen = pygame.display.set_mode((603,603))
screen.fill("white")
myboard = Board(603,603,screen,"hard")
myboard.draw()
myboard.fill_board()
print("userboard",myboard.user_board)
print("answer",myboard.answer)
print("ogr",myboard.original_board)
myboard.user_sudoku.print_board()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            #print(myboard.original_board[myboard.click(x,y)[1]][myboard.click(x,y)[0]])
            if myboard.original_board[y//67][x//67] == 0:
                myboard.select(x//67,y//67)
            #myboard.sketch(1)
            #print("userboard", myboard.user_board)
            # pygame.time.delay(10)
            # myboard.clear()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                myboard.reset_to_original()
            if event.key == pygame.K_c:
                myboard.clear()
            if event.key == pygame.K_s:
                sketch = True
            if event.key == pygame.K_1:
                if sketch:
                    myboard.sketch(1)
                    sketch = False
                else:
                    myboard.place_number(1)
            if event.key == pygame.K_2:
                if sketch:
                    myboard.sketch(2)
                    sketch = False
                else:
                    myboard.place_number(2)
            if event.key == pygame.K_3:
                if sketch:
                    myboard.sketch(3)
                    sketch = False
                else:
                    myboard.place_number(3)
            if event.key == pygame.K_4:
                if sketch:
                    myboard.sketch(4)
                    sketch = False
                else:
                    myboard.place_number(4)
            if event.key == pygame.K_5:
                if sketch:
                    myboard.sketch(5)
                    sketch = False
                else:
                    myboard.place_number(5)
            if event.key == pygame.K_6:
                if sketch:
                    myboard.sketch(6)
                    sketch = False
                else:
                    myboard.place_number(6)
            if event.key == pygame.K_7:
                if sketch:
                    myboard.sketch(7)
                    sketch = False
                else:
                    myboard.place_number(7)
            if event.key == pygame.K_8:
                if sketch:
                    myboard.sketch(8)
                    sketch = False
                else:
                    myboard.place_number(8)
            if event.key == pygame.K_9:
                if sketch:
                    myboard.sketch(9)
                    sketch = False
                else:
                    myboard.place_number(9)

    pygame.display.update()
'''
#from sudoku_generator import *
#import pygame

#class Board:
 #   """Represents the Sudoku game board with all functionality."""

  #  def __init__(self, width, height, screen, difficulty):
   #     self.width = width
    #    self.height = height
     #   self.screen = screen
      #  self.difficulty = difficulty
       # self.row = 0
      #  self.col = 0
      #  self.difficulty_dict = {'easy': 30, 'medium': 40, 'hard': 50}
       # self.user_sudoku = SudokuGenerator(self.difficulty_dict[difficulty])
        #self.user_sudoku.fill_values()
        #self.answer = [[], [], [], [], [], [], [], [], []]
        #for i in range(0, 9):
         #   for j in range(0, 9):
          #      self.answer[i].append(self.user_sudoku.get_board()[i][j])
        #self.user_sudoku.remove_cells()
        #self.original_board = [[], [], [], [], [], [], [], [], []]
        #for i in range(0, 9):
         #   for j in range(0, 9):
          #      self.original_board[i].append(self.user_sudoku.get_board()[i][j])
        #self.user_board = self.user_sudoku.get_board()

    #def draw(self):
     #   """Draws the Sudoku grid with bold lines for 3x3 boxes."""
      #  for i in range(0, 9):
       #     if i % 3 == 0:
        #        pygame.draw.line(
         #           self.screen,
          #          "black",
           #         (0, i * 67),
            #        (603, i * 67),
             #       10)
            #else:
             #   pygame.draw.line(
              #      self.screen,
               #     "black",
                #    (0, i * 67),
                 #   (603, i * 67),
                  #  4)

        #for i in range(0, 9):
         #   if i % 3 == 0:
          #      pygame.draw.line(
           #         self.screen,
            #        "black",
             #       (i * 67, 0),
              #      (i * 67, 603),
               #     10)
            #else:
             #   pygame.draw.line(
              #      self.screen,
               #     "black",
                #    (i * 67, 0),
                 #   (i * 67, 603),
                  #  4)

    #def fill_board(self):
     #   """Fills the board with initial values from the original board."""
      #  for i in range(0, 9):
       #     for j in range(0, 9):
        #        if self.original_board[i][j] != 0:
         #           self.row = j
          #          self.col = i
           #         self.place_number(self.original_board[i][j])

#    def select(self, row, col):
 #       """Marks a cell as selected."""
  #      Board.draw(self)
   #     self.row = row
    #    self.col = col
     #   pygame.draw.rect(self.screen, "red", (row * 67, col * 67, 70, 70), 3)

    #def click(self, row, col):
     #   """Returns the cell position based on click coordinates."""
      #  return (row // 67, col // 67)

    #def clear(self):
     #   """Clears the value of the selected cell."""
      #  pygame.draw.rect(self.screen, "white", (self.row * 67 + 3, self.col * 67 + 3, 63, 63))
       # self.update_board(0)

#    def sketch(self, value):
 #       """Sketches a number in the selected cell."""
  #      sketch_font = pygame.font.Font(None, 20)
   #     sketch_surf = sketch_font.render(str(value), 5, "black")
    #    sketch_rect = sketch_surf.get_rect(topleft=(self.row * 67 + 10, self.col * 67 + 10))
     #   pygame.draw.rect(self.screen, "white", (self.row * 67 + 10, self.col * 67 + 10, 12, 12))
      #  self.screen.blit(sketch_surf, sketch_rect)

    #def place_number(self, value):
     #   """Places a number in the selected cell."""
      #  num_font = pygame.font.Font(None, 60)
       # num_surf = num_font.render(str(value), 10, "black")
        #num_rect = num_surf.get_rect(topleft=(self.row * 67 + 25, self.col * 67 + 20))
       # pygame.draw.rect(self.screen, "white", (self.row * 67 + 25, self.col * 67 + 20, 30, 40))
       # self.screen.blit(num_surf, num_rect)
        #self.update_board(value)

   # def reset_to_original(self):
    #    """Resets the board to its initial state."""
     #   self.screen.fill("white")
      #  self.draw()
       # self.fill_board()

    #def is_full(self):
     #   """Checks if the board is completely filled."""
      #  for i in range(0, 9):
       #     for j in range(0, 9):
        #        if self.user_board[i][j] == 0:
         #           return False
       # return True

    #def update_board(self, value):
     #   """Updates the value of the selected cell in the board."""
      #  self.user_board[self.col][self.row] = value

    #def find_empty(self):
     #   """Finds an empty cell in the board."""
      #  for i in range(0, 9):
       #     for j in range(0, 9):
        #        if self.user_board[i][j] == 0:
         #           return (i, j)
        #return False

    #def check_board(self):
     #   """Checks if the board matches the solution."""
      #  for i in range(0, 9):
       #     for j in range(0, 9):
        #        if self.user_board[i][j] != self.answer[i][j]:
         #           return False
       # return True


# Ensure the code below only runs if this script is executed directly
#if __name__ == "__main__":
 #   pygame.init()
  #  sketch = False
   # screen = pygame.display.set_mode((603, 603))
    #screen.fill("white")
    #myboard = Board(603, 603, screen, "hard")
 #   myboard.draw()
  #  myboard.fill_board()
   # print("userboard", myboard.user_board)
 #   print("answer", myboard.answer)
  #  print("ogr", myboard.original_board)
   # myboard.user_sudoku.print_board()

 #   while True:
  #      for event in pygame.event.get():
   #         if event.type == pygame.QUIT:
    #            pygame.quit()
     #           exit()
      #      if event.type == pygame.MOUSEBUTTONDOWN:
       #         x, y = event.pos
        #        if myboard.original_board[y // 67][x // 67] == 0:
         #           myboard.select(x // 67, y // 67)
          #  if event.type == pygame.KEYDOWN:
           #     if event.key == pygame.K_SPACE:
            #        myboard.reset_to_original()
             #   if event.key == pygame.K_c:
              #      myboard.clear()
               # if event.key == pygame.K_1:
                #    myboard.place_number(1)
