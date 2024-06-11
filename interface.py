import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from contextlib import contextmanager
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

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
        update_bank_fields_state()

    def update_bank_fields_state():
        if selectedPayMethod.get() == 'Bank':
            bankNameDropList.config(state='normal')
            accountTypeDropList.config(state='normal')
            branchNameDropList.config(state='normal')
            accountNumberDropList.config(state='normal')
        else:
            bankNameDropList.config(state='disabled')
            accountTypeDropList.config(state='disabled')
            branchNameDropList.config(state='disabled')
            accountNumberDropList.config(state='disabled')

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
                # Check and handle transaction based on payment method before inserting into Expenses table
                if withdraw_place == 'Bank':
                    if not handle_bank_transaction(cursor, transaction_date, amount, transaction_description, bank_branch_name, account_number):
                        return
                elif withdraw_place == 'Cash Box':
                    if not handle_cashbox_transaction(cursor, transaction_date, amount, transaction_description):
                        return

                # Insert into Expenses table
                cursor.execute(
                    "INSERT INTO Expenses (expense_type, amount, date_paid, withdraw_place, bank_branch_name, account_number) VALUES (%s, %s, %s, %s, %s, %s)",
                    (expense_type, amount, date_paid, withdraw_place, bank_branch_name, account_number)
                )

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
            "SELECT account_id, balance FROM BankAccounts WHERE bank_name = %s AND branch_name = %s AND account_number = %s",
            (selectedBankName.get(), bank_branch_name, account_number)
        )
        account = cursor.fetchone()
        if account:
            account_id, balance = account
            if balance < amount:
                messagebox.showerror("Error", "Insufficient balance.")
                return False
            # Insert into BankTransactions table
            cursor.execute(
                "INSERT INTO BankTransactions (account_id, transaction_date, amount, description, transaction_type) VALUES (%s, %s, %s, %s, %s)",
                (account_id, transaction_date, amount, description, 'Withdrawal')
            )
            # Update BankAccounts balance
            cursor.execute(
                "UPDATE BankAccounts SET balance = balance - %s WHERE account_id = %s",
                (amount, account_id)
            )
            return True
        else:
            messagebox.showerror("Error", "Bank account not found.")
            return False

    def handle_cashbox_transaction(cursor, transaction_date, amount, description):
        # Fetch the current balance from the CashBox table
        cursor.execute("SELECT balance FROM CashBox")
        cashbox_balance = cursor.fetchone()
        if cashbox_balance:
            current_balance = cashbox_balance[0]
            if current_balance < amount:
                messagebox.showerror("Error", "Insufficient balance in Cash Box.")
                return False
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
            return True
        else:
            messagebox.showerror("Error", "Cash Box balance not found.")
            return False

    def delete_info():
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
                # Check and handle transaction based on payment method before deleting from Expenses table
                if withdraw_place == 'Bank':
                    if not handle_bank_transaction_delete(cursor, transaction_date, amount, transaction_description,
                                                          bank_branch_name, account_number):
                        return
                elif withdraw_place == 'Cash Box':
                    if not handle_cashbox_transaction_delete(cursor, transaction_date, amount, transaction_description):
                        return

                # Delete from Expenses table
                cursor.execute(
                    "DELETE FROM Expenses WHERE expense_type = %s AND amount = %s AND date_paid = %s AND withdraw_place = %s AND bank_branch_name = %s AND account_number = %s",
                    (expense_type, amount, date_paid, withdraw_place, bank_branch_name, account_number)
                )

            connection.commit()
            messagebox.showinfo("Success", "Information deleted successfully.")
            clearFields()
        except pymysql.MySQLError as err:
            messagebox.showerror("Error", f"Database error: {err}")
        except ValueError as ve:
            messagebox.showerror("Input Error", f"Invalid input: {ve}")

    def handle_bank_transaction_delete(cursor, transaction_date, amount, description, bank_branch_name, account_number):
        # Find the account_id based on bank details
        cursor.execute(
            "SELECT account_id, balance FROM BankAccounts WHERE bank_name = %s AND branch_name = %s AND account_number = %s",
            (selectedBankName.get(), bank_branch_name, account_number)
        )
        account = cursor.fetchone()
        if account:
            account_id, balance = account
            # Delete from BankTransactions table
            cursor.execute(
                "DELETE FROM BankTransactions WHERE transaction_date = %s AND amount = %s AND description = %s",
                (transaction_date, amount, description)
            )
            # Update BankAccounts balance
            cursor.execute(
                "UPDATE BankAccounts SET balance = balance + %s WHERE account_id = %s",
                (amount, account_id)
            )
            return True
        else:
            messagebox.showerror("Error", "Bank account not found.")
            return False

    def handle_cashbox_transaction_delete(cursor, transaction_date, amount, description):
        # Fetch the current balance from the CashBox table
        cursor.execute("SELECT balance FROM CashBox")
        cashbox_balance = cursor.fetchone()
        if cashbox_balance:
            # Delete from CashBoxTransactions table
            cursor.execute(
                "DELETE FROM CashBoxTransactions WHERE transaction_date = %s AND amount = %s AND description = %s",
                (transaction_date, amount, description)
            )
            # Update CashBox balance
            cursor.execute(
                "UPDATE CashBox SET balance = balance + %s",
                (amount,)
            )
            return True
        else:
            messagebox.showerror("Error", "Cash Box balance not found.")
            return False

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
    selectedPayMethod.trace('w', lambda *args: update_bank_fields_state())
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

    # Delete button
    deleteButton = tk.Button(top, text='Delete', command=delete_info)
    deleteButton.grid(row=5, column=3, padx=10, pady=10, sticky='W')

    # Clear button
    clearButton = tk.Button(top, text='Clear', command=clearFields)
    clearButton.grid(row=5, column=1, padx=10, pady=10, sticky='W')

    # Close button
    closeButton = tk.Button(top, text='Close', command=top.destroy)
    closeButton.grid(row=5, column=2, padx=10, pady=10, sticky='W')

    update_bank_fields_state()


