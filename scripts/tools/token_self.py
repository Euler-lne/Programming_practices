class Token:
    def __init__(self):
        self.token = []
        self.len = 0
        pass

    def getLen(self):
        return self.len

    def addToken(self, type, value):
        self.token.append((type, value))
        self.len += 1

    def getEndType(self):
        """
        返回最后一个元素
        """
        if self.len != 0:
            return self.token[self.len - 1][0]
        else:
            return None

    def getType(self, index):
        if index < self.len:
            return self.token[index][0]
        else:
            return None

    def getValue(self, index):
        if index < self.len:
            return self.token[index][1]
        else:
            return None

    def swapToken(self):
        if self.len >= 2:
            temp = self.token[self.len - 1]
            self.token[self.len - 1] = self.token[self.len - 2]
            self.token[self.len - 2] = temp

    def printToken(self, start, end):
        i = start
        while i < end:
            print(str(self.token[i]), end=" ")
            i += 1
        print(" ")
