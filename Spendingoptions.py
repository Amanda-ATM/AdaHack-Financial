import pygame
import sys

class SpendingOptions:
    def __init__(self, screen, current_savings):
        #Store the screen and money available
        self.screen = screen
        self.current_savings = current_savings
        
        #create fonts in different sizes
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.title_font = pygame.font.Font(None, 48)
        
        #define colors using RGB values (Red, Green, Blue)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (100, 100, 100)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 0, 0)
        self.BLUE = (100, 150, 255)
        self.YELLOW = (255, 215, 0)
        
        #shopping cart - stores selected items from each category
        self.cart = {
            'food': None,      #will store selected food item
            'toy': None,       #will store selected toy item
            'litter': None,    #will store selected litter item
            'tower': None      #will store selected tower piece
        }
        
        #all available items organized by category
        self.items = {
            'food': [
                {'name': 'Basic Food', 'price': 1.5, 'desc': '(1 day)'},
                {'name': 'Good Food', 'price': 3, 'desc': '(1 day)'},
                {'name': 'Premium Food', 'price': 6, 'desc': '(1 day)'}
            ],
            'toy': [
                {'name': 'Small Toy', 'price': 4, 'desc': ''},
                {'name': 'Medium Toy', 'price': 20, 'desc': ''},
                {'name': 'Large Toy', 'price': 30, 'desc': ''}
            ],
            'litter': [
                {'name': 'Basic Litter', 'price': 7, 'desc': '(1 week)'},
                {'name': 'Premium Litter', 'price': 15, 'desc': '(1 week)'}
            ],
            'tower': [
                {'name': 'Small Piece', 'price': 10, 'desc': 'Tower part'},
                {'name': 'Medium Piece', 'price': 25, 'desc': 'Tower part'},
                {'name': 'Large Piece', 'price': 35, 'desc': 'Tower part'},
                {'name': 'Deluxe Piece', 'price': 50, 'desc': 'Tower part'},
                {'name': 'Premium Piece', 'price': 100, 'desc': 'Tower part'}
            ]
        }
        
        #lists to store button positions (will be created later)
        self.buttons = []
        self.confirm_button = None
        self.back_button = None
        
    def calculate_total(self):
        #add up the prices of all selected items
        total = 0
        for category, item in self.cart.items():
            if item is not None:  #only add if something is selected
                total += item['price']
        return total
    
    def create_buttons(self):
        #create all clickable button rectangles
        self.buttons = []
        y_start = 150          #buttons start 150 pixels from top
        x_left = 50            #left column starts at x=50
        x_right = 450          #right column starts at x=450
        
        # ceate food buttons in left column
        for i, item in enumerate(self.items['food']):
            #create rectangle: (x, y, width, height)
            rect = pygame.Rect(x_left, y_start + i * 70, 350, 60)
            #store button info
            self.buttons.append({
                'rect': rect,
                'category': 'food',
                'item': item,
                'index': i
            })
        
        #create toy buttons in right column
        y_start_right = 150
        for i, item in enumerate(self.items['toy']):
            rect = pygame.Rect(x_right, y_start_right + i * 70, 350, 60)
            self.buttons.append({
                'rect': rect,
                'category': 'toy',
                'item': item,
                'index': i
            })
        
        #create litter buttons in left column (below food)
        y_litter = y_start + len(self.items['food']) * 70 + 20
        for i, item in enumerate(self.items['litter']):
            rect = pygame.Rect(x_left, y_litter + i * 70, 350, 60)
            self.buttons.append({
                'rect': rect,
                'category': 'litter',
                'item': item,
                'index': i
            })
        
        #create tower buttons in right column (below toys)
        y_tower = y_start_right + len(self.items['toy']) * 70 + 20
        for i, item in enumerate(self.items['tower']):
            rect = pygame.Rect(x_right, y_tower + i * 70, 350, 60)
            self.buttons.append({
                'rect': rect,
                'category': 'tower',
                'item': item,
                'index': i
            })
        
        #create confirm button at bottom center
        self.confirm_button = pygame.Rect(250, 650, 200, 50)
        #create back button at top left
        self.back_button = pygame.Rect(50, 20, 150, 40)
    
    def draw(self):
        #clear screen with white background
        self.screen.fill(self.WHITE)
        
        #draw back button in top left
        pygame.draw.rect(self.screen, self.YELLOW, self.back_button) 
        pygame.draw.rect(self.screen, self.BLACK, self.back_button, 2)  
        back_text = self.font.render("Back", True, self.BLACK)
        self.screen.blit(back_text, (self.back_button.x + 40, self.back_button.y + 5))
        
        #draw title
        title = self.title_font.render("Shopping Time!", True, self.BLACK)
        self.screen.blit(title, (300, 20))
        
        #display available money
        savings_text = self.font.render(f"Available: £{self.current_savings:.2f}", True, self.GREEN)
        self.screen.blit(savings_text, (50, 80))
        
        #display cart total
        total = self.calculate_total()
        total_text = self.font.render(f"Cart Total: £{total:.2f}", True, self.BLUE)
        self.screen.blit(total_text, (500, 80))
        
        #draw all item buttons
        for btn in self.buttons:
            #check if this item is currently selected
            is_selected = (self.cart[btn['category']] == btn['item'])
            
            #calculate if player can afford this item
            #remove current selection's price, add this item's price
            can_afford = (total - (self.cart[btn['category']]['price'] if self.cart[btn['category']] else 0) + btn['item']['price']) <= self.current_savings
            
            #choose button color based on state
            if is_selected:
                color = self.GREEN  #green if selected
            elif not can_afford:
                color = self.DARK_GRAY  #dark gray if too expensive
            else:
                color = self.GRAY  #light gray if available
            
            #draw button rectangle
            pygame.draw.rect(self.screen, color, btn['rect'])
            pygame.draw.rect(self.screen, self.BLACK, btn['rect'], 2)  
            
            #draw text on button
            item_text = self.small_font.render(f"{btn['item']['name']}", True, self.BLACK)
            price_text = self.small_font.render(f"£{btn['item']['price']}", True, self.BLACK)
            desc_text = self.small_font.render(f"{btn['item']['desc']}", True, self.BLACK)
            
            #position text on button
            self.screen.blit(item_text, (btn['rect'].x + 10, btn['rect'].y + 5))
            self.screen.blit(price_text, (btn['rect'].x + 10, btn['rect'].y + 28))
            self.screen.blit(desc_text, (btn['rect'].x + 200, btn['rect'].y + 28))
        
        #draw confirm button (green if affordable, dark gray if not)
        confirm_color = self.GREEN if total <= self.current_savings else self.DARK_GRAY
        pygame.draw.rect(self.screen, confirm_color, self.confirm_button)
        pygame.draw.rect(self.screen, self.BLACK, self.confirm_button, 2)
        confirm_text = self.font.render("Confirm", True, self.BLACK)
        self.screen.blit(confirm_text, (self.confirm_button.x + 40, self.confirm_button.y + 10))
        
        #update display to show all changes
        pygame.display.flip()
    
    def run(self):
        #create all buttons
        self.create_buttons()
        clock = pygame.time.Clock()
        
        #main game loop
        while True:
            #check all events (mouse clicks, window close, etc)
            for event in pygame.event.get():
                #if window close button clicked
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                #if mouse button clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # Get click position
                    
                    #check if any item button was clicked
                    for btn in self.buttons:
                        if btn['rect'].collidepoint(mouse_pos):
                            #calculate new total if we select this item
                            current_total = self.calculate_total()
                            #remove old selection from this category
                            if self.cart[btn['category']]:
                                current_total -= self.cart[btn['category']]['price']
                            #add new item's price
                            new_total = current_total + btn['item']['price']
                            
                            #only add to cart if we can afford it
                            if new_total <= self.current_savings:
                                self.cart[btn['category']] = btn['item']
                    
                    #check if confirm button clicked
                    if self.confirm_button.collidepoint(mouse_pos):
                        total = self.calculate_total()
                        #only confirm if we can afford everything
                        if total <= self.current_savings:
                            return self.cart  #return purchases to main game
                    
                    #check if back button clicked
                    if self.back_button.collidepoint(mouse_pos):
                        return None  #rturn None to cancel shopping
            
            self.draw()
            clock.tick(60) # 60 frames per second


#test code - only runs if this file is run directly
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((850, 750))
    pygame.display.set_caption("Spending Options Test")
    
    #create shopping screen with £50 available
    spending = SpendingOptions(screen, 50)
    result = spending.run()
    
    #print what was purchased
    if result:
        print("Purchases made:")
        for category, item in result.items():
            if item:
                print(f"  {category}: {item['name']} - £{item['price']}")
    else:
        print("Shopping cancelled")
    
    pygame.quit()