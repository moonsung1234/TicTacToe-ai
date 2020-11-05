import numpy as np
import json

class FileManager :
    def __init__(self, path) :
        self.path = path

    def getFileContents(self) :
        with open(self.path, "r") as f :
            lines = f.readlines()
            tmp_str = str()

            for line in lines :
                tmp_str += line

            return tmp_str

    def setFileContents(self, content) :
        with open(self.path, "w") as f :
            f.write(content)

    def setContentsAsNp(self, content) :
        return np.array(content)

    def setContentsAsArray(self, content) :
        return content.tolist()