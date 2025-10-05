import pygame
import sys

class Setup:
    def __init__(self, screen):
        self.screen = screen
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (100, 100, 255)
        self.font = pygame.font.Font(None, 36)
        
        # Cats
        self.cats = ["Black", "Ginger", "Grey"]
        
        # Load and resize cat images
        try:
            bcat_image = pygame.image.load("blacksit.png")
            gingercat_image = pygame.image.load("gingersit.png") 
            greycat_image = pygame.image.load("greysit.png")
            
            target_height = 200
            self.black_cat = pygame.transform.scale(bcat_image, 
                (int(bcat_image.get_width() * target_height / bcat_image.get_height()), target_height))
            self.ginger_cat = pygame.transform.scale(gingercat_image,
                (int(gingercat_image.get_width() * target_height / gingercat_image.get_height()), target_height))
            self.grey_cat = pygame.transform.scale(greycat_image,
                (int(greycat_image.get_width() * target_height / greycat_image.get_height()), target_height))
            
            self.cat_images = [self.black_cat, self.ginger_cat, self.grey_cat]
        except:
            # Create placeholder images if files not found
            self.cat_images = []
            for i in range(3):
                surf = pygame.Surface((150, 200))
                surf.fill((100 + i*50, 100 + i*50, 100 + i*50))
                self.cat_images.append(surf)
        
        # Input variables
        self.name = ""
        self.cat_name = ""
        self.active_input = True
        self.chosen_cat = None
        self.naming_cat = False
        
        # Create buttons
        self.buttons = []
        button_y = 600
        button_height = 50
        button_width = 120
        button_gap = 50
        
        for i, cat in enumerate(self.cats):
            x = 100 + i * (button_width + button_gap)
            self.buttons.append(pygame.Rect(x, button_y, button_width, button_height))

    def run(self):
        running = True
        while running:
            self.screen.fill(self.BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                    
                if event.type == pygame.KEYDOWN and self.active_input:
                    if event.key == pygame.K_BACKSPACE:
                        if self.naming_cat:
                            self.cat_name = self.cat_name[:-1]
                        else:
                            self.name = self.name[:-1]
                    elif event.key == pygame.K_RETURN:
                        if self.naming_cat:
                            self.active_input = False
                            self.naming_cat = False
                        else:
                            if self.name.strip():  # Only proceed if name is not empty
                                self.active_input = False
                    else:
                        if self.naming_cat:
                            self.cat_name += event.unicode
                        else:
                            self.name += event.unicode
                
                if event.type == pygame.MOUSEBUTTONDOWN and not self.active_input and not self.naming_cat:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, button in enumerate(self.buttons):
                        if button.collidepoint(mouse_pos):
                            self.chosen_cat = self.cats[i]
                            self.active_input = True
                            self.naming_cat = True

            # Display instructions
            if self.active_input:
                if self.naming_cat:
                    text_surface = self.font.render(f"Name your pet cat: {self.cat_name}", True, self.WHITE)
                else:
                    text_surface = self.font.render("Enter your name: " + self.name, True, self.WHITE)
            else:
                if self.chosen_cat is None:
                    text_surface = self.font.render(f"Hello, {self.name}! Choose your cat:", True, self.WHITE)
                else:
                    text_surface = self.font.render(f"Cute! Hello {self.cat_name}!", True, self.WHITE)
            
            self.screen.blit(text_surface, (50, 50))

            # Draw cat buttons and images if no cat chosen
            if not self.active_input and self.chosen_cat is None:
                for i, button in enumerate(self.buttons):
                    pygame.draw.rect(self.screen, self.BLUE, button)
                    cat_text = self.font.render(self.cats[i], True, self.WHITE)
                    text_rect = cat_text.get_rect(center=button.center)
                    self.screen.blit(cat_text, text_rect)

                    # Draw cat image above button
                    img = self.cat_images[i]
                    img_rect = img.get_rect(midbottom=(button.centerx, button.top - 20))
                    self.screen.blit(img, img_rect)

            # Draw chosen cat if one is selected and named
            if self.chosen_cat is not None and not self.active_input:
                i = self.cats.index(self.chosen_cat)
                img = self.cat_images[i]
                img_rect = img.get_rect(center=(425, 375))
                self.screen.blit(img, img_rect)
                
                # Add continue prompt
                continue_text = self.font.render("Press ENTER to continue...", True, self.WHITE)
                self.screen.blit(continue_text, (300, 550))
                
                # Check for enter to finish setup
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    return {
                        'name': self.name,
                        'cat': self.chosen_cat.lower(),
                        'cat_name': self.cat_name
                    }

            pygame.display.flip()

        return None






