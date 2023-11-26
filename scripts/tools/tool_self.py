from tools import const

def stringToBool(val):
    if len(val) == 1:
        if val == "阴":
            val = True
        elif val == "阳":
            val = False
        else:
            val = bool(val)
    else:
        val = bool(val)
    return val


def boolToString(val):
    if val:
        val = "true"
    else:
        val = "false"
    return val

def forwordIndex(i):
    """
    指针前移，返回前进的指针下标和token类型
    condition为前移条件，如果有条件那么就不向前移动
    """
    i += 1
    # 越界检查
    if i >= const.end_index:
        char = None
        i = const.end_index
    else:
        char = const.token.getType(i)
    return (i, char)

def updateIndex():
    return (const.start_index, const.token.getType(const.start_index))

def getIndex(index):
    return (index, const.token.getType(index))

def tokenToList(end_char=""):
    """
    返回从当前token的起始下标到终止下标的数组
    """
    index, char = updateIndex()
    tokens = []
    while index < const.end_index and char != end_char:
        tokens.append(char)
        index, char = forwordIndex(index)
    return tokens
