import random
import pygame


class Meal:

    MEAL_ENERGY = 25

    def __init__(self):
        self.energy = self.MEAL_ENERGY
        self.color = (50, 190, 28)
        self.position = [random.randint(0, 19), random.randint(0, 19)]

    def draw(self, screen, meal_size):
        x = self.position[0] * meal_size
        y = self.position[1] * meal_size
        pygame.draw.rect(screen, self.color, (x, y, meal_size, meal_size))
