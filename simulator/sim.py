class pin:
    def __init__(self):
        self.output = False
class IC7408:
    def __init__(self):
        self.pins = [pin, pin, pin, pin, pin, pin, pin, pin, pin, pin, pin, pin, pin, pin]
    def update(self):
        if(self.pins[6].output == False and self.pins[13] == 1):
            self.pins[2] = self.pins[1] and self.pins[0]
            self.pins[5] = self.pins[4] and self.pins[3]
            self.pins[7] = self.pins[8] and self.pins[9]
            self.pins[10] = self.pins[11] and self.pins[12]
        else:
            self.pins[2] = self.pins[5] = self.pins[7] = self.pins[10] = False
class IC7432:
    def __init__(self):
        self.pins = [pin, pin, pin, pin, pin, pin, pin, pin, pin, pin, pin, pin, pin, pin]
    def update(self):
        if(self.pins[6].output == False and self.pins[13] == 1):
            self.pins[2] = self.pins[1] or self.pins[0]
            self.pins[5] = self.pins[4] or self.pins[3]
            self.pins[7] = self.pins[8] or self.pins[9]
            self.pins[10] = self.pins[11] or self.pins[12]
        else:
            self.pins[2] = self.pins[5] = self.pins[7] = self.pins[10] = False
class IC7486:
    def __init__(self):
        self.pins = [pin, pin, pin, pin, pin, pin, pin, pin, pin, pin, pin, pin, pin, pin]
    def update(self):
        if(self.pins[6].output == False and self.pins[13] == 1):
            self.pins[2] = self.pins[1] == self.pins[0]
            self.pins[5] = self.pins[4] == self.pins[3]
            self.pins[7] = self.pins[8] == self.pins[9]
            self.pins[10] = self.pins[11] == self.pins[12]
        else:
            self.pins[2] = self.pins[5] = self.pins[7] = self.pins[10] = False
class IC7406:
    def __init__(self):
        self.pins = [pin, pin, pin, pin, pin, pin, pin, pin, pin, pin, pin, pin, pin, pin]
    def update(self):
        if(self.pins[6].output == False and self.pins[13] == 1):
            self.pins[1] = not self.pins[0]
            self.pins[3] = not self.pins[2]
            self.pins[5] = not self.pins[4]
            self.pins[7] = not self.pins[8]
            self.pins[9] = not self.pins[10]
            self.pins[11] = not self.pins[12]
        else:
            self.pins[2] = self.pins[5] = self.pins[7] = self.pins[10] = False

class memoryIC:
    pass