import pygame
from meal import Meal
from dot import Dot


class Game_Life:

    MIN_REPRODUCTION = 17
    MAX_REPRODUCTION = 55
    CLOCK_FRAMES = 10
    INITIAL_MEALS = 80
    INITIAL_DOTS = 5
    WIDTH = 400
    HEIGHT = 400
    SIZE = 20

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.cell_size = self.SIZE
        self.meal_size = self.SIZE
        self.dots = []
        self.meals = []
        self.font = pygame.font.SysFont('Arial', 12)

        for _ in range(self.INITIAL_DOTS):
            self.dots.append(Dot())

        for _ in range(self.INITIAL_MEALS):
            self.meals.append(Meal())

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
            if (dot.age >= self.MIN_REPRODUCTION and
               dot.age <= self.MAX_REPRODUCTION):
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
                self.meals.append(Meal())

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
            clock.tick(self.CLOCK_FRAMES)
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
