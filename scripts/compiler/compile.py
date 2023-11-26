from compiler import read
from block import run_block as B
from block import normal_block as Bnormal
from tools import enums
from tools.calculate_expression import *
from tools import const
from tools.error import *


const.start_index = 0  # 当前的Token起始下标
const.end_index = 0  # 当前Token的结束下标的后一位
const.id = {}  # 用于保存const.id 以及其对应的值，字典键为变量名字，值为一个类型和变量值


class Compiler(read.Read):
    """
    用于词法分析，解析目标代码
    主要有4个状态：普通语句，IF语句，WHILE语句，SWITCH语句，这四个状态通过readBlock返回得知
    其中普通语句又有：赋值语句，声明语句，print语句，
    """

    def __init__(self, path, encodeing="utf-8"):
        super().__init__(path, encodeing)
        self.state = enums.NONE  # 当前的语句状态
        self.start()

    def start(self):
        while True:
            self.state = self.readBlock()
            # 进行可能的错误检测
            if self.state == enums.END:
                # 结束的时候还有可能有字符，这可能是应为忘记写。或者！导致分块没有成功
                if const.start_index != const.end_index:
                    return errorExpect(". or !", self.len_num)
                return enums.END
            elif self.state == enums.ERROR:
                return enums.ERROR
            # 错误检测结束进行语法分析
            const.end_index = const.token.getLen()
            val = None
            if self.state == enums.ACCEPT:  # 普通代码以句号结束的
                val = Bnormal.normalBlock(self.len_num)
            elif self.state == enums.IF:  # if代码块
                val = B.ifBlock(self.len_num, const.end_index)
            elif self.state == enums.SWITCH:  # switch 代码块
                val = B.switchBlock(self.len_num, const.end_index)
            elif self.state == enums.WHILE:  # while 代码块
                val = B.whileBlock(self.len_num, const.end_index)
            if val is None:
                return enums.NONE

            const.start_index = const.token.len  # 准备读取下一个代码块
