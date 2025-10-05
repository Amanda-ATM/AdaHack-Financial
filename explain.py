import pygame

class Explain:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        self.title_font = pygame.font.Font(None, 48)
        
        # Colors
        self.text_color = (60, 60, 60)
        self.bg_color = (255, 248, 240)
        self.button_color = (255, 223, 99)
        
        self.slides = [
            "Are you ready to put your financial skills to the test?\n\n"
            "In FinCat, your mission is simple: keep your cat happy and healthy "
            "while managing your money wisely. If you make wise decisions your cat will remain happy and healthy.\n\n"
            "But if you make poor decisions your cat can become upset/angry and even get sick.\n\n"
            "Every decision you make, big or small, will directly affect your cat. "
            "If you manage to balance fun and finance you will have a positive experience, "
            "but if you don't then there will be consequences.\n\n"
            "Start the game and see the impact of your choices unfold.\n\n"
            "Good Luck! 😺",
            
            "As the player you will have a weekly income of £50 which you can spend or save.",
            
            "There are three categories you have to take care of: feeding, cleaning, and playing with your cat.",
            
            "The quality and prices of the products you buy will have a direct impact on your cat's lifestyle and mood. So choose wisely.",
            
            "As you purchase food and products your balance will decrease. Manage your money carefully!",
            
            "You can also invest in building a cat tower! Buy blocks to create a comfortable home for your cat by investing your savings."
        ]
        
        self.current_slide = 0

    def wrap_text(self, text, max_chars):
        words = text.split()
        lines = []
        current = ""
        for word in words:
            if len(current + word) < max_chars:
                current += word + " "
            else:
                lines.append(current)
                current = word + " "
        lines.append(current)
        return lines

    def draw_slide(self):
        self.screen.fill(self.bg_color)
        
        # Title
        title = self.title_font.render("FinCat Tutorial 🐾", True, self.text_color)
        self.screen.blit(title, (300, 50))
        
        # Text Box
        text_box = pygame.Rect(75, 150, 700, 450)
        pygame.draw.rect(self.screen, (255, 255, 255), text_box, border_radius=20)
        pygame.draw.rect(self.screen, (200, 200, 200), text_box, 3, border_radius=20)
        
        # Current slide text
        slide_text = self.slides[self.current_slide]
        lines = self.wrap_text(slide_text, 70)
        for i, line in enumerate(lines):
            text_s = self.font.render(line, True, self.text_color)
            self.screen.blit(text_s, (100, 180 + i * 35))
        
        # Navigation info
        nav_text = self.small_font.render(
            f"Slide {self.current_slide + 1}/{len(self.slides)} - Press SPACE to continue, ESC to skip", 
            True, (120, 120, 120))
        self.screen.blit(nav_text, (75, 620))
        
        # Continue prompt on last slide
        if self.current_slide == len(self.slides) - 1:
            continue_text = self.font.render("Press SPACE to start the game!", True, (0, 100, 0))
            self.screen.blit(continue_text, (300, 650))

    def run(self):
        running = True
        while running:
            self.draw_slide()
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.current_slide += 1
                        if self.current_slide >= len(self.slides):
                            return True
                    elif event.key == pygame.K_ESCAPE:
                        return True
                    elif event.key == pygame.K_BACKSPACE:
                        self.current_slide = max(0, self.current_slide - 1)
            
            self.clock.tick(60)
        
        return True
