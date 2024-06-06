CREATE TABLE Units (
    unit_id INT AUTO_INCREMENT PRIMARY KEY,
    unit_number VARCHAR(10),
    owner_name VARCHAR(100),
    owner_contact VARCHAR(15),
    unit_contact VARCHAR(15)
);

CREATE TABLE Employees (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    id_number VARCHAR(20),
    birth_date DATE,
    gender VARCHAR(10),
    marital_status VARCHAR(20),
    children_count INT,
    job_type VARCHAR(50),
    hire_date DATE,
    work_experience INT,
    salary DECIMAL(10, 2),
    benefits VARCHAR(100),
    contract_text TEXT
);

CREATE TABLE Receipts (
    receipt_id INT AUTO_INCREMENT PRIMARY KEY,
    receipt_type VARCHAR(50),
    amount DECIMAL(10, 2),
    date_received DATE,
    deposit_place VARCHAR(50),
    bank_branch_name VARCHAR(50),
    account_number VARCHAR(20),
    unit_id INT,
    FOREIGN KEY (unit_id) REFERENCES Units(unit_id)
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

CREATE TABLE Contractors (
    contractor_id INT AUTO_INCREMENT PRIMARY KEY,
    contract_type VARCHAR(50),
    company_name VARCHAR(100),
    contract_text TEXT,
    start_date DATE,
    end_date DATE,
    advance_payment DECIMAL(10, 2),
    monthly_payment DECIMAL(10, 2)
);

CREATE TABLE Insurance (
    insurance_id INT AUTO_INCREMENT PRIMARY KEY,
    insurance_type VARCHAR(50),
    contract_text TEXT,
    start_date DATE,
    end_date DATE,
    advance_payment DECIMAL(10, 2),
    monthly_payment DECIMAL(10, 2)
);

CREATE TABLE BankAccounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    bank_name VARCHAR(100),
    branch_name VARCHAR(100),
    account_number VARCHAR(20),
    account_type VARCHAR(50),
    balance DECIMAL(10, 2)
);

CREATE TABLE BankTransactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT,
    transaction_date DATE,
    amount DECIMAL(10, 2),
    description TEXT,
    transaction_type VARCHAR(10),
    FOREIGN KEY (account_id) REFERENCES BankAccounts(account_id)
);

CREATE TABLE CashBox (
    cashbox_id INT AUTO_INCREMENT PRIMARY KEY,
    balance DECIMAL(10, 2)
);

CREATE TABLE CashBoxTransactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_date DATE,
    amount DECIMAL(10, 2),
    description TEXT,
    transaction_type VARCHAR(10)
);

-- Insert data into Units
INSERT INTO Units (unit_number, owner_name, owner_contact, unit_contact) 
VALUES 
('101', 'John Doe', '555-1234', '555-5678'),
('102', 'Jane Smith', '555-2345', '555-6789'),
('103', 'Alice Johnson', '555-3456', '555-7890'),
('104', 'Bob Martin', '555-4567', '555-8901'),
('105', 'Charlie Brown', '555-5678', '555-9012'),
('106', 'David Wilson', '555-6789', '555-0123'),
('107', 'Eve Davis', '555-7890', '555-1234'),
('108', 'Frank Thomas', '555-8901', '555-2345'),
('109', 'Grace Lee', '555-9012', '555-3456'),
('110', 'Hank White', '555-0123', '555-4567');

-- Insert data into Employees
INSERT INTO Employees (name, id_number, birth_date, gender, marital_status, children_count, job_type, hire_date, work_experience, salary, benefits, contract_text)
VALUES
('Bob Williams', 'A123456', '1980-04-15', 'Male', 'Married', 2, 'Manager', '2010-06-01', 10, 50000.00, 'Health Insurance', 'Manager contract text'),
('Susan Brown', 'B234567', '1990-08-20', 'Female', 'Single', 0, 'Accountant', '2015-09-10', 5, 40000.00, 'Retirement Plan', 'Accountant contract text'),
('Jack Green', 'C345678', '1985-12-11', 'Male', 'Married', 1, 'Technician', '2013-01-15', 7, 45000.00, 'Health Insurance', 'Technician contract text'),
('Linda Black', 'D456789', '1975-07-30', 'Female', 'Divorced', 3, 'Cleaner', '2018-02-05', 2, 30000.00, 'None', 'Cleaner contract text'),
('Mike Harris', 'E567890', '1995-03-25', 'Male', 'Single', 0, 'Security', '2020-11-01', 1, 35000.00, 'None', 'Security contract text');

