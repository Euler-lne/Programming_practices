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

    def swapToken(self):
        if self.len >= 2:
            temp = self.token[self.len - 1]
            self.token[self.len - 1] = self.token[self.len - 2]
            self.token[self.len - 2] = temp
