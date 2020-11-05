import numpy as np
import random
import time
import json

class Core :
    def __init__(self, interface, fileManager) :
        self.fileManager = fileManager
        self.interface = interface
        self.learning_table = []
        self.END = -999

    def beGreedy(self, table) :
        max_value = np.argmax(table)

        if np.reshape(table, (1, 9))[0, max_value] == self.END :
            return None

        return max_value

    def chooseAtRandom(self, table) :
        tmp_table = np.reshape(table, (1, 9))
        result = random.randint(0, len(tmp_table[0]) - 1)

        while True :
            for i in range(len(tmp_table[0])) :
                if tmp_table[0, i] == 0 :
                    break

                elif i == len(tmp_table[0]) - 1 :
                    return None

            if tmp_table[0, result] == 0 :
                return result

            else :
                result = random.randint(0, len(tmp_table[0]) - 1)

    def getCompareValue(self, table) :
        return np.where(table>0, self.END, table)

    def getCompareValueWithPlayer(self, player, index, table) :
        tmp_table = np.where(table>0, self.END, table)
        tmp_table = np.reshape(tmp_table, (1, 9))
        tmp_table[0, index] = player
        
        return np.reshape(tmp_table, (3, 3))

    def getCorrectTable(self, player, table) :
        if len(self.learning_table) == 0 :
            return (np.array([[]]), self.END)

        else :
            tmp_table = np.reshape(table, (1, 9))
            final_table = [self.END, np.array([[]])]
            next_index = None

            for tb in self.learning_table :
                compared_table = np.reshape(tb[1], (1, 9))
                compared_score = tb[0]
                wrong_count = 0
                tmp_index = None

                for i in range(len(tmp_table[0])) :
                    if not str(tmp_table[0, i]) == str(compared_table[0, i]) :
                        wrong_count += 1
                        tmp_index = i

                if wrong_count == 1 and compared_table[0, tmp_index] == player and tmp_table[0, tmp_index] == 0 and not compared_score == -1 :
                    #print("\n찾은 테이블 : ", np.reshape(compared_table, (3, 3)), "\n")    
                    
                    if compared_score >= final_table[0] :
                        final_table = tb 
                        next_index = tmp_index

                wrong_count = 0

            if len(final_table[1][0]) == 0 :
                return (np.array([[]]), self.END)

            elif not next_index == None :
                return (final_table[1], next_index)

    def checkIsExist(self, table) :
        for i in range(len(self.learning_table)) :
            checked_table = table == self.learning_table[i][1]
            checked_table = np.reshape(checked_table, (1, 9))

            for j in range(len(checked_table[0])) :
                if not checked_table[0, j] :
                    break

                elif j == len(checked_table[0]) - 1 :
                    return True
        
        return False

    def setTablesScore(self, tables, player, game_state) :
        for i in range(len(tables)) :
            if player == self.interface.player1 :
                if i % 2 == 0 :
                    tables[i][0] = game_state

                else :
                    tables[i][0] = -1

            elif player == self.interface.player2 :
                if not i == 0 and not i % 2 == 0 :
                    tables[i][0] = game_state

                elif not i == 0 :
                    tables[i][0] = -1

            else :
                tables[i][0] = 0

            if not self.checkIsExist(tables[i][1]) :
                self.learning_table.append(tables[i])

    def learn(self, count) :
        for _ in range(count) :
            turned = self.interface.player1
            check_data = self.fileManager.getFileContents()
            match_tables = []
            is_first_count = 0

            if not len(check_data) == 0 :
                self.learning_table = json.loads(check_data)

                for i in range(len(self.learning_table)) :
                    self.learning_table[i][0] = int(self.learning_table[i][0])
                    self.learning_table[i][1] = self.fileManager.setContentsAsNp(self.learning_table[i][1])

            while True :
                print(self.interface.getTable())

                tb_list = self.getCorrectTable(turned, self.interface.getTable())
                index = None

                if len(tb_list[0][0]) == 0 :
                    index = self.chooseAtRandom(self.getCompareValue(self.interface.getTable()))

                elif is_first_count == 0 :
                    index = self.chooseAtRandom(self.getCompareValue(self.interface.getTable()))
                    is_first_count += 1

                else :
                    index = self.beGreedy(self.getCompareValueWithPlayer(turned, tb_list[1], tb_list[0]))

                if index == None :
                    self.interface.setTable(self.interface.player1, self.interface.player2, self.interface.default_score)
                    self.setTablesScore(match_tables, self.END, 0)
                    print("\n무승부\n")

                    break

                if turned == self.interface.player1 :
                    decided = self.interface.apply(turned, index)

                else :
                    #decided = self.interface.apply(turned, index)
                    #match_tables.append([self.END, decided.copy()])
                    index = int(input())
                    #index = self.chooseAtRandom(self.getCompareValue(self.interface.getTable()))
                    self.interface.apply(turned, index)

                match_tables.append([self.END, decided.copy()])

                if self.interface.check(turned, index) :
                    print("\nplayer1" if turned == self.interface.player1 else "player2", " 승리 : ", self.interface.getTable(), "\n")
                    self.interface.setTable(self.interface.player1, self.interface.player2, self.interface.default_score)
                    self.setTablesScore(match_tables, turned, 1)

                    break

                if turned == self.interface.player1 :
                    turned = self.interface.player2
            
                else :
                    turned = self.interface.player1

                #time.sleep(2)

            for i in range(len(self.learning_table)) :
                self.learning_table[i][1] = self.fileManager.setContentsAsArray(self.learning_table[i][1])

            self.fileManager.setFileContents(json.dumps(self.learning_table))
        
        print(len(json.loads(self.fileManager.getFileContents())))

