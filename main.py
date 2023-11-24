import tools.compile as compile
import time



def main():
    start = time.time()
    compiler = compile.Compiler("./scripts/1.txt")
    compiler.saveToken()
    end = time.time()
    print(end - start)


if __name__ == "__main__":
    main()
