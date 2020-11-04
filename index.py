from threading import Thread
from game import Game
from core import Core

interface = Game(3, 3)
learner = Core(interface)

def learnByCore() :
    interface.setTable(1, 2, 0)
    learner.learn(27)

core1 = Thread(target=learnByCore)
core1.start()