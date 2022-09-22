from collections import Counter


class Bottle:
    def __init__(self, *args):
        self.capacity = 4
        self.colors = [arg for arg in args]

    def is_sorted(self):  # checks if the bottle is sorted (four segments in one color or empty)
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
    def __init__(self):
        self.bottles = []
        self.moves_history = []
        self.bottle_from = None
        self.bottle_to = None
        self.recursion_level = 1

    def add(self, bottle):
        self.bottles.append(bottle)

    def status(self):
        print()
        for i, bottle in enumerate(self.bottles):
            if bottle is self.bottle_from:
                print(i+1, bottle.colors, '--> FROM')
            elif bottle is self.bottle_to:
                print(i+1, bottle.colors, '<-- TO')
            else:
                print(i+1, bottle.colors)
        print()

    def check_data_input(self):
        color_list = []
        for b in self.bottles:
            color_list += b.colors
        counter = Counter(color_list)
        print('Check:', counter)
        return all(counter[each] == 4 or counter[each] == 0 for each in counter)

    def all_drinks_sorted(self):
        return all(b.is_sorted() for b in self.bottles)

    def move(self, x, y, z):
        if x.colors:  # if the vessel is not empty
            if x is not y:  # if it's different from the one to pour into
                if z + len(y.colors) <= 4:  # if there is space for a number of colors
                    if not y.colors or (x.colors[-1] == y.colors[-1]):  # if the vessel to pour into is empty or the same color
                        if not x.is_sorted():  # if the vessel to pour from is not sorted yet
                            if not (z + len(y.colors) == 4 and (x.count_same_colors() > z)):
                            # if (y, x, x.colors[-1]) not in self.moves_history:  # prevent hopping between the same two vessels
                                for _ in range(z):  # for a number of colors
                                    y.colors.append(x.colors.pop())  # append to the second vessel the color we take from first vessel
                                self.moves_history.append((x, y, y.colors[-1]))
                                self.bottle_from = x
                                self.bottle_to = y
                                return True

    def sort(self):
        if self.all_drinks_sorted():
            return True

        for b in self.bottles:
            for c in self.bottles:
                for d in range(1, b.count_same_colors() + 1):
                    if self.move(b, c, d):
                        print('IN', self.recursion_level)
                        self.recursion_level += 1
                        self.status()
                        self.sort()
                        self.moves_history.pop()
                        self.recursion_level -= 1
                        print('OUT', self.recursion_level)


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

if game.check_data_input():
    print('Correct input')
    game.status()
    game.sort()
else:
    print('Invalid input\n')

if game.all_drinks_sorted():
    print('Sorting completed')
else:
    print('Sorting failed')
