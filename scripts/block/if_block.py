from tools import enums
from tools import const
from tools.error import *
from tools import tool_self as tool
from block import base_statement as base


def checkIfBlockFront(len_num):
    """检查if语句的前半部分，也就是 若……，则……返回后的指针指向then(则)的后一位

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理

    Returns:
        None: 代表检测到错误 \n
        bool: 代表if后面逻辑的值
    """
    index, char = tool.updateIndex()
    if char != "if":
        return errorExpect("if", len_num)
    index, char = tool.forwordIndex(index)  # 向前移动一位
    const.start_index = index  # 要进入另外一个函数需要改变const.start_index
    val = base.logicExpression(len_num)
    if val is None:
        return enums.ERROR
    index, char = tool.updateIndex()
    if char != ",":
        return errorExpect(",", len_num)
    index, char = tool.forwordIndex(index)  # 向前移动一位
    if char != "then":
        return errorExpect("then", len_num)
    index, char = tool.forwordIndex(index)  # 向前移动一位
    const.start_index = index
    return val


def checkIfBlockEnd(len_num, mid, end):
    """判断IF语句后续是否完整，检测终end!/end;，返回后的指针不变。

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理 \n
        mid (integer): if 语句块中else的位置，指向else，没有则mid == mid \n
        end (integer): if 语句块终止的位置的下一位。IF语句块结束后，下一个语句的起始位置。

    Returns:
        None: 代表检测到错误 \n
        1: 代表没有错误，IF语句块完整
    """
    if mid != end:
        index, char = tool.getIndex(mid - 2)
        if char != "end":
            return errorExpect("end", len_num)
        index, char = tool.forwordIndex(index)
        if char != ";":
            return errorExpect(";", len_num)
    index, char = tool.getIndex(end - 2)
    if char != "end":
        return errorExpect("end", len_num)
    index, char = tool.forwordIndex(index)
    if char != "!":
        return errorExpect("!", len_num)
    return enums.OK


def divideIfBlock(len_num, end):
    """将if 块划分为两块，或者一块，也就是寻找转跳下标。

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理 \n
        end (integer): if 语句块终止的位置的下一位。IF语句块结束后，下一个语句的起始位置。

    Returns:
        None: 代表检测到错误 \n
        (integer, integer): 第一位代表else的位置，第二位代表IF语句块结束后，下一个语句的起始位置。
    """
    stack = ["if"]  # 指针已经跳过了if 所以把if添加到栈底
    i = -1
    j = -1
    index, char = tool.updateIndex()
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
        index, char = tool.forwordIndex(index)
    if len(stack) != 0:
        return errorExpect("!", len_num)
    if i == -1:  # 为-1说明不存在else语句
        return (j + 1, j + 1)
    else:
        return (i, j + 1)  # j要指向下一个待执行的语句，不是!
