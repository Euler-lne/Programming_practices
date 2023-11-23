from tools import token_self


class Read:
    """
    读取文件类，边读边生成Token
    """

    def __init__(self, path, encodeing="utf-8"):
        self.path = path
        self.encodeing = encodeing
        self.token = token_self.Token()
        self.temp_id = ""
        self.is_conmment = False  # 标记现在是否处于注释状态
        self.is_string = False  # 标记现在是否处于字符串状态
        self.stack = []  # 用于进行引号匹配，是一个栈
        self.string = ""  # 用于保存字符串
        self.len_num = 1
        self.readFile()

    # 读取待编译的文件
    def readFile(self):
        """
        读取文件，边读边生成Token，保存到self.token中
        """
        with open(self.path, "r", encoding=self.encodeing) as file:
            while True:
                char = file.read(1)
                if not char:
                    break
                if self.is_conmment or self.is_string:
                    if self.is_conmment:  # 注释状态
                        if char == "\n":
                            self.is_conmment = False
                            self.len_num += 1
                    else:  # 字符串状态
                        if char == "“":  # “入栈
                            self.stack.append(char)
                            self.string += char
                        elif char == "”":  # ”出栈
                            self.stack.pop()
                            if len(self.stack) != 0:  # 长度不为0说明还是字符串
                                self.string += char
                            else:  # 长度为0说明字符串结束
                                self.token.addToken("str", self.string)
                                self.is_string = False
                                self.string = ""
                        else:
                            if char == "\n":
                                self.len_num += 1
                            self.string += char
                else:
                    if self.buildToken(file, char) == -1:
                        return -1
        self.checkID(False)

    def buildToken(self, file, char):
        """
        该函数用于生成Token，返回-1代表代码有词法问题
        """
        if char == "#":
            self.is_conmment = True
        elif char == "“":
            self.is_string = True
            self.stack.append(char)
        elif char in ["\n", " ", "\t", "\r"]:  # 出去换行和空格
            if char == "\n":
                self.len_num += 1
            return 0
        elif char == "有":  # 判断“有X曰”这个是变量声明。
            temp_char = char
            char = file.read(1)
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
                char = file.read(1)
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
        elif char == "加":
            self.token.addToken("+", char)
            self.checkID()
        elif char == "减":
            self.token.addToken("-", char)
            self.checkID()
        elif char == "乘":
            self.token.addToken("*", char)
            self.checkID()
        elif char == "除":
            self.token.addToken("/", char)
            self.checkID()
        elif char == "若":
            temp_char = char
            file_position = file.tell()  # 记录文件指针位置
            char = file.read(1)
            if char and char == "为":
                temp_char += char
                self.token.addToken("case", temp_char)
                self.checkID()
            else:
                file.seek(file_position)  # 指针回退
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
            char = file.read(1)
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
        elif char.isdigit() or char == "-":  # 如果char是数字
            temp_char = char
            file_position = file.tell()  # 记录文件指针位置
            if char == "-":
                char = file.read(1)
                if char and char.isdigit():
                    dot = 0
                    while char and (char.isdigit() or (char == "." and dot < 1)):
                        # 要么是数字，要么是.且.没有出现过
                        temp_char += char
                        if char == ".":
                            dot += 1
                        file_position = file.tell()  # 记录文件指针位置
                        char = file.read(1)

                    if temp_char == "-":  # 说明只有一个"-"
                        self.error(char)
                        return -1
                    else:
                        self.error(char)
                        file.seek(file_position)  # 指针回退

                else:  # 出错"-"后面没有跟着数字
                    self.error("-" + char)
                    return -1
            else:
                char = file.read(1)
                dot = 0
                while char and (char.isdigit() or (char == "." and dot < 1)):
                    # 要么是数字，要么是.且.没有出现过
                    temp_char += char
                    if char == ".":
                        dot += 1
                    file_position = file.tell()  # 记录文件指针位置
                    char = file.read(1)
                self.token.addToken("num", temp_char)
                file.seek(file_position)  # 指针回退

            pass
        elif "\u4e00" <= char <= "\u9fff":
            self.temp_id += char
        else:
            self.error(char)
            return -1
        return 0

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

    def error(self, char):
        print("Unexpected char: " + char + " in line " + str(self.len_num))
