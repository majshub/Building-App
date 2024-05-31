import tkinter as tk
from tkinter import ttk, messagebox


root = tk.Tk()
root.title('Building App')


def openExpenses():
    top = tk.Toplevel()
    top.title('Expenses Page')

    #creating expenses dropdown list
    expenseLable = tk.Label(top, text='Expense Type').grid(row= 0, column=0, padx=10, pady=10)
    ExpenseTypes = ['Utility', 'Salary', 'Maintenance']
    selectedExpenseType = tk.StringVar()
    selectedExpenseType.set(ExpenseTypes[0])
    expenseTypeList = tk.OptionMenu(top, selectedExpenseType, *ExpenseTypes).grid(row= 0, column=1, columnspan=3, padx=10, pady=10)

    


expensesButton = tk.Button(root, text='Expenses', command=openExpenses).pack(padx=10, pady=10)

tk.mainloop()
