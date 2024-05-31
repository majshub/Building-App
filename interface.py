import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title('Building App')

def openExpenses():
    top = tk.Toplevel()
    top.title('Expenses Page')

    # Creating expenses dropdown list
    expenseLabel = tk.Label(top, text='Expense Type')
    expenseLabel.grid(row=0, column=0, padx=10, pady=10, sticky='W')

    ExpenseTypes = ['Utility', 'Salary', 'Maintenance']
    selectedExpenseType = tk.StringVar()
    selectedExpenseType.set(ExpenseTypes[0])
    expenseTypeList = tk.OptionMenu(top, selectedExpenseType, *ExpenseTypes)
    expenseTypeList.grid(row=0, column=1, padx=10, pady=10, sticky='W')

    # Creating expense entry
    cost_label = tk.Label(top, text='Cost')
    cost_label.grid(row=0, column=2, padx=10, pady=10, sticky='W')

    cost = tk.Entry(top, width=35, borderwidth=3)
    cost.grid(row=0, column=3, columnspan=3, padx=10, pady=10, sticky='W')

    # Creating date frame
    dateFrame = tk.LabelFrame(top, text='Date', padx=10, pady=10)
    dateFrame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='W')

    dayLabel = tk.Label(dateFrame, text='Day')
    dayLabel.grid(row=0, column=0, sticky='W')
    days = [str(d) for d in range(1, 32)]
    day = tk.StringVar()
    dayDropList = tk.OptionMenu(dateFrame, day, *days)
    dayDropList.grid(row=0, column=1, padx=10, pady=10, sticky='W')

    monthLabel = tk.Label(dateFrame, text='Month')
    monthLabel.grid(row=0, column=2, sticky='W')
    months = [str(m) for m in range(1, 13)]
    month = tk.StringVar()
    monthDropList = tk.OptionMenu(dateFrame, month, *months)
    monthDropList.grid(row=0, column=3, padx=10, pady=10, sticky='W')

    yearLabel = tk.Label(dateFrame, text='Year')
    yearLabel.grid(row=0, column=4, sticky='W')
    years = [str(y) for y in range(2010, 2025)]
    year = tk.StringVar()
    yearDropList = tk.OptionMenu(dateFrame, year, *years)
    yearDropList.grid(row=0, column=5, padx=10, pady=10, sticky='W')

    # Creating payment method frame
    payMethodFrame = tk.LabelFrame(top, text='Payment Method', padx=10, pady=10)
    payMethodFrame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky='W')

    selectedPayMethod = tk.StringVar()
    bankButton = tk.Radiobutton(payMethodFrame, text='Bank', variable=selectedPayMethod, value='Bank')
    bankButton.grid(row=0, column=0, padx=10, pady=10, sticky='W')
    cashBoxButton = tk.Radiobutton(payMethodFrame, text='Cash Box', variable=selectedPayMethod, value='Cash Box')
    cashBoxButton.grid(row=0, column=1, padx=10, pady=10, sticky='W')

    # Creating Bank Account frame
    bankAccountFrame = tk.LabelFrame(top, text='Bank Account', padx=10, pady=10)
    bankAccountFrame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky='W')

    # Bank Name dropdown
    bankNameLabel = tk.Label(bankAccountFrame, text='Bank Name')
    bankNameLabel.grid(row=0, column=0, sticky='W')
    bankNames = ['Bank A', 'Bank B', 'Bank C']
    selectedBankName = tk.StringVar()
    selectedBankName.set(bankNames[0])
    bankNameOptionMenu = tk.OptionMenu(bankAccountFrame, selectedBankName, *bankNames)
    bankNameOptionMenu.grid(row=0, column=1, padx=10, pady=10, sticky='W')

    # Account Type dropdown
    accountTypeLabel = tk.Label(bankAccountFrame, text='Account Type')
    accountTypeLabel.grid(row=0, column=2, sticky='W')
    accountTypes = ['Checking', 'Savings', 'Business']
    selectedAccountType = tk.StringVar()
    selectedAccountType.set(accountTypes[0])
    accountTypeOptionMenu = tk.OptionMenu(bankAccountFrame, selectedAccountType, *accountTypes)
    accountTypeOptionMenu.grid(row=0, column=3, padx=10, pady=10, sticky='W')

    # Branch Name dropdown
    branchNameLabel = tk.Label(bankAccountFrame, text='Branch Name')
    branchNameLabel.grid(row=1, column=0, sticky='W')
    branchNames = ['Main Branch', 'Secondary Branch', 'Tertiary Branch']
    selectedBranchName = tk.StringVar()
    selectedBranchName.set(branchNames[0])
    branchNameOptionMenu = tk.OptionMenu(bankAccountFrame, selectedBranchName, *branchNames)
    branchNameOptionMenu.grid(row=1, column=1, padx=10, pady=10, sticky='W')

    # Account Number entry
    accountNumberLabel = tk.Label(bankAccountFrame, text='Account Number')
    accountNumberLabel.grid(row=1, column=2, sticky='W')
    accountNumberEntry = tk.Entry(bankAccountFrame, width=20, borderwidth=3)
    accountNumberEntry.grid(row=1, column=3, padx=10, pady=10, sticky='W')

    def getValues():
        global expense_type, amount, date_paid, payment_method
        expense_type = selectedExpenseType.get()
        amount = cost.get()
        date_paid = f"{year.get()}-{month.get()}-{day.get()}"
        payment_method = selectedPayMethod.get()
        bank_name = selectedBankName.get()
        account_type = selectedAccountType.get()
        branch_name = selectedBranchName.get()
        account_number = accountNumberEntry.get()
        messagebox.showinfo("Info", f"Expense Type: {expense_type}\nCost: {amount}\nDate Paid: {date_paid}\nPayment Method: {payment_method}\nBank Name: {bank_name}\nAccount Type: {account_type}\nBranch Name: {branch_name}\nAccount Number: {account_number}")

    submitButton = tk.Button(top, text="Submit", command=getValues)
    submitButton.grid(row=4, column=0, columnspan=4, pady=10)

expensesButton = tk.Button(root, text='Expenses', command=openExpenses)
expensesButton.pack(padx=10, pady=10)

tk.mainloop()
