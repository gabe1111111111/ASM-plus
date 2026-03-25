import tkinter as tk
import time
from abc import ABC, abstractmethod
from tkinter import simpledialog

class IC(ABC):
    _count = 0  # track how many ICs created
    
    def __init__(self, pinWidth=4, pinLength=8):
        self.pinWidth = pinWidth
        self.pinLength = pinLength
        self.pinNumber = pinLength * 2
        self.gui_frame = None
        IC._count += 1
        self.id = IC._count
        self.pins = [Pin(i) for i in range(self.pinNumber)]

    def show(self, root):
        canvas_width = self.pinWidth * 30
        canvas_height = (self.pinLength + 2) * 30

        self.gui_frame = tk.Frame(root)
        frame = self.gui_frame

        # Canvas
        canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height, highlightthickness=0)
        canvas.grid(row=0, column=1, rowspan=self.pinLength + 2, columnspan=self.pinWidth)

        canvas.create_rectangle(2, 2, canvas_width - 2, canvas_height - 2, outline="black", width=2)

        canvas.create_text(
            canvas_width // 2,
            canvas_height // 2,
            text=self.__class__.__name__,
            font=("Arial", 10, "bold"),
            angle=90
        )

        self.pin_vars = []
        self.pin_widgets = []

        for i in range(self.pinNumber):
            pin = self.pins[i]

            # LEFT SIDE
            if i < self.pinLength:
                row = i + 1
                label_col = 1
                input_col = 0
                label_sticky = "e"
            # RIGHT SIDE
            else:
                row = i - self.pinLength + 1
                label_col = self.pinWidth
                input_col = self.pinWidth + 1
                label_sticky = "w"

            # Dropdown variable
            var = tk.StringVar(value="None")

            options = ["None"] + [f.name for f in flags]

            dropdown = tk.OptionMenu(frame, var, *options)
            dropdown.config(width=5)
            dropdown.grid(row=row, column=input_col, padx=2, pady=2)

            # 🔥 Handle selection
            def on_select(v=var, p=pin):
                name = v.get()

                # Find existing flag connected to this pin
                old_flag = next((f for f in flags if f.input == p or f.output == p), None)

                # Disconnect old flag
                if old_flag:
                    if old_flag.input == p:
                        old_flag.input = None
                    if old_flag.output == p:
                        old_flag.output = None

                if name == "None":
                    return

                # Connect new flag
                f = next((f for f in flags if f.name == name), None)
                if f:
                    if p.index in self.__class__.inputs:
                        f.input = p
                    else:
                        f.output = p
                        
            var.trace_add("write", lambda *args, v=var, func=on_select: func())

            # Register for global refresh
            all_flag_menus.append((dropdown, var, pin, self))

            # Label
            label = tk.Label(frame, text=str(i + 1))
            label.grid(row=row, column=label_col, sticky=label_sticky, padx=2, pady=2)

            self.pin_vars.append(var)
            self.pin_widgets.append(dropdown)





    def remove(self):
        if self.gui_frame:
            self.gui_frame.destroy()
            self.gui_frame = None

    @abstractmethod
    def update(self):
        """Override this in subclasses to implement IC logic"""
        pass

class Pin:
    def __init__(self, index):
        self.output = False
        self.index = index

