from tools import enums


def errorUndefine(name, len_num, is_print=True):
    if is_print:
        string = name + " have not been statement. "
        string += "The error near the line " + str(len_num) + "."
        print(string)
    return enums.ERROR


def errorUninit(name, len_num, is_print=True):
    if is_print:
        string = name + " is not initialized. "
        string += "The error near the line " + str(len_num) + "."
        print(string)
    return enums.ERROR


def errorInit(name, len_num, is_print=True):
    if is_print:
        string = name + " had been initialized. "
        string += "The error near the line " + str(len_num) + "."
        print(string)
    return enums.ERROR


def errorUnexpectChar(char, len_num, is_print=True):
    if is_print:
        string = "Unexpected char of " + char
        string += ". You should examine your code near "
        string += str(len_num) + "."
        print(string)
    return enums.ERROR


def errorUnexpectType(type_error, type_exp, len_num, is_print=True):
    if is_print:
        string = "Unexpected type. You should use "
        string += type_exp + " as "
        string += "a type of expression. Not "
        string += type_error
        string += ". The error near the line " + str(len_num) + "."
        print(string)
    return enums.ERROR


def errorExpect(char, len_num, is_print=True):
    if is_print:
        string = "Expected " + char
        string += ". You should examine your code near "
        string += str(len_num) + "."
        print(string)
    return enums.ERROR
