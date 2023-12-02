import compiler.compile as compile


def main():
    """主函数"""
    encoding = input("请输入文件的编码：")
    path = input("请输入文件的路径：")
    compile.Compiler(path=path, encodeing=encoding)
    # compiler.saveToken("../log/token")


if __name__ == "__main__":
    main()
