import random


def get_variable_int(base_value: int, variation_value: int):
    random_offset = random.randint(-variation_value, variation_value)
    return base_value + random_offset


def get_variable_float(base_value: float, variation_value: float):
    random_offset = random.uniform(-variation_value, variation_value)
    return base_value + random_offset
