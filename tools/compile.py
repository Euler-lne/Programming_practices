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
        self.id = {}  # 用于保存id 以及其对应的值，字典键为变量名字，值为一个列表
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
            while char and char not in [",", ".", "="]:
                if char == "id":
                    name = self.token.getValue(index)
                    self.id[name] = []
                    self.id[name].append(type)
                    self.id[name].append(None)
                else:
                    string = "There was a problem defining the variable, the character "
                    string += char + " was unknown. "
                    string += "The error near the line " + str(self.len_num) + "."
                    print(string)
                    return enums.ERROR
                index, char = self.forwordIndex(index)
            if char == "=":
                # 如果是等号那么就读取等号右边的值
                index, char = self.forwordIndex(index)
                if char:
                    # 如果字符存在，移动开始指针，应为之后调用的函数需要从特定位置开始计算
                    self.index_start = index
                    if type == "float":
                        val = self.ariExpression()  # 计算表达式的值
                    elif type == "string":
                        val = self.strExpression()
                    else:
                        val = self.logicExpression()
                    if val is not None:
                        # 表达式的值正确
                        self.id[name][1] = val  # 保存表达式的值
                        index = self.index_start  # 移动当前指针
                        char = self.token.getType(index)
                else:
                    string = "An expression is required after =. "
                    string += "The error near the line " + str(self.len_num) + "."
                    print(string)
                    return enums.ERROR
            elif char == "," or char == ".":
                index, char = self.forwordIndex(index)
            else:
                string = "Unexpected type of " + char
                string += ". You should examine your code near "
                string += str(self.len_num) + "."
                print(string)
                return enums.ERROR
        return enums.OK

    def assignment1(self):
        """
        第一种赋值方式
        id=id+表达式
        id=表达式
        """
        index = self.index_start

        return enums.OK

    def ariExpression(self, error=True):
        """
        检查算数表达式，并计算表达式中的值
        传入的值用来进行对某些打印类型是否输出的判断，应为布尔值的判断可能会用到
        返回算数表达式的值
        """
        index = self.index_start
        char = self.token.getType(index)
        tokens = []
        while char and char not in const.ARIEXP:
            # 算术表达式读到const.ARIEXP结束
            if char == "id":
                # 如果是id
                name = self.token.getValue(index)
                if name not in self.id:
                    string = name + " have not been statement. "
                    string += "The error near the line " + str(self.len_num) + "."
                    print(string)
                    return enums.ERROR
                type = self.id[name][0]
                value = self.id[name][1]
                if value is None:
                    string = name + " is not initialized. "
                    string += "The error near the line " + str(self.len_num) + "."
                    print(string)
                    return enums.ERROR
                if type != "float":
                    # 类型错误
                    # 类型错误的判断在逻辑表达式的判断不需要检测
                    if error:
                        string = "Unexpected type. You should use float as "
                        string += "a type of expression. Not "
                        string += type
                        string += ". The error near the line " + str(self.len_num) + "."
                        print(string)
                    return enums.ERROR
                else:
                    tokens.append(value)
            elif char == "num":
                # 如果是数字
                value = self.token.getValue(index)
                tokens.append(value)
            elif char in ["+", "-", "*", "/"]:
                # 算数表达式
                tokens.append(char)
            else:
                # 出现了其他符号
                if error:
                    string = "Unexpected type of " + char
                    string += ". You should examine your code near "
                    string += str(self.len_num) + "."
                    print(string)
                return enums.ERROR
            index, char = self.forwordIndex(index)
        val = find_invalid_ari(tokens)
        if val == None:
            # 如果翻译出的式子为一个表达式，调整开始指针，然后返回计算的值
            self.index_start = index
            return calculate_expression(tokens)
        elif val != -1:
            # 不是表达式
            string = "Unexpected type of " + tokens[val]
            string += " .You should examine your code near "
            string += str(self.len_num) + " ."
            print(string)
            return enums.ERROR

    def strExpression(self):
        """
        检查字符串表达式，并计算表达式中的值
        返回字符串表达式的值
        """
        index = self.index_start
        char = self.token.getType(index)
        tokens = []
        while char and char not in const.STREXP:
            index, char = self.forwordIndex(index)
        self.index_start = index
        return "1"

    def logicExpression(self):
        """
        检查逻辑表达式，并计算表达式中的值
        返回逻辑表达式的值
        """
        index = self.index_start
        char = self.token.getType(index)
        tokens = []
        while char and char not in const.STREXP:
            # 循环到遇到, 或者.
            val = self.ariExpression(False)  # 尝试计算表达式的值，失败的情况也要考虑
            if val:
                # 如果成功了那么开始字符已经移动过了
                if val == 0:
                    tokens.append("false")
                else:
                    tokens.append("true")
            else:
                # 失败了开始字符没有移动过
                name = self.token.getValue(index)
                if char == "true" or char == "false":
                    tokens.append(char)
                elif char == "id":
                    type = self.id[name][0]
                    val = self.id[name][1]
                    if type == "bool":
                        tokens.append(val)
                    else:
                        string = "Unexpected type. You should use bool as "
                        string += "a type of logic expression. Not "
                        string += type
                        string += ". The error near the line " + str(self.len_num) + "."
                        print(string)
                        return enums.ERROR
            # 这一个代码之前用于处理布尔值
            index, char = self.forwordIndex(index)  # 下移一个
            # 这个代码之后用于处理连接布尔值的关键字，and 和 or
            if char and char in const.LOGIC:
                # 匹配成功
                tokens.append(char)
                index, char = self.forwordIndex(index)
            elif char and char not in const.ARIEXP:
                # 匹配失败
                # 表示算数表达式后面可用跟随的符号
                # ARIEXP = ["==", "and", "or", "<", ">", "<=", ">=", "!=", ",", "."]
                string = "Unexpected " + char
                string += ". The error near the line " + str(self.len_num) + "."
                print(string)
                return enums.ERROR
        if len(tokens) == 0:
            # 长度为0表示原本想要逻辑表达式子，但是没有输入
            string = "Expected a logic expression"
            string += ". The error near the line " + str(self.len_num) + "."
            print(string)
            return enums.ERROR
        else:
            val = find_invalid_logic(tokens)
            if val is None:
                # 检测逻辑表达式是否合法
                self.index_start = index  # 移动指针表示，已经读取完成
                return calculate_logic_expression(tokens)
            else:
                # 逻辑表达式不合法
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