-- Insert data into Receipts
INSERT INTO Receipts (receipt_type, amount, date_received, deposit_place, bank_branch_name, account_number, unit_id)
VALUES
('Monthly Charge', 1000.00, '2024-05-01', 'Bank', 'Main Branch', '12345678', 1),
('Monthly Charge', 1000.00, '2024-05-02', 'Bank', 'Main Branch', '12345678', 2),
('Monthly Charge', 1000.00, '2024-05-03', 'Bank', 'Main Branch', '12345678', 3),
('Advertising Revenue', 200.00, '2024-05-10', 'Bank', 'Main Branch', '12345678', NULL),
('Monthly Charge', 1000.00, '2024-06-01', 'Bank', 'Main Branch', '12345678', 1),
('Monthly Charge', 1000.00, '2024-06-02', 'Bank', 'Main Branch', '12345678', 2),
('Monthly Charge', 1000.00, '2024-06-03', 'Bank', 'Main Branch', '12345678', 3),
('Monthly Charge', 1000.00, '2024-06-04', 'Bank', 'Main Branch', '12345678', 4),
('Monthly Charge', 1000.00, '2024-06-05', 'Bank', 'Main Branch', '12345678', 5),
('Monthly Charge', 1000.00, '2024-07-01', 'Bank', 'Main Branch', '12345678', 1),
('Monthly Charge', 1000.00, '2024-07-02', 'Bank', 'Main Branch', '12345678', 2),
('Monthly Charge', 1000.00, '2024-07-03', 'Bank', 'Main Branch', '12345678', 3),
('Monthly Charge', 1000.00, '2024-07-04', 'Bank', 'Main Branch', '12345678', 4),
('Monthly Charge', 1000.00, '2024-07-05', 'Bank', 'Main Branch', '12345678', 5),
('Monthly Charge', 1000.00, '2024-08-01', 'Bank', 'Main Branch', '12345678', 1),
('Monthly Charge', 1000.00, '2024-08-02', 'Bank', 'Main Branch', '12345678', 2),
('Monthly Charge', 1000.00, '2024-08-03', 'Bank', 'Main Branch', '12345678', 3),
('Monthly Charge', 1000.00, '2024-08-04', 'Bank', 'Main Branch', '12345678', 4),
('Monthly Charge', 1000.00, '2024-08-05', 'Bank', 'Main Branch', '12345678', 5),
('Event Revenue', 500.00, '2024-08-10', 'Bank', 'Main Branch', '12345678', NULL);

-- Insert data into Expenses
INSERT INTO Expenses (expense_type, amount, date_paid, withdraw_place, bank_branch_name, account_number)
VALUES
('Utility', 500.00, '2024-05-01', 'Bank', 'Main Branch', '12345678'),
('Salary', 2000.00, '2024-05-01', 'Bank', 'Main Branch', '12345678'),
('Maintenance', 300.00, '2024-05-02', 'Bank', 'Main Branch', '12345678'),
('Utility', 600.00, '2024-06-01', 'Bank', 'Main Branch', '12345678'),
('Salary', 2100.00, '2024-06-01', 'Bank', 'Main Branch', '12345678'),
('Maintenance', 350.00, '2024-06-02', 'Bank', 'Main Branch', '12345678'),
('Utility', 550.00, '2024-07-01', 'Bank', 'Main Branch', '12345678'),
('Salary', 2200.00, '2024-07-01', 'Bank', 'Main Branch', '12345678'),
('Maintenance', 400.00, '2024-07-02', 'Bank', 'Main Branch', '12345678'),
('Utility', 700.00, '2024-08-01', 'Bank', 'Main Branch', '12345678'),
('Salary', 2300.00, '2024-08-01', 'Bank', 'Main Branch', '12345678'),
('Maintenance', 450.00, '2024-08-02', 'Bank', 'Main Branch', '12345678');

