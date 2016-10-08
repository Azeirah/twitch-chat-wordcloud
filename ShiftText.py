class ShiftText():
    def __init__(self, maxLength):
        self.buffer = ""
        self.maxLength = maxLength

    def push(self, text):
        lenDiff = (len(text) + len(self.buffer)) - self.maxLength
        if lenDiff > 0:
            self.buffer = self.buffer[:-lenDiff]

        self.buffer = text + self.buffer

    def __repr__(self):
        return self.buffer

    def __len__(self):
        return len(self.buffer)

# bla = ShiftText(10)
# bla.push('abc') # abc
# print(bla)
# bla.push('123') # 123abc
# print(bla)
# bla.push('def') # def123abc
# print(bla)
# bla.push('456') # 456def123a
# print(bla)

