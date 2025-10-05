# main.py 
import pygame
import sys
import time

#import all modules from teammates
try:
    from Setup import Setup
    from explain import Explain  # Fixed lowercase
    from Visual import CatVisual
    from Spendingoptions import SpendingOptions  # Fixed case
    from Financialstatuscalculator import FinancialStatus
except ImportError as e:
    print(f"Warning: Could not import module: {e}")

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((850, 750))
        pygame.display.set_caption("FinCat - Cat Finance Manager")
        self.clock = pygame.time.Clock()
        
        #game state
        self.running = True
        self.game_state = "SETUP"  #set up, explaining, playing 
        
        #player data
        self.player_name = ""
        self.cat_choice = None
        self.cat_name = ""
        
        #time tracking - 5 minutes per day
        self.current_day = 1
        self.day_length = 300  #5 minutes in seconds
        self.day_start_time = None
        
        #cat stats
        self.cat_hunger = 50
        self.cat_happiness = 50
        self.cat_cleanliness = 50
        
        #financial status
        self.finance = FinancialStatus(50)  # £50 weekly income
        self.finance.savings = 50  # Start with £50 available
        
    def run_setup(self):
        #Run Setup.py first
        try:
            setup = Setup(self.screen)
            player_data = setup.run()
            
            if player_data:
                self.player_name = player_data.get('name', 'Player')
                self.cat_choice = player_data.get('cat', 'black')  # Fixed default
                self.cat_name = player_data.get('cat_name', 'Kitty')
                self.game_state = "EXPLAIN"
            else:
                self.running = False
        except Exception as e:
            print(f"Setup error: {e}, using defaults")
            self.player_name = "Player"
            self.cat_choice = "black"
            self.cat_name = "Kitty"
            self.game_state = "EXPLAIN"
    
    def run_explanation(self):
       
        try:
            explain = Explain(self.screen)
            continue_game = explain.run()
            if continue_game:
                self.game_state = "PLAYING"
                self.day_start_time = time.time()
            else:
                self.running = False
        except Exception as e:
            print(f"Explain error: {e}, going to game")
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
        self.cat_hunger = max(0, self.cat_hunger - 20)
        self.cat_happiness = max(0, self.cat_happiness - 10)
        self.cat_cleanliness = max(0, self.cat_cleanliness - 15)
        
        #Reset finance for new week (every 7 days)
        if self.current_day % 7 == 1:
            self.finance.next_week()
            self.finance.savings = self.finance.income  # Reset savings for new week
        
        print(f"Day {self.current_day} started")
        print(f"Hunger: {self.cat_hunger}, Happiness: {self.cat_happiness}, Cleanliness: {self.cat_cleanliness}")
    
    def handle_spending(self):
        try:
            
            available_money = self.finance.savings
            spending_screen = SpendingOptions(self.screen, available_money)
            purchases = spending_screen.run()
            
            if purchases:
                total_cost = sum(item['price'] for item in purchases.values() if item)
                self.finance.add_spending(total_cost)
                self.update_cat_stats(purchases)
                return True
        except Exception as e:
            print(f"Spending error: {e}")
        return False
    
    def update_cat_stats(self, purchases):
        if purchases:
            #Update cat stats based on what was purchased
            if purchases.get('food'):
                self.cat_hunger = min(100, self.cat_hunger + 30)
            if purchases.get('toy'):
                self.cat_happiness = min(100, self.cat_happiness + 20)
            if purchases.get('litter'):
                self.cat_cleanliness = min(100, self.cat_cleanliness + 25)
    
    def run_visual(self):
        
        try:
            visual = CatVisual(
                self.screen,
                self.player_name,
                self.cat_choice,
                self.current_day,
                self.cat_hunger,
                self.cat_happiness,
                self.cat_cleanliness,
                self.finance
            )
            action = visual.draw()
            
            # Handle actions from visual screen
            if action == "shop":
                self.handle_spending()
            elif action == "tower":
                print("Cat tower feature coming soon!")  
               
                self.show_message("Cat Tower feature coming in next update!")
            elif action == "quit":
                self.running = False
                
        except Exception as e:
            
            print(f"Visual error: {e}")
            self.show_fallback_screen()
    
    def show_message(self, message):
        """Show a temporary message"""
        font = pygame.font.Font(None, 36)
        self.screen.fill((255, 255, 255))
        text = font.render(message, True, (0, 0, 0))
        self.screen.blit(text, (200, 350))
        pygame.display.flip()
        pygame.time.wait(2000)  # Show for 2 seconds
    
    def show_fallback_screen(self):
        """Fallback screen if Visual.py fails"""
        self.screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        text = font.render("Game Screen - Press SPACE to shop, Q to quit", True, (0, 0, 0))
        self.screen.blit(text, (200, 350))
        
        # Display basic info
        info_text = font.render(f"Day: {self.current_day} | Money: £{self.finance.savings}", True, (0, 0, 0))
        self.screen.blit(info_text, (200, 400))
        
        pygame.display.flip()
        
        #check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.handle_spending()
                elif event.key == pygame.K_q:
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