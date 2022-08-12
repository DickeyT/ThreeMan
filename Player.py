class Player:
    def __init__(self, name, is_current=False, is_three=False, is_ai=False):
        self.name = name
        self.points = 75
        self.double_count = 0
        self.is_current = is_current
        self.is_three = is_three
        self.is_ai = is_ai

    def __str__(self):
        return self.name

    def display(self):
        return f'Name: {self.name}\nPoints: {self.points}\nDouble Count: {self.double_count}\n' \
               f'Is Current: {self.is_current}\nIs Three: {self.is_three}\nIs AI: {self.is_ai}'

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def toggle_three(self):
        self.is_three = not self.is_three

    def set_three(self):
        self.is_three = True

    def get_current(self):
        return self.is_current

    def set_current(self, bool=True):
        self.is_current = bool

    def toggle_current(self):
        self.is_current = not self.is_current

    def get_points(self):
        return self.points

    def set_points(self, points):
        self.points = points

    def sub_points(self, change):
        self.points -= change

    def add_points(self, change):
        self.points += change

    def get_double_count(self):
        return self.double_count

    def set_double_count(self, count):
        self.double_count = count

    def add_double_count(self, count):
        self.double_count += count

    def reset_double_count(self):
        self.double_count = 0


