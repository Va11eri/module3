from random import randint


class BoardOutExceptions(Exception):
    pass


class BoardUsedException(Exception):
    pass


class BoardWrongShipException(Exception):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, bow, l, o ):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y
            if self.o == 0:        #вертикаль
                cur_x += 1
            elif self.o == 1:        #горизонталь
                cur_y += 1
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots
    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.hid = hid
        self.size = size
        self.count = 0                      #кол-во раненных кораблей
        self.field = [['0'] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    def __str__(self):
        saw = ''
        saw += '    1   2   3   4   5   6'
        for i, row in enumerate(self.field):
            saw += f'\n{i + 1} | '+' | '.join(row)+' |'
        if self.hid:
            saw = saw.replace('&','o')
        return saw

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        near = [
            (-1, 1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
            ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = '&'
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutExceptions()
        if d in self.busy:
            raise BoardUsedException()
        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = 'X'
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Ship killed!")
                    return False
                else:
                    print("The Ship is wounded!")
                    return True

        self.field[d.x][d.y] = "."
        print("Miss")
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                purpose = self.ask()
                repeat = self.enemy.shot(purpose)
                return repeat
            except Exception as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0,5), randint(0,5))
        print(f"Move AI: {d.x+1} {d.y+1}")
        return d


class User(Player):
    def ask(self):
        while True:
            coordinates = input("Enter your move: ").split()
            if len(coordinates) != 2:
                print("Enter two numbers:")
                continue

            x, y = coordinates
            if not (x.isdigit()) or not (y.isdigit()):
                print("You must enter two numbers")
                continue
            x, y = int(x), int(y)

            return Dot(x-1, y-1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 1000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass

        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board


    def greetings(self):
        print("Welcome to the game 'Battleship'")
        print("You need to enter two numbers, x and y")
        print("x - it is line's number, y -it is column's number")

    def loop(self):
        num = 0
        while True:
            print("Player board")
            print(self.us.board)
            print("AI board")
            print(self.ai.board)
            if num % 2 == 0:
                print("User's move: ")
                repeat = self.us.move()
            else:
                print("AI's move: ")
                repeat = self.ai.move()

            if repeat:
                num -= 1
            if self.ai.board.count == 7:
                print("User win!")
                break
            if self.us.board.count == 7:
                print("AI win")
                break
            num += 1

    def start(self):
        self.greetings()
        self.loop()


g = Game()
g.start()












