from tools import enums
from tools import const
from tools.error import *
from tools import tool_self as tool
from block import base_statement as base


def normalBlock(len_num):
    """如果正常执行，那么将会执行到."""
    index = const.start_index
    type = const.token.getType(index)
    if type == "float" or type == "string" or type == "bool":
        return declareVar(len_num)
    elif type == "print":  # 打印函数
        return compilePrint(len_num)
    elif type == "input":  # 打印函数
        return compileInput(len_num)
    else:
        tokens = tool.tokenToList(".")  # 只将逗号之前的划分为一个列表
        if "=" in tokens:  # 第一种赋值语句
            if type == "id":
                return base.assignment1(len_num)
            else:
                return errorExpect("a variable", len_num)
        elif "=_" in tokens:  # 第二种赋值语句
            if type == "id":
                val = base.assignment2(len_num)
                if val is not None:  # 不为None
                    const.start_index, char = tool.forwordIndex(const.start_index)
                    if char == ".":  # 保证都以.结束
                        return val
                    else:
                        return errorExpect(".", len_num)
                return val
            else:
                return errorExpect("a variable", len_num)
        else:  # 无用语句
            return errorUnhelpfulStatement(len_num)


def declareVar(len_num):
    """ "
    声明变量语句
    只有type类型正确才会进入，type的错误被隔离在函数之外
    type == "float" or type == "string" or type == "bool"
    """
    index = const.start_index
    type = const.token.getType(index)  # 记录当前的变量类型
    index, char = tool.forwordIndex(index)
    if char == None or char != ":":  # 语法错误
        return errorExpect(":", len_num)
    index, char = tool.forwordIndex(index)
    while char and char != ".":
        while char and char not in [",", ".", "="]:
            if char == "id":
                name = const.token.getValue(index)
                if name in const.id:  # 声明过的变量不可以声明
                    return errorInit(name, len_num)
                const.id[name] = []
                const.id[name].append(type)
                const.id[name].append(None)
            else:  # 语法错误
                return errorUnexpectChar(char, len_num)
            index, char = tool.forwordIndex(index)
        if char == "=":  # 如果是等号那么就读取等号右边的值
            index, char = tool.forwordIndex(index)
            if char:  # 如果字符存在，移动开始指针，应为之后调用的函数需要从特定位置开始计算
                const.start_index = index
                if type == "float":  # float 类型
                    val = base.ariExpression(len_num)  # 计算表达式的值
                elif type == "string":  # 字符串类型
                    val = base.strExpression(len_num)
                else:  # 算数表达式类型，这里必定为type
                    val = base.logicExpression(len_num)
                if val is not None:  # 表达式的值正确
                    if name not in const.id:  # 防止出现 int =的情况
                        return errorExpect(name, len_num)
                    const.id[name][1] = val  # 保存表达式的值
                    index = const.start_index  # 移动当前指针
                    char = const.token.getType(index)
                else:  # 表达式不正确
                    return enums.ERROR
            else:  # 语法错误，出现等号没有算术表达式
                return errorExpect("an expression", len_num)
        elif char == ",":  # 向前移动指针防止死循环
            index, char = tool.forwordIndex(index)
    return enums.OK


def compilePrint(len_num):
    const.start_index, char = tool.forwordIndex(const.start_index)
    if char != ":":
        return errorExpect(":", len_num)
    const.start_index, char = tool.forwordIndex(const.start_index)
    string = base.strExpression(len_num)
    if string:
        print(string)
    else:
        return enums.ERROR
    return enums.OK


def compileInput(len_num):
    const.start_index, char = tool.forwordIndex(const.start_index)
    if char != ":":
        return errorExpect(":", len_num)
    if const.end_index - const.start_index != 3:
        string = "There is a problem with the input function."
        return errorUniversal(string, len_num)
    const.start_index, char = tool.forwordIndex(const.start_index)
    name = const.token.getValue(const.start_index)
    if name not in const.id:
        return errorUndefine(name, len_num)
    type = const.id[name][0]
    val = input()
    if type == "float":
        try:
            val = int(val)  # 尝试转换为整数
        except ValueError:
            try:
                val = float(val)  # 尝试转换为浮点数
            except ValueError:
                string = "It's not a number that's being entered."
                return errorUniversal(string, len_num)  # 如果无法转换，返回原始字符串
    elif type == "bool":
        val = tool.stringToBool(val)
    const.id[name][1] = val
    return enums.OK
