from threading import Thread
from filem import FileManager
from game import Game
from core import Core

fileManager = FileManager("data.json")
interface = Game(3, 3)
learner = Core(interface, fileManager)

interface.setTable(1, 2, 0)
learner.learn(1)


