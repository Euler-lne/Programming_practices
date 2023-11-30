import compiler.compile as compile


def main():
    """_summary_ 主函数
    """
    encoding = input("请输入文件的编码：")
    compiler = compile.Compiler("./data/商场客服机器人.txt",encodeing=encoding)
    compiler.saveToken("./log/token")


if __name__ == "__main__":
    main()
