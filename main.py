from collections import Counter


class Bottle:
    def __init__(self, *args):
        self.capacity = 4
        self.colors = [arg for arg in args]
        self.occupancy = len(self.colors)

    def is_sorted(self):  # checks if the bottle is sorted (one color or empty)
        return (len(set(self.colors)) == 1 and len(self.colors) == 4) or not self.colors

    def count_same_colors(self):  # counts how many layers of the same color are in a specific vessel
        if not self.colors:
            return 0

        counter = 1
        for i in range(-1, -len(self.colors), -1):
            if self.colors[i] == self.colors[i - 1]:
                counter += 1
            else:
                return counter
        return counter


class Game:
    bottles = []

    def add(self, bottle):
        self.bottles.append(bottle)

    def check_data_input(self):
        color_list = []
        for b in self.bottles:
            color_list += b.colors
        counter = Counter(color_list)
        print(counter)
        return all(counter[each] == 4 or counter[each] == 0 for each in counter)

    def all_drinks_sorted(self):
        return all(b.is_sorted() for b in self.bottles)

    def move(self, x, y, z):
        if x.colors:  # if the vessel is not empty
            if x is not y:  # if it's different from the one to pour into
                if z + len(y.colors) <= 4:  # if there is space for a number of colors
                    if not y.colors or (x.colors[-1] == y.colors[-1]):  # if the vessel to pour into is empty or the same color
                        for _ in range(z):  # for a number of colors
                            y.colors.append(x.colors.pop())  # append to the second vessel the color we take from first vessel
                        return True

    def sort(self):
        if self.all_drinks_sorted():
            return True

        for b in self.bottles:
            for c in self.bottles:
                for d in range(1, b.count_same_colors() + 1):
                    if self.move(b, c, d):
                        print('I')
                        self.sort()
        print('O')
        return False


game = Game()
game.add(Bottle('mint', 'green', 'blue', 'blue'))
game.add(Bottle('sea', 'light blue', 'gray', 'yellow'))
game.add(Bottle('green', 'yellow', 'gray', 'sea'))
game.add(Bottle('light blue', 'red', 'pink', 'yellow'))
game.add(Bottle('yellow', 'dark blue', 'pink'))
game.add(Bottle('blue', 'skin', 'skin'))
game.add(Bottle('pink', 'pink', 'light blue'))
game.add(Bottle('dark blue', 'gray', 'light blue'))
game.add(Bottle('dark blue', 'green', 'sea', 'dark blue'))
game.add(Bottle('mint', 'green', 'orange', 'gray'))
game.add(Bottle('blue', 'skin', 'red'))
game.add(Bottle('red', 'mint', 'mint'))
game.add(Bottle('sea', 'skin', 'orange', 'red'))
game.add(Bottle('orange', 'orange'))

game.sort()

for bottle in game.bottles:
    print(bottle.colors)
