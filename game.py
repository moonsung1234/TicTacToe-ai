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

    def check(self, player, index) :
        i, j, tmp_index = 0, 0, index

        while tmp_index >= 3 :
            tmp_index -= 3
            i += 1

        j = tmp_index

        if self.table[i, 0] == self.table[i, 1] == self.table[i, 2] :
            return True

        elif self.table[0, j] == self.table[1, j] == self.table[2, j] :
            return True 

    def apply(self, player, index) :
        self.table = np.reshape(self.table, (1, 9))
        self.table[0, index] = player
        self.table = np.reshape(self.table, (3, 3))

        return self.table


        



    
    
