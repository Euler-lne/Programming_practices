class Token:
    """Token 类用于对Token进行一些操作"""

    def __init__(self):
        self.token = []
        self.len = 0
        pass

    def getLen(self):
        """获取Token长度

        Returns:
            integer: 返回现在的Token长度
        """
        return self.len

    def addToken(self, type, value):
        """新加Token

        Args:
            type (string): 类型
            value (string): 值
        """
        self.token.append((type, value))
        self.len += 1

    def getEndType(self):
        """获取最后一个token的类型

        Returns:
            None: Token中没有元素
            (string, string): 返回最后一个token的类型
        """
        if self.len != 0:
            return self.token[self.len - 1][0]
        else:
            return None

    def getType(self, index):
        """获取指定下标的token类型

        Args:
            index (integer): 下标

        Returns:
            None: Token中没有元素
            string: 返回指定下标的token的类型
        """
        if index < self.len:
            return self.token[index][0]
        else:
            return None

    def getValue(self, index):
        """获取指定下标的token值

        Args:
            index (integer): 下标

        Returns:
            None: Token中没有元素
            string: 返回指定下标的token的值
        """
        if index < self.len:
            return self.token[index][1]
        else:
            return None

    def swapToken(self):
        """交换最后两个token的位置"""
        if self.len >= 2:
            temp = self.token[self.len - 1]
            self.token[self.len - 1] = self.token[self.len - 2]
            self.token[self.len - 2] = temp

    def printToken(self, start, end):
        """打印token

        Args:
            start (integer): 起始位置 \n
            end (integer): 结束位置
        """
        i = start
        while i < end:
            print(str(self.token[i]), end=" ")
            i += 1
        print(" ")
