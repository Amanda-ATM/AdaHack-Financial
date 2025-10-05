#main.py 

import pygame
import sys
import time

#import all modules from teammates
try:
    from Setup import Setup
    from Explain import Explain
    from Visual import CatVisual
    from Spendingoptions import SpendingOptions
except ImportError as e:
    print(f"Warning: Could not import module: {e}")

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((850, 750))
        pygame.display.set_caption("Cat Finance Manager")
        self.clock = pygame.time.Clock()
        
        #game state
        self.running = True
        self.game_state = "SETUP"  #set up, explaining, playing 
        
        #player data
        self.player_name = ""
        self.cat_choice = None
        
        #time tracking - 5 minutes per day
        self.current_day = 1
        self.day_length = 300  #5 minutes in seconds
        self.day_start_time = None
        
        #cat stats
        self.cat_hunger = 100
        self.cat_happiness = 100
        self.cat_cleanliness = 100
        
    def run_setup(self):
        #Run Setup.py first
        try:
            setup = Setup(self.screen)
            player_data = setup.run()
            
            if player_data:
                self.player_name = player_data.get('name', 'Player')
                self.cat_choice = player_data.get('cat', 'orange')
                self.game_state = "EXPLAIN"
            else:
                self.running = False
        except:
            print("Setup not ready, using defaults")
            self.player_name = "Player"
            self.cat_choice = "orange"
            self.game_state = "EXPLAIN"
    
    def run_explanation(self):
        #Run Explain.py second
        try:
            explain = Explain(self.screen)
            explain.run()
            self.game_state = "PLAYING"
            self.day_start_time = time.time()
        except:
            print("Explain not ready, going to game")
            self.game_state = "PLAYING"
            self.day_start_time = time.time()
    
    def check_day_timer(self):
        #Check if 5 minutes passed, start new day
        if self.day_start_time is not None:
            elapsed = time.time() - self.day_start_time
            if elapsed >= self.day_length:
                self.start_new_day()
    
    def start_new_day(self):
        #Start new day and decrease cat stats
        self.current_day += 1
        self.day_start_time = time.time()
        
        #decrease cat stats each day
        self.cat_hunger -= 20
        self.cat_happiness -= 10
        self.cat_cleanliness -= 15
        
        print(f"Day {self.current_day} started")
        print(f"Hunger: {self.cat_hunger}, Happiness: {self.cat_happiness}, Cleanliness: {self.cat_cleanliness}")
    
    def run_visual(self):
        #Run Visual.py - it displays everything
        try:
            visual = CatVisual(
                self.screen,
                self.player_name,
                self.cat_choice,
                self.current_day,
                self.cat_hunger,
                self.cat_happiness,
                self.cat_cleanliness
            )
            visual.draw()
        except:
            #fallback if Visual.py not ready
            self.screen.fill((255, 255, 255))
            font = pygame.font.Font(None, 36)
            text = font.render("Waiting for Visual.py (Amanda's file)", True, (0, 0, 0))
            self.screen.blit(text, (200, 350))
            pygame.display.flip()
            
            #check for quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
    
    def run(self):
        #Main game loop - just calls components in order
        while self.running:
            if self.game_state == "SETUP":
                self.run_setup()
            
            elif self.game_state == "EXPLAIN":
                self.run_explanation()
            
            elif self.game_state == "PLAYING":
                self.check_day_timer()
                self.run_visual()
            
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
