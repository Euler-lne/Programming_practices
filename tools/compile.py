from tools import read
from tools import enums
from tools.calculate_expression import *
from tools import const
from tools.error import *
from tools import tool_self


class Compiler(read.Read):
    """
    用于词法分析，解析目标代码
    主要有4个状态：普通语句，IF语句，WHILE语句，SWITCH语句，这四个状态通过readBlock返回得知
    其中普通语句又有：赋值语句，声明语句，print语句，
    """

    def __init__(self, path, encodeing="utf-8"):
        super().__init__(path, encodeing)
        self.id = {}  # 用于保存id 以及其对应的值，字典键为变量名字，值为一个类型和变量值
        self.start_index = 0  # 当前的Token起始下标
        self.end_index = 0  # 当前Token的结束下标的后一位
        self.state = enums.NONE  # 当前的语句状态
        self.start()

    def start(self):
        while True:
            self.state = self.readBlock()
            # 进行可能的错误检测
            if self.state == enums.END:
                # 结束的时候还有可能有字符，这可能是应为忘记写。或者！导致分块没有成功
                if self.start_index != self.end_index:
                    return errorExpect(". or !", self.len_num)
                return enums.END
            elif self.state == enums.ERROR:
                return enums.ERROR
            # 错误检测结束进行语法分析
            self.end_index = self.token.getLen()
            val = None
            if self.state == enums.ACCEPT:  # 普通代码以句号结束的
                val = self.normalBlock()
            elif self.state == enums.IF:  # if代码块
                val = self.ifBlock(self.end_index)
            elif self.state == enums.SWITCH:  # switch 代码块
                val = self.switchBlock(self.end_index)
            elif self.state == enums.WHILE:  # while 代码块
                val = self.whileBlock(self.end_index)
            if val is None:
                return enums.NONE

            self.start_index = self.token.len  # 准备读取下一个代码块

    def normalBlock(self):
        """如果正常执行，那么将会执行到."""
        index = self.start_index
        type = self.token.getType(index)
        if type == "float" or type == "string" or type == "bool":
            return self.declareVar()
        elif type == "print":  # 打印函数
            return self.compilePrint()
        elif type == "input":  # 打印函数
            return self.compileInput()
        else:
            tokens = self.tokenToList(".")  # 只将逗号之前的划分为一个列表
            if "=" in tokens:  # 第一种赋值语句
                if type == "id":
                    return self.assignment1()
                else:
                    return errorExpect("a variable", self.len_num)
            elif "=_" in tokens:  # 第二种赋值语句
                if type == "id":
                    val = self.assignment2()
                    if val is not None:  # 不为None
                        self.start_index, char = self.forwordIndex(self.start_index)
                        if char == ".":  # 保证都以.结束
                            return val
                        else:
                            return errorExpect(".", self.len_num)
                    return val
                else:
                    return errorExpect("a variable", self.len_num)
            else:  # 无用语句
                return errorUnhelpfulStatement(self.len_num)

    def runBlock(self, end):
        """结束后指向下一个新的代码块"""
        if self.start_index == end:  # 递归结束条件
            return enums.OK
        off = 0
        val = None
        index, char = self.updateIndex()
        if char == "if":
            val = self.ifBlock(end)  # 指向完后指针指向下一个待指向语句
        elif char == "while":
            i = self.divideWhileSwitchBlock(end)
            if i is None:
                return enums.ERROR
            val = self.whileBlock(i)
        elif char == "end":  # 读到end，跳过end，end也代表代码块要结束了
            if self.checkBlockEnd(end):  # 检查end 的正确性
                self.start_index = end  # switch跳过了中间代码，其他跳过了end;|end!
                val = "end"  # 正确则改变val的值，因为后面还有可能有语句
        else:
            index, char = self.forwordIndex(index)
            if char == "switch":
                i = self.divideWhileSwitchBlock(end)
                if i is None:
                    return enums.ERROR
                val = self.switchBlock(i)  # 由于存在递归的情况，不是每一次都是刚好在！的位置停
            else:
                val = self.normalBlock()  # 执行完成之后会指向.
                off = 1
        return self.forwordBlock(val, end, off)

    def forwordBlock(self, val, end, off=0):
        if val is not None:
            self.start_index += off  # 跳过.
            return self.runBlock(end)
        else:
            return val

    def ifBlock(self, end):
        val = self.checkIfBlockFront()  # 指针指向了then的后一位
        result = self.divideIfBlock(end)  # 这里指针已经跳过了if
        if val is None or result is None:
            return enums.ERROR
        return self.runIfBlock(val, result[0], result[1])

    def runIfBlock(self, val, mid, end):
        """执行if块语句，能够进入到这里的都是代表能够在词法分析分块的。end要指向下一条要执行的语句"""
        if self.checkIfBlockEnd(mid, end) is None:
            return enums.ERROR
        if val:  # val 为 True  或者是 False
            if self.runBlock(mid) is not None:
                self.start_index = end
            else:
                return enums.ERROR
        else:
            if mid != end:  # 不等说明有else mid 指向else，相等指向下一个待执行语句，不用 +1
                self.start_index = mid + 1
            else:
                self.start_index = mid
            if self.runBlock(end) is None:
                return enums.ERROR
        return enums.OK

    def checkBlockEnd(self, end):
        """检查代码块结束的合法性，合法返回1，不合法返回None。开始指针不移动"""
        index, char = self.getIndex(end - 2)
        if char != "end":
            return errorExpect("end", self.len_num)
        index, char = self.forwordIndex(index)
        if char != "!" and char != ";":
            return errorExpect("! or ;", self.len_num)
        return enums.OK

    def checkIfBlockFront(self):
        """检查if语句的前半部分，也就是 若……，则
        返回后的指针指向则的后一位
        """
        index, char = self.updateIndex()
        if char != "if":
            return errorExpect("if", self.len_num)
        index, char = self.forwordIndex(index)  # 向前移动一位
        self.start_index = index  # 要进入另外一个函数需要改变self.start_index
        val = self.logicExpression()
        if val is None:
            return enums.ERROR
        index, char = self.updateIndex()
        if char != ",":
            return errorExpect(",", self.len_num)
        index, char = self.forwordIndex(index)  # 向前移动一位
        if char != "then":
            return errorExpect("then", self.len_num)
        index, char = self.forwordIndex(index)  # 向前移动一位
        self.start_index = index
        return val

    def checkIfBlockEnd(self, mid, end):
        """失败返回None，正确返回1"""
        if mid != end:
            index, char = self.getIndex(mid - 2)
            if char != "end":
                return errorExpect("end", self.len_num)
            index, char = self.forwordIndex(index)
            if char != ";":
                return errorExpect(";", self.len_num)
        index, char = self.getIndex(end - 2)
        if char != "end":
            return errorExpect("end", self.len_num)
        index, char = self.forwordIndex(index)
        if char != "!":
            return errorExpect("!", self.len_num)
        return enums.OK

    def divideIfBlock(self, end):
        """
        将if 块划分为两块，或者一块，也就是寻找转跳下标。
        这里的if 和 ！一定可以匹配因为，词法分析已经匹配过了
        返回i,j i指向了else 或者!后一位，j指向!后一位
        """
        stack = ["if"]  # 指针已经跳过了if 所以把if添加到栈底
        i = -1
        j = -1
        index, char = self.updateIndex()
        while index < end:
            if char in ["if", "while", "switch"]:
                stack.append(char)
            elif char == "else" and len(stack) == 1:
                # 得到不成立时候的下标
                i = index  # 指向else
            elif char == "!":
                stack.pop()
                if len(stack) == 0:  # 得到if块结束的下标，这个为end-1
                    j = index
                    break
            index, char = self.forwordIndex(index)
        if len(stack) != 0:
            return errorExpect("!", self.len_num)
        if i == -1:  # 为-1说明不存在else语句
            return (j + 1, j + 1)
        else:
            return (i, j + 1)  # j要指向下一个待执行的语句，不是!

    def whileBlock(self, end):
        start = self.start_index
        val = self.checkWhileBlockFront()
        if val is None:
            return enums.ERROR
        if val:  # val 为 True 或者 False
            if self.runBlock(end) is not None:  # 执行while代码块
                self.start_index = start  # 执行结束改变指针
                return self.whileBlock(end)  # 递归条用
            else:
                return enums.ERROR
        else:  # 递归结束出口
            self.start_index = end
        return enums.OK

    def checkWhileBlockFront(self):
        index, char = self.updateIndex()
        if char != "while":
            return errorExpect("while", self.len_num)
        index, char = self.forwordIndex(index)  # 向前移动一位
        self.start_index = index  # 要进入另外一个函数需要改变self.start_index
        val = self.logicExpression()
        if val is None:
            return enums.ERROR
        index, char = self.updateIndex()
        if char != ",":
            return errorExpect(",", self.len_num)
        index, char = self.forwordIndex(index)  # 向前移动一位
        if char != "then":
            return errorExpect("then", self.len_num)
        index, char = self.forwordIndex(index)  # 向前移动一位
        self.start_index = index
        return val

    def divideWhileSwitchBlock(self, end):
        """返回指向!后一个的指针，指针起始位置指向["if", "while", "switch"]"""
        stack = []  # 指针起始位置指向["if", "while", "switch"]所以不用向栈里面添加任何元素
        i = -1
        index, char = self.updateIndex()
        while index < end:
            if char in ["if", "while", "switch"]:
                stack.append(char)
            elif char == "!":
                stack.pop()
                if len(stack) == 0:  # 得到if块结束的下标，这个为end-1
                    i = index
                    break
            index, char = self.forwordIndex(index)
        if len(stack) != 0:
            return errorExpect("!", self.len_num)
        return i + 1

    def switchBlock(self, end):
        name = self.checkSwitchBlockFront()
        if name is None:
            return enums.ERROR
        val = self.findRightPositon(name, end)
        if val is None:
            return enums.ERROR
        else:
            self.start_index = end
            return enums.OK

    def checkSwitchBlockFront(self):
        """指针指向了:后方，正确返回变量名字，错误返回None"""
        index, char = self.updateIndex()
        if char != "id":
            return errorExpect("id", self.len_num)
        name = self.token.getValue(index)
        if name not in self.id:  # 没有声明的不可以用
            return errorUndefine(name, self.len_num)
        type = self.id[name][0]
        if type == "bool":
            return errorUnexpectType("bool", "float or string", self.len_num)
        index, char = self.forwordIndex(index)
        if char != "switch":
            return errorExpect("switch", self.len_num)
        index, char = self.forwordIndex(index)
        if char != ":":
            return errorExpect(":", self.len_num)
        index, char = self.forwordIndex(index)
        self.start_index = index
        return name

    def findRightPositon(self, name, end):
        index, char = self.updateIndex()
        while index < end:
            if char == "case":
                self.start_index = index  # 更新下标
                match = self.checkSwitchBranch(name)
                if match is None:
                    return enums.ERROR
                if match:  # 如果两个值相等了，就退出
                    self.runBlock(end)  # 开始指针指向了正确位置
                    break
            elif char == "else":
                index, char = self.forwordIndex(index)
                self.start_index = index  # 让开始指针指向正确位置
                self.runBlock(end)
                break
            index, char = self.forwordIndex(index)
        return enums.OK

    def checkSwitchBranch(self, name):
        """检查每一个分支语句的前半部分是否满足要求，退出后指针指向then后一位"""
        index, char = self.updateIndex()
        if char != "case":
            return errorExpect("case", self.len_num)
        index, char = self.forwordIndex(index)
        self.start_index = index  # 要调用运算函数需要调整指针
        type = self.id[name][0]
        value = self.id[name][1]
        val = None
        if type == "float":
            val = self.ariExpression()
            if val is None:
                return enums.ERROR
        else:  # 只有可能为float 或者 string，应为语法定义
            val = self.strExpression()
            if val is None:
                return enums.ERROR
        index, char = self.updateIndex()  # 调用完运算函数需要调整指针
        if char != ",":
            return errorExpect(",", self.len_num)
        index, char = self.forwordIndex(index)
        if char != "then":
            return errorExpect("then", self.len_num)
        index, char = self.forwordIndex(index)
        self.start_index = index
        if val == value:
            return True
        else:
            return False

    def compilePrint(self):
        self.start_index, char = self.forwordIndex(self.start_index)
        if char != ":":
            return errorExpect(":", self.len_num)
        self.start_index, char = self.forwordIndex(self.start_index)
        string = self.strExpression()
        if string:
            print(string)
        else:
            return enums.ERROR
        return enums.OK

    def compileInput(self):
        self.start_index, char = self.forwordIndex(self.start_index)
        if char != ":":
            return errorExpect(":", self.len_num)
        if self.end_index - self.start_index != 3:
            string = "There is a problem with the input function."
            return errorUniversal(string, self.len_num)
        self.start_index, char = self.forwordIndex(self.start_index)
        name = self.token.getValue(self.start_index)
        if name not in self.id:
            return errorUndefine(name, self.len_num)
        type = self.id[name][0]
        val = input()
        if type == "float":
            try:
                val = int(val)  # 尝试转换为整数
            except ValueError:
                try:
                    val = float(val)  # 尝试转换为浮点数
                except ValueError:
                    string = "It's not a number that's being entered."
                    return errorUniversal(string, self.len_num)  # 如果无法转换，返回原始字符串
        elif type == "bool":
            val = tool_self.stringToBool(val)
        self.id[name][1] = val
        return enums.OK

    def assignment1(self):
        """
        进行类似于 苹果为苹果加3 的赋值运算
        结束的时候指针指向=_
        """
        index, char = self.updateIndex()
        if char == "id":  # 检测是否为id
            name = self.token.getValue(index)
            if name not in self.id:  # 是否初始化
                return errorUndefine(name, self.len_num)
            type = self.id[name][0]
            index, char = self.forwordIndex(index)
            if char != "=":
                return errorExpect("=", self.len_num)
            self.start_index, char = self.forwordIndex(index)
            val = None
            if type == "float":
                val = self.ariExpression()
            elif type == "bool":
                val = self.logicExpression()
            elif type == "string":
                val = self.strExpression()
            if val is not None:  # 不为None
                self.id[name][1] = val
                return enums.OK
            else:
                return val
        else:  # 不是 id 报错
            return errorUnexpectChar(char, self.len_num)

    def assignment2(self, print_error=True):
        """
        进行类似于 苹果加3也 的赋值运算
        结束的时候指针指向=_，返回"NO"代表不是第二种赋值方式
        """
        index, char = self.updateIndex()
        while char and char != "=_" and char not in const.STREXP:
            index, char = self.forwordIndex(index)
        if char != "=_":
            errorUnexpectChar(char, self.len_num, print_error)
            return "NO"  # 代表不是第二类赋值语句
        index, char = self.updateIndex()
        if char == "id":
            name = self.token.getValue(index)
            if name not in self.id:
                return errorUndefine(name, self.len_num)
            type = self.id[name][0]
            if type == "float":
                self.start_index, char = self.forwordIndex(index)
                return self.assignReadOperator(name)
            else:
                return errorUnexpectType(type, "flaot", self.len_num)
        else:
            return errorUnexpectChar(char, self.len_num)

    def assignReadOperator(self, name):
        """
        进行检测运算符操作
        """
        index, char = self.updateIndex()
        if char in ["+", "-", "*", "/"]:
            operator = char
            self.start_index, char = self.forwordIndex(index)
            return self.assignReadAri(name, operator)
        else:
            return errorExpect("a operator", self.len_num)

    def assignReadAri(self, name, operator):
        val = self.ariExpression(False)
        index, char = self.updateIndex()
        if val is None:
            return errorExpect("an expression", self.len_num)
        elif char == "=_":  # 结束的时候指针指向=_
            return self.calculate(name, operator, val)
        else:
            return errorExpect("=_", self.len_num)

    def calculate(self, name, operator, val):
        if operator == "+":
            self.id[name][1] += val
        elif operator == "-":
            self.id[name][1] -= val
        elif operator == "*":
            self.id[name][1] *= val
        elif operator == "/":
            self.id[name][1] /= val
        return self.id[name][1]

    def declareVar(self):
        """ "
        声明变量语句
        只有type类型正确才会进入，type的错误被隔离在函数之外
        type == "float" or type == "string" or type == "bool"
        """
        index = self.start_index
        type = self.token.getType(index)  # 记录当前的变量类型
        index, char = self.forwordIndex(index)
        if char == None or char != ":":  # 语法错误
            return errorExpect(":", self.len_num)
        index, char = self.forwordIndex(index)
        while char and char != ".":
            while char and char not in [",", ".", "="]:
                if char == "id":
                    name = self.token.getValue(index)
                    if name in self.id:  # 声明过的变量不可以声明
                        return errorInit(name, self.len_num)
                    self.id[name] = []
                    self.id[name].append(type)
                    self.id[name].append(None)
                else:  # 语法错误
                    return errorUnexpectChar(char, self.len_num)
                index, char = self.forwordIndex(index)
            if char == "=":  # 如果是等号那么就读取等号右边的值
                index, char = self.forwordIndex(index)
                if char:  # 如果字符存在，移动开始指针，应为之后调用的函数需要从特定位置开始计算
                    self.start_index = index
                    if type == "float":  # float 类型
                        val = self.ariExpression()  # 计算表达式的值
                    elif type == "string":  # 字符串类型
                        val = self.strExpression()
                    else:  # 算数表达式类型，这里必定为type
                        val = self.logicExpression()
                    if val is not None:  # 表达式的值正确
                        if name not in self.id:  # 防止出现 int =的情况
                            return errorExpect(name, self.len_num)
                        self.id[name][1] = val  # 保存表达式的值
                        index = self.start_index  # 移动当前指针
                        char = self.token.getType(index)
                    else:  # 表达式不正确
                        return enums.ERROR
                else:  # 语法错误，出现等号没有算术表达式
                    return errorExpect("an expression", self.len_num)
            elif char == ",":  # 向前移动指针防止死循环
                index, char = self.forwordIndex(index)
        return enums.OK

    def ariExpression(self, print_error=True):
        """
        检查算数表达式，并计算表达式中的值
        传入的值用来进行对某些打印类型是否输出的判断，应为布尔值的判断可能会用到
        返回算数表达式的值，错误返回None
        结束后指针指向ARIEXP
        """
        index = self.start_index
        char = self.token.getType(index)
        tokens = []
        while char and char not in const.ARIEXP and char != "=_":
            # 算术表达式读到const.ARIEXP结束
            # ARIEXP = ["==", "and", "or", "<", ">", "<=", ">=", "!=", ",", "."]
            if char == "id":
                # 如果是id
                name = self.token.getValue(index)
                if name not in self.id:  # 没有声明的不可以用
                    return errorUndefine(name, self.len_num)
                val = self.assignment2(False)
                if val == "NO":  # 说明不是第二类赋值语句
                    type = self.id[name][0]
                    value = self.id[name][1]
                    if value is None:
                        return errorUninit(name, self.len_num)
                    if type != "float":  # 类型检测，如果不是float 那么就报错
                        len_num = self.len_num
                        return errorUnexpectType(type, "float", len_num, print_error)
                    else:
                        tokens.append(value)
                elif val is None:
                    return enums.ERROR
                else:
                    tokens.append(val)
                    index, char = self.updateIndex()
            elif char == "num":  # 如果是数字
                value = self.token.getValue(index)
                tokens.append(value)
                # 这里刚好会跳过=_
            elif char in ["+", "-", "*", "/"]:  # 算数表达式
                tokens.append(char)
            else:  # 出现了其他符号
                return errorUnexpectChar(char, self.len_num, print_error)
            index, char = self.forwordIndex(index)  # 指针前移
        # 写入tokens的元素只可能是数字字符串或者运算符
        val = findInvalidAri(tokens)  # 检测表达式是否合法
        if val == None:  # 表达式合法
            self.start_index = index  # 指针调整
            return calculateExpression(tokens)
        elif val != -1:  # 表达式不合法
            return errorUnexpectChar(tokens[val], self.len_num)
        else:  # 表达式为空
            return errorExpect("arithmetic expressions", self.len_num)

    def strExpression(self):
        """
        检查字符串表达式，并计算表达式中的值
        返回字符串表达式的值，错误返回None
        """
        index = self.start_index
        char = self.token.getType(index)
        tokens = ""
        check = False  # 检查是否出现 + str 或者 str + + 的情况
        # 为False 代表可用继续加入字符
        # True代表期待读到一个+或者已经结束
        while char and char not in const.STREXP:
            if char == "str" and check == False:
                string = self.token.getValue(index)
                tokens += string
                check = True  # 期待+或者结束
            elif char == "id" and check == False:
                name = self.token.getValue(index)
                if name not in self.id:  # 如果变量没有声明
                    return errorUndefine(name, self.len_num)
                type = self.id[name][0]
                val = self.id[name][1]
                if val is not None:  # 被初始化了
                    if type == "float":  # 根据类型来决定下一步
                        val = str(val)
                    elif type == "bool":
                        if val:  # 返回True / False
                            val = "阳"
                        else:
                            val = "阴"
                    tokens += val  # 字符串粘贴
                    check = True  # 期待+或者结束
                else:
                    errorUninit(name, self.len_num)
            elif char == "+" and check:
                check = False  # 期待一个字符串
            else:
                if check:
                    return errorExpect("+ or .", self.len_num)
                else:
                    return errorExpect("a string or a variable", self.len_num)
            index, char = self.forwordIndex(index)
        if check == False:
            return errorExpect("a string or a variable", self.len_num)
        self.start_index = index
        return tokens

    def logicExpression(self):
        """
        检查逻辑表达式，并计算表达式中的值
        返回逻辑表达式的值True/False，错误返回None
        结束后指针指向, 或者 .
        """
        index = self.start_index
        char = self.token.getType(index)
        tokens = []  # 保存逻辑表达式的列表
        compare = []  # 保存当前的比较关系
        while char and char not in const.STREXP:  # 循环到遇到, 或者.
            if char in ["id", "num", "-"]:
                self.start_index = index
                val = self.ariExpression()
                if val is not None:
                    compare.append(val)
                    index, char = self.updateIndex()
                    continue
                elif char == "id":  # 不是运算符只用考虑，变量为布尔值的情况
                    name = self.token.getValue(index)
                    if name not in self.id:
                        return errorUndefine(name, self.len_num)
                    type = self.id[name][0]
                    val = self.id[name][1]
                    if type == "bool" and val:
                        val = tool_self.boolToString(val)
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
                    val = findInvalidCompare(compare)
                    if val is not None:
                        return errorUnexpectChar(compare[val], self.len_num)
                    else:
                        val = calculateCompareExpression(compare)
                        tokens.append(val)
                        compare = []
                tokens.append(char)
            else:
                return errorUnexpectChar(char, self.len_num)
            index, char = self.forwordIndex(index)
        length = len(compare)
        if length != 0:
            val = findInvalidCompare(compare)
            if val is not None:
                return errorUnexpectChar(compare[val], self.len_num)
            else:
                val = calculateCompareExpression(compare)
                tokens.append(val)
                compare = []
        val = findInvalidLogic(tokens)
        if val is None:  # 逻辑表达式合法
            self.start_index = index  # 移动指针表示，已经读取完成
            return calculateLogicExpression(tokens)
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
            if i >= self.end_index:
                char = None
                i = self.end_index
            else:
                char = self.token.getType(i)
            return (i, char)
        else:
            char = self.token.getType(i)
            if char and char not in condition:
                i, char = self.forwordIndex(i)
            return (i, char)

    def updateIndex(self):
        return (self.start_index, self.token.getType(self.start_index))

    def getIndex(self, index):
        return (index, self.token.getType(index))

    def tokenToList(self, end_char=""):
        """
        返回从当前token的起始下标到终止下标的数组
        """
        index, char = self.updateIndex()
        tokens = []
        while index < self.end_index and char != end_char:
            tokens.append(char)
            index, char = self.forwordIndex(index)
        return tokens
