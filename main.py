from functools import total_ordering
import pickle
# Поработаем с магическими методами на примере сюжета игры Super Mario Bros.


@total_ordering
class MarioPlayer:
    def __init__(self, name, score,  lives):
        self.name = name
        self.score = score
        self.lives = lives
        self.status = [name, score, lives]

    def __getitem__(self, item):
        return self.status[item]

    def __del__(self):
        del self.status

    def __str__(self):
        return f'name 🏃 {self.status[0]}, score 📋 {self.status[1]}, lives ❤ {self.status[2]}'

    def __eq__(self, other):
        return self.status[1] == other.status[1]    # проводим сравнение игроков по очкам

    def __gt__(self, other):
        return self.status[1] > other.status[1]
# так как мы используем @total_ordering, остальные методы сравнения можем не прописывать
# применим __le__, хотя он не прописан

    def __add__(self, other):
        return MarioPlayer(self.name, self.score + other.score, self.lives)
# метод сложения прибавляет очки противника

    def __sub__(self, other):
        return MarioPlayer(self.name, self.score, self.lives - other.lives)
# метод вычитания отнимает жизни

    def __mul__(self, other):
        return MarioPlayer(self.name, self.score * other, self.lives)

    def __call__(self, other):      # вызов экземпляра при взаимодействии с противником или с бонусом
        if isinstance(other, MarioPlayer):
            return MarioPlayer(self.name, self.score + other.score, self.lives)
        elif isinstance(other, int):
            return MarioPlayer(self.name, self.score, self.lives + other)

    def __getstate__(self):             # метод для сериализации
        return self.status

    def __setstate__(self, state):      # метод для десериализации
        self.status = state


if __name__ == '__main__':
    Mario = MarioPlayer('Mario', 0, 3)
    Luigi = MarioPlayer("Luigi", 0, 3)
    mushroom = MarioPlayer('', 10, 1)   # противник - грибочек
    turtle = MarioPlayer('', 50, 1)     # противник - черепаха
    bonus = 1       # +1 жизнь
    print('Метод __str__:')
    print(Mario)
    print(Luigi)
    print('Метод __getitem__:')
    print(Mario[2])
    print('Методы __add__, __sub__, __mul__:')
    Mario += mushroom
    Mario -= turtle
    print(Mario)    # Марио раздавил грибочек, но не справился с черепахой
    Luigi += mushroom * 2
    print(Luigi)    # Луиджи прыгнул на 2 гриба
    print('Методы __eq__, __le__:')
    print(Mario == Luigi)
    print(Mario <= Luigi)
    print('Метод __call__:')
    print(Mario(turtle))    # Марио отомстил черепахе
    print(Mario(bonus))     # Марио восстановил 1 жизнь
    print('Метод __getstate__ (сериализация) и __setstate__ (десериализация):')
    # сериализация
    f = open('SuperMario.pkl', 'wb')
    pickle.dump(Luigi, f)
    f.close()
    # десериализация
    f = open('SuperMario.pkl', 'rb')
    read_from_pickle = pickle.load(f)
    print(Luigi)
    print(read_from_pickle)     # данные совпадают
    f.close()

    del Mario, Luigi    # очистка памяти
