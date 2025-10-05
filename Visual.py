import pygame as pg
import sqlite3 as sql

class CatVisual:
    def __init__(self, screen, player_name, cat_choice, current_day, cat_hunger, cat_happiness, cat_cleanliness, finance):
        self.screen = screen
        self.player_name = player_name
        self.cat_choice = cat_choice
        self.current_day = current_day
        self.cat_hunger = cat_hunger
        self.cat_happiness = cat_happiness
        self.cat_cleanliness = cat_cleanliness
        self.finance = finance
        
    def get_cat_state(self):
        """Determine cat state based on stats"""
        state = "neutral"
        
        if self.cat_hunger >= 75:
            state = "fat"
        elif self.cat_hunger <= 25:
            state = "skinny"

        if self.cat_cleanliness <= 30:
            state = "stinky"
        elif self.cat_cleanliness <= 45 and self.cat_hunger <= 40:
            state = "sick"

        if self.cat_happiness <= 45:
            state = "sad"
        elif self.cat_happiness <= 25:
            state = "angry"
        elif self.cat_happiness >= 90 and (25 < self.cat_hunger < 75) and self.cat_cleanliness > 31:
            state = "spoiled"
        elif self.cat_happiness >= 70 and (25 < self.cat_hunger < 75) and self.cat_cleanliness > 31:
            state = "happy"
            
        return state

    def get_status_message(self, state):
        """Status messages based on cat state"""
        messages = {
            "spoiled": "Your cat is spoiled. Well done! 😻",
            "happy": "Your cat is happy. Good job! 😺",
            "stinky": "Your cat is stinky! Buy litter 🐾",
            "sick": "Your cat is sick! Buy food and litter 🤢", 
            "angry": "Your cat is angry. Your cat needs toys now 😾",
            "sad": "No toys made your cat cry. Buy toys 😿",
            "skinny": "Your cat is starving! Feed it! 🍖",
            "fat": "Your cat is obese, please feed him less 🐖",
            "neutral": "Your cat is doing well. Keep it up! 🐱"
        }
        return messages.get(state, "Your cat is doing well. Keep it up! 🐱")

    def draw(self):
        """Single frame draw method that returns user action"""
        # Setup
        width, height = 850, 750
        bg_color = (200, 230, 200)  # Softer green background
        color_dark = (80, 80, 80)
        color_light = (120, 120, 120)
        button_color = (70, 130, 180)  # Nice blue for buttons
        
        self.screen.fill(bg_color)
        
        # Determine cat state
        state = self.get_cat_state()
        status_message = self.get_status_message(state)
        
        # Fonts
        title_font = pg.font.SysFont('Arial', 32, bold=True)
        font = pg.font.SysFont('Arial', 24)
        small_font = pg.font.SysFont('Arial', 20)
        button_font = pg.font.SysFont('Arial', 22, bold=True)
        
        # Draw header section
        header_rect = pg.Rect(0, 0, width, 80)
        pg.draw.rect(self.screen, (60, 100, 60), header_rect)
        
        # Header text
        day_text = title_font.render(f"Day {self.current_day}", True, (255, 255, 255))
        player_text = font.render(f"Player: {self.player_name}", True, (255, 255, 255))
        money_text = font.render(f"Available: £{self.finance.savings:.2f}", True, (255, 255, 255))
        
        self.screen.blit(day_text, (50, 25))
        self.screen.blit(player_text, (250, 25))
        self.screen.blit(money_text, (500, 25))
        
        # Draw status message
        status_bg = pg.Rect(50, 100, width-100, 60)
        pg.draw.rect(self.screen, (255, 255, 255), status_bg, border_radius=10)
        pg.draw.rect(self.screen, (100, 100, 100), status_bg, 2, border_radius=10)
        
        status_surface = font.render(status_message, True, (40, 40, 40))
        status_rect = status_surface.get_rect(center=(width//2, 130))
        self.screen.blit(status_surface, status_rect)
        
        # Draw cat section
        cat_section = pg.Rect(50, 180, 350, 300)
        pg.draw.rect(self.screen, (255, 255, 255), cat_section, border_radius=15)
        pg.draw.rect(self.screen, (100, 100, 100), cat_section, 2, border_radius=15)
        
        # Draw cat image or placeholder
        cat_color = self.cat_choice.lower() if self.cat_choice else "black"
        try:
            # Try different possible image paths
            possible_paths = [
                f"Images/Cat/{cat_color.capitalize()} cat/{cat_color}{state}.png",
                f"Images/Cat/{cat_color.capitalize()} cat/{cat_color}sit.png",
                f"Images/Cat/{cat_color.capitalize()} cat/{cat_color}.png",
                f"{cat_color}cat.png",
                f"{cat_color}.png"
            ]
            
            cat_image = None
            for path in possible_paths:
                try:
                    cat_image = pg.image.load(path).convert_alpha()
                    break
                except:
                    continue
            
            if cat_image is None:
                raise FileNotFoundError("No cat image found")
                
            # Scale image if too large
            if cat_image.get_width() > 200 or cat_image.get_height() > 200:
                cat_image = pg.transform.scale(cat_image, (200, 200))
                
        except:
            # Create a nice colored placeholder with cat emoji
            cat_image = pg.Surface((200, 200), pg.SRCALPHA)
            color_map = {
                "black": (50, 50, 50), 
                "ginger": (210, 120, 50), 
                "grey": (150, 150, 150)
            }
            color = color_map.get(cat_color, (100, 100, 100))
            pg.draw.rect(cat_image, color, (0, 0, 200, 200), border_radius=20)
            pg.draw.rect(cat_image, (80, 80, 80), (0, 0, 200, 200), 2, border_radius=20)
            
            # Add cat emoji and text
            emoji_font = pg.font.SysFont('Arial', 80)
            emoji_text = emoji_font.render("🐱", True, (255, 255, 255))
            emoji_rect = emoji_text.get_rect(center=(100, 80))
            cat_image.blit(emoji_text, emoji_rect)
            
            name_font = pg.font.SysFont('Arial', 20)
            name_text = name_font.render(f"{cat_color.title()} Cat", True, (255, 255, 255))
            state_text = name_font.render(f"State: {state}", True, (255, 255, 255))
            
            name_rect = name_text.get_rect(center=(100, 150))
            state_rect = state_text.get_rect(center=(100, 175))
            
            cat_image.blit(name_text, name_rect)
            cat_image.blit(state_text, state_rect)

        cat_rect = cat_image.get_rect(center=(cat_section.centerx, cat_section.centery))
        self.screen.blit(cat_image, cat_rect)
        
        # Draw cat stats
        stats_bg = pg.Rect(50, 500, 350, 120)
        pg.draw.rect(self.screen, (255, 255, 255), stats_bg, border_radius=10)
        pg.draw.rect(self.screen, (100, 100, 100), stats_bg, 2, border_radius=10)
        
        stats_title = font.render("Cat Stats:", True, (40, 40, 40))
        self.screen.blit(stats_title, (70, 515))
        
        hunger_text = small_font.render(f"🍖 Hunger: {self.cat_hunger}/100", True, (40, 40, 40))
        happy_text = small_font.render(f"🎮 Happiness: {self.cat_happiness}/100", True, (40, 40, 40))
        clean_text = small_font.render(f"🧼 Cleanliness: {self.cat_cleanliness}/100", True, (40, 40, 40))
        
        self.screen.blit(hunger_text, (70, 545))
        self.screen.blit(happy_text, (70, 570))
        self.screen.blit(clean_text, (70, 595))
        
        # Draw financial section
        finance_bg = pg.Rect(420, 180, 380, 200)
        pg.draw.rect(self.screen, (255, 255, 255), finance_bg, border_radius=15)
        pg.draw.rect(self.screen, (100, 100, 100), finance_bg, 2, border_radius=15)
        
        # Draw financial status
        self.finance.draw_status(self.screen, 440, 200)
        
        # Draw buttons
        button_width, button_height = 150, 50
        button_y = 550
        
        buttons = []
        
        # Shop button
        shop_rect = pg.Rect(100, button_y, button_width, button_height)
        shop_text = button_font.render('🛒 Shop', True, (255, 255, 255))
        buttons.append(("shop", shop_rect, shop_text))
        
        # Cat Tower button  
        tower_rect = pg.Rect(350, button_y, button_width, button_height)
        tower_text = button_font.render('🏗️ Tower', True, (255, 255, 255))
        buttons.append(("tower", tower_rect, tower_text))
        
        # Quit button
        quit_rect = pg.Rect(600, button_y, button_width, button_height)
        quit_text = button_font.render('🚪 Quit', True, (255, 255, 255))
        buttons.append(("quit", quit_rect, quit_text))
        
        # Mouse position for hover effects
        mouse_pos = pg.mouse.get_pos()
        
        # Draw buttons with hover effects
        for action, rect, text in buttons:
            if rect.collidepoint(mouse_pos):
                pg.draw.rect(self.screen, color_light, rect, border_radius=10)
            else:
                pg.draw.rect(self.screen, button_color, rect, border_radius=10)
            
            pg.draw.rect(self.screen, (50, 50, 50), rect, 2, border_radius=10)
            
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
        
        pg.display.flip()
        
        # Event handling - return action to main.py
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "quit"
            if event.type == pg.MOUSEBUTTONDOWN:
                for action, rect, text in buttons:
                    if rect.collidepoint(event.pos):
                        return action
        
        return None