import pygame


class TutorialSlide:
    def __init__(self, text, bg_color=(255, 248, 240)):
        self.text = text
        self.bg_color = bg_color


class FinCatTutorial:
    def __init__(self):
        # Initialize PyGame
        pygame.init()
        # Set up the window
        self.screen = pygame.display.set_mode((850, 750), pygame.RESIZABLE)
        pygame.display.set_caption("🐾 FinCat Tutorial")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)

        # Colors
        self.text_color = (60, 60, 60)
        self.bg_color = (255, 248, 240)
        self.button_color = (255, 223, 99)

        self.slides = [
            TutorialSlide(
                "Are you ready to put your financial skills to the test?\n\n"
                "In FinCat, your mission is simple: keep your cat happy and healthy "
                "while managing your money wisely. If you make wise decisions your cat will remain happy and healthy.\n\n"
                "But if you make poor decisions your cat can become upset/angry and even get sick. \n\n "
                "Every decision you make, big or small, will directly affect your cat. "
                "If you manage to balance fun and finance you will have a positive experience, "
                "but if you don’t then there will be consequences. \n\n"
                "Start the game and see the impact of your choices unfold. \n\n"
                "Good Luck! 😺"
            ),
            TutorialSlide(
                "As the player you will have a weekly income of £50 which you can spend or save."),
            TutorialSlide(
                "There are three categories you have to take care of."),
            TutorialSlide("You have to feed, clean and play with your cat although the quality and prices of the products you buy will have a direct impact on your cat's lifestyle and mood. So choose wisely."),
            TutorialSlide(
                "As you purchase food and products your balance in your account will start to decrease."),
            TutorialSlide("In order to invest, you can buy blocks to build a tower. You can make your cat a happy and comfortable home by adding more blocks onto the tower by investing your money.")
        ]

        self.current_slide = 0

    def draw_slide(self):
        slide = self.slides[self.current_slide]
        self.screen.fill(slide.bg_color)

        # Text Box
        text_box = pygame.Rect(75, 150, 650, 500)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         text_box, border_radius=20)
        pygame.draw.rect(self.screen, (200, 200, 200),
                         text_box, 3, border_radius=20)

        lines = self.wrap_text(slide.text, 60)
        for i, line in enumerate(lines):
            text_s = self.font.render(line, True, self.text_color)
            self.screen.blit(text_s, (100, 170 + i * 40))

        counter_text = self.small_font.render(
            f"Slide {self.current_slide + 1}/{len(self.slides)}", True, (120, 120, 120))
        self.screen.blit(counter_text, (700, 650))

        # Navigation
        hint = self.small_font.render(
            "Press -> or SPACE to continue, <- to go back", True, (120, 120, 120))
        self.screen.blit(hint, (75, 650))

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

    def run_tutorial(self):
        running = True
        while running:
            self.screen.fill((255, 255, 255))

            self.draw_slide()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RIGHT, pygame.K_SPACE]:
                        self.current_slide += 1
                        if self.current_slide >= len(self.slides):
                            running = False  # end
                    elif event.key == pygame.K_LEFT:
                        self.current_slide = max(0, self.current_slide - 1)

            self.clock.tick(30)

        pygame.quit()


if __name__ == "__main__":
    tutorial = FinCatTutorial()
    tutorial.run_tutorial()
