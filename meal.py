import random
import pygame
from settings import Settings


class Meal:

    def __init__(self, settings: Settings):
        self.settings = settings
        self.energy = self.settings.meal_energy
        self.color = (50, 190, 28)
        self.position = [random.randint(0, 19), random.randint(0, 19)]

    def draw(self, screen, meal_size):
        x = self.position[0] * meal_size
        y = self.position[1] * meal_size
        pygame.draw.rect(screen, self.color, (x, y, meal_size, meal_size))
