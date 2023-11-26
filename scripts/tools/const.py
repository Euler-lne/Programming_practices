from tools import token_self

# 表示逻辑表达式
LOGIC = ["==", "and", "or", "<", ">", "<=", ">=", "!="]

#
COMPARE = ["==", "<", ">", "<=", ">=", "!="]


# 表示算数表达式后面可用跟随的符号
ARIEXP = ["==", "and", "or", "<", ">", "<=", ">=", "!=", ",", "."]

# 表示字符串表达式后可跟随的符号
STREXP = [",", "."]

# 表示算数符号
ARI = ["+", "-", "*", "/"]

start_index = 0  # 当前的Token起始下标
end_index = 0  # 当前Token的结束下标的后一位
id = {}  # 用于保存id 以及其对应的值，字典键为变量名字，值为一个类型和变量值
token = token_self.Token()
