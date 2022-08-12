import random


face = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']


class Dice:
    def __init__(self, sides, value=6, color='white', dot_color='black'):
        self.sides = sides
        self.value = value

    def __str__(self):
        return f"{face[self.value - 1]}"

    def get_value(self):
        return self.value

    def roll(self):
        self.value = random.randint(1, self.sides)

