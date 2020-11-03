import numpy as np
import time
import json

class Core :
    def __init__(self, interface) :
        self.interface = interface
        self.learning_table = list()
        self.END = -999

    def beGreedy(self, table) :
        max_value = np.argmax(table)

        if np.reshape(table, (1, 9))[0][max_value] == self.END :
            return None

        return max_value

    def getCompareValue(self, table) :
        tmp_table = self.interface.getTable()
        tmp_table = np.where(tmp_table>0, -999, tmp_table)

        return tmp_table

    def learn(self) :
        turned = self.interface.player1

        for _ in range(10) :
            print(self.interface.getTable())
            index = self.beGreedy(self.getCompareValue(self.interface.getTable()))

            if index == None :
                print("끝")
                break

            self.interface.apply(turned, index)

            if turned == self.interface.player1 :
                turned = self.interface.player2
            
            else :
                turned = self.interface.player1

            time.sleep(2)

