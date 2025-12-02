import pygame
from meal import Meal
from dot import Dot
from settings import DEFAULT_SETTINGS, Settings
import matplotlib.pyplot as plt


class Game_Life:

    def __init__(self, settings: Settings = DEFAULT_SETTINGS):
        self.settings = settings
        pygame.init()
        self.screen = pygame.display.set_mode((self.settings.board_width,
                                               self.settings.board_height))
        self.cell_size = self.settings.instance_size
        self.meal_size = self.settings.instance_size
        self.dots = []
        self.meals = []
        self.stats = []
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
            if (self.settings.dot_min_age_reproduction <= dot.age
               <= self.settings.dot_max_age_reproduction):
                if len(self.dots) < self.settings.dot_max_population:
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

        plt.ion()
        fig, ax = plt.subplots()
        line_count, = ax.plot([], [], label="Count")
        line_avg, = ax.plot([], [], label="Avg Age")
        ax.set_xlim(0, 700)
        ax.set_ylim(0, self.settings.dot_max_population + 10)
        ax.set_xlabel("Ticks")
        ax.set_ylabel("Value")
        ax.legend()

        tick_number = 0

        while run:
            clock.tick(self.settings.clock_frames)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if not self.dots:
                print("All dots dead")
                run = False
            else:
                ages = [dot.age for dot in self.dots]
                avg_age = sum(ages) / len(ages)
                tick_stats = {
                    "count": len(ages),
                    "avg_age": avg_age
                }
                self.stats.append(tick_stats)

                # Update live plot
                tick_number += 1
                xs = list(range(tick_number))
                counts = [s["count"] for s in self.stats]
                avgs = [s["avg_age"] for s in self.stats]

                line_count.set_data(xs, counts)
                line_avg.set_data(xs, avgs)

                ax.set_xlim(0, max(700, tick_number))
                ax.set_ylim(0, max(self.settings.dot_max_population + 10,
                                   max(avgs)+5))
                fig.canvas.draw()
                fig.canvas.flush_events()

            self.screen.fill((0, 0, 0))
            self.update()
            self.draw()
            pygame.display.update()

        plt.ioff()
        plt.show()
