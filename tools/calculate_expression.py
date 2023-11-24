def calculate_expression(tokens):
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}

    def apply_operator(operators, values):
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
                    apply_operator(operators, values)  # 执行运算
                operators.append(token)  # 将运算符压入运算符堆栈
            else:  # 如果是数字或小数点则作为操作数压入值堆栈
                if "." in token:
                    values.append(float(token))
                else:
                    values.append(int(token))
        while operators:  # 执行剩余的运算
            apply_operator(operators, values)
        return values[0]  # 返回最终结果

    return evaluate(tokens)


def find_invalid_position(sequence):
    """
    检查表达式是否合理，合理则返回None，否则返回错误所在位置
    """
    operators = set(["+", "-", "*", "/"])
    last_element = None

    for idx, element in enumerate(sequence):
        if element.isdigit():  # 如果元素是数字
            # 如果前一个元素也是数字，则表达式格式不正确，返回当前位置
            if last_element and last_element.isdigit():
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
