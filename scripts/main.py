import compiler.compile as compile


def main():
    compiler = compile.Compiler("./data/5.txt")
    compiler.saveToken()


if __name__ == "__main__":
    main()
