import pygame, random, time

pygame.init()
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Pizza Tycoon")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Список клиентов и заказов
clients = []
active_order = None
score = 0

class Client:
    def __init__(self):
        self.name = random.choice(["Аня", "Боб", "Клара", "Игорь"])
        self.toppings = random.sample(["сыр", "пепперони", "грибы", "ананас"], 2)
        self.time_limit = 20  # секунд
        self.start_time = time.time()

    def is_time_up(self):
        return time.time() - self.start_time > self.time_limit

    def draw(self, surface, y):
        text = f"{self.name} хочет: {', '.join(self.toppings)}"
        t = font.render(text, True, (0, 0, 0))
        surface.blit(t, (20, y))

# Кнопки выбора топпингов
topping_buttons = []

class ToppingButton:
    def __init__(self, name, x, y):
        self.name = name
        self.rect = pygame.Rect(x, y, 100, 40)

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 150, 100), self.rect)
        label = font.render(self.name, True, (0, 0, 0))
        screen.blit(label, (self.rect.x + 5, self.rect.y + 5))

    def handle_click(self, selected):
        if self.name not in selected:
            selected.append(self.name)

# Инициализация кнопок
for i, t in enumerate(["сыр", "пепперони", "грибы", "ананас"]):
    topping_buttons.append(ToppingButton(t, 700, 100 + i * 50))

selected_toppings = []
running = True
spawn_timer = 0

while running:
    screen.fill((245, 230, 200))
    confirm_clicked = False  # Сброс каждый кадр

    # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for btn in topping_buttons:
                if btn.rect.collidepoint(event.pos):
                    btn.handle_click(selected_toppings)

            confirm_rect = pygame.Rect(700, 400, 200, 50)
            if confirm_rect.collidepoint(event.pos):
                confirm_clicked = True

    # Создание новых клиентов
    if time.time() - spawn_timer > 5 and len(clients) < 5:
        clients.append(Client())
        spawn_timer = time.time()

    # Отображение клиентов
    i = 0
    while i < len(clients):
        client = clients[i]
        client.draw(screen, 20 + i * 50)
        if client.is_time_up():
            clients.pop(i)
            score -= 5
        else:
            i += 1

    # Кнопки топпингов
    for btn in topping_buttons:
        btn.draw(screen)

    # Кнопка "Готово"
    confirm_rect = pygame.Rect(700, 400, 200, 50)
    pygame.draw.rect(screen, (50, 180, 50), confirm_rect)
    screen.blit(font.render("Готово", True, (255, 255, 255)), (740, 410))

    # Обработка заказа
    if confirm_clicked and clients:
        current = clients[0]
        if set(selected_toppings) == set(current.toppings):
            score += 10
        else:
            score -= 5
        clients.pop(0)
        selected_toppings = []

    # Очки
    score_text = font.render(f"Очки: {score}", True, (0, 0, 0))
    screen.blit(score_text, (800, 20))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
