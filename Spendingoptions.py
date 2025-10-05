import pygame
import sys

class SpendingOptions:
    def __init__(self, screen, current_savings):
        self.screen = screen
        self.current_savings = current_savings
        
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.title_font = pygame.font.Font(None, 48)
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (100, 100, 100)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 0, 0)
        self.BLUE = (100, 150, 255)
        self.YELLOW = (255, 215, 0)
        
        self.cart = {
            'food': None,
            'toy': None,
            'litter': None,
            'tower': None
        }
        
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
        
        self.buttons = []
        self.confirm_button = None
        self.back_button = None
        
    def calculate_total(self):
        total = 0
        for category, item in self.cart.items():
            if item is not None:
                total += item['price']
        return total
    
    def create_buttons(self):
        self.buttons = []
        y_start = 150
        x_left = 50
        x_right = 450
        
        # Food buttons
        for i, item in enumerate(self.items['food']):
            rect = pygame.Rect(x_left, y_start + i * 70, 350, 60)
            self.buttons.append({
                'rect': rect,
                'category': 'food',
                'item': item,
                'index': i
            })
        
        # Toy buttons
        y_start_right = 150
        for i, item in enumerate(self.items['toy']):
            rect = pygame.Rect(x_right, y_start_right + i * 70, 350, 60)
            self.buttons.append({
                'rect': rect,
                'category': 'toy',
                'item': item,
                'index': i
            })
        
        # Litter buttons
        y_litter = y_start + len(self.items['food']) * 70 + 20
        for i, item in enumerate(self.items['litter']):
            rect = pygame.Rect(x_left, y_litter + i * 70, 350, 60)
            self.buttons.append({
                'rect': rect,
                'category': 'litter',
                'item': item,
                'index': i
            })
        
        # Tower buttons
        y_tower = y_start_right + len(self.items['toy']) * 70 + 20
        for i, item in enumerate(self.items['tower']):
            rect = pygame.Rect(x_right, y_tower + i * 70, 350, 60)
            self.buttons.append({
                'rect': rect,
                'category': 'tower',
                'item': item,
                'index': i
            })
        
        self.confirm_button = pygame.Rect(250, 650, 200, 50)
        self.back_button = pygame.Rect(50, 20, 150, 40)
    
    def draw(self):
        self.screen.fill(self.WHITE)
        
        # Back button
        pygame.draw.rect(self.screen, self.YELLOW, self.back_button) 
        pygame.draw.rect(self.screen, self.BLACK, self.back_button, 2)  
        back_text = self.font.render("Back", True, self.BLACK)
        self.screen.blit(back_text, (self.back_button.x + 40, self.back_button.y + 5))
        
        # Title
        title = self.title_font.render("Shopping Time!", True, self.BLACK)
        self.screen.blit(title, (300, 20))
        
        # Money info
        savings_text = self.font.render(f"Available: £{self.current_savings:.2f}", True, self.GREEN)
        self.screen.blit(savings_text, (50, 80))
        
        total = self.calculate_total()
        total_text = self.font.render(f"Cart Total: £{total:.2f}", True, self.BLUE)
        self.screen.blit(total_text, (500, 80))
        
        # Draw item buttons
        for btn in self.buttons:
            is_selected = (self.cart[btn['category']] == btn['item'])
            
            # Calculate affordability
            current_category_price = self.cart[btn['category']]['price'] if self.cart[btn['category']] else 0
            potential_total = total - current_category_price + btn['item']['price']
            can_afford = potential_total <= self.current_savings
            
            if is_selected:
                color = self.GREEN
            elif not can_afford:
                color = self.DARK_GRAY
            else:
                color = self.GRAY
            
            pygame.draw.rect(self.screen, color, btn['rect'])
            pygame.draw.rect(self.screen, self.BLACK, btn['rect'], 2)
            
            item_text = self.small_font.render(f"{btn['item']['name']}", True, self.BLACK)
            price_text = self.small_font.render(f"£{btn['item']['price']:.2f}", True, self.BLACK)
            desc_text = self.small_font.render(f"{btn['item']['desc']}", True, self.BLACK)
            
            self.screen.blit(item_text, (btn['rect'].x + 10, btn['rect'].y + 5))
            self.screen.blit(price_text, (btn['rect'].x + 10, btn['rect'].y + 28))
            self.screen.blit(desc_text, (btn['rect'].x + 200, btn['rect'].y + 28))
        
        # Confirm button
        confirm_color = self.GREEN if total <= self.current_savings and total > 0 else self.DARK_GRAY
        pygame.draw.rect(self.screen, confirm_color, self.confirm_button)
        pygame.draw.rect(self.screen, self.BLACK, self.confirm_button, 2)
        confirm_text = self.font.render("Confirm", True, self.BLACK)
        self.screen.blit(confirm_text, (self.confirm_button.x + 40, self.confirm_button.y + 10))
        
        pygame.display.flip()
    
    def run(self):
        self.create_buttons()
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    
                    for btn in self.buttons:
                        if btn['rect'].collidepoint(mouse_pos):
                            current_total = self.calculate_total()
                            current_category_price = self.cart[btn['category']]['price'] if self.cart[btn['category']] else 0
                            new_total = current_total - current_category_price + btn['item']['price']
                            
                            if new_total <= self.current_savings:
                                self.cart[btn['category']] = btn['item']
                    
                    if self.confirm_button.collidepoint(mouse_pos):
                        total = self.calculate_total()
                        if total <= self.current_savings and total > 0:
                            return self.cart
                    
                    if self.back_button.collidepoint(mouse_pos):
                        return None
            
            self.draw()
            clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((850, 750))
    pygame.display.set_caption("Spending Options Test")
    
    spending = SpendingOptions(screen, 50)
    result = spending.run()
    
    if result:
        print("Purchases made:")
        for category, item in result.items():
            if item:
                print(f"  {category}: {item['name']} - £{item['price']:.2f}")
    else:
        print("Shopping cancelled")
    
    pygame.quit()