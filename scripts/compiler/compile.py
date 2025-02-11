from compiler import read
from block import run_block as B
from block import normal_block as Bnormal
from tools import enums
from tools.calculate_expression import *
from tools import const
from tools.error import *


class Compiler(read.Read):
    """用于词法分析，解析目标代码，采用扫描一遍的形式

    Args:
        read (class): 用于词法分析
    """

    def __init__(self, path, encodeing="utf-8"):
        """类初始化

        Args:
            path (string): 文件路径
            encodeing (str, optional): 编码. Defaults to "utf-8".
        """
        super().__init__(path, encodeing)
        self.state = enums.NONE  # 当前的语句状态
        self.start()

    def start(self):
        """执行编译器

        Returns:
            * None 代表检测到错误
            * 10 代表执行结束
        """
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
                return enums.ERROR

            const.start_index = const.token.len  # 准备读取下一个代码块
