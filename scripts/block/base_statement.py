from tools import enums
from tools.calculate_expression import *
from tools import const
from tools.error import *
from tools import tool_self as tool


def ariExpression(len_num, print_error=True):
    """检查算数表达式，并计算表达式中的值，结束时指针指向["==", "and", "or", "<", ">", "<=", ">=", "!=", ",", "."]

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理 \n
        print_error (bool, optional): 用于控制错误是否输出，因为有时候会调用这个函数检测某个式子是否为算术表达式. Defaults to True.

    Returns:
        None: 代表检测到错误 \n
        integer / flaot: 这个算数表达式计算后的值
    """
    index = const.start_index
    char = const.token.getType(index)
    tokens = []
    while char and char not in const.ARIEXP and char != "=_":
        # 算术表达式读到const.ARIEXP结束
        # ARIEXP = ["==", "and", "or", "<", ">", "<=", ">=", "!=", ",", "."]
        if char == "id":
            # 如果是id
            name = const.token.getValue(index)
            if name not in const.id:  # 没有声明的不可以用
                return errorUndefine(name, len_num)
            val = assignment2(len_num, False)
            if val == "NO":  # 说明不是第二类赋值语句
                type = const.id[name][0]
                value = const.id[name][1]
                if value is None:
                    return errorUninit(name, len_num)
                if type != "float":  # 类型检测，如果不是float 那么就报错
                    len_num = len_num
                    return errorUnexpectType(type, "float", len_num, print_error)
                else:
                    tokens.append(value)
            elif val is None:
                return enums.ERROR
            else:
                tokens.append(val)
                index, char = tool.updateIndex()
        elif char == "num":  # 如果是数字
            value = const.token.getValue(index)
            tokens.append(value)
            # 这里刚好会跳过=_
        elif char in ["+", "-", "*", "/"]:  # 算数表达式
            tokens.append(char)
        else:  # 出现了其他符号
            return errorUnexpectChar(char, len_num, print_error)
        index, char = tool.forwordIndex(index)  # 指针前移
    # 写入tokens的元素只可能是数字字符串或者运算符
    val = findInvalidAri(tokens)  # 检测表达式是否合法
    if val == None:  # 表达式合法
        const.start_index = index  # 指针调整
        return calculateExpression(tokens)
    elif val != -1:  # 表达式不合法
        return errorUnexpectChar(tokens[val], len_num)
    else:  # 表达式为空
        return errorExpect("arithmetic expressions", len_num)


def strExpression(len_num):
    """检查字符串表达式，并计算字符串表达式中的值，结束后指针指向[",", "."]

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理

    Returns:
        None: 代表检测到错误\n
        string: 字符串表达式返回字符串的值
    """
    index = const.start_index
    char = const.token.getType(index)
    tokens = ""
    check = False  # 检查是否出现 + str 或者 str + + 的情况
    # 为False 代表可用继续加入字符
    # True代表期待读到一个+或者已经结束
    while char and char not in const.STREXP:
        if char == "str" and check == False:
            string = const.token.getValue(index)
            tokens += string
            check = True  # 期待+或者结束
        elif char == "id" and check == False:
            name = const.token.getValue(index)
            if name not in const.id:  # 如果变量没有声明
                return errorUndefine(name, len_num)
            type = const.id[name][0]
            val = const.id[name][1]
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
                errorUninit(name, len_num)
        elif char == "+" and check:
            check = False  # 期待一个字符串
        else:
            if check:
                return errorExpect("+ or .", len_num)
            else:
                return errorExpect("a string or a variable", len_num)
        index, char = tool.forwordIndex(index)
    if check == False:
        return errorExpect("a string or a variable", len_num)
    const.start_index = index
    return tokens


def logicExpression(len_num):
    """检查逻辑表达式，并计算表达式中的值，结束后指针指向[",", "."]

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理

    Returns:
        None: 代表检测到错误 \n
        bool: 这个逻辑表达式返回的布尔值
    """
    index = const.start_index
    char = const.token.getType(index)
    tokens = []  # 保存逻辑表达式的列表
    compare = []  # 保存当前的比较关系
    while char and char not in const.STREXP:  # 循环到遇到, 或者.
        if char in ["id", "num", "-"]:  # 如果是这三种说明为算数表达式
            const.start_index = index
            val = ariExpression(len_num, False)
            if val is not None:
                compare.append(val)
                index, char = tool.updateIndex()
                continue
            elif char == "id":  # 不是运算符只用考虑，变量为布尔值的情况
                name = const.token.getValue(index)
                if name not in const.id:
                    return errorUndefine(name, len_num)
                type = const.id[name][0]
                val = const.id[name][1]
                if type == "bool" and val is not None:
                    val = tool.boolToString(val)
                    compare.append(val)
                elif val is None:  # 没有初始化
                    return errorUninit(name, len_num)
                else:  # 不是bool变量
                    return errorUnexpectType(type, "bool", len_num)
            else:  # 运算符号出现问题
                return errorExpect("arithmetic expressions", len_num)
        elif char == "true" or char == "false":
            compare.append(char)
        elif char in const.COMPARE:
            compare.append(char)
        elif char in ["or", "and"]:
            length = len(compare)
            if length != 0:
                val = findInvalidCompare(compare)
                if val is not None:
                    return errorUnexpectChar(compare[val], len_num)
                else:
                    val = calculateCompareExpression(compare)
                    tokens.append(val)
                    compare = []
            tokens.append(char)
        else:
            return errorUnexpectChar(char, len_num)
        index, char = tool.forwordIndex(index)
    length = len(compare)
    if length != 0:
        val = findInvalidCompare(compare)
        if val is not None:
            return errorUnexpectChar(compare[val], len_num)
        else:
            val = calculateCompareExpression(compare)
            tokens.append(val)
            compare = []
    val = findInvalidLogic(tokens)
    if val is None:  # 逻辑表达式合法
        const.start_index = index  # 移动指针表示，已经读取完成
        return calculateLogicExpression(tokens)
    else:  # 逻辑表达式不合法
        return errorUnexpectChar(tokens[val], len_num)


