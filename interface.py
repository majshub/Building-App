import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

# Database connection details
host = "localhost"  # Your MySQL server hostname
user = "root"  # Your MySQL username
password = "123454321"  # Your MySQL password
database = "sql_building"  # Your MySQL database name


def connect_db():
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print("Successfully connected to the database")
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("You're connected to database:", record)
        return connection
    except pymysql.MySQLError as err:
        messagebox.showerror("Connection Error", f"Error: {err}")
        return None


connection = connect_db()

root = tk.Tk()
root.title('Building App')


def openExpenses():
    def clearFields():
        # Clearing expense type
        selectedExpenseType.set(ExpenseTypes[0])

        # Clearing cost
        cost.delete(0, tk.END)

        # Clearing date fields
        day.set(days[0])
        month.set(months[0])
        year.set(years[0])

        # Clearing payment method
        selectedPayMethod.set('')

        # Clearing bank account fields
        selectedBankName.set(bankNames[0])
        selectedAccountType.set(accountTypes[0])
        selectedBranchName.set(branchNames[0])
        selectedAccountNumber.set(accountNumbers[0])

        # Clearing description
        description.delete('1.0', tk.END)

    def register_info():
        if not connection:
            return
        try:
            expense_type = selectedExpenseType.get()
            amount = float(cost.get())
            date_paid = f"{year.get()}-{month.get()}-{day.get()}"
            withdraw_place = selectedPayMethod.get()
            bank_branch_name = selectedBranchName.get()
            account_number = selectedAccountNumber.get()
            transaction_date = date_paid  # Use the same date as the expense date for bank transactions
            transaction_description = description.get("1.0", tk.END)

            with connection.cursor() as cursor:
                # Insert into Expenses table
                cursor.execute(
                    "INSERT INTO Expenses (expense_type, amount, date_paid, withdraw_place, bank_branch_name, account_number) VALUES (%s, %s, %s, %s, %s, %s)",
                    (expense_type, amount, date_paid, withdraw_place, bank_branch_name, account_number)
                )

                # Insert into corresponding transaction table based on payment method
                if withdraw_place == 'Bank':
                    handle_bank_transaction(cursor, transaction_date, amount, transaction_description, bank_branch_name, account_number)
                elif withdraw_place == 'Cash Box':
                    handle_cashbox_transaction(cursor, transaction_date, amount, transaction_description)

            connection.commit()
            messagebox.showinfo("Success", "Information registered successfully.")
            clearFields()
        except pymysql.MySQLError as err:
            messagebox.showerror("Error", f"Database error: {err}")
        except ValueError as ve:
            messagebox.showerror("Input Error", f"Invalid input: {ve}")

    def handle_bank_transaction(cursor, transaction_date, amount, description, bank_branch_name, account_number):
        # Find the account_id based on bank details
        cursor.execute(
            "SELECT account_id FROM BankAccounts WHERE bank_name = %s AND branch_name = %s AND account_number = %s",
            (selectedBankName.get(), bank_branch_name, account_number)
        )
        account_id = cursor.fetchone()
        if account_id:
            cursor.execute(
                "INSERT INTO BankTransactions (account_id, transaction_date, amount, description, transaction_type) VALUES (%s, %s, %s, %s, %s)",
                (account_id[0], transaction_date, amount, description, 'Withdrawal')
            )
        else:
            messagebox.showerror("Error", "Bank account not found.")

    def handle_cashbox_transaction(cursor, transaction_date, amount, description):
        # Insert into CashBoxTransactions table
        cursor.execute(
            "INSERT INTO CashBoxTransactions (transaction_date, amount, description, transaction_type) VALUES (%s, %s, %s, %s)",
            (transaction_date, amount, description, 'Withdrawal')
        )
        # Update CashBox balance
        cursor.execute(
            "UPDATE CashBox SET balance = balance - %s",
            (amount,)
        )

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
    bankNameDropList = tk.OptionMenu(bankAccountFrame, selectedBankName, *bankNames)
    bankNameDropList.grid(row=0, column=1, padx=10, pady=10, sticky='W')

    # Account Type dropdown
    accountTypeLabel = tk.Label(bankAccountFrame, text='Account Type')
    accountTypeLabel.grid(row=0, column=2, sticky='W')
    accountTypes = ['Checking', 'Savings', 'Business']
    selectedAccountType = tk.StringVar()
    selectedAccountType.set(accountTypes[0])
    accountTypeDropList = tk.OptionMenu(bankAccountFrame, selectedAccountType, *accountTypes)
    accountTypeDropList.grid(row=0, column=3, padx=10, pady=10, sticky='W')

    # Branch Name dropdown
    branchNameLabel = tk.Label(bankAccountFrame, text='Branch Name')
    branchNameLabel.grid(row=1, column=0, sticky='W')
    branchNames = ['Main Branch', 'Secondary Branch', 'Tertiary Branch']
    selectedBranchName = tk.StringVar()
    selectedBranchName.set(branchNames[0])
    branchNameDropList = tk.OptionMenu(bankAccountFrame, selectedBranchName, *branchNames)
    branchNameDropList.grid(row=1, column=1, padx=10, pady=10, sticky='W')

    # Account Number dropdown
    accountNumberLabel = tk.Label(bankAccountFrame, text='Account Number')
    accountNumberLabel.grid(row=1, column=2, sticky='W')
    accountNumbers = ['12345678', '23456789', '34567890']
    selectedAccountNumber = tk.StringVar()
    selectedAccountType.set(accountTypes[0])
    accountNumberDropList = tk.OptionMenu(bankAccountFrame, selectedAccountNumber, *accountNumbers)
    accountNumberDropList.grid(row=1, column=3, padx=10, pady=10, sticky='W')

    # Creating description field
    descriptionLabel = tk.Label(top, text='Description')
    descriptionLabel.grid(row=4, column=0, padx=10, pady=10, sticky='W')
    description = tk.Text(top, height=4, width=50)
    description.grid(row=4, column=1, columnspan=4, padx=10, pady=10, sticky='W')

    # Register button
    registerButton = tk.Button(top, text='Register', command=register_info)
    registerButton.grid(row=5, column=0, padx=10, pady=10, sticky='W')

    # Clear button
    clearButton = tk.Button(top, text='Clear', command=clearFields)
    clearButton.grid(row=5, column=1, padx=10, pady=10, sticky='W')

    # Close button
    closeButton = tk.Button(top, text='Close', command=top.destroy)
    closeButton.grid(row=5, column=2, padx=10, pady=10, sticky='W')


mainLabel = tk.Label(root, text='Building App', font=('Helvetica', 16))
mainLabel.pack(pady=20)

openExpensesButton = tk.Button(root, text='Open Expenses Page', command=openExpenses)
openExpensesButton.pack(pady=20)

closeButton = tk.Button(root, text='Close', command=root.quit)
closeButton.pack(pady=20)

root.mainloop()
