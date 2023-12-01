from tools import enums
from tools import const
from tools.error import *
from tools import tool_self as tool
from block import base_statement as base


def checkWhileBlockFront(len_num):
    """检查while语句中的前半部分是否满足要求，返回后指针指向then的后一位

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理

    Returns:
        * None 代表检测到错误
        * bool 返回while语句中的循环变量是否为True
    """
    index, char = tool.updateIndex()
    if char != "while":
        return errorExpect("while", len_num)
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


def divideWhileSwitchBlock(len_num, end):
    """定位while语句和switch语句的结束位置，返回指向!后一个的指针，指针起始位置指向["if", "while", "switch"]

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理 \n
        end (integer): 语句块终止的位置的下一位。语句块结束后，下一个语句的起始位置。

    Returns:
        * None 代表检测到错误
        * integer 返回while语句和switch语句的结束位置并返回
    """
    stack = []  # 指针起始位置指向["if", "while", "switch"]所以不用向栈里面添加任何元素
    i = -1
    index, char = tool.updateIndex()
    while index < end:
        if char in ["if", "while", "switch"]:
            stack.append(char)
        elif char == "!":
            stack.pop()
            if len(stack) == 0:  # 得到if块结束的下标，这个为end-1
                i = index
                break
        index, char = tool.forwordIndex(index)
    if len(stack) != 0:
        return errorExpect("!", len_num)
    return i + 1
