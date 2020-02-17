# Memory V3
# All game features are implemented
# There is a 2 second elay between each tile being flipped back
# When two tiles are the same, they remain permanently flipped

import pygame, random, time


def main():
   # Initialize all pygame modules 
   pygame.init()
   
   # Create a pygame display window
   pygame.display.set_mode((500, 400))
   
   # Set the title of the display window
   pygame.display.set_caption('Memory') 
   
   # GHet the display surface
   w_surface = pygame.display.get_surface()
   
   # Create a game object
   game = Game(w_surface)
   
   # Start the main game loop by calling the play method on the game object
   game.play()
   
   # Quit pygame and clean up the pygame window
   pygame.quit() 



class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Common attributes
      self.surface = surface
      self.bg_color = pygame.Color('black')
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # Game specific attributes
      self.board = []
      self.board_size = 4
      self.score = 0
      self.create_board()
       # Other game attributes
      self.clicked_tiles = []
      self.chosen_tiles = []
           
   def create_board(self):
      # Creates the board
      Tile.set_surface(self.surface)
      # Loading the images
      pics = ['image1.bmp','image2.bmp','image3.bmp','image4.bmp','image5.bmp','image6.bmp','image7.bmp','image8.bmp']
      image = []
      for pic in pics:
         i = pygame.image.load(pic)
         image.append(i)
      images = image + image
      random.shuffle(images)
      width = 100
      height = 100
      
      for row_index in range(0, self.board_size):
         row = []
         for col_index in range(0, self.board_size):
            x = width * col_index
            y = height * row_index
            tile = Tile(x, y, images[row_index*4 + col_index])
            row.append(tile)
         self.board.append(row)
      
   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.
      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         if event.type == pygame.MOUSEBUTTONUP and self.continue_game:
            self.handle_mouse_up(event)
   
   def handle_mouse_up(self, event):
      for row in self.board:
         for tile in row:
            chosen_tiles = []
            valid_click = tile.select(event.pos)
            if valid_click == True:
               tile.change()
               self.chosen_tiles.append(tile)
               #if len(self.chosen_tiles) == 2:
                  #self.check()
               #self.clicked_tiles.append(tile)
               
   def check(self):
      if self.chosen_tiles[0] == self.chosen_tiles[1]:
         self.clicked_tiles.append(self.chosen_tiles[0])
         self.clicked_tiles.append(self.chosen_tiles[1])
         self.chosen_tiles = []
      else:
         for tile in self.chosen_tiles:
            tile.change()
         self.chosen_tiles = []      
           

   def draw(self):
      # Clear the display surface first
      self.surface.fill(self.bg_color) 
      
      # Draw the tiles
      for each_row in self.board:
         for each_tile in each_row:
            each_tile.draw()
            
      # Draws the score      
      self.draw_score()
      
      # Make the updated surface appear on the display      
      pygame.display.update() 

   def update(self):
      # Update the game objects for the next frame.
      self.score = pygame.time.get_ticks()//1000
      
      #time.sleep(0.5)
      #for row in self.board:
         #for tile in row:
            #result = tile.re_exposed()
            #if result == True:
               #tile.change()
      if len(self.chosen_tiles) == 2:
         self.check()
         time.sleep(0.5)
      

   def decide_continue(self):
      # Check and remember if the game should continue      
      if len(self.clicked_tiles) == 16:
         self.continue_game = False
   
   def draw_score(self):
      # Set the color
      fg_color = pygame.Color('white')
      
      # Create font object
      font = pygame.font.SysFont(None, 100)
      
      # Create a textbox by rendering the font
      text_string = str(self.score)
      text_box = font.render(text_string, True, fg_color, self.bg_color) 
      
      # Compute location of the textbox
      width = self.surface.get_width() - text_box.get_width()
      location = (width,0) 
      
      # Blit the textbox on the surface
      self.surface.blit(text_box, location)   


class Tile:
   # Shared attributes or Class attributes
   surface = None
   border_color = pygame.Color('black') 
   border_size = 5
   hidden_tile = pygame.image.load('image0.bmp')
   @classmethod
   def set_surface(cls, game_surface):
      cls.surface = game_surface
   
   # Instance methods
   def __init__(self, x, y, image):
      self.image = image
      width = self.image.get_width()
      height = self.image.get_height()
      self.rect = pygame.Rect(x, y, width, height)
      self.exposed = False

   def draw(self):
      if self.exposed == False:
         # Draws the question mark
         pygame.draw.rect(Tile.surface, Tile.border_color, self.rect, Tile.border_size)
         Tile.surface.blit(Tile.hidden_tile, self.rect)
         
      else:
         # Draws the image
         pygame.draw.rect(Tile.surface, Tile.border_color, self.rect, Tile.border_size)
         Tile.surface.blit(self.image, self.rect)                

   def change(self):
      # This method, when called, changes the tile's state to exposed 
      if self.exposed == False:
         self.exposed = True
      else:
         self.exposed = False
         
      def re_exposed(self):
         return self.exposed
   
   def select(self, position):
      valid_click = False
      if self.rect.collidepoint(position) and self.exposed == False:
         valid_click = True  
      return valid_click
   
   def __eq__(self, other):
      if isinstance(other, Tile):
         if other.image == self.image:
            return True
      
main()