from collections import Counter


class Bottle:
    def __init__(self, *args):
        self.capacity = 4
        self.colors = [arg for arg in args]

    def is_empty(self):
        return not self.colors

    def is_full(self):
        return len(self.colors) == self.capacity

    def is_single_colored(self):
        return len(set(self.colors)) == 1

    def is_sorted(self):
        return (self.is_single_colored() and self.is_full()) or self.is_empty()

    def count_layers(self):  # how many layers of the same color are in a specific vessel
        if self.is_empty():
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
        self.bottle_from = None
        self.bottle_to = None
        self.recursion_level = 1
        self.moves_history = []
        self.walkthrough = []

    def add_bottle(self, bottle):
        self.bottles.append(bottle)

    def check_data_input(self):
        color_list = []
        for bottle in self.bottles:
            color_list += bottle.colors
        color_counter = Counter(color_list)
        print('Input check:', color_counter)
        return all(color_counter[each] == 4 or color_counter[each] == 0 for each in color_counter)

    def status(self, step_hint=True):
        print()
        for i, bottle in enumerate(self.bottles):
            if step_hint and bottle is self.bottle_from:
                print(i+1, bottle.colors, '--> FROM')
            elif step_hint and bottle is self.bottle_to:
                print(i+1, bottle.colors, '<-- TO')
            else:
                print(i+1, bottle.colors)
        print()

    def all_drinks_sorted(self):
        return all(bottle.is_sorted() for bottle in self.bottles)

    def move(self, b, c):
        if b.colors:  # if the vessel is not empty
            if b is not c:  # if it's different from the one to pour into
                if c.is_empty() or (b.colors[-1] == c.colors[-1]):  # if the vessel to pour into is empty or the same color
                    if not b.is_sorted():  # if the vessel to pour from is not sorted yet
                        if not (b.is_single_colored() and c.is_empty()):  # prevent from moving color to an empty vessel is it's sorted but not yet full
                            room_available = c.capacity - len(c.colors)
                            if room_available:  # if there is room for color to be poured
                                if (c, b, b.colors[-1]) not in self.moves_history:  # prevent from moving one color between two vessels
                                    print('IN', self.recursion_level)
                                    self.recursion_level += 1
                                    self.bottle_from = b
                                    self.bottle_to = c
                                    self.status()
                                    layers = min(room_available, b.count_layers())
                                    for _ in range(layers):  # for a number of colors
                                        c.colors.append(b.colors.pop())  # append to the second vessel the color we take from first vessel
                                    self.moves_history.append((b, c, c.colors[-1]))
                                    return layers

    def sort(self):
        if self.all_drinks_sorted():
            return True

        for b in self.bottles:
            for c in self.bottles:
                move = self.move(b, c)
                if move:
                    self.sort()
                    if not self.all_drinks_sorted():
                        for _ in range(move):
                            b.colors.append(c.colors.pop())
                        self.moves_history.pop()
                        self.recursion_level -= 1
                        print('OUT', self.recursion_level)


def game_solver(game):
    if game.check_data_input():
        print('Input correct')
        game.status()
        game.sort()
    else:
        print('Input invalid')

    if game.all_drinks_sorted():
        print('Sorting completed')
    else:
        print('Sorting failed')
    game.status(step_hint=False)


game = Game()

game.add_bottle(Bottle('mint', 'lightblue', 'lightblue'))
game.add_bottle(Bottle('yellow', 'gray', 'pink', 'pink'))
game.add_bottle(Bottle('gray', 'violet', 'blue', 'blue'))
game.add_bottle(Bottle('purple', 'yellow', 'blue', 'skin'))
game.add_bottle(Bottle('lime', 'purple', 'lightblue', 'skin'))
game.add_bottle(Bottle('purple', 'purple'))
game.add_bottle(Bottle('violet', 'skin', 'lightblue', 'lime'))
game.add_bottle(Bottle('gray', 'violet', 'pink'))
game.add_bottle(Bottle('mint', 'violet', 'lime', 'mint'))
game.add_bottle(Bottle('lazur', 'red', 'yellow'))
game.add_bottle(Bottle('yellow'))
game.add_bottle(Bottle('skin', 'mint', 'blue', 'gray'))
game.add_bottle(Bottle('lime', 'red', 'lazur', 'lazur'))
game.add_bottle(Bottle('lazur', 'pink', 'red', 'red'))

game_solver(game)