def openInsurance():
    insurancePage = tk.Toplevel()
    insurancePage.title('Insurance Page')

    endingInsuranceFrame = tk.LabelFrame(insurancePage, text="Ending Insurance", padx=20, pady=20, font=('Helvetica'))
    endingInsuranceFrame.grid(row=0, column=0, padx=20, pady=20)

    # Query to fetch insurances expiring in two months
    query = f"""
    SELECT insurance_type, end_date FROM Insurance
    WHERE end_date <= DATE_ADD(CURDATE(), INTERVAL 2 MONTH)
    """

    try:
        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(query)

            # Fetch all results
            results = cursor.fetchall()

            if results:
                # Display insurances expiring within two months on the Insurance Page
                for index, row in enumerate(results, start=1):
                    insurance_type, end_date = row
                    tk.Label(endingInsuranceFrame, text=f"{insurance_type} Insurance is going to expire on {end_date}").pack(padx=10, pady=10)
            else:
                messagebox.showinfo("No Insurances", "No Insurances are about to expire")
    except pymysql.MySQLError as err:
        messagebox.showerror("Error", f"Database error: {err}")
    finally:
        # Close the connection
        connection.close()

def openContracts():
    contractsPage = tk.Toplevel()
    contractsPage.title("Contracts Page")

    endingContractsFrame = tk.LabelFrame(contractsPage, text="Ending Contracts", padx=20, pady=20, font=("Helvetica"))
    endingContractsFrame.grid(row=0, column=0, padx=20, pady=20)


    # Query to fetch insurances expiring in two months
    query = f"""
       SELECT company_name, end_date FROM contractors
       WHERE end_date <= DATE_ADD(CURDATE(), INTERVAL 2 MONTH)
       """

    try:
        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(query)

            # Fetch all results
            results = cursor.fetchall()

            if results:
                # Display insurances expiring within two months on the Insurance Page
                for index, row in enumerate(results, start=1):
                    company_name, end_date = row
                    tk.Label(endingContractsFrame, text=f"{company_name} contract is going to end on {end_date}").pack(padx=10, pady=10)
            else:
                messagebox.showinfo("No Contracts", "No Contracts are about to expire")
    except pymysql.MySQLError as err:
        messagebox.showerror("Error", f"Database error: {err}")
    finally:
        # Close the connection
        connection.close()


