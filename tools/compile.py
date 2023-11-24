from tools import read
from tools import enums
from tools.calculate_expression import *
from tools import const


class Compiler(read.Read):
    """
    用于词法分析，解析目标代码
    主要有4个状态：普通语句，IF语句，WHILE语句，SWITCH语句，这四个状态通过readBlock返回得知
    其中普通语句又有：赋值语句，声明语句，逻辑语句
    """

    def __init__(self, path, encodeing="utf-8"):
        super().__init__(path, encodeing)
        self.id = {}  # 用于保存id 以及其对应的值
        self.index_start = 0  # 当前的Token起始下标
        self.index_end = 0  # 当前Token的结束下标的后一位
        self.state = enums.NONE  # 当前的语句状态
        self.start()

    def start(self):
        while True:
            self.state = self.readBlock()
            # 进行可能的错误检测
            if self.state == enums.END:
                # 结束的时候还有可能有字符，这可能是应为忘记写。或者！导致分块没有成功
                return enums.END
            elif self.state == enums.ERROR:
                return enums.ERROR
            # 错误检测结束进行语法分析
            self.index_end = self.token.getLen()

            if self.state == enums.ACCEPT:
                # 普通代码以句号结束的
                self.normalBlock()
            elif self.state == enums.IF:
                # if代码块
                self.ifBlock()
            elif self.state == enums.SWITCH:
                # switch 代码块
                self.switchBlock()
            elif self.state == enums.WHILE:
                # while 代码块
                self.whileBlock()

            self.index_start = self.token.len  # 准备读取下一个代码块

    def normalBlock(self):
        index = self.index_start
        type = self.token.getType(index)
        if type == "float" or type == "string" or type == "bool":
            self.declareVar()

    def ifBlock(self):
        pass

    def whileBlock(self):
        pass

    def switchBlock(self):
        pass

    def declareVar(self):
        index = self.index_start
        type = self.token.getType(index)  # 记录当前的变量类型
        index, char = self.forwordIndex(index)
        if char == None or char != ":":
            # 如果接下来的字符不是:，或者这个字符是最后一个
            print("Expected : near the " + self.token.getValue(index - 1))
            return enums.ERROR
        index, char = self.forwordIndex(index)
        while index < self.index_end:
            pass
        pass

    def assignment1(self):
        """
        第一种赋值方式
        id=id+表达式
        id=表达式
        """
        index = self.index_start

    def expression(self):
        """
        检查表达式，并计算表达式中的值
        返回算数表达式的值
        """
        index = self.index_start
        char = self.token.getType(index)
        end_list = const.LOGIC.append(",", ".")
        tokens = []
        while char and char not in end_list:
            if char == "id":
                name = self.token.getValue(index)
                type = self.id[name][0]
                value = self.id[name][1]
                if type != "float":
                    # 类型错误
                    string = "Unexpected type. You should use float as "
                    string += "a type of expression. Not "
                    string += type
                    string += " . The error near the line " + str(self.len_num) + " ."
                    print(string)
                    return enums.ERROR
                else:
                    tokens.append(value)
            elif char == "num":
                value = self.token.getValue(index)
                tokens.append(value)
            elif char in ["+", "-", "*", "/"]:
                tokens.append(char)
            else:
                # 出现了其他符号
                string = "Unexpected type of " + char
                string += " .You should examine your code near "
                string += str(self.len_num) + " ."
                print(string)
                return enums.ERROR
            index, char = self.forwordIndex(index)
        val = find_invalid_position(tokens)
        if val == None:
            # 如果翻译出的式子为一个表达式，调整开始指针，然后返回计算的值
            self.index_start = index
            return calculate_expression(tokens)
        else:
            # 不是表达式
            string = "Unexpected type of " + tokens[val]
            string += " .You should examine your code near "
            string += str(self.len_num) + " ."
            print(string)
            return enums.ERROR

    def forwordIndex(self, i):
        """
        指针前移，返回前进的指针下标和token类型
        """
        i += 1
        # 越界检查
        if i >= self.index_end:
            char = None
            i = self.index_end
        else:
            char = self.token.getType(i)
        return (i, char)
