from tools import enums


def errorUniversal(char, len_num):
    """出现了一个普遍错误

    Args:
        char (string): 要输出的字符串 \n
        len_num (integer): 错误出现的行

    Returns:
        * None 代表出现错误
    """
    string = char
    string += " The error near the line " + str(len_num) + "."
    print(string)
    return enums.ERROR


def errorUndefine(name, len_num, is_print=True):
    """出现了未定义的错误

    Args:
        name (str): 未定义的名字 \n
        len_num (integer): 错误出现的行 \n
        is_print (bool, optional): 是否打印错误信息. Defaults to True.

    Returns:
        * None 代表出现错误
    """
    if is_print:
        string = name + " have not been statement. "
        string += "The error near the line " + str(len_num) + "."
        print(string)
    return enums.ERROR


def errorUninit(name, len_num, is_print=True):
    """出现了未初始化的错误

    Args:
        name (str): 未初始化的名字 \n
        len_num (integer): 错误出现的行 \n
        is_print (bool, optional): 是否打印错误信息. Defaults to True.

    Returns:
        * None 代表出现错误
    """
    if is_print:
        string = name + " is not initialized. "
        string += "The error near the line " + str(len_num) + "."
        print(string)
    return enums.ERROR


def errorInit(name, len_num, is_print=True):
    """初始化错误

    Args:
        name (str): 初始化错误的名字 \n
        len_num (integer): 错误出现的行 \n
        is_print (bool, optional): 是否打印错误信息. Defaults to True.

    Returns:
        * None 代表出现错误
    """
    if is_print:
        string = name + " had been initialized. "
        string += "The error near the line " + str(len_num) + "."
        print(string)
    return enums.ERROR


def errorUnexpectChar(char, len_num, is_print=True):
    """没有被允许的字符

    Args:
        char (str): 错误字符 \n
        len_num (integer): 错误出现的行 \n
        is_print (bool, optional): 是否打印错误信息. Defaults to True.

    Returns:
        * None 代表出现错误
    """
    if is_print:
        string = "Unexpected char of " + char
        string += ". You should examine your code near "
        string += str(len_num) + "."
        print(string)
    return enums.ERROR


def errorUnexpectType(type_error, type_exp, len_num, is_print=True):
    """不可期待的错误

    Args:
        type_error (string): 错误类型 \n
        type_exp (string): 期待的类型 \n
        len_num (integer): 错误出现的行 \n
        is_print (bool, optional): 是否打印错误信息. Defaults to True.

    Returns:
        * None 代表出现错误
    """
    if is_print:
        string = "Unexpected type. You should use "
        string += type_exp + " as "
        string += "a type of expression. Not "
        string += type_error
        string += ". The error near the line " + str(len_num) + "."
        print(string)
    return enums.ERROR


def errorExpect(char, len_num, is_print=True):
    """出现错误，期待一个字符

    Args:
        char (str): 期待的字符 \n
        len_num (integer): 错误出现的行 \n
        is_print (bool, optional): 是否打印错误信息. Defaults to True.

    Returns:
        * None 代表出现错误
    """
    if is_print:
        string = "Expected " + char
        string += ". You should examine your code near "
        string += str(len_num) + "."
        print(string)
    return enums.ERROR


def errorUnhelpfulStatement(len_num):
    """出现了无用语句

    Args:
        len_num (integer): 错误出现的行

    Returns:
        * None 代表出现错误
    """
    string = (
        "Note that we detect that the script you wrote has an unhelpful statement, "
    )
    string += "and we will skip this code. \nIf there is an error in the skipped code, it will not affect the execution of the code. \n"
    string += ". You should examine your code near "
    string += str(len_num) + "."
    print(string)
    return enums.ERROR