# 7408 - AND
class IC7408(IC):
    count = 0
    inputs = [0, 1, 3, 4, 6, 8, 9, 11, 12, 13]
    outputs=[2,5,7,10]
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
    inputs = [0, 1, 3, 4, 6, 8, 9, 11, 12, 13]
    outputs=[2,5,7,10]
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
    inputs = [0, 1, 3, 4, 6, 8, 9, 11, 12, 13]
    outputs=[2,5,7,10]
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
    inputs = [0, 2, 4, 6, 8, 10, 12, 13]
    outputs=[1,3,5,7,9,11]
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
    inputs = [0, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 15]
    outputs = [8,5,1,14,13]
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
    inputs = [1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    outputs = [4, 5]
    
    def __init__(self):
        super().__init__(pinWidth=4, pinLength=8)
    
    def update(self):
        if self.pins[15].output and not self.pins[7].output:  # VCC = pin12, GND = pin5 (adjust if needed)
            index = (self.pins[8].output << 2) | (self.pins[9].output << 1) | self.pins[10].output
            self.pins[5].output = self.pins[[3, 2, 1, 0, 14, 13, 12, 11][index]].output
            if self.pins[6].output:
                self.pins[5].output = 0
            self.pins[4].output = not self.pins[5].output
        else:
            for i in [4, 5]:
                self.pins[i].output = False

class IC74244(IC):
    count = 0
    inputs = [0, 1, 3, 5, 7, 9, 10, 12, 14, 16, 18, 19]
    outputs = [2, 4, 6, 8, 11, 13, 15, 17]
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
    inputs = [0, 2, 3, 6, 7, 9, 10, 12, 13, 16, 17, 19]
    outputs = [1, 4, 5, 8, 11, 14, 15, 18]
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
    inputs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 19, 20, 21, 22, 23, 24, 25, 26, 27]
    outputs = [10, 11, 12, 14, 15, 16, 17, 18]
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
    inputs = [0, 1, 2, 3, 4, 5, 7, 15]
    outputs = [14, 13, 12, 11, 10, 9, 8, 6]
    def __init__(self):
        super().__init__(pinWidth=4, pinLength=8)
    
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
    inputs = [7, 8, 10, 15]
    outputs = [0, 14, 13, 11, 12, 3, 1, 2, 4, 5, 6, 8]
    def __init__(self):
        super().__init__(pinWidth=4, pinLength=8)
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
    
from tkinter import simpledialog

class junction:
    count = 0

    def __init__(self):
        self.ID = junction.count
        junction.count += 1
        self.inputs = [Pin(i) for i in range(1)]
        self.output = Pin(0)
        self.gui_frame = None

    def update(self):
        self.output.output = False
        for i in self.inputs:
            self.output.output |= i.output

    def show(self, root, x=0, y=0):
        self.parent = root

        self.gui_frame = tk.Frame(root)
        frame = self.gui_frame

        height = len(self.inputs) * 30
        width = 60

        canvas = tk.Canvas(frame, width=width, height=height, highlightthickness=0)
        canvas.grid(row=0, column=1, rowspan=len(self.inputs))

        # vertical line
        canvas.create_line(width//2, 5, width//2, height-5, width=2)

        self.input_vars = []
        self.input_widgets = []

        # INPUTS (left side)
        for i in range(len(self.inputs)):
            pin = self.inputs[i]

            var = tk.StringVar(value="None")
            options = ["None"] + [f.name for f in flags]

            dropdown = tk.OptionMenu(frame, var, *options)
            dropdown.config(width=5)
            dropdown.grid(row=i, column=0, padx=2, pady=2)

            # connect logic
            def on_select(v=var, p=pin):
                name = v.get()

                # Disconnect old
                old_flag = next((f for f in flags if f.output == p), None)
                if old_flag:
                    old_flag.output = None

                if name == "None":
                    return

                f = next((f for f in flags if f.name == name), None)
                if f:
                    f.output = p

            var.trace_add("write", lambda *args, v=var, func=on_select: func())

            all_flag_menus.append((dropdown, var, pin, self))

            self.input_vars.append(var)
            self.input_widgets.append(dropdown)

        # OUTPUT (centered)
        out_row = (len(self.inputs) - 1) // 2
        out_pin = self.output

        out_var = tk.StringVar(value="None")
        options = ["None"] + [f.name for f in flags]

        out_dropdown = tk.OptionMenu(frame, out_var, *options)
        out_dropdown.config(width=5)
        out_dropdown.grid(row=out_row, column=2, padx=2)

        def on_output_select(v=out_var, p=out_pin):
            name = v.get()

            old_flag = next((f for f in flags if f.input == p), None)
            if old_flag:
                old_flag.input = None

            if name == "None":
                return

            f = next((f for f in flags if f.name == name), None)
            if f:
                f.input = p
                
        out_var.trace_add("write", lambda *args, v=out_var, func=on_output_select: func())

        all_flag_menus.append((out_dropdown, out_var, out_pin, self))

        # right click config
        frame.bind("<Button-3>", self.configure_inputs)
        canvas.bind("<Button-3>", self.configure_inputs)

        self.gui_frame.place(x=x, y=y)
    def configure_inputs(self, event):
        new_val = simpledialog.askinteger("Inputs","Number of inputs:",initialvalue=len(self.inputs))

        if new_val and new_val > 0:
            # ✅ update inputs list properly
            self.inputs = [Pin(i) for i in range(new_val)]

            # save position BEFORE destroy
            x = self.gui_frame.winfo_x()
            y = self.gui_frame.winfo_y()

            self.gui_frame.destroy()

            # redraw at same position
            self.show(self.parent, x, y)

class flag:
    def __init__(self, name="Unnamed flag"):
        self.input = None
        self.output = None
        self.name = name
    def update(self):
        if self.input and self.output:
            self.output.output = self.input.output
            
class circuit:
    def __init__(self):
        self.inputs = []
        self.ICs = []
        self.outputs = []
    def collapse(self):
        for _ in range(10):
            for f in flags:
                f.update()
            for i in self.ICs:
                i.update()



root = tk.Tk()
root.title("Simulator")

placing_ic = None  # stores class, not instance
flags = []
all_flag_menus = []
c = circuit()

workspace = tk.Canvas(root, bg="white", width=800, height=600)
workspace.pack(fill="both", expand=True)

# Create menu bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# -------- File Menu --------
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="New", command=lambda: print("New"))
file_menu.add_command(label="Open", command=lambda: print("Open"))
file_menu.add_command(label="Save", command=lambda: print("Save"))
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# -------- Add Menu --------
add_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Add", menu=add_menu)

