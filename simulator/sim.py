import tkinter as tk
import time
from abc import ABC, abstractmethod


class IC(ABC):
    _count = 0  # track how many ICs created

    def __init__(self, pinWidth=4, pinLength=8):
        self.pinWidth = pinWidth
        self.pinLength = pinLength
        self.pinNumber = pinLength * 2
        self.gui_frame = None
        IC._count += 1
        self.id = IC._count
        self.pins = [Pin() for _ in range(self.pinNumber)]

    def show(self, root):
        # Use dynamic sizing
        canvas_width = self.pinWidth * 30
        canvas_height = (self.pinLength + 2) * 30

        self.gui_frame = tk.Frame(root)
        self.gui_frame.pack(padx=10, pady=10)
        frame = self.gui_frame

        # Canvas in center
        canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height, highlightthickness=0)
        canvas.grid(row=0, column=1, rowspan=self.pinLength + 2, columnspan=self.pinWidth)

        # Outline rectangle
        canvas.create_rectangle(2, 2, canvas_width - 2, canvas_height - 2, outline="black", width=2)

        # IC label, rotated
        canvas.create_text(canvas_width // 2, canvas_height // 2, text=self.__class__.__name__,font=("Arial", 10, "bold"), angle=90)

        self.pins = []

        for i in range(self.pinNumber):
            # LEFT SIDE
            if i < self.pinLength:
                row = i + 1
                # Left label right next to canvas
                label_col = 1
                button_col = 0
                label_sticky = "e"
            # RIGHT SIDE
            else:
                row =  self.pinNumber - i
                # Right label right next to canvas
                label_col = self.pinWidth
                button_col = self.pinWidth + 1
                label_sticky = "w"

            # Pin button
            button = tk.Button(frame, text=" ", width=2, height=1)
            button.grid(row=row, column=button_col, padx=2, pady=2)

            # Pin label
            label = tk.Label(frame, text=str(i + 1))
            label.grid(row=row, column=label_col, sticky=label_sticky, padx=2, pady=2)

            self.pins.append((button, label))





    def remove(self):
        if self.gui_frame:
            self.gui_frame.destroy()
            self.gui_frame = None

    @abstractmethod
    def update(self):
        """Override this in subclasses to implement IC logic"""
        pass

class Pin:
    def __init__(self):
        self.output = False

# 7408 - AND
class IC7408(IC):
    count = 0
    def __init__(self):
        super().__init__(pinWidth=4, pinLength=7)
    
    def update(self):
        if self.pins[13].output and not self.pins[6].output:  # VCC = 1, GND = 0
            self.pins[2].output  = self.pins[0].output and self.pins[1].output
            self.pins[5].output  = self.pins[3].output and self.pins[4].output
            self.pins[7].output  = self.pins[8].output and self.pins[9].output
            self.pins[10].output = self.pins[11].output and self.pins[12].output
        else:
            for i in [2,5,7,10]:
                self.pins[i].output = False
    
# 7432 - OR
class IC7432(IC):
    count = 0
    def __init__(self):
        super().__init__(pinWidth=4, pinLength=7)
    
    def update(self):
        if self.pins[13].output and not self.pins[6].output:
            self.pins[2].output  = self.pins[0].output or self.pins[1].output
            self.pins[5].output  = self.pins[3].output or self.pins[4].output
            self.pins[7].output  = self.pins[8].output or self.pins[9].output
            self.pins[10].output = self.pins[11].output or self.pins[12].output
        else:
            for i in [2,5,7,10]:
                self.pins[i].output = False

# 7486 - XOR
class IC7486(IC):
    count = 0
    def __init__(self):
        super().__init__(pinWidth=4, pinLength=7)
    
    def update(self):
        if self.pins[13].output and not self.pins[6].output:
            self.pins[2].output  = self.pins[0].output != self.pins[1].output
            self.pins[5].output  = self.pins[3].output != self.pins[4].output
            self.pins[7].output  = self.pins[8].output != self.pins[9].output
            self.pins[10].output = self.pins[11].output != self.pins[12].output
        else:
            for i in [2,5,7,10]:
                self.pins[i].output = False

# 7406 - NOT (inverter)
class IC7406(IC):
    count = 0
    def __init__(self):
        super().__init__(pinWidth=4, pinLength=7)
    
    def update(self):
        if self.pins[13].output and not self.pins[6].output:
            self.pins[1].output  = not self.pins[0].output
            self.pins[3].output  = not self.pins[2].output
            self.pins[5].output  = not self.pins[4].output
            self.pins[7].output  = not self.pins[8].output
            self.pins[9].output  = not self.pins[10].output
            self.pins[11].output = not self.pins[12].output
        else:
            for i in [1,3,5,7,9,11]:
                self.pins[i].output = False
    
# 7483 - 4-bit adder
class IC7483(IC):
    count = 0
    def __init__(self):
        super().__init__(pinWidth=4, pinLength=8)
    
    def update(self):
        if self.pins[11].output and not self.pins[4].output:  # VCC = pin12, GND = pin5 (adjust if needed)
            a = (self.pins[9].output << 3) | (self.pins[7].output << 2) | (self.pins[2].output << 1) | self.pins[0].output
            b = (self.pins[10].output << 3) | (self.pins[6].output << 2) | (self.pins[3].output << 1) | self.pins[15].output
            carry_in = 1 if self.pins[12].output else 0
            total = a + b + carry_in
            
            self.pins[8].output  = bool((total >> 3) & 1)
            self.pins[5].output  = bool((total >> 2) & 1)
            self.pins[1].output  = bool((total >> 1) & 1)
            self.pins[14].output = bool(total & 1)
            self.pins[13].output = bool(total > 15)
        else:
            for i in [8,5,1,14,13]:
                self.pins[i].output = False
   
class IC74151(IC):
    count = 0
    def __init__(self):
        super().__init__(pinWidth=4, pinLength=8)
    
    def update(self):
        if self.pins[15].output and not self.pins[7].output:  # VCC = pin12, GND = pin5 (adjust if needed)
            index = (self.pins[8].output << 2) | (self.pins[9].output << 1) | self.pins[10].output
            self.pins[5] = self.pins[[3, 2, 1, 0, 14, 13, 12, 11][index]].output
            if self.pins[6].output:
                self.pins[5].output = 0
            self.pins[4].output = not self.pins[5].output
        else:
            for i in [4, 5]:
                self.pins[i].output = False

class IC74244(IC):
    count = 0
    def __init__(self):
        super().__init__(pinWidth=4, pinLength=10)
    
    def update(self):
        for i in [2, 4, 6, 8, 11, 13, 15, 17]:
                self.pins[i].output = False
        if self.pins[19].output and not self.pins[10].output:  # VCC = pin12, GND = pin5 (adjust if needed)
            if not self.pins[0].output:
                self.pins[17].output = self.pins[1].output
                self.pins[15].output = self.pins[3].output
                self.pins[13].output = self.pins[5].output
                self.pins[11].output = self.pins[7].output
            if not self.pins[18].output:
                self.pins[2].output = self.pins[16].output
                self.pins[4].output = self.pins[14].output
                self.pins[6].output = self.pins[12].output
                self.pins[8].output = self.pins[10].output
    
class IC74273(IC):
    count = 0
    def __init__(self):
        super().__init__(pinWidth=4, pinLength=10)
    
    def update(self):
        if self.pins[15].output and not self.pins[7].output:  # VCC = pin12, GND = pin5 (adjust if needed)
            if(not self.pins[0].output):
                for i in [1, 4, 5, 8, 11, 14, 15, 18]:
                    self.pins[i].output = False
            if self.pins[10].output:
                self.pins[1].output = self.pins[2].output
                self.pins[4].output = self.pins[3].output
                self.pins[5].output = self.pins[6].output
                self.pins[8].output = self.pins[7].output
                self.pins[11].output = self.pins[12].output
                self.pins[14].output = self.pins[13].output
                self.pins[15].output = self.pins[16].output
                self.pins[18].output = self.pins[17].output
        else:
            for i in [1, 4, 5, 8, 11, 14, 15, 18]:
                self.pins[i].output = False          
    
class ICHM62256(IC):
    count = 0
    def __init__(self):
        super().__init__(pinWidth=7, pinLength=14)
        self.data = [0 for _ in range(2**15)]
    
    def update(self):
        if self.pins[27].output and not self.pins[13].output and self.pins[19].output:  # VCC = pin12, GND = pin5 (adjust if needed)
            address = (self.pins[0].output << 14) | (self.pins[25].output << 13) | (self.pins[1].output << 12) | (self.pins[22].output << 11) | (self.pins[20].output << 10) | (self.pins[23].output << 9) | (self.pins[24].output << 8) | (self.pins[2].output << 7) | (self.pins[3].output << 6) | (self.pins[4].output << 5) | (self.pins[5].output << 4) | (self.pins[6].output << 3) | (self.pins[7].output << 2) | (self.pins[8].output << 1) | self.pins[9].output
            if not self.pins[26].output:
                data = (self.pins[18].output << 7) | (self.pins[17].output << 6) | (self.pins[16].output << 5) | (self.pins[15].output << 4) | (self.pins[14].output << 3) | (self.pins[12].output << 2) | (self.pins[11].output << 1) | self.pins[10].output
                self.data[address] = data
            if not self.pins[21].output:
                data = self.data[address]
                self.pins[18].output  = bool((data >> 7) & 1)
                self.pins[17].output  = bool((data >> 6) & 1)
                self.pins[16].output  = bool((data >> 5) & 1)
                self.pins[15].output  = bool((data >> 4) & 1)
                self.pins[14].output  = bool((data >> 3) & 1)
                self.pins[12].output  = bool((data >> 2) & 1)
                self.pins[11].output  = bool((data >> 1) & 1)
                self.pins[10].output  = bool(data & 1)
        else:
            for i in [10, 11, 12, 14, 15, 16, 17, 18]:
                self.pins[i].output = False
   
class IC74138(IC):
    count = 0
    def __init__(self):
        super().__init__(pinWidth=4, pinLength=7)
    
    def update(self):
        out = [14, 13, 12, 11, 10, 9, 8, 6]
        for i in out:
                self.pins[i].output = False
        if self.pins[15].output and not self.pins[7].output:  # VCC = pin12, GND = pin5 (adjust if needed)
            index = (self.pins[2].output << 2) | (self.pins[1].output << 1) | self.pins[0].output
            if not self.pins[3].output and not self.pins[4].output and  self.pins[5].output:
                self.pins[out[index]].output = True
    
class IC744040(IC):
    count = 0
    def __init__(self):
        super().__init__(pinWidth=4, pinLength=7)
        self.data = 0
    
    def update(self):
        if self.pins[15].output and not self.pins[7].output:  # VCC = pin12, GND = pin5 (adjust if needed)
            if not self.pins[10].output:
                self.data = self.data + 1 if self.data < 2**12 - 1 else 0
            
            self.pins[0].output  = bool((self.data >> 11) & 1)
            self.pins[14].output  = bool((self.data >> 10) & 1)
            self.pins[13].output  = bool((self.data >> 9) & 1)
            self.pins[11].output  = bool((self.data >> 8) & 1)
            self.pins[12].output  = bool((self.data >> 7) & 1)
            self.pins[3].output  = bool((self.data >> 6) & 1)
            self.pins[1].output  = bool((self.data >> 5) & 1)
            self.pins[2].output  = bool((self.data >> 4) & 1)
            self.pins[4].output  = bool((self.data >> 3) & 1)
            self.pins[5].output  = bool((self.data >> 2) & 1)
            self.pins[6].output  = bool((self.data >> 1) & 1)
            self.pins[8].output  = bool(self.data & 1)
        else:
            for i in [0, 14, 13, 11, 12, 3, 1, 2, 4, 5, 6, 8]:
                self.pins[i].output = False
    
class junction:
    count = 0
    def __init__(self):
        self.ID = junction.count
        junction.count += 1
        self.inputs = []
        self.output = Pin()
    def update(self):
        self.output.output = False
        for i in self.inputs:
            self.output.output = self.output.output | i.output

class circuit:
    def __init__(self):
        self.inputs = []
        self.ICs = []
        self.outputs = []
    def collapse(self):
        for _ in range(10):
            for i in self.ICs:
                i.update


root = tk.Tk(screenName="simulator", baseName="simulator", className="simulator")


root.mainloop()