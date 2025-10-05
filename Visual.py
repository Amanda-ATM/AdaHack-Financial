import pygame as pg
import sqlite3 as sql
import re

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
        
        # Initialize database if needed
        self.init_database()
        
    def init_database(self):
        try:
            con = sql.connect('catStats.db')
            cursor = con.cursor()
            
            # Check if tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='CatStats'")
            if not cursor.fetchone():
                self.createdb()
                
        except Exception as e:
            print(f"Database init error: {e}")

    def createdb(self):
        con = sql.connect('catStats.db')
        cursor = con.cursor()

        # Drop tables if they exist
        cursor.execute("DROP TABLE IF EXISTS CatStats")
        cursor.execute("DROP TABLE IF EXISTS Tower")

        # SQL query to create the tables
        tableCreate = """
            CREATE TABLE CatStats(
                Hunger INT NOT NULL,
                Happiness INT NOT NULL,
                Clean INT NOT NULL
            );
        """

        towerCreate = """
            CREATE TABLE Tower(
                Parts VARCHAR(255) NOT NULL,
                Acquired BOOLEAN NOT NULL
            );
        """

        # Execute the table creation query and add stats
        cursor.execute(tableCreate)
        cursor.execute(towerCreate)
        cursor.execute("INSERT INTO CatStats VALUES (50, 50, 50)")
        
        # Initialize tower pieces
        tower_pieces = [
            ('Base', False),
            ('Leg One', False),
            ('Leg Two', False), 
            ('Leg Three', False),
            ('Box', False),
            ('Hammock', False),
            ('Top', False),
            ('Toy', False)
        ]
        
        for piece, acquired in tower_pieces:
            cursor.execute("INSERT INTO Tower VALUES (?, ?)", (piece, acquired))

        con.commit()
        con.close()

    def checkStatus(self):
        try:
            con = sql.connect('catStats.db')
            cursor = con.cursor()
            
            cursor.execute("SELECT Hunger, Happiness, Clean FROM CatStats")
            result = cursor.fetchone()
            con.close()
            
            if result:
                return int(result[0]), int(result[1]), int(result[2])
            return 50, 50, 50  # Default values
        except:
            return 50, 50, 50

    def editDB(self, value, stat):
        try:
            con = sql.connect('catStats.db')
            cursor = con.cursor()

            if stat == "hunger":
                cursor.execute("UPDATE CatStats SET Hunger = Hunger + ?", (value,))
            elif stat == "happiness":
                cursor.execute("UPDATE CatStats SET Happiness = Happiness + ?", (value,))
            else:
                cursor.execute("UPDATE CatStats SET Clean = Clean + ?", (value,))

            con.commit()
            con.close()
            return True
        except:
            return False

    def draw(self):
        # Determine cat state based on stats
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

        # Colors
        bg_color = (0, 220, 0)
        color_dark = (100, 100, 100)
        color_light = (170, 170, 170)
        
        self.screen.fill(bg_color)

        # Text
        font = pg.font.SysFont('freesansbold.ttf', 36)
        smallfont = pg.font.SysFont('Corbel', 35)

        # Status message based on state
        status_messages = {
            "spoiled": "Your cat is spoiled. Well done!",
            "happy": "Your cat is happy. Good job.",
            "stinky": "Your cat is stinky! Buy litter",
            "sick": "Your cat is sick! Buy food and litter", 
            "angry": "Your cat is angry. Your cat needs toys now",
            "sad": "No toys made your cat cry. Buy toys",
            "skinny": "Your cat is starving! Feed it!",
            "fat": "Your cat is obese, please feed him less",
            "neutral": "Your cat is doing well. Keep it up!"
        }

        status_text = status_messages.get(state, "Your cat is doing well. Keep it up!")
        statusTx = font.render(status_text, True, 'black')
        statusRect = statusTx.get_rect(center=(425, 180))

        # Draw cat image based on choice and state - IMPROVED FALLBACK
        cat_color = self.cat_choice.lower() if self.cat_choice else "black"
        try:
            # Try to load appropriate cat image - adjust path as needed
            image_path = f"Images/Cat/{cat_color.capitalize()} cat/{cat_color}{state}.png"
            cat_image = pg.image.load(image_path).convert_alpha()
        except:
            # Better fallback - create colored rectangle with text
            cat_image = pg.Surface((200, 200), pg.SRCALPHA)
            color_map = {"black": (50, 50, 50), "ginger": (200, 100, 50), "grey": (150, 150, 150)}
            color = color_map.get(cat_color, (100, 100, 100))
            cat_image.fill(color)
            
            # Add text to identify the cat
            fallback_font = pg.font.Font(None, 24)
            name_text = fallback_font.render(f"{cat_color} Cat", True, (255, 255, 255))
            state_text = fallback_font.render(f"State: {state}", True, (255, 255, 255))
            
            name_rect = name_text.get_rect(center=(100, 80))
            state_rect = state_text.get_rect(center=(100, 120))
            
            cat_image.blit(name_text, name_rect)
            cat_image.blit(state_text, state_rect)

        cat_rect = cat_image.get_rect(center=(425, 350))
        self.screen.blit(cat_image, cat_rect)

        # Draw buttons
        width, height = 850, 750
        
        # Shop button
        shop_rect = pg.Rect(width-200, height-400, 140, 40)
        shop_text = smallfont.render('Shop', True, 'white')
        
        # Cat Tower button  
        tower_rect = pg.Rect(width-200, height-350, 140, 40)
        tower_text = smallfont.render('Cat Tower', True, 'white')
        
        # Quit button
        quit_rect = pg.Rect(width-200, height-300, 140, 40)
        quit_text = smallfont.render('Quit', True, 'white')

        # Get mouse position for hover effects
        mouse = pg.mouse.get_pos()

        # Draw buttons with hover effects
        buttons = [
            (shop_rect, "shop", shop_text),
            (tower_rect, "tower", tower_text), 
            (quit_rect, "quit", quit_text)
        ]

        action = None

        for rect, btn_type, text in buttons:
            if rect.collidepoint(mouse):
                pg.draw.rect(self.screen, color_light, rect)
            else:
                pg.draw.rect(self.screen, color_dark, rect)
            
            self.screen.blit(text, (rect.x + 20, rect.y + 5))

        # Draw status text and financial info
        self.screen.blit(statusTx, statusRect)
        
        # Draw financial status
        self.finance.draw_status(self.screen, 50, 500)
        
        # Draw cat stats
        stats_text = f"Hunger: {self.cat_hunger} | Happiness: {self.cat_happiness} | Cleanliness: {self.cat_cleanliness}"
        stats_surface = font.render(stats_text, True, 'black')
        self.screen.blit(stats_surface, (50, 450))
        
        # Draw day info
        day_text = font.render(f"Day: {self.current_day}", True, 'black')
        self.screen.blit(day_text, (50, 50))
        
        # Draw player and cat name
        player_text = font.render(f"Player: {self.player_name}", True, 'black')
        self.screen.blit(player_text, (50, 90))

        pg.display.flip()

        # Event handling
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "quit"
            
            if event.type == pg.MOUSEBUTTONDOWN:
                if shop_rect.collidepoint(event.pos):
                    return "shop"
                elif tower_rect.collidepoint(event.pos):
                    return "tower"
                elif quit_rect.collidepoint(event.pos):
                    return "quit"

        return None