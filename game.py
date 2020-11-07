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

        elif not self.table[0, 0] == 0 and self.table[0, 0] == self.table[1, 1] == self.table[2, 2] :
            return True

        elif not self.table[0, 2] == 0 and self.table[0, 2] == self.table[1, 1] == self.table[2, 0] :
            return True

        return False

    def checkFull(self) :
        table = np.reshape(self.table, (1, 9))

        for i in range(len(table[0])) :
            if table[0, i] == 0 :
                return False

            elif i == len(table[0]) - 1 :
                return True

    def getNextTurned(self, turned) :
        if turned == self.player1 :
            return self.player2

        elif turned == self.player2 :
            return self.player1
 
    def apply(self, player, index) :
        self.table = np.reshape(self.table, (1, 9))
        self.table[0, index] = player
        self.table = np.reshape(self.table, (3, 3))

        return self.table


        



    
    