def start_placing(ic_class):
    global placing_ic
    placing_ic = ic_class

def refresh_flag_menus():
    options = ["None"] + [f.name for f in flags]

    for dropdown, var, pin, ic in all_flag_menus:
        menu = dropdown["menu"]
        menu.delete(0, "end")

        for name in options:
            menu.add_command(
                label=name,
                command=lambda v=var, n=name: v.set(n)
            )

add_menu.add_command(label="7408 AND", command=lambda: start_placing(IC7408))
add_menu.add_command(label="7432 OR", command=lambda: start_placing(IC7432))
add_menu.add_command(label="7486 XOR", command=lambda: start_placing(IC7486))
add_menu.add_command(label="7406 NOT", command=lambda: start_placing(IC7406))
add_menu.add_command(label="7483 ADDER", command=lambda: start_placing(IC7483))
add_menu.add_command(label="74151 8 TO 1 selector", command=lambda: start_placing(IC74151))
add_menu.add_command(label="74244 tri-state buffer", command=lambda: start_placing(IC74244))
add_menu.add_command(label="74273 8 bit register", command=lambda: start_placing(IC74273))
add_menu.add_command(label="HM62256 RAM", command=lambda: start_placing(ICHM62256))
add_menu.add_command(label="74138 3 to 8 decoder", command=lambda: start_placing(IC74138))
add_menu.add_command(label="744040 counter", command=lambda: start_placing(IC744040))

menubar.add_command(label="Junction", command=lambda: start_placing(junction))

def createFlag():
    global flags
    name = simpledialog.askstring("Flag", "Enter flag name:", initialvalue="Unnamed flag")
    
    
    if not name:
        return

    if any(f.name == name for f in flags):
        print("Flag already exists")
        return

    flags.append(flag(name))
    refresh_flag_menus()

menubar.add_command(label="create flag", command=lambda: createFlag())

def on_canvas_click(event):
    global placing_ic

    if placing_ic is None:
        return

    ic = placing_ic()
    c.ICs.append(ic)

    # Create a frame at mouse position
    ic.show(workspace)

    # Move the IC to mouse position
    ic.gui_frame.update_idletasks()

    w = ic.gui_frame.winfo_width()
    h = ic.gui_frame.winfo_height()

    ic.gui_frame.place(x=event.x - w//2, y=event.y - h//2)

    placing_ic = None  # exit placement mode

workspace.bind("<Button-1>", on_canvas_click)









root.mainloop()