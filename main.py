from tools import read


def main():
    reader = read.Read("./scripts/1.txt")
    for i in reader.token.token:
        print(i)


if __name__ == "__main__":
    main()
