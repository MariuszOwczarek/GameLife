import pygame
from meal import Meal
from dot import Dot
from settings import DEFAULT_SETTINGS, Settings


class Game_Life:

    def __init__(self, settings: Settings = DEFAULT_SETTINGS):
        self.settings = settings
        pygame.init()
        self.screen = pygame.display.set_mode((self.settings.board_w,
                                               self.settings.board_h))
        self.cell_size = self.settings.size
        self.meal_size = self.settings.size
        self.dots = []
        self.meals = []
        self.font = pygame.font.SysFont('Arial', 12)

        for _ in range(self.settings.initial_dots):
            self.dots.append(Dot(self.settings))

        for _ in range(self.settings.initial_meals):
            self.meals.append(Meal(self.settings))

    def update(self):
        alive_dots = []
        babies_to_add = []
        meals_to_remove = []
        planned_baby_positions = set()

        occupied = {(d.position[0], d.position[1]) for d in self.dots}

        for dot in self.dots:
            dot.move()
            if not dot.live():
                continue

            for meal in self.meals:
                if (
                    (meal.position[0], meal.position[1]) ==
                    (dot.position[0], dot.position[1])
                ):
                    dot.energy += meal.energy
                    meals_to_remove.append(meal)
                    break

            baby = None
            if (dot.age >= self.settings.min_reproduction and
               dot.age <= self.settings.max_reproduction):
                baby = dot.reproduce()

            if baby:
                baby_pos = (baby.position[0], baby.position[1])
                if (
                    baby_pos not in occupied
                    and baby_pos not in planned_baby_positions
                ):
                    babies_to_add.append(baby)
                    planned_baby_positions.add(baby_pos)

            alive_dots.append(dot)
            occupied.add((dot.position[0], dot.position[1]))

        if meals_to_remove:
            self.meals = [m for m in self.meals if m not in meals_to_remove]
            for _ in range(len(meals_to_remove)):
                self.meals.append(Meal(self.settings))

        if babies_to_add:
            alive_dots.extend(babies_to_add)

        self.dots = alive_dots

    def draw(self):
        for dot in self.dots:
            dot.draw(self.screen, self.cell_size, self.font)

        for meal in self.meals:
            meal.draw(self.screen, self.meal_size)

        number_dots = self.font.render(str(f'Ilość: {len(self.dots)}'),
                                       True, (255, 255, 255))
        self.screen.blit(number_dots, (10, 10))
        if self.dots:
            oldest_dot = max(self.dots, key=lambda d: d.age)
            oldest_age = oldest_dot.age
        else:
            oldest_age = 0
        oldest = self.font.render(str(f'Wiek: {oldest_age}'),
                                  True, (255, 255, 255))
        self.screen.blit(oldest, (10, 30))

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(self.settings.clock_frames)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if len(self.dots) == 0:
                print("All dots dead")
                run = False

            self.screen.fill((0, 0, 0))
            self.update()
            self.draw()
            pygame.display.update()
