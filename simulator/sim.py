class transistor:
    def __init__(self):
        self.base = None
        self.emitter = None
        self.collector = None
        self.Vbe = 0
        self.saturationVoltage = 0
        self.outputVoltage = 0
    def update(self):
        Vb = self.base.outputVoltage
        Vc = self.collector.outputVoltage
        if Vb >= self.saturationVoltage:
            self.outputVoltage = Vc
        elif self.base < self.Vbe:
            self.outputVoltage = 0
        else:
            self.outputVoltage = Vb-self.Vbe


class input:
    def __init__(self):
        self.output = None
        self.outputVoltage = 0
class delay:
    def __init__(self):
        self.input = None
        self.outputVoltage = 0
class junction:
    def __inti__(self):
        self.input = None
        self.output = []
        self.outputVoltage = 0
class circuit:
    def __init__(self):
        self.inputs = []
        self.outputs = []