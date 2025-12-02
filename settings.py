from dataclasses import dataclass


@dataclass
class Settings:
    board_w: int = 400
    board_h: int = 400
    size: int = 20
    initial_dots: int = 4
    initial_meals: int = 100
    clock_frames: int = 8
    meal_energy: int = 30
    repro_threshold: int = 110
    min_repro: int = 17
    max_repro: int = 55
    dot_max_age: int = 120
    dot_initial_energy = 100
    min_reproduction: int = 17
    max_reproduction: int = 55


DEFAULT_SETTINGS = Settings()
