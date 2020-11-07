import numpy as np
import random
import time
import json

class Core :
    def __init__(self, interface, fileManager) :
        self.interface = interface
        self.fileManager = fileManager
        self.learning_table = []
        self.rand_table = [0 for zero in range(self.interface.width * self.interface.height)]
        self.DECREASE = 0.09
        self.UNKNOWN = -9999
        self.WIN = 1
        self.LOSE = -1
        self.DRAW = 0

    def getCorrectTable(self, target_table) :
        returned_table = [0 for zero in range(self.interface.width * self.interface.height)]

        if not len(self.learning_table) == 0 :
            next_table = self.getNextTable(target_table)

            for n_table in next_table :
                returned_table[n_table[0]] += self.DECREASE * n_table[1][0]

            for i in range(len(returned_table)) :
                returned_table[i] = round(returned_table[i], 2)

            return returned_table

        return returned_table

    def getCorrectIndex(self, target_correct_table) :
        target_table = np.array(target_correct_table.copy())
        max_index = np.argmax(target_table)

        for _ in range(self.interface.width * self.interface.height) :
            if np.reshape(self.interface.getTable(), (1, 9))[0, max_index] == 0 :
                return max_index

            else :
                target_table[max_index] = self.UNKNOWN
                max_index = np.argmax(target_table)

        return None

    def getNextTable(self, target_table) :
        returned_table = []
        
        for table in self.learning_table :
            bool_table = np.reshape(target_table == table[1], (1, 9))
            wrong_count = 0
            wrong_index = None

            for i in range(len(bool_table[0])) :
                if bool_table[0, i] == False :
                    wrong_count += 1
                    wrong_index = i

            if wrong_count == 1 :
                returned_table.append([wrong_index, table])

        return returned_table

    def getRandomIndex(self, target_table) :
        while True :
            rand_int = random.randint(0, 8)

            if target_table[0, rand_int] == 0 :
                return rand_int

        return None

    def checkIsExist(self, target_table) :
        wrong_count = 0
        
        for table in self.learning_table :
            bool_table = np.reshape(target_table == table[1], (1, 9))

            for i in range(len(bool_table[0])) :
                if bool_table[0, i] == False :
                    wrong_count += 1
                    break

                elif i == len(bool_table[0]) - 1:
                    return True
            
        return False

    def setSectionToTable(self, player, section_table) :
        for i in range(len(section_table)) :
            if player == self.interface.player1 :
                if i % 2 == 0 :
                    section_table[i][0] = self.WIN

                else :
                    section_table[i][0] = self.LOSE

                self.learning_table.append(section_table[i])

            elif player == self.interface.player2 :
                if not i % 2 == 0 :
                    section_table[i][0] = self.WIN

                else :
                    section_table[i][0] = self.LOSE

                self.learning_table.append(section_table[i])

            elif player == self.UNKNOWN :
                section_table[i][0] = self.DRAW
                self.learning_table.append(section_table[i])

    def learn(self, count) :
        for _ in range(count) :
            turned = self.interface.player1
            section_table = []
            file_content = self.fileManager.getFileContents()

            if not len(file_content) == 0 :
                self.learning_table = json.loads(file_content)

                for i in range(len(self.learning_table)) :
                    self.learning_table[i][0] = int(self.learning_table[i][0])
                    self.learning_table[i][1] = self.fileManager.setContentsAsNp(self.learning_table[i][1])

            while True :
                print(self.interface.getTable())
                print(self.getCorrectTable(self.interface.getTable()), "\n")
                print(len(self.learning_table))
                index = self.getCorrectIndex(self.getCorrectTable(self.interface.getTable()))

                noise = random.randint(1, 4)

                if index == None :
                    index = self.getRandomIndex(np.reshape(self.interface.getTable(), (1, 9)))

                if turned == self.interface.player1 :
                    if not noise == 1:
                        index = self.getRandomIndex(np.reshape(self.interface.getTable(), (1, 9)))

                    index = int(input())

                    section_table.append([self.UNKNOWN, self.interface.apply(turned, index).copy()])

                elif turned == self.interface.player2 :
                    #if noise == 1:
                    #    index = self.getRandomIndex(np.reshape(self.interface.getTable(), (1, 9)))

                    #index = int(input())

                    section_table.append([self.UNKNOWN, self.interface.apply(turned, index).copy()])

                if self.interface.check(turned, index) :
                    self.setSectionToTable(turned, section_table)
                    print("player1" if turned == self.interface.player1 else "player2", " 승리")
                    
                    self.interface.setTable(self.interface.player1, self.interface.player2, self.interface.default_score)
                    break

                if self.interface.checkFull() :
                    self.setSectionToTable(self.UNKNOWN, section_table)
                    print("무승부")

                    self.interface.setTable(self.interface.player1, self.interface.player2, self.interface.default_score)
                    break

                turned = self.interface.getNextTurned(turned)

            for i in range(len(self.learning_table)) :
                self.learning_table[i][1] = self.fileManager.setContentsAsArray(self.learning_table[i][1])

            self.fileManager.setFileContents(json.dumps(self.learning_table))
                

