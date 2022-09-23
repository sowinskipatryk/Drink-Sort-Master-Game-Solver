from collections import Counter


class Bottle:
    def __init__(self, *args):
        self.capacity = 4
        self.colors = [arg for arg in args]

    def is_sorted(self):  # checks if the bottle is sorted (four segments in one color or empty)
        return (len(set(self.colors)) == 1 and len(self.colors) == self.capacity) or not self.colors

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
        self.bottle_from = None
        self.bottle_to = None
        self.recursion_level = 1
        self.moves_history = []

    def add(self, bottle):
        self.bottles.append(bottle)

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

    def check_data_input(self):
        color_list = []
        for b in self.bottles:
            color_list += b.colors
        counter = Counter(color_list)
        print('Input check:', counter)
        return all(counter[each] == 4 or counter[each] == 0 for each in counter)

    def all_drinks_sorted(self):
        return all(b.is_sorted() for b in self.bottles)

    def move(self, x, y):
        if x.colors:  # if the vessel is not empty
            if x is not y:  # if it's different from the one to pour into
                if not y.colors or (x.colors[-1] == y.colors[-1]):  # if the vessel to pour into is empty or the same color
                    if not x.is_sorted():  # if the vessel to pour from is not sorted yet
                        if not (len(set(x.colors)) == 1 and not y.colors):  # prevent from moving color to an empty vessel is it's sorted but not yet full
                            space = y.capacity - len(y.colors)
                            if space:  # if there is room for color to be poured
                                if (y, x, x.colors[-1]) not in self.moves_history:  # prevent from moving one color between two vessels
                                    print('IN', self.recursion_level)
                                    self.recursion_level += 1
                                    self.bottle_from = x
                                    self.bottle_to = y
                                    self.status()
                                    limit = min(space, x.count_same_colors())
                                    for _ in range(limit):  # for a number of colors
                                        y.colors.append(x.colors.pop())  # append to the second vessel the color we take from first vessel
                                    self.moves_history.append((x, y, y.colors[-1]))
                                    return limit

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

game.add(Bottle('mint', 'lightblue', 'lightblue'))
game.add(Bottle('yellow', 'gray', 'pink', 'pink'))
game.add(Bottle('gray', 'violet', 'blue', 'blue'))
game.add(Bottle('purple', 'yellow', 'blue', 'skin'))
game.add(Bottle('lime', 'purple', 'lightblue', 'skin'))
game.add(Bottle('purple', 'purple'))
game.add(Bottle('violet', 'skin', 'lightblue', 'lime'))
game.add(Bottle('gray', 'violet', 'pink'))
game.add(Bottle('mint', 'violet', 'lime', 'mint'))
game.add(Bottle('lazur', 'red', 'yellow'))
game.add(Bottle('yellow'))
game.add(Bottle('skin', 'mint', 'blue', 'gray'))
game.add(Bottle('lime', 'red', 'lazur', 'lazur'))
game.add(Bottle('lazur', 'pink', 'red', 'red'))

game_solver(game)
