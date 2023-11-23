class Read:
    def __init__(self, path, encodeing='utf-8'):
        self.path = path
        self.encodeing = encodeing
        self.text
        self.ReadFile()

    # 读取待编译的文件
    def ReadFile(self):
        text = ""
        with open(self.path, "r", encoding=self.encodeing) as file:
            while True:
                char = file.read(1)
                if not char:
                    break
                text += char

        self.text = text

    def BuildToken(self):
        pass
