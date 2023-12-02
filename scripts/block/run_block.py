from tools import enums
from tools import const
from tools.error import *
from tools import tool_self as tool
from block import if_block as Bif
from block import while_block as Bwhile
from block import switch_block as Bswitch
from block import normal_block as Bnormal


def runBlock(len_num, end):
    """运行if, while, switch代码块，返回后的指针指向下一个待执行的代码块

    Args:
        Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理 \n
        end (integer): 语句块终止的位置的下一位。语句块结束后，下一个语句的起始位置。

    Returns:
        * None 代表检测到错误
        * 其他 代表块执行成功，由于这里需要执行if, while, switch以及普通语句，所以返回值类型比较多
            * 普通语句
                * 若为赋值语句，返回赋值语句返回的值
                * 若不为赋值语句则返回1
            * 其他语句，则是使用了递归调用进行语句块的执行。

    """
    if const.start_index == end:  # 递归结束条件
        return enums.OK
    off = 0
    val = None
    index, char = tool.updateIndex()
    if char == "if":
        val = ifBlock(len_num, end)  # 指向完后指针指向下一个待指向语句
    elif char == "while":
        i = Bwhile.divideWhileSwitchBlock(len_num, end)
        if i is None:
            return enums.ERROR
        val = whileBlock(len_num, i)
    elif char == "end":  # 读到end，跳过end，end也代表代码块要结束了
        if checkBlockEnd(len_num, end):  # 检查end 的正确性
            const.start_index = end  # switch跳过了中间代码，其他跳过了end;|end!
            val = "end"  # 正确则改变val的值，因为后面还有可能有语句
    else:
        index, char = tool.forwordIndex(index)
        if char == "switch":
            i = Bwhile.divideWhileSwitchBlock(len_num, end)
            if i is None:
                return enums.ERROR
            val = switchBlock(len_num, i)  # 由于存在递归的情况，不是每一次都是刚好在！的位置停
        else:
            val = Bnormal.normalBlock(len_num)  # 执行完成之后会指向.
            off = 1
    if val is None:
        return enums.ERROR
    const.start_index += off  # 跳过.
    return runBlock(len_num, end)


def ifBlock(len_num, end):
    """if语句初步执行，执行到，用于判断需if条件是否成立，然后执行相应代码

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理 \n
        end (integer): 语句块终止的位置的下一位。语句块结束后，下一个语句的起始位置。

    Returns:
        * None 代表检测到错误
        * 1 代表执行语句成功
    """
    val = Bif.checkIfBlockFront(len_num)  # 指针指向了then的后一位
    result = Bif.divideIfBlock(len_num, end)  # 这里指针已经跳过了if
    if val is None or result is None:
        return enums.ERROR
    return runIfBlock(len_num, val, result[0], result[1])


def runIfBlock(len_num, val, mid, end):
    """执行if块语句

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理 \n
        val (bool): if条件是否成立 \n
        mid (integer): 指向else的位置，如果没有其值和end一样 \n
        end (integer): 语句块终止的位置的下一位。语句块结束后，下一个语句的起始位置。

    Returns:
        * None 代表检测到错误
        * 1 代表执行语句成功
    """
    if Bif.checkIfBlockEnd(len_num, mid, end) is None:
        return enums.ERROR
    if val:  # val 为 True  或者是 False
        if runBlock(len_num, mid) is not None:
            const.start_index = end
        else:
            return enums.ERROR
    else:
        if mid != end:  # 不等说明有else mid 指向else，相等指向下一个待执行语句，不用 +1
            const.start_index = mid + 1
        else:
            const.start_index = mid
        if runBlock(len_num, end) is None:
            return enums.ERROR
    return enums.OK


def whileBlock(len_num, end):
    """执行while块语句

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理 \n
        end (integer): 语句块终止的位置的下一位。语句块结束后，下一个语句的起始位置。

    Returns:
        * None 代表检测到错误
        * 1 代表执行语句成功
    """
    start = const.start_index
    val = Bwhile.checkWhileBlockFront(len_num)
    if val is None:
        return enums.ERROR
    if val:  # val 为 True 或者 False
        if runBlock(len_num, end) is not None:  # 执行while代码块
            const.start_index = start  # 执行结束改变指针
            return whileBlock(len_num, end)  # 递归条用
        else:
            return enums.ERROR
    else:  # 递归结束出口
        const.start_index = end
    return enums.OK


def switchBlock(len_num, end):
    """执行switch块语句

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理 \n
        end (integer): 语句块终止的位置的下一位。语句块结束后，下一个语句的起始位置。

    Returns:
        * None 代表检测到错误
        * 1 代表执行语句成功
    """
    name = Bswitch.checkSwitchBlockFront(len_num)
    if name is None:
        return enums.ERROR
    val = findRightPositon(len_num, name, end)
    if val is None:
        return enums.ERROR
    else:
        const.start_index = end
        return enums.OK


def findRightPositon(len_num, name, end):
    """找到合适的位置，然后执行语句

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理 \n
        name (string): 为switch语句中的变量的名字 \n
        end (integer): 语句块终止的位置的下一位。语句块结束后，下一个语句的起始位置。

    Returns:
        * None 代表检测到错误
        * 1 代表执行语句成功
    """
    index, char = tool.updateIndex()
    while index < end:
        if char == "case":  # 检测case
            const.start_index = index  # 更新下标
            match = Bswitch.checkSwitchBranch(len_num, name)
            if match is None:
                return enums.ERROR
            if match:  # 如果两个值相等了，就退出
                if runBlock(len_num, end) is None:
                    return enums.ERROR  
                break
        elif char == "else":  # 检测else
            index, char = tool.forwordIndex(index)
            const.start_index = index  # 让开始指针指向正确位置
            runBlock(len_num, end)
            break
        elif char == "switch":  # 需要跳过switch 语句
            index = Bwhile.divideWhileSwitchBlock(len_num, end) - 1  # 指向！就好了
            char = const.token.getType(index)  # 更新字符
            continue
        index, char = tool.forwordIndex(index)
    return enums.OK


def checkBlockEnd(len_num, end):
    """检查代码块结束的合法性。开始指针不移动

    Args:
        len_num (integer): 现在读取到哪一行，用于进行报错处理 \n
        end (integer): 语句块终止的位置的下一位。语句块结束后，下一个语句的起始位置。

    Returns:
        * None 代表检测到错误
        * 1 代表执行语句成功
    """
    index, char = tool.getIndex(end - 2)
    if char != "end":
        return errorExpect("end", len_num)
    index, char = tool.forwordIndex(index)
    if char != "!" and char != ";":
        return errorExpect("! or ;", len_num)
    return enums.OK
