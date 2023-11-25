from tools import read
from tools import enums
from tools.calculate_expression import *
from tools import const
from tools.error import *


class Compiler(read.Read):
    """
    用于词法分析，解析目标代码
    主要有4个状态：普通语句，IF语句，WHILE语句，SWITCH语句，这四个状态通过readBlock返回得知
    其中普通语句又有：赋值语句，声明语句，逻辑语句
    """

    def __init__(self, path, encodeing="utf-8"):
        super().__init__(path, encodeing)
        self.id = {}  # 用于保存id 以及其对应的值，字典键为变量名字，值为一个类型和变量值
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
        """ "
        声明变量语句
        只有type类型正确才会进入，type的错误被隔离在函数之外
        type == "float" or type == "string" or type == "bool"
        """
        index = self.index_start
        type = self.token.getType(index)  # 记录当前的变量类型
        index, char = self.forwordIndex(index)
        if char == None or char != ":":  # 语法错误
            return errorExpect(":", self.len_num)
        index, char = self.forwordIndex(index)
        while index < self.index_end:
            while char and char not in [",", ".", "="]:
                if char == "id":
                    name = self.token.getValue(index)
                    if name in self.id:
                        return errorInit(name, self.len_num)
                    self.id[name] = []
                    self.id[name].append(type)
                    self.id[name].append(None)
                else:  # 语法错误
                    return errorUnexpectChar(char, self.len_num)
                index, char = self.forwordIndex(index)
            if char == "=":  # 如果是等号那么就读取等号右边的值
                index, char = self.forwordIndex(index)
                if char:
                    # 如果字符存在，移动开始指针，应为之后调用的函数需要从特定位置开始计算
                    self.index_start = index
                    if type == "float":  # float 类型
                        val = self.ariExpression()  # 计算表达式的值
                    elif type == "string":  # 字符串类型
                        val = self.strExpression()
                    else:  # 算数表达式类型，这里必定为type
                        val = self.logicExpression()
                    if val is not None:  # 表达式的值正确
                        self.id[name][1] = val  # 保存表达式的值
                        index = self.index_start  # 移动当前指针
                        char = self.token.getType(index)
                    else:  # 表达式不正确
                        return enums.ERROR
                else:  # 语法错误，出现等号没有算术表达式
                    return errorExpect("an expression", self.len_num)
            elif char == "," or char == ".":  # 向前移动指针防止死循环
                index, char = self.forwordIndex(index)
            else:  # 赋值语句中出现了其他字符
                return errorUnexpectChar(char, self.len_num)
        return enums.OK

    def ariExpression(self, print_error=True):
        """
        检查算数表达式，并计算表达式中的值
        传入的值用来进行对某些打印类型是否输出的判断，应为布尔值的判断可能会用到
        返回算数表达式的值，错误返回None
        结束后指针指向ARIEXP
        """
        index = self.index_start
        char = self.token.getType(index)
        tokens = []
        while char and char not in const.ARIEXP:
            # 算术表达式读到const.ARIEXP结束
            # ARIEXP = ["==", "and", "or", "<", ">", "<=", ">=", "!=", ",", "."]
            if char == "id":
                # 如果是id
                name = self.token.getValue(index)
                if name not in self.id:
                    return errorUndefine(name, self.len_num)
                type = self.id[name][0]
                value = self.id[name][1]
                if value is None:
                    return errorUninit(name, self.len_num)
                if type != "float":  # 类型检测
                    return errorUnexpectType(type, "float", self.len_num, print_error)
                else:
                    tokens.append(value)
            elif char == "num":  # 如果是数字
                value = self.token.getValue(index)
                tokens.append(value)
            elif char in ["+", "-", "*", "/"]:  # 算数表达式
                tokens.append(char)
            else:  # 出现了其他符号
                return errorUnexpectChar(char, self.len_num, print_error)
            index, char = self.forwordIndex(index)  # 指针前移
        # 写入tokens的元素只可能是数字字符串或者运算符
        val = find_invalid_ari(tokens)  # 检测表达式是否合法
        if val == None:  # 表达式合法
            self.index_start = index  # 指针调整
            return calculate_expression(tokens)
        elif val != -1:  # 表达式不合法
            return errorUnexpectChar(tokens[val], self.len_num)
        else:  # 表达式为空
            return errorExpect("arithmetic expressions", self.len_num)

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
        返回逻辑表达式的值，错误返回None
        结束后指针指向, 或者 .
        """
        index = self.index_start
        char = self.token.getType(index)
        tokens = []  # 保存逻辑表达式的列表
        compare = []  # 保存当前的比较关系
        while char and char not in const.STREXP:  # 循环到遇到, 或者.
            if char in ["id", "num", "-"]:
                self.index_start = index
                val = self.ariExpression()
                if val:
                    compare.append(val)
                    index, char = self.updateIndex()
                    continue
                elif char == "id":  # 不是运算符只用考虑，变量为布尔值的情况
                    name = self.token.getValue(index)
                    type = self.id[name][0]
                    val = self.id[name][1]
                    if type == "bool" and val:
                        tokens.append(val)
                    elif val is None:  # 没有初始化
                        return errorUninit(name, self.len_num)
                    else:  # 不是bool变量
                        return errorUnexpectType(type, "bool", self.len_num)
                else:  # 运算符号出现问题
                    return errorExpect("arithmetic expressions", self.len_num)
            elif char == "true" or char == "false":
                tokens.append(char)
            elif char in const.COMPARE:
                compare.append(char)
            elif char in ["or", "and"]:
                length = len(compare)
                if length != 0:
                    val = find_invalid_compare(compare)
                    if val:
                        return errorUnexpectChar(compare[val], self.len_num)
                    else:
                        val = calculate_compare_expression(compare)
                        tokens.append(val)
                        compare = []
                tokens.append(char)
            else:
                return errorUnexpectChar(char, self.len_num)
            index, char = self.forwordIndex(index)
        length = len(compare)
        if length != 0:
            val = find_invalid_compare(compare)
            if val:
                return errorUnexpectChar(compare[val], self.len_num)
            else:
                val = calculate_compare_expression(compare)
                tokens.append(val)
                compare = []
        val = find_invalid_logic(tokens)
        if val is None:  # 逻辑表达式合法
            self.index_start = index  # 移动指针表示，已经读取完成
            return calculate_logic_expression(tokens)
        else:  # 逻辑表达式不合法
            return errorUnexpectChar(tokens[val], self.len_num)

    def forwordIndex(self, i, condition=[]):
        """
        指针前移，返回前进的指针下标和token类型
        condition为前移条件，如果有条件那么就不向前移动
        """
        n = len(condition)
        if n == 0:
            i += 1
            # 越界检查
            if i >= self.index_end:
                char = None
                i = self.index_end
            else:
                char = self.token.getType(i)
            return (i, char)
        else:
            char = self.token.getType(i)
            if char and char not in condition:
                i, char = self.forwordIndex(i)
            return (i, char)

    def updateIndex(self):
        return (self.index_start, self.token.getType(self.index_start))
