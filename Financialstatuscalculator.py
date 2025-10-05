import pygame


class FinancialStatus:
    def __init__(self, income=50):
        self.income = income
        self.spending = 0
        self.savings = 0
        self.debt = 0
        self.debt_carry = 0
        self.week = 1
        self.base_income = income
        self.message = "Let's take care of your cat!🐾"
        self.cat_face = "😺"

        # Visual
        self.bg_color = (255, 248, 240)
        self.panel_color = (255, 255, 255)
        self.text_color = (40, 40, 40)
        self.green = (144, 238, 144)
        self.yellow = (255, 223, 99)
        self.blue = (173, 216, 230)
        self.red = (255, 105, 97)
        self.gray = (210, 210, 210)

        # Fonts
        self.font = pygame.font.Font(None, 28)
        self.title_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 22)
        self.annotation_font = pygame.font.Font(None, 24)

    def add_spending(self, amount):
        self.spending += amount
        self.update_balance()

    def add_saving(self, amount):
        self.savings += amount
        self.update_balance()

    def update_balance(self):
        total_spent = self.spending

        if total_spent > self.income:
            self.debt = total_spent - self.income
            self.savings = 0
            self.message = "Oh no! You overspent 💸"
            self.cat_face = "😿"
        else:
            self.debt = 0
            self.savings = self.income - self.spending
            if self.savings >= 20:
                self.message = "You saved more than £20, that's impressive!"
                self.cat_face = "😻"
            elif self.savings > 0:
                self.message = "Nice job, you saved some money!"
                self.cat_face = "😺"
            else:
                self.message = "All spent! Be careful next time!"
                self.cat_face = "😿"

    def next_week(self):
        self.week += 1
        if self.debt > 0:
            self.debt_carry += self.debt
        self.spending = 0
        self.income = max(self.base_income - self.debt_carry, 0)
        self.update_balance()
        self.message = f"Week {self.week} begins! You earned £{self.base_income}, but owe £{self.debt_carry}."
        self.cat_face = "🐾"

    def get_summary(self):
        return {
            "Week": self.week,
            "Income": self.income,
            "Spending": self.spending,
            "Savings": self.savings,
            "Debt": self.debt,
            "Debt carried": self.debt_carry
        }

    def draw_chart(self, screen, x, y):
        # green - savings
        # yellow = spending
        # red = debt

        total = self.income if self.income > 0 else 1

        spent_ratio = self.spending / total
        savings_ratio = self.savings / total
        debt_ratio = self.debt / total

        start_x = x

        pygame.draw.rect(screen, self.gray, (x, y, 300, 30), border_radius=8)

        # Spending (yellow)
        spent_width = 300 * spent_ratio
        pygame.draw.rect(screen, self.yellow,
                         (start_x, y, spent_width, 30), border_radius=8)
        start_x += spent_width

        # Savings (green)
        save_width = 300 * savings_ratio
        pygame.draw.rect(screen, self.green,
                         (start_x, y, save_width, 30), border_radius=8)
        start_x += save_width

        # Debt (red)
        if self.debt > 0:
            debt_width = 300 * debt_ratio
            pygame.draw.rect(screen, self.red,
                             (start_x, y, debt_width, 30), border_radius=8)

        pygame.draw.rect(screen, (80, 80, 80),
                         (x, y, 300, 30), 2, border_radius=8)

        # numbers above chart
        self.draw_numbers(screen, x, y - 25)
        self._draw_legend(screen, x, y + 80)

        self.draw_annotations(screen, x, y + 40, spent_width,
                              save_width, debt_ratio > 0)

    def draw_annotations(self, screen, x, y, spent_width, save_width, has_debt):
        spend_label = self.annotation_font.render(
            f"Spent £{self.spending}", True, self.text_color)
        screen.blit(spend_label, (x, y))

        if self.savings > 0:
            save_label = self.annotation_font.render(
                f"Saved £{self.savings}", True, self.text_color)
            screen.blit(save_label, (x + spent_width + 5, y))

        if has_debt:
            debt_label = self.annotation_font.render(
                f"Debt £{self.debt}", True, self.text_color)
            screen.blit(debt_label, (x + spent_width + save_width + 10, y))

    def _draw_legend(self, screen, x, y):
        colors = [
            ("Spending", self.yellow),
            ("Savings", self.green),
            ("Debt", self.red)
        ]
        offset = 0
        for label, color in colors:
            pygame.draw.rect(screen, color, (x+offset, y, 20, 20))
            text = self.font.render(label, True, self.text_color)
            screen.blit(text, (x + offset + 25, y - 2))
            offset += 130

    def draw_numbers(self, screen, x, y):
        summary_text = f"🛒 Spending: £{self.spending} | 🏦 Savings: £{self.savings} | 💳 Debt: £{self.debt} | 📉 Debt carry: £{self.debt_carry} | 💰 Income: £{self.income}"

        box_width, box_height = 720, 55
        box_x, box_y = x - 50, y - 100

        pygame.draw.rect(screen, (255, 255, 255), (box_x + 3, box_y+3,
                         box_width, box_height), border_radius=12)
        pygame.draw.rect(screen, (200, 200, 200), (box_x, box_y,
                         box_width, box_height), border_radius=12)

        numbers = self.font.render(summary_text, True, (50, 50, 50))
        text_rect = numbers.get_rect(
            center=(x+box_width/2 - 50, y + box_height/2 - 100))
        screen.blit(numbers, text_rect)

    def draw_status(self, screen, x, y):
        pygame.draw.rect(screen, (240, 240, 240),
                         (x - 30, y - 30, 420, 200), border_radius=10)

        # Title
        title = self.font.render(
            "Your Financial Summary", True, self.text_color)
        screen.blit(title, (x, y-20))

        # Chart
        self.draw_chart(screen, x+20, y + 20)

        # Cat face
        cat_text = self.font.render(self.cat_face, True, (0, 0, 0))
        screen.blit(cat_text, (x+350, y-10))

        # message
        msg = self.font.render(self.message, True, self.text_color)
        screen.blit(msg, (x+150, y+200))

        # Short summary
        summary = self.get_budget_summary()
        summary_text = self.font.render(summary, True, (100, 100, 100))
        screen.blit(summary_text, (x+20, y+140))

    def get_budget_summary(self):
        if self.debt > 0:
            return "You owe money! try cutting spending next time 😿 "
        elif self.savings >= 20:
            return "Excellent! It seems like you are going to make an investment soon 😺"
        elif self.savings > 0:
            return "You balanced your week well. Keep saving! 🐾"
        else:
            return "No savings left = let's plan better next week! 🫙"


    # example
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((850, 750))
    pygame.display.set_caption("FinCat Calculator")
    clock = pygame.time.Clock()

    finance = FinancialStatus(50)
    finance.add_spending(20)
    finance.add_saving(0)

    running = True
    while running:
        screen.fill((255, 255, 255))
        finance.draw_status(screen, 100, 200)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(30)
    pygame.quit()