-- Insert data into Contractors
INSERT INTO Contractors (contract_type, company_name, contract_text, start_date, end_date, advance_payment, monthly_payment)
VALUES
('Technical', 'Tech Solutions', 'Technical contract text', '2023-01-01', '2023-12-31', 1000.00, 200.00),
('Services', 'Clean Services', 'Services contract text', '2023-02-01', '2024-01-31', 500.00, 100.00),
('Technical', 'Elevator Corp', 'Elevator maintenance contract text', '2023-03-01', '2025-02-28', 1500.00, 300.00),
('Security', 'SafeGuard', 'Security contract text', '2023-04-01', '2024-03-31', 2000.00, 400.00);

-- Insert data into Insurance
INSERT INTO Insurance (insurance_type, contract_text, start_date, end_date, advance_payment, monthly_payment)
VALUES
('Fire', 'Fire insurance contract text', '2023-01-01', '2024-01-01', 1200.00, 100.00),
('Earthquake', 'Earthquake insurance contract text', '2023-01-01', '2024-01-01', 1500.00, 125.00),
('Flood', 'Flood insurance contract text', '2023-05-01', '2025-04-30', 1800.00, 150.00),
('Burglary', 'Burglary insurance contract text', '2023-06-01', '2024-05-31', 1100.00, 90.00);

-- Insert data into BankAccounts
INSERT INTO BankAccounts (bank_name, branch_name, account_number, account_type, balance)
VALUES
('Bank A', 'Main Branch', '12345678', 'Checking', 10000.00),
('Bank B', 'Secondary Branch', '23456789', 'Savings', 5000.00),
('Bank C', 'Tertiary Branch', '34567890', 'Business', 15000.00);

-- Insert data into BankTransactions
INSERT INTO BankTransactions (account_id, transaction_date, amount, description, transaction_type)
VALUES
(1, '2024-05-01', 1000.00, 'Deposit from unit 101', 'Deposit'),
(1, '2024-05-02', 500.00, 'Withdrawal for utility payment', 'Withdrawal'),
(1, '2024-06-01', 2000.00, 'Deposit from unit 102', 'Deposit'),
(1, '2024-06-02', 300.00, 'Withdrawal for maintenance', 'Withdrawal'),
(2, '2024-07-01', 1000.00, 'Deposit from unit 103', 'Deposit'),
(2, '2024-07-02', 350.00, 'Withdrawal for repair', 'Withdrawal'),
(3, '2024-08-01', 1500.00, 'Deposit from unit 104', 'Deposit'),
(3, '2024-08-02', 450.00, 'Withdrawal for security', 'Withdrawal');

-- Insert data into CashBox
INSERT INTO CashBox (balance)
VALUES
(2000.00);

-- Insert data into CashBoxTransactions
INSERT INTO CashBoxTransactions (transaction_date, amount, description, transaction_type)
VALUES
('2024-05-01', 300.00, 'Deposit from unit 105', 'Deposit'),
('2024-05-02', 100.00, 'Withdrawal for minor repairs', 'Withdrawal'),
('2024-06-01', 200.00, 'Deposit from unit 106', 'Deposit'),
('2024-06-02', 50.00, 'Withdrawal for supplies', 'Withdrawal'),
('2024-07-01', 150.00, 'Deposit from unit 107', 'Deposit'),
('2024-07-02', 75.00, 'Withdrawal for cleaning', 'Withdrawal'),
('2024-08-01', 100.00, 'Deposit from unit 108', 'Deposit'),
('2024-08-02', 80.00, 'Withdrawal for maintenance', 'Withdrawal');


/*
    WHY TABLES ARE NORMALIZED:

    Units: This table seems appropriately normalized. Each unit has its own unique unit_id, and owner information is stored separately from the unit details.

    Employees: This table also appears to be normalized. Each employee has a unique employee_id, and their personal information is stored separately from the job-related details.

    Receipts: This table could be normalized further. The receipt_type could potentially be moved to a separate table if there are many different types of receipts. However, it depends on the nature of your data and if you expect new types to be added frequently.

    Expenses: Similar to Receipts, the expense_type could be moved to a separate table for normalization. This would allow for easier management if new types of expenses are introduced.

    Contractors and Insurance: Both these tables seem to be normalized as they store separate information about contracts and insurance.

    BankAccounts: This table is normalized, storing information about bank accounts separately from transactions.

    BankTransactions: This table appears to be normalized, linking transactions to bank accounts using the account_id foreign key.

    CashBox and CashBoxTransactions: These tables are normalized, storing separate information about cash box balance and transactions.
 */