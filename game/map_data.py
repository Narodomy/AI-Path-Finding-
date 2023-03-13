from game.entities import Ball, Coin
from game.map import Wall, Win


class MapLevel01:
    def __init__(self):
        # Player position
        self.player_x = 75
        self.player_y = 146

        self.coin = Coin()
        self.area = Win(738, 84, 1, 42)
        self.ball1 = Ball(235, 154, 1)
        self.ball2 = Ball(665, 202, 2)
        self.ball3 = Ball(235, 250, 3)
        self.ball4 = Ball(665, 298, 4)

        # Lists
        self.balls = [self.ball1, self.ball2, self.ball3, self.ball4]

        for ball in self.balls:
            ball.limit = [665, 235]

        self.wall1 = Wall(15, 78, 6, 294, 'e')
        self.wall2 = Wall(255, 318, 437, 6, 'i')
        self.wall3 = Wall(207, 126, 437, 6, 's')
        self.wall4 = Wall(15, 366, 245, 6, 'i')
        self.wall5 = Wall(15, 78, 150, 6, 's')
        self.wall6 = Wall(879, 78, 6, 294, 'd')
        self.wall7 = Wall(159, 78, 6, 245, 'd')
        self.wall8 = Wall(159, 318, 53, 6, 's')
        self.wall8 = Wall(255, 318, 6, 53, 'd')
        self.wall9 = Wall(639, 78, 6, 53, 'e')
        self.wall10 = Wall(639, 78, 245, 6, 's')
        self.wall11 = Wall(207, 126, 6, 197, 'e')
        self.wall12 = Wall(687, 126, 6, 197, 'd')
        self.wall13 = Wall(687, 126, 53, 6, 'i')
        self.wall14 = Wall(159, 318, 53, 6, 's')
        self.wall15 = Wall(735, 126, 6, 245, 'e')
        self.wall16 = Wall(735, 366, 149, 6, 'i')

        self.walls = [self.wall1, self.wall2, self.wall3,
                      self.wall4, self.wall5, self.wall6,
                      self.wall7, self.wall8, self.wall9,
                      self.wall10, self.wall11, self.wall12,
                      self.wall13, self.wall14, self.wall15, self.wall16]


class MapLevel02:
    def __init__(self):
        # Player position
        self.player_x = 118
        self.player_y = 185
        # Coin
        self.coin = Coin()
        self.coin.x = 474
        self.coin.y = 186
        self.area = Win(763, 142, 1, 90)
        # balls Superiores
        self.ball1 = Ball(0, 67, 1)
        self.ball3 = Ball(0, 67, 3)
        self.ball5 = Ball(0, 67, 5)
        self.ball7 = Ball(0, 67, 7)
        self.ball9 = Ball(0, 67, 9)
        self.ball11 = Ball(0, 67, 11)

        # balls Inferiores
        self.ball2 = Ball(0, 306, 2)
        self.ball4 = Ball(0, 306, 4)
        self.ball6 = Ball(0, 306, 6)
        self.ball8 = Ball(0, 306, 8)
        self.ball10 = Ball(0, 306, 10)
        self.ball12 = Ball(0, 306, 12)

        self.balls = [self.ball1, self.ball2, self.ball3, self.ball4, self.ball5, self.ball6, self.ball7, self.ball8,
                      self.ball9, self.ball10, self.ball11, self.ball12]

        for ball in self.balls:
            ball.lv2()
            ball.limit = [318, 67]

        self.wall1 = Wall(40, 232, 150, 6, 'i')
        self.wall2 = Wall(40, 136, 6, 102, 'e')
        self.wall3 = Wall(40, 136, 150, 6, 's')
        self.wall4 = Wall(184, 40, 6, 102, 'e')
        self.wall5 = Wall(184, 40, 582, 6, 's')
        self.wall6 = Wall(759, 40, 6, 102, 'd')
        self.wall7 = Wall(759, 232, 6, 102, 'd')
        self.wall8 = Wall(184, 328, 582, 6, 'i')
        self.wall9 = Wall(184, 232, 6, 102, 'e')

        self.walls = [self.wall1, self.wall2, self.wall3,
                      self.wall4, self.wall5, self.wall6,
                      self.wall7, self.wall8, self.wall9]
