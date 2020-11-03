from threading import Thread
import numpy as np

class Game :
    def __init__(self, width, height) :
        self.height = height
        self.width = width

    def setTable(self, player1, player2, default_score) :
        self.player1 = player1
        self.player2 = player2
        self.default_score = default_score
        self.table = np.array([[self.default_score for score in range(self.width)] for score2 in range(self.height)])

        return self.table

    def getTable(self) :
        return self.table

    def apply(self, player, index) :
        self.table = np.reshape(self.table, (1, 9))
        self.table[0, index] = player
        self.table = np.reshape(self.table, (3, 3))

        return self.table


        



    
    
