# Building Management Application

This is a Building Management Application developed using Python and Tkinter for the GUI. It interacts with a MySQL database to manage various aspects such as expenses, insurance, contracts, and generates various reports.

## Features

- **Expenses Management**: Register and delete expenses, specifying details such as type, cost, date, payment method, and bank account details.
- **Insurance Management**: View insurance policies that are about to expire within two months.
- **Contracts Management**: View contracts that are about to end within two months.
- **Expense Analysis**: Visualize monthly expenses using matplotlib.
- **Reports**: Generate reports on expenses per month, receipts per year, current cashbox balance, and bank account balances.

## Prerequisites

- Python 3.x
- MySQL Server
- Necessary Python packages (listed in `requirements.txt`)

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/BuildingManagementApp.git
    cd BuildingManagementApp
    ```

2. **Install Python Packages**:
    Ensure you have `pip` installed. Then, run:
    ```bash
    pip install -r requirements.txt
    ```

3. **Database Setup**:
    - Ensure you have a MySQL server running.
    - Create a database named `sql_building`:
      ```sql
      CREATE DATABASE sql_building;
      ```
    - Create the necessary tables by running the following SQL commands:
      ```sql
      CREATE TABLE BankAccounts (
          account_id INT AUTO_INCREMENT PRIMARY KEY,
          bank_name VARCHAR(50),
          branch_name VARCHAR(50),
          account_number VARCHAR(20),
          balance DECIMAL(10, 2)
      );

      CREATE TABLE CashBox (
          balance DECIMAL(10, 2)
      );

      CREATE TABLE BankTransactions (
          transaction_id INT AUTO_INCREMENT PRIMARY KEY,
          account_id INT,
          transaction_date DATE,
          amount DECIMAL(10, 2),
          description TEXT,
          transaction_type VARCHAR(50)
      );

      CREATE TABLE CashBoxTransactions (
          transaction_id INT AUTO_INCREMENT PRIMARY KEY,
          transaction_date DATE,
          amount DECIMAL(10, 2),
          description TEXT,
          transaction_type VARCHAR(50)
      );

      CREATE TABLE Expenses (
          expense_id INT AUTO_INCREMENT PRIMARY KEY,
          expense_type VARCHAR(50),
          amount DECIMAL(10, 2),
          date_paid DATE,
          withdraw_place VARCHAR(50),
          bank_branch_name VARCHAR(50),
          account_number VARCHAR(20)
      );

      CREATE TABLE Insurance (
          insurance_id INT AUTO_INCREMENT PRIMARY KEY,
          insurance_type VARCHAR(50),
          end_date DATE
      );

      CREATE TABLE Contractors (
          contractor_id INT AUTO_INCREMENT PRIMARY KEY,
          company_name VARCHAR(50),
          end_date DATE
      );

      CREATE TABLE Receipts (
          receipt_id INT AUTO_INCREMENT PRIMARY KEY,
          amount DECIMAL(10, 2),
          date_received DATE
      );
      ```

## Usage

1. **Start the Application**:
    ```bash
    python app.py
    ```

2. **Main Menu**:
    - **Expenses**: Open the Expenses window to register or delete expenses.
    - **Expense Analysis**: View a graphical analysis of monthly expenses.
    - **Insurances**: Check for insurances that are nearing expiration.
    - **Contracts**: Check for contracts that are nearing their end date.
    - **Reports**: Generate various financial reports.

3. **Registering Expenses**:
    - Fill in the necessary fields and click `Register` to save the expense.
    - Use the `Clear` button to reset the form.
    - The `Delete` button allows you to remove an expense entry.

4. **Bank and Cash Box Transactions**:
    - Depending on the payment method selected (Bank or Cash Box), the appropriate transactions will be handled and recorded in the database.

## Notes

- Ensure your MySQL server is running before starting the application.
- Modify the `host`, `user`, `password`, and `database` variables in the script to match your MySQL configuration.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI
- [pymysql](https://pypi.org/project/PyMySQL/) for MySQL connection
- [matplotlib](https://matplotlib.org/) for plotting graphs
