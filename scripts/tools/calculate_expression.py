def calculateExpression(tokens):
    """
    计算一个表达式的值，数字可以是字符串或者是数字
    """
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}
    if (
        len(tokens) == 2 and tokens[0] in ["+", "-"] and tokens[1] not in ["+", "-"]
    ):  # 检查是否为-2, +3这种形式
        if tokens[0] == "+":
            if "." in tokens[1]:
                return float(tokens[1])
            else:
                return int(tokens[1])
        else:
            if "." in tokens[1]:
                return 0 - float(tokens[1])
            else:
                return 0 - int(tokens[1])

    def applyOperator(operators, values):
        operator = operators.pop()  # 弹出一个运算符
        right = values.pop()  # 弹出右操作数
        left = values.pop()  # 弹出左操作数
        # 根据运算符执行相应的运算并将结果压入值堆栈
        if operator == "+":
            values.append(left + right)
        elif operator == "-":
            values.append(left - right)
        elif operator == "*":
            values.append(left * right)
        elif operator == "/":
            if isinstance(left, int) and isinstance(right, int):
                values.append(left // right)
            else:
                values.append(left / right)

    def evaluate(tokens):
        operators = []  # 运算符堆栈
        values = []  # 值堆栈
        for token in tokens:
            if token in precedence:  # 如果是运算符
                while operators and precedence[operators[-1]] >= precedence[token]:
                    # 最后一个运算符的优先级大于当前运算符的优先级
                    # 如果运算符堆栈没有符号那么表达式为False
                    # 也就是只有读取到* 或者 / 才进行运算操作
                    applyOperator(operators, values)  # 执行运算
                operators.append(token)  # 将运算符压入运算符堆栈
            else:  # 如果是数字或小数点则作为操作数压入值堆栈
                if isinstance(token, int) or isinstance(token, float):
                    values.append(token)
                else:
                    if "." in token:
                        values.append(float(token))
                    else:
                        values.append(int(token))
        while operators:  # 执行剩余的运算
            applyOperator(operators, values)
        return values[0]  # 返回最终结果

    return evaluate(tokens)


def findInvalidAri(sequence):
    """
    检查表达式是否合理，合理则返回None，否则返回错误所在位置
    """
    operators = set(["+", "-", "*", "/"])
    last_element = None

    if sequence is None:
        return -1
    if (
        len(sequence) == 2
        and sequence[0] in ["+", "-"]
        and sequence[1] not in ["+", "-"]
    ):  # 检查是否为-2, +3这种形式
        return None

    for idx, element in enumerate(sequence):
        if element not in operators:  # 如果元素是数字
            # 如果前一个元素也是数字，则表达式格式不正确，返回当前位置
            if last_element and last_element not in operators:
                return idx
        elif element in operators:  # 如果元素是运算符
            # 如果前一个元素也是运算符，则表达式格式不正确，返回当前位置
            if last_element and last_element in operators:
                return idx
        else:
            return idx  # 如果元素不是数字或运算符，则表达式格式不正确，返回当前位置

        last_element = element

    # 如果最后一个元素是运算符，则表达式格式不正确，返回最后一个位置
    if last_element in operators:
        return len(sequence) - 1

    return None  # 如果表达式格式正确，则返回 None


def calculateLogicExpression(expression):
    operators = []  # 运算符堆栈
    values = []  # 值堆栈
    valid_values = {"true", "false"}
    valid_operators = {"and", "or"}

    def string_bool(item):
        if item == "true":
            return True
        elif item == "false":
            return False
        else:
            return item

    if len(expression) == 1:
        return string_bool(expression[0])

    def applyOperator(operators, values):
        operator = operators.pop()  # 弹出一个运算符
        right = string_bool(values.pop())  # 弹出右操作数
        left = string_bool(values.pop())  # 弹出左操作数
        # 根据运算符执行相应的运算并将结果压入值堆栈
        if operator == "and":
            values.append(right and left)
        elif operator == "or":
            values.append(left or right)

    for token in expression:
        if token in valid_operators:
            if len(operators) == 1:
                applyOperator(operators, values)
            operators.append(token)
        elif token in valid_values:
            values.append(token)
    applyOperator(operators, values)

    return values[0]


def findInvalidLogic(sequence):
    """
    检查逻辑表达式是否合法，合法则返回 None，否则返回第一个不合法的位置
    """
    valid_values = {"true", "false"}
    valid_operators = {"and", "or"}
    has_operand = False
    if sequence is None:
        return 0

    for idx, token in enumerate(sequence):
        if token in valid_values:
            has_operand = True
        elif token in valid_operators:
            if not has_operand:
                return idx
            has_operand = False
        else:
            return idx

    # 检查最后一个元素是否为操作数
    if not has_operand:
        return len(sequence) - 1

    return None  # 如果表达式格式正确，则返回 None


def calculateCompareExpression(sequence):
    if len(sequence) == 1:
        value = sequence[0]
        if value == "true" or value == "false":
            return value
        elif value != 0:
            return "true"
        else:
            return "false"
    left = sequence[0]
    right = sequence[2]
    compare = sequence[1]
    result = "false"
    if compare == "==":
        result = left == right
    if compare == "!=":
        result = left != right
    if compare == ">=":
        result = left >= right
    if compare == "<=":
        result = left <= right
    if compare == ">":
        result = left > right
    if compare == "<":
        result = left < right
    if result:
        return "true"
    else:
        return "false"


def findInvalidCompare(sequence):
    COMPARE = ["==", "<", ">", "<=", ">=", "!="]
    if len(sequence) == 1:
        value = sequence[0]
        if (
            isinstance(value, int)
            or isinstance(value, float)
            or value == "false" or value == "true"
        ):
            return None
        else:
            return 0
    if len(sequence) != 3:
        return 0
    left = sequence[0]
    right = sequence[2]
    compare = sequence[1]
    if left not in COMPARE and right not in COMPARE and compare in COMPARE:
        return None
    else:
        return 0


"""
tokens = ["2", "+", "4", "+", "3", "*", "5"]
values = [2]
tokens = [+]
token = 4 

values = [2, 4]
tokens = [+]
token = +

token 入栈
values = [2, 4]
tokens = [+, +]

运算符出栈
右操作数出栈
左操作数出栈
values = []
tokens = [+]

计算后的值 6 入栈
values = [6]
tokens = [+]
token = 3

values = [6, 3]
tokens = [+]
token = *

values = [6, 3]
tokens = [+, *]
token = 5

values = [6, 3, 5]
tokens = [+, *]

逐个弹出计算
"""
