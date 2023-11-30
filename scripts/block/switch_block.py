from tools import enums
from tools import const
from tools.error import *
from tools import tool_self as tool
from block import base_statement as base


def checkSwitchBlockFront(len_num):
    """指针指向了:后方，正确返回变量名字，错误返回None

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理

    Returns:
        None: 代表检测到错误 \n
        string: 返回switch语句中的变量名字
    """
    index, char = tool.updateIndex()
    if char != "id":
        return errorExpect("id", len_num)
    name = const.token.getValue(index)
    if name not in const.id:  # 没有声明的不可以用
        return errorUndefine(name, len_num)
    type = const.id[name][0]
    if type == "bool":
        return errorUnexpectType("bool", "float or string", len_num)
    index, char = tool.forwordIndex(index)
    if char != "switch":
        return errorExpect("switch", len_num)
    index, char = tool.forwordIndex(index)
    if char != ":":
        return errorExpect(":", len_num)
    index, char = tool.forwordIndex(index)
    const.start_index = index
    return name


def checkSwitchBranch(len_num, name):
    """检查每一个分支语句的前半部分是否满足要求，退出后指针指向then后一位

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理 \n
        name (string): 为switch语句中的变量的名字

    Returns:
        None: 代表检测到错误 \n
        bool: 返回switch语句中的变量特定case对应的值是否等于switch中的变量名字
    """
    index, char = tool.updateIndex()
    if char != "case":
        return errorExpect("case", len_num)
    index, char = tool.forwordIndex(index)
    const.start_index = index  # 要调用运算函数需要调整指针
    type = const.id[name][0]
    value = const.id[name][1]
    val = None
    if type == "float":
        val = base.ariExpression(len_num)
        if val is None:
            return enums.ERROR
    else:  # 只有可能为float 或者 string，应为语法定义
        val = base.strExpression(len_num)
        if val is None:
            return enums.ERROR
    index, char = tool.updateIndex()  # 调用完运算函数需要调整指针
    if char != ",":
        return errorExpect(",", len_num)
    index, char = tool.forwordIndex(index)
    if char != "then":
        return errorExpect("then", len_num)
    index, char = tool.forwordIndex(index)
    const.start_index = index
    if val == value:
        return True
    else:
        return False
