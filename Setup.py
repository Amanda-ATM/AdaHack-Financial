import pygame
import sys

pygame.init()

# Window setup
WIDTH, HEIGHT = 850, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("FinCat")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)

# Button positions
button_y = 600
button_height = 50
button_width = 120
button_gap = 50
buttons = []

# Fonts
font = pygame.font.Font(None, 36)

# Cats
cats = ["Black", "Ginger", "Grey"]

# Load and resize cat images to consistent dimensions
bcat_image = pygame.image.load("blacksit.png")
gingercat_image = pygame.image.load("gingersit.png")
greycat_image = pygame.image.load("greysit.png")

# Scale all cats to the same height while maintaining aspect ratio
target_height = 200  # Increased from 300 to 400
black_cat = pygame.transform.scale(bcat_image, 
                                  (int(bcat_image.get_width() * target_height / bcat_image.get_height()), 
                                   target_height))
ginger_cat = pygame.transform.scale(gingercat_image, 
                                   (int(gingercat_image.get_width() * target_height / gingercat_image.get_height()), 
                                    target_height))
grey_cat = pygame.transform.scale(greycat_image, 
                                 (int(greycat_image.get_width() * target_height / greycat_image.get_height()), 
                                  target_height))

cat_images = [black_cat, ginger_cat, grey_cat]

# Input variables
name = ""
cat_name = ""
active_input = True     # True when typing
chosen_cat = None
naming_cat = False      # True when naming the cat

# Create button rects
for i, cat in enumerate(cats):
    x = 100 + i * (button_width + button_gap)
    buttons.append(pygame.Rect(x, button_y, button_width, button_height))

# Main loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Handle text input
        if event.type == pygame.KEYDOWN and active_input:
            if event.key == pygame.K_BACKSPACE:
                if naming_cat:
                    cat_name = cat_name[:-1]
                else:
                    name = name[:-1]
            elif event.key == pygame.K_RETURN:
                if naming_cat:
                    active_input = False
                    naming_cat = False
                else:
                    active_input = False
            else:
                if naming_cat:
                    cat_name += event.unicode
                else:
                    name += event.unicode
        
        # Handle mouse clicks for cat selection
        if event.type == pygame.MOUSEBUTTONDOWN and not active_input and not naming_cat:
            mouse_pos = pygame.mouse.get_pos()
            for i, button in enumerate(buttons):
                if button.collidepoint(mouse_pos):
                    chosen_cat = cats[i]
                    active_input = True
                    naming_cat = True

    # Display instructions
    if active_input:
        if naming_cat:
            text_surface = font.render(f"Name your pet cat: {cat_name}", True, WHITE)
        else:
            text_surface = font.render("Enter your name: " + name, True, WHITE)
    else:
        if chosen_cat is None:
            text_surface = font.render(f"Hello, {name}! Choose your cat:", True, WHITE)
        else:
            text_surface = font.render(f"Cute! Hello {cat_name}!", True, WHITE)
    
    screen.blit(text_surface, (50, 50))

    # Draw cat buttons and images if no cat chosen
    if not active_input and chosen_cat is None:
        for i, button in enumerate(buttons):
            pygame.draw.rect(screen, BLUE, button)
            cat_text = font.render(cats[i], True, WHITE)
            text_rect = cat_text.get_rect(center=button.center)
            screen.blit(cat_text, text_rect)

            # Draw cat image above the button with consistent positioning
            img = cat_images[i]
            # Position the cat image with its bottom at a fixed distance above the button
            img_rect = img.get_rect(midbottom=(button.centerx, button.top - 20))
            screen.blit(img, img_rect)

    # Draw chosen cat if one is selected
    if chosen_cat is not None:
        i = cats.index(chosen_cat)
        img = cat_images[i]
        img_rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(img, img_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()






