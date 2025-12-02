from dataclasses import dataclass


@dataclass
class Settings:
    clock_frames: int = 5
    board_width: int = 400
    board_height: int = 400
    instance_size: int = 20
    initial_dots: int = 5
    initial_meals: int = 200
    meal_energy: int = 35
    dot_initial_energy = 100
    dot_min_age_reproduction: int = 16
    dot_max_age_reproduction: int = 501
    dot_reproduction_threshold: int = 115
    dot_max_life_age: int = 115
    dot_max_population = 200


DEFAULT_SETTINGS = Settings()