def assignment1(len_num):
    """第一种赋值语句，进行类似于 苹果为苹果加3 的赋值运算，结束后指针指向[",", "."]

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理

    Returns:
        None: 出现错误 \n
        integer / float: 算数表达式被赋予的值 \n
        string: 字符串表达式被赋予的值 \n
        bool: 逻辑表达式被赋予的值
    """
    index, char = tool.updateIndex()
    if char == "id":  # 检测是否为id
        name = const.token.getValue(index)
        if name not in const.id:  # 是否初始化
            return errorUndefine(name, len_num)
        type = const.id[name][0]
        index, char = tool.forwordIndex(index)
        if char != "=":
            return errorExpect("=", len_num)
        const.start_index, char = tool.forwordIndex(index)
        val = None
        if type == "float":
            val = ariExpression(len_num)
        elif type == "bool":
            val = logicExpression(len_num)
        elif type == "string":
            val = strExpression(len_num)
        if val is not None:  # 不为None
            const.id[name][1] = val
            return enums.OK
        else:
            return val
    else:  # 不是 id 报错
        return errorUnexpectChar(char, len_num)


def assignment2(len_num, print_error=True):
    """第二种赋值语句，进行类似于 苹果加3也 的赋值运算，结束后指针指向"=_"

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理 \n
        print_error (bool, optional): 用于控制错误是否输出，因为有时候会调用这个函数检测某个式子是否为第二种赋值语句. Defaults to True.

    Returns:
        None: 代表检测到错误 \n
        "NO": 代表不是第二类赋值语句 \n
        integer / flaot: 其他则进行检测算数运算符操作，并计返回算最终变量应该有的值/None
    """
    index, char = tool.updateIndex()
    while char and char != "=_" and char not in const.STREXP:
        index, char = tool.forwordIndex(index)
    if char != "=_":
        errorUnexpectChar(char, len_num, print_error)
        return "NO"  # 代表不是第二类赋值语句
    index, char = tool.updateIndex()
    if char == "id":
        name = const.token.getValue(index)
        if name not in const.id:
            return errorUndefine(name, len_num)
        type = const.id[name][0]
        if type == "float":
            const.start_index, char = tool.forwordIndex(index)
            return assignReadOperator(len_num, name)
        else:
            return errorUnexpectType(type, "flaot", len_num)
    else:
        return errorUnexpectChar(char, len_num)


def assignReadOperator(len_num, name):
    """进行检测算数运算符操作

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理 \n
        name (string): 传入变量的的名字，用于对变量进行赋值

    Returns:
        None : None代表检测到错误 \n
        integer / flaot: 其他则进行检测被操作数字操作，并计返回算最终变量应该有的值/None
    """
    index, char = tool.updateIndex()
    if char in ["+", "-", "*", "/"]:
        operator = char
        const.start_index, char = tool.forwordIndex(index)
        return assignReadAri(len_num, name, operator)
    else:
        return errorExpect("a operator", len_num)


def assignReadAri(len_num, name, operator):
    """进行检测算数运算符操作

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理 \n
        name (string): 传入变量的的名字，用于对变量进行赋值 \n
        operator (char): 操作符号的类型["+", "-", "*", "/"]
    Returns:
        None: 代表检测到错误 \n
        integer / flaot: 这个算数表达式计算后的值
    """
    val = ariExpression(len_num, False)
    index, char = tool.updateIndex()
    if val is None:
        return errorExpect("an expression", len_num)
    elif char == "=_":  # 结束的时候指针指向=_
        return calculate(name, operator, val)
    else:
        return errorExpect("=_", len_num)


def calculate(name, operator, val):
    """第二类赋值语句的算术表达式的值

    Args:
        name (string): 传入变量的的名字，用于对变量进行赋值 \n
        operator (char): 操作符号的类型["+", "-", "*", "/"] \n
        val (integer/float): 需要和变量名为name的变量进行预算操作的数值 \n

    Returns:
        integer / flaot: 这个算数表达式计算后的值
    """
    if operator == "+":
        const.id[name][1] += val
    elif operator == "-":
        const.id[name][1] -= val
    elif operator == "*":
        const.id[name][1] *= val
    elif operator == "/":
        const.id[name][1] /= val
    return const.id[name][1]
