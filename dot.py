import pygame
import random


class Dot:
    REPRO_THRESHOLD = 110
    MAXIMUM_AGE = 110
    ENERGY = 100

    def __init__(self):
        self.age = 0
        self.max_age = self.MAXIMUM_AGE
        self.energy = self.ENERGY
        self.color = (random.randint(0, 255), random.randint(0, 255),
                      random.randint(0, 255))

        self.position = [random.randint(0, 19), random.randint(0, 19)]

    def move(self):
        direction = random.choice(['up', 'down', 'left', 'right'])
        if direction == 'up':
            self.position[1] = max(0, self.position[1] - 1)
        elif direction == 'down':
            self.position[1] = min(19, self.position[1] + 1)
        elif direction == 'left':
            self.position[0] = max(0, self.position[0] - 1)
        elif direction == 'right':
            self.position[0] = min(19, self.position[0] + 1)

    def live(self):
        if self.energy > 0 and self.age < self.max_age:
            self.age += 1
            self.energy -= 1
            return True
        return False

    def reproduce(self):
        if self.energy >= self.REPRO_THRESHOLD:
            child_energy = self.energy // 2
            self.energy -= child_energy

            baby = Dot()
            baby.age = 0

            neighbors = []
            x, y = self.position
            if x > 0:
                neighbors.append((x-1, y))
            if x < 19:
                neighbors.append((x+1, y))
            if y > 0:
                neighbors.append((x, y-1))
            if y < 19:
                neighbors.append((x, y+1))

            if not neighbors:
                return None

            new_x, new_y = random.choice(neighbors)
            baby.position = [new_x, new_y]
            baby.energy = int(child_energy)
            return baby
        return None

    def draw(self, screen, cell_size, font):
        x = self.position[0] * cell_size
        y = self.position[1] * cell_size
        pygame.draw.rect(screen, self.color, (x, y, cell_size, cell_size))
        text_surface = font.render(str(self.age), True, (255, 255, 255))
        screen.blit(text_surface, (x, y + 5))
