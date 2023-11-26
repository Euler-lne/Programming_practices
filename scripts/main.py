import compiler.compile as compile


def main():
    compiler = compile.Compiler("./data/6.txt")
    compiler.saveToken("./log/token")


if __name__ == "__main__":
    main()
