from tools import const
import os


def stringToBool(val):
    """将"阴"/"阳" 转换为 True/False

    Args:
        val (string): "true"/"false"

    Returns:
        * bool True/False
    """
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
    """将True/False 转换为 "true"/"false"

    Args:
        val (bool): True/False

    Returns:
        * string "true"/"false"
    """
    if val:
        val = "true"
    else:
        val = "false"
    return val


def forwordIndex(i):
    """在指定下标下指针前移

    Args:
        i (integer): 下标

    Returns:
        * (string, string) 在传入下标的基础上前进的指针下标和token类型
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
    """获取当前start_index指针下标和指向的token类型

    Returns:
        * (string, string) 当前start_index指针下标和指向的token类型
    """
    return (const.start_index, const.token.getType(const.start_index))


def getIndex(index):
    """获取一个下标下的指针下标和指向的token类型

    Args:
        (integer): 下标

    Returns:
        * (string, string) 传入下标的指针下标和token类型
    """
    return (index, const.token.getType(index))


def tokenToList(end_char=""):
    """获取从当前token的起始下标到终止下标的数组

    Args:
        end_char (str, optional): 结束的字符. Defaults to "".

    Returns:
        * list 返回当前token的起始下标到终止下标的数组
    """
    index, char = updateIndex()
    tokens = []
    while index < const.end_index and char != end_char:
        tokens.append(char)
        index, char = forwordIndex(index)
    return tokens


def openFile():
    """打开文件

    Returns:
        * file 被打开的文件
    """
    if os.path.exists(const.PATH):  # 检查文件是否存在
        # 如果文件存在，则以读写模式打开文件
        file = open(const.PATH, "r+", encoding="utf-8")
    else:
        # 如果文件不存在，则创建一个新文件并以读写模式打开
        file = open(const.PATH, "w+", encoding="utf-8")

    return file


def findData(id):
    """查找特定文件下的id标识

    Args:
        id (string): 每一行的第一个标识符号

    Returns:
        * list 表头内容和每一行第一个字符为id的行，这是一个二维列表
    """
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