def openExpenseAnalysis():
    cursor = connection.cursor()

    with connection:
        if not connection:
            return


        query = """
        SELECT DATE_FORMAT(date_paid, '%Y-%m') AS month, SUM(amount) AS total_expense
        FROM Expenses
        GROUP BY month
        ORDER BY month
        """
        cursor.execute(query)
        result = cursor.fetchall()

        df = pd.DataFrame(result, columns=['Month', 'Total_Expense'])
        df['Month'] = pd.to_datetime(df['Month'])

        fig, ax = plt.subplots()
        ax.plot(df['Month'], df['Total_Expense'], marker='o', linestyle='-')

        ax.set_title('Monthly Expenses')
        ax.set_xlabel('Time')
        ax.set_ylabel('Expenses ($)')
        ax.grid(True)

        analysis_window = tk.Toplevel(root)
        analysis_window.title('Expense Analysis')

        espenseAnalysisLable = tk.Label(analysis_window, text='Expense Analysis', font=('Helvetica', 16))
        espenseAnalysisLable.pack(pady=50)

        canvas = FigureCanvasTkAgg(fig, master=analysis_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



def openReports():
    reportsPage = tk.Toplevel()
    reportsPage.title("Reports Page")

    totalPerMonthFrame = tk.LabelFrame(reportsPage, text='Expenses Per Month', padx=10, pady=10, font=('Helvetica'))
    totalPerMonthFrame.grid(row=0, column=0, padx=10, pady=10)
    expensePerMonthQuery = """
     SELECT SUM(amount) AS total_per_month, date_format(date_paid, '%m') as Month
     FROM Expenses
     group BY Month"""

    receivedPerYearFrame = tk.LabelFrame(reportsPage, text='Received Per Year', padx=10, pady=10, font=('Helvetica'))
    receivedPerYearFrame.grid(row=1, column=0, padx=10, pady=10)
    receivedPerYearQuery = """
    SELECT SUM(amount) AS received_per_year, date_format(date_received, '%y') as Year
    FROM receipts
    group by Year"""

    cashboxFrame = tk.LabelFrame(reportsPage, text='Cash Box Balance', padx=10, pady=10, font=('Helvetica'))
    cashboxFrame.grid(row=2, column=0, padx=10, pady=10)
    cashboxBalanceQuery = """
    SELECT balance
    FROM cashbox
    """

    bankBalanceFrame = tk.LabelFrame(reportsPage, text='Bank Balance', padx=10, pady=10, font=('Helvetica'))
    bankBalanceFrame.grid(row=3, column=0, padx=10, pady=10)
    bankBalanceQuery = """
    SELECT sum(balance) AS total_balance
    from bankaccounts
    """


    try:
        # Execute the query
        with connection.cursor() as cursor:
            cursor.execute(expensePerMonthQuery)
            # Fetch all results
            expensePerMonthResult = cursor.fetchall()

            if expensePerMonthResult:
                # Display insurances expiring within two months on the Insurance Page
                for index, row in enumerate(expensePerMonthResult, start=1):
                    total_per_month, month = row
                    tk.Label(totalPerMonthFrame, text=f"${total_per_month} spent on month {month}").pack(padx=20, pady=1)
            else:
                messagebox.showinfo("Failed", "Process failed")

            cursor.execute(receivedPerYearQuery)
            receivedPerYearResult = cursor.fetchall()

            if receivedPerYearResult:
                for index, row in enumerate(receivedPerYearResult, start=1):
                    total_per_year, year = row
                    tk.Label(receivedPerYearFrame, text=f"${total_per_year} received in year {year}").pack(padx=20, pady=1)
            else:
                messagebox.showinfo("Failed", "Process failed")

            cursor.execute(cashboxBalanceQuery)
            cashboxBalanceResult = cursor.fetchall()

            if cashboxBalanceResult:
                for index, row in enumerate(cashboxBalanceResult):
                    total = row[0]
                    tk.Label(cashboxFrame, text=f"${total}").pack(padx=20, pady=1)
            else:
                messagebox.showinfo("Failed", "Process failed")

            cursor.execute(bankBalanceQuery)
            bankBalanceResult = cursor.fetchall()
            if bankBalanceResult:
                for index, row in enumerate(bankBalanceResult):
                    total = row[0]
                    tk.Label(bankBalanceFrame, text=f"${total}").pack(padx=20, pady=1)
            else:
                messagebox.showerror("Failed", "Process failed")

    except pymysql.MySQLError as err:
        messagebox.showerror("Error", f"Database error: {err}")
    finally:
        # Close the connection
        connection.close()



mainFrame = tk.LabelFrame(root, text='Building App', font=('Helvetica', 16))
mainFrame.pack(pady=20, padx=20)

openExpensesButton = tk.Button(mainFrame, text='Expenses', command=openExpenses)
openExpensesButton.pack(pady=20, padx=100)

expenseAnalysisButton = tk.Button(mainFrame, text='Expense Analysis', command=openExpenseAnalysis)
expenseAnalysisButton.pack(pady=10, padx=100)

insuranceButton = tk.Button(mainFrame, text='Insurances', command=openInsurance)
insuranceButton.pack(pady=10, padx=100)

contractButton = tk.Button(mainFrame, text='Contracts', command=openContracts)
contractButton.pack(pady=10, padx=100)

reportButton = tk.Button(mainFrame, text='Reports', command=openReports)
reportButton.pack(padx=20, pady=20)

closeButton = tk.Button(mainFrame, text='Close', command=root.quit)
closeButton.pack(pady=20, padx=100)

root.mainloop()
