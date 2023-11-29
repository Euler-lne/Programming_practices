import compiler.compile as compile


def main():
    compiler = compile.Compiler("./data/商场客服机器人.txt")
    compiler.saveToken("./log/token")


if __name__ == "__main__":
    main()
