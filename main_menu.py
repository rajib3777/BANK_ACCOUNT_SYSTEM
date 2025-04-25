import datetime
import random
import csv
import os
import sys


class Admin:
    _total_transaction = 0

    def __init__(self, username="Admin", password="54321"):
        self.username = username
        self.password = password

    def login(self, user, passw):
        return self.username == user and self.password == passw

    def total_transaction_today(self):
        print(f"Total transaction today is: {Admin._total_transaction}")

    def show_all_user_accounts(self, bank_system):
        print("\n--- All User Accounts ---")
        if not bank_system.accounts:
            print("No user accounts found.")
        else:
            for acc in bank_system.accounts:
                acc.show_details()
        print("-" * 40)


class Transaction:
    def __init__(self, time, type_, amount):
        self.time = time
        self.type = type_
        self.amount = amount

    def __str__(self):
        return f"{self.time} | {self.type} | {self.amount}"


class Bankaccount:
    used_account_number = set()

    def __init__(self, holder_name, pin, balance=0):
        self.account_number = self.generate_account_number()
        self.holder_name = holder_name
        self._balance = balance
        self._transactions = []
        self._pin = pin

    def generate_account_number(self):
        while True:
            number = "AC" + str(random.randint(10000, 99999))
            if number not in Bankaccount.used_account_number:
                Bankaccount.used_account_number.add(number)
                return number

    def verify_pin(self):
        pin_input = input("Enter PIN: ")
        return pin_input == self._pin

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            self.add_transaction("Deposit", amount)
            Admin._total_transaction += amount
            print(f"{amount} deposited. New balance {self._balance}")
        else:
            print("Invalid Transaction")

    def withdraw(self, amount):
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            self.add_transaction("Withdraw", amount)
            Admin._total_transaction += amount
            print(f"{amount} withdrawn. New balance {self._balance}")
        else:
            print("Withdrawal failed: Try another time")

    def add_transaction(self, type_, amount):
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._transactions.append(Transaction(time, type_, amount))

    def show_transactions(self):
        print(f"--- Transaction History for {self.account_number} ---")
        for entry in self._transactions:
            print(entry)
        print('-' * 40)

    def export_transactions_csv(self):
        filename = f"{self.account_number}_transactions.csv"
        with open(filename, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Time", "Type", "Amount"])
            for t in self._transactions:
                writer.writerow([t.time, t.type, t.amount])
        print(f"Transactions exported to {filename}")

    def show_details(self):
        print(f"Account Number: {self.account_number}")
        print(f"Holder Name: {self.holder_name}")
        print(f"Balance: {self._balance}")
        print("-" * 40)

    def get_balance(self):
        return self._balance


class Savingsaccount(Bankaccount):
    def __init__(self, holder_name, pin, balance=0, interest_rate=0.05):
        super().__init__(holder_name, pin, balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest = self._balance * self.interest_rate
        self._balance += interest
        self.add_transaction("Interest", interest)
        print(f"Interest of {interest:.2f} applied. New balance is {self._balance:.2f}")


class Currentaccount(Bankaccount):
    def __init__(self, holder_name, pin, balance=0, overdraft_limit=1000):
        super().__init__(holder_name, pin, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > 0 and amount <= (self._balance + self.overdraft_limit):
            self._balance -= amount
            self.add_transaction("Withdraw", amount)
            Admin._total_transaction += amount
            print(f"{amount} withdrawn with overdraft. New Balance: {self._balance}")
        else:
            print("Overdraft limit exceeded or invalid withdrawal.")


class Banksystem:
    def __init__(self):
        self.accounts = []

    def create_account(self, account_type, name, pin, initial_deposit):
        if not pin.isdigit() or len(pin) != 4:
            print("PIN must be a 4-digit number.")
            return

        if account_type == 'savings':
            account = Savingsaccount(name, pin, initial_deposit)
        elif account_type == 'current':
            account = Currentaccount(name, pin, initial_deposit)
        else:
            print("Invalid account type!")
            return

        self.accounts.append(account)
        print(f"{account_type.capitalize()} Account created! Account Number: {account.account_number}")

    def find_account(self, account_number):
        for acc in self.accounts:
            if acc.account_number == account_number:
                return acc
        return None


def clear_screen():
    pass  # Disable for now to see output clearly


def Main_Function():
    admin = Admin()
    system = Banksystem()

    while True:
        clear_screen()
        print("\n--- Welcome to Bank System ---")
        print("1. Admin Login")
        print("2. User Login")
        print("3. Create New Account")
        print("4. Exit")

        try:
            choice = int(input("Enter between (1 - 4): "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        if choice == 1:
            user = input("Username: ")
            password = input("Password: ")
            if admin.login(user, password):
                print("Admin login successful")
                while True:
                    print("\n--- Admin Menu ---")
                    print("1. Show Today Transaction")
                    print("2. Show All Account Details")
                    print("3. Log Out")
                    try:
                        choice_2 = int(input("Enter between (1 - 3): "))
                    except ValueError:
                        print("Invalid input!")
                        continue

                    if choice_2 == 1:
                        admin.total_transaction_today()
                    elif choice_2 == 2:
                        admin.show_all_user_accounts(system)
                    elif choice_2 == 3:
                        break
                    else:
                        print("Invalid choice")
            else:
                print("Admin credentials incorrect")

        elif choice == 2:
            acc_num = input("Enter Account Number: ")
            account = system.find_account(acc_num)

            if account:
                if account.verify_pin():
                    print(f"\nWelcome {account.holder_name}!")
                    while True:
                        print("\n--- User Menu ---")
                        print("1. Check Balance")
                        print("2. Deposit Money")
                        print("3. Withdraw Money")
                        print("4. Show Transaction History")
                        print("5. Export Transaction CSV")
                        if isinstance(account, Savingsaccount):
                            print("6. Apply Interest")
                            print("7. Log Out")
                        else:
                            print("6. Log Out")

                        try:
                            user_choice = int(input("Choose: "))
                        except ValueError:
                            print("Invalid input!")
                            continue

                        if user_choice == 1:
                            print(f"Current Balance: {account.get_balance()}")
                        elif user_choice == 2:
                            try:
                                amt = float(input("Enter amount to deposit: "))
                                account.deposit(amt)
                            except ValueError:
                                print("Invalid amount.")
                        elif user_choice == 3:
                            try:
                                amt = float(input("Enter amount to withdraw: "))
                                account.withdraw(amt)
                            except ValueError:
                                print("Invalid amount.")
                        elif user_choice == 4:
                            account.show_transactions()
                        elif user_choice == 5:
                            account.export_transactions_csv()
                        elif user_choice == 6 and isinstance(account, Savingsaccount):
                            account.apply_interest()
                        elif (user_choice == 6 and isinstance(account, Currentaccount)) or \
                             (user_choice == 7 and isinstance(account, Savingsaccount)):
                            print("Logged out successfully.")
                            break
                        else:
                            print("Invalid choice.")
                else:
                    print("Invalid PIN")
            else:
                print("Account not found")

        elif choice == 3:
            print("\n--- Create Account ---")
            name = input("Enter your name: ")
            pin = input("Set your 4-digit PIN: ")
            acc_type = input("Enter account type (savings/current): ").lower()
            try:
                initial = float(input("Enter initial deposit: "))
                system.create_account(acc_type, name, pin, initial)
            except ValueError:
                print("Invalid amount entered.")

        elif choice == 4:
            print("Exiting system...")
            sys.exit()

        else:
            print("Invalid choice!")


Main_Function()
