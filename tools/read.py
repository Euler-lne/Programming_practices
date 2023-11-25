from tools import token_self
from tools import enums
from tools.error import *


class Read:
    """
    读取文件类，词法分析边读边生成Token，以一个语法块为一个单位。
    然后返回给compile
    """

    def __init__(self, path, encodeing="utf-8"):
        self.path = path  # 文件路径
        self.encodeing = encodeing  # 编码
        self.token = token_self.Token()  # 用于记录当前的Token
        self.temp_id = ""  # 用于记录当前不为关键字的汉字
        self.is_conmment = False  # 标记现在是否处于注释状态
        self.is_string = False  # 标记现在是否处于字符串状态
        self.stack1 = []  # 用于进行引号匹配，是一个栈
        self.stack2 = []  # 用于语句块划分
        self.string = ""  # 用于保存字符串
        self.len_num = 1  # 用于记录当前有几行
        self.senten_state = enums.NONE  # 记录语句状态
        self.file = open(self.path, "r", encoding=self.encodeing)

    def readBlock(self):
        """
        读取文件，边读边生成Token，保存到self.token中。
        每次读取到逗号，如果有分支或者循环读取到相应的分支或者循环的终！
        返回enums.ERROR代表出现了词法错误。
        """
        len = self.token.getLen()
        while True:
            char = self.file.read(1)
            if not char:
                # 文末
                self.checkID(False)
                self.file.close()
                return enums.END
            if self.buildToken(char) == enums.ERROR:
                # 出现错误
                self.file.close()
                return enums.ERROR
            elif len != self.token.getLen():
                # 如果Token长度在循环终改变了
                temp = self.divideToken()
                if temp == enums.ACCEPT:
                    state = self.senten_state
                    self.senten_state = enums.NONE  # 接收之后要保证状态转换为enums.NONE
                    return state
                elif temp == enums.ERROR:
                    return enums.ERROR
            len = self.token.getLen()

    def checkChar(self, char):
        """
        检查相关的字符，然后加入到Token中
        """
        if char == "#":
            self.is_conmment = True
        elif char == "“":
            self.is_string = True
            self.stack1.append(char)
        elif char in ["\n", " ", "\t", "\r"]:  # 出去换行和空格
            if char == "\n":
                self.len_num += 1
            return enums.OK
        elif char == "有":  # 判断“有X曰”这个是变量声明。
            temp_char = char
            char = self.file.read(1)
            match_type = ""
            temp_char += char
            if char and char == "数":
                match_type = "float"
            elif char and char == "言":
                match_type = "string"
            elif char and char == "爻":
                match_type = "bool"
            if match_type == "":  # 没有匹配，添加到临时ID中
                self.temp_id += temp_char
            else:
                char = self.file.read(1)
                temp_char += char
                if char and char == "曰":
                    self.token.addToken(match_type, temp_char)
                    self.checkID()
                else:
                    self.temp_id += temp_char
        elif char == "为":
            self.token.addToken("=", char)
            self.checkID()
        elif char == "也":
            self.token.addToken("=_", char)
            self.checkID()
        elif char == "加" or char == "+":
            self.token.addToken("+", char)
            self.checkID()
        elif char == "减" or char == "-":
            self.token.addToken("-", char)
            self.checkID()
        elif char == "乘" or char == "*":
            self.token.addToken("*", char)
            self.checkID()
        elif char == "除" or char == "/":
            self.token.addToken("/", char)
            self.checkID()
        elif char == "若":
            temp_char = char
            file_position = self.file.tell()  # 记录文件指针位置
            char = self.file.read(1)
            if char and char == "为":
                temp_char += char
                self.token.addToken("case", temp_char)
                self.checkID()
            else:
                self.file.seek(file_position)  # 指针回退
                self.token.addToken("if", temp_char)
                self.checkID()
        elif char == "则":
            self.token.addToken("then", char)
            self.checkID()
        elif char == "凡":
            self.token.addToken("while", char)
            self.checkID()
        elif char == "终":
            self.token.addToken("end", char)
            self.checkID()
        elif char == "者":
            self.token.addToken("switch", char)
            self.checkID()
        elif char == "非":
            temp_char = char
            char = self.file.read(1)
            temp_char += char
            match_type = ""
            if char and char == "同":
                match_type = "!="
            elif char and char == "大":
                match_type = "<="
            elif char and char == "小":
                match_type = ">="
            elif char and char == "者":
                match_type = "else"
            if match_type == "":  # 没有匹配，如：非他
                self.temp_id += temp_char
            else:
                self.token.addToken(match_type, temp_char)
                self.checkID()
        elif char == "同":
            self.token.addToken("==", char)
            self.checkID()
        elif char == "且":
            self.token.addToken("and", char)
            self.checkID()
        elif char == "或":
            self.token.addToken("or", char)
            self.checkID()
        elif char == "小":
            self.token.addToken("<", char)
            self.checkID()
        elif char == "大":
            self.token.addToken(">", char)
            self.checkID()
        elif char == "曰":
            self.token.addToken("print", char)
            self.checkID()
        elif char in ["获", "得", "受"]:
            self.token.addToken("input", char)
            self.checkID()
        elif char == "阴":
            self.token.addToken("false", char)
            self.checkID()
        elif char == "阳":
            self.token.addToken("true", char)
            self.checkID()
        elif char == "！":
            self.token.addToken("!", char)
            self.checkID()
        elif char == "：":
            self.token.addToken(":", char)
            self.checkID()
        elif char == "，":
            self.token.addToken(",", char)
            self.checkID()
        elif char == "。":
            self.token.addToken(".", char)
            self.checkID()
        elif char == "；":
            self.token.addToken(";", char)
            self.checkID()
        elif char.isdigit():  # 如果char是数字
            temp_char = char
            file_position = self.file.tell()  # 记录文件指针位置
            char = self.file.read(1)
            dot = 0
            while char and (char.isdigit() or (char == "." and dot < 1)):
                # 要么是数字，要么是.且.没有出现过
                temp_char += char
                if char == ".":
                    dot += 1
                file_position = self.file.tell()  # 记录文件指针位置
                char = self.file.read(1)
            self.token.addToken("num", temp_char)
            self.file.seek(file_position)  # 指针回退，应为每次都多读了以为
            # 比如12.3.4，那么如果不会退位置那么指针就指向了第二个.，这样这个.就被舍去了

        elif "\u4e00" <= char <= "\u9fff":
            self.temp_id += char
        else:
            return errorUnexpectChar(char, self.len_num)
        return enums.OK

    def checkID(self, is_swap=True):
        """
        作用：检查是否为ID，由于ID没有特定的标识，
        所以不为buildToken中的所有汉字都有可能为ID。
        在两个能匹配项之间的汉字记为ID，能匹配指的是处于token.md的
        当buildToken检测匹配时才调用这个函数进行添加ID
        """
        if self.temp_id != "":
            self.token.addToken("id", self.temp_id)
            self.temp_id = ""
            if is_swap:
                self.token.swapToken()

    def buildToken(self, char):
        """
        创建Token
        """
        if self.is_conmment or self.is_string:
            if self.is_conmment:  # 注释状态
                if char == "\n":
                    self.is_conmment = False
                    self.len_num += 1
            else:  # 字符串状态
                self.checkString(char)
        else:
            if self.checkChar(char) == enums.ERROR:
                return enums.ERROR
        return enums.OK

    def saveToken(self, path="./log/token", encoding="utf-8", col=5):
        """
        将Token 保存到指定路径，指定编码，指定列数
        """
        if self.token.getLen() == 0:
            print("Token is empety!")
        else:
            if ".txt" not in path:
                path = path + str(self.path).split("/")[-1]
            with open(path, mode="w", encoding=encoding) as f:
                j = 0
                for i in self.token.token:
                    f.write(str(i))
                    j += 1
                    if j == col:
                        j = 0
                        f.write("\n")

    def checkString(self, char):
        """
        完成字符串检查，通过控制栈来实现
        """
        if char == "“":  # “入栈
            self.stack1.append(char)
            self.string += char
        elif char == "”":  # ”出栈
            self.stack1.pop()
            if len(self.stack1) != 0:  # 长度不为0说明还是字符串
                self.string += char
            else:  # 长度为0说明字符串结束
                self.token.addToken("str", self.string)
                self.is_string = False
                self.string = ""
        else:
            if char == "\n":
                self.len_num += 1
            self.string += char

    def divideToken(self):
        """
        将现有的Token划分未块，起到一个检测块边界的问题
        由于id 采用特殊的匹配方式，如果没有匹配到id那么Token不会增长，导致if会多次入栈。
        所以，divideToken函数之后在Token改变了才调用
        """
        if self.senten_state == enums.NONE:
            if self.token.getEndType() == ".":  # 最后一个元素是"."说明这个一语句
                self.senten_state = enums.ACCEPT
                return enums.ACCEPT
            elif self.token.getEndType() == "if":
                self.senten_state = enums.IF
                self.stack2.append("if")
            elif self.token.getEndType() == "while":
                self.senten_state = enums.WHILE
                self.stack2.append("while")
            elif self.token.getEndType() == "switch":
                self.senten_state = enums.SWITCH
                self.stack2.append("switch")
        else:
            temp = self.token.getEndType()
            if self.token.getEndType() == "!":
                self.stack2.pop()
                if len(self.stack2) == 0:  # 长度为0说明代码块匹配结束
                    return enums.ACCEPT
            elif temp == "if" or temp == "while" or temp == "switch":
                self.stack2.append(temp)
        return enums.NONE
