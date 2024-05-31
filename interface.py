import tkinter as tk
from tkinter import ttk, messagebox


root = tk.Tk()
root.title('Building App')


def openExpenses():
    top = tk.Toplevel()
    top.title('Expenses Page')

    


expensesButton = tk.Button(root, text='Expenses', command=openExpenses).pack(padx=10, pady=10)

tk.mainloop()
