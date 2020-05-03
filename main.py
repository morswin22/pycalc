import tkinter as tk

class Calculator(tk.Frame):
  def __init__(self, master=None):
    super().__init__(master)
    self.master = master
    self.pack()
    self.current_operation = None
    self.current_value = "0"
    self.memorized_value = None
    self.ops = {
      "+": Calculator.add, 
      "-": Calculator.subtract, 
      "*": Calculator.multiply, 
      "/": Calculator.divide
    }
    self.create_widgets()

  def create_widgets(self):
    self.output_frame = tk.LabelFrame(self, text="Wynik", padx=5, pady=5)

    self.output_long = tk.Label(self.output_frame, text="")
    self.output_long.pack()
    self.output_short = tk.Label(self.output_frame, text=self.current_value)
    self.output_short.pack()

    self.output_frame.pack()

    self.inputs_frame = tk.LabelFrame(self, text="Wprowadzanie", padx=5, pady=5)

    self.numbers = [
      {"row": 4, "column": 0, "columnspan": 2}, 
      {"row": 3, "column": 0}, 
      {"row": 3, "column": 1},
      {"row": 3, "column": 2}, 
      {"row": 2, "column": 0}, 
      {"row": 2, "column": 1},
      {"row": 2, "column": 2}, 
      {"row": 1, "column": 0}, 
      {"row": 1, "column": 1},
      {"row": 1, "column": 2}
    ]
    for i in range(10):
      number = tk.Button(self.inputs_frame, text=i, command=(lambda num: lambda: self.input(num))(str(i)))
      number.grid(**self.numbers[i])
      self.numbers[i] = number

    self.operations = {
      "CE": {"row": 0, "column": 0},
      "C": {"row": 0, "column": 1},
      "+": {"row": 2, "column": 3},
      "-": {"row": 1, "column": 3},
      "*": {"row": 0, "column": 2},
      "/": {"row": 0, "column": 3},
      "=": {"row": 3, "column": 3, "rowspan": 2},
      ",": {"row": 4, "column": 2}
    }
    for operation in self.operations:
      button = tk.Button(self.inputs_frame, text=operation, command=(lambda op: lambda: self.operation(op))(operation))
      button.grid(**self.operations[operation])
      self.operations[operation] = button

    self.inputs_frame.pack()

  def input(self, number):
    new = (self.current_value + number).split(',')
    start = 0
    for i in range(len(new[0])):
      if new[0][i] != "0":
        start = i
        break
    if len(new) == 2:
      self.current_value = ','.join([new[0][start:], new[1]])
    else:
      self.current_value = new[0][start:]
    self.output_short['text'] = self.current_value

  def operation(self, op):
    if op == 'CE':
      self.current_value = self.current_value[:-1]
      if self.current_value == "":
        self.current_value = "0"
      self.output_short['text'] = self.current_value 
    elif op == 'C':
      self.current_operation = None
      self.current_value = "0"
      self.memorized_value = None
      self.output_long['text'] = "" 
      self.output_short['text'] = self.current_value 
    elif op == ',':
      parts = self.current_value.split(',')
      if len(parts) == 1:
        self.current_value += ','
        self.output_short['text'] = self.current_value 
    elif op == '+' or op == '-' or op == '*' or op == '/':
      if self.memorized_value != None:
        self.memorized_value = self.current_operation(self.memorized_value, self.current_value)
      else:
        self.memorized_value = self.current_value
      self.current_operation = self.ops[op]
      self.current_value = "0"
      self.output_long['text'] = self.memorized_value + ' ' + op
      self.output_short['text'] = self.current_value
    elif op == '=':
      self.current_value = self.current_operation(self.memorized_value, self.current_value)
      self.current_operation = None
      self.memorized_value = None
      self.output_long['text'] = ""
      self.output_short['text'] = self.current_value

  def number(x):
    return float(x.replace(',','.'))

  def string(x):
    new = str(x).split('.')
    start = 0
    for i in range(len(new[0])):
      if new[0][i] != "0":
        start = i
        break
    if new[1] != "0":
      return ','.join([new[0][start:], new[1]])
    else:
      return new[0][start:]

  def add(a, b):
    return Calculator.string(Calculator.number(a) + Calculator.number(b))

  def subtract(a, b):
    return Calculator.string(Calculator.number(a) - Calculator.number(b))

  def multiply(a, b):
    return Calculator.string(Calculator.number(a) * Calculator.number(b))

  def divide(a, b):
    return Calculator.string(Calculator.number(a) / Calculator.number(b))

root = tk.Tk()
app = Calculator(master=root)
app.mainloop()