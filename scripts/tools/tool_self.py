from tools import const
import os


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


def openFile():
    if os.path.exists(const.PATH):  # 检查文件是否存在
        # 如果文件存在，则以读写模式打开文件
        file = open(const.PATH, "r+", encoding="utf-8")
    else:
        # 如果文件不存在，则创建一个新文件并以读写模式打开
        file = open(const.PATH, "w+", encoding="utf-8")

    return file


def findData(id):
    """查找特定文件下的id标识是否存在，如果存在那么就然会表头和内容，id为每一行的第一个标识符号，找不到返回None"""
    file = openFile()
    first_line = file.readline()
    result = []
    schemal = []
    content = []
    if first_line:
        schemal = first_line.strip().split(" ")
    else:
        return None
    result.append(schemal)
    is_match = False
    for line in file:
        for char in line.strip().split(" "):
            if char == id:
                is_match = True
            if is_match:
                content.append(char)
        if is_match:
            result.append(content)
            is_match = False
            content = []
    if len(result) > 1:
        return result
    return None
