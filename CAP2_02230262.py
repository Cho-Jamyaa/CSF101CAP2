import random

class Account:
    def _init_(self, account_number, account_type):
        self.account_number = account_number
        self.balance = 0.0
        self.account_type = account_type

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def to_str(self):
        return f"{self.account_number},{self.balance},{self.account_type}"

    @classmethod
    def from_str(cls, account_str):
        account_number, balance, account_type = account_str.strip().split(',')
        if account_type.lower() == 'personal':
            account = PersonalAccount(account_number)
        elif account_type.lower() == 'business':
            account = BusinessAccount(account_number)
        else:
            raise ValueError("Unknown account type")
        account.balance = float(balance)
        return account

class PersonalAccount(Account):
    def _init_(self, account_number):
        super()._init_(account_number, 'Personal')

class BusinessAccount(Account):
    def _init_(self, account_number):
        super()._init_(account_number, 'Business')

class Bank:
    def _init_(self):
        self.accounts = {}
        self.load_from_file()

    def create_account(self, account_type):
        account_number = str(random.randint(100000, 999999))
        account_type = account_type.lower()
        if account_type == 'personal':
            account = PersonalAccount(account_number)
        elif account_type == 'business':
            account = BusinessAccount(account_number)
        else:
            raise ValueError("Unknown account type")
        password = str(random.randint(1000, 9999))
        self.accounts[account_number] = {'account': account, 'password': password}
        self.save_to_file()
        return account_number, password

    def login(self, account_number, password):
        account_info = self.accounts.get(account_number)
        if account_info and account_info['password'] == password:
            return account_info['account']
        return None

    def transfer_money(self, from_account, to_account_number, amount):
        to_account_info = self.accounts.get(to_account_number)
        if to_account_info and from_account.withdraw(amount):
            to_account_info['account'].deposit(amount)
            self.save_to_file()
            return True
        return False

    def delete_account(self, account_number):
        if self.accounts.pop(account_number, None):
            self.save_to_file()
            return True
        return False

    def save_to_file(self):
        with open('accounts.txt', 'w') as file:
            for acc_number, acc_info in self.accounts.items():
                account_str = acc_info['account'].to_str()
                password = acc_info['password']
                file.write(f"{account_str},{password}\n")

    def load_from_file(self):
        try:
            with open('accounts.txt', 'r') as file:
                for line in file:
                    account_str, password = line.strip().rsplit(',', 1)
                    account = Account.from_str(account_str)
                    self.accounts[account.account_number] = {'account': account, 'password': password}
        except FileNotFoundError:
            pass

def main():
    bank = Bank()

    while True:
        print("\n--- Bank Application Menu ---")
        choice = input("1. Create Account\n2. Login\n3. Exit\nEnter choice: ")

        if choice == '1':
            account_type = input("Enter account type (Personal/Business): ").strip().lower()
            if account_type not in ['personal', 'business']:
                print("Invalid account type. Please enter 'Personal' or 'Business'.")
                continue
            acc_num, pwd = bank.create_account(account_type)
            print(f"Account created. Account Number: {acc_num}, Password: {pwd}")

        elif choice == '2':
            acc_num = input("Enter account number: ")
            pwd = input("Enter password: ")
            account = bank.login(acc_num, pwd)
            if account:
                while True:
                    print("\n--- Account Menu ---")
                    acc_choice = input("1. Deposit\n2. Withdraw\n3. Check Balance\n4. Transfer Money\n5. Delete Account\n6. Logout\nEnter choice: ")

                    if acc_choice == '1':
                        amount = float(input("Enter amount to deposit: "))
                        if account.deposit(amount):
                            bank.save_to_file()
                            print("Deposit successful.")
                        else:
                            print("Deposit failed.")

                    elif acc_choice == '2':
                        amount = float(input("Enter amount to withdraw: "))
                        if account.withdraw(amount):
                            bank.save_to_file()
                            print("Withdrawal successful.")
                        else:
                            print("Insufficient funds.")

                    elif acc_choice == '3':
                        print(f"Balance: {account.balance}")

                    elif acc_choice == '4':
                        to_acc_num = input("Enter account number to transfer to: ")
                        amount = float(input("Enter amount to transfer: "))
                        if bank.transfer_money(account, to_acc_num, amount):
                            print("Transfer successful.")
                        else:
                            print("Transfer failed.")

                    elif acc_choice == '5':
                        if bank.delete_account(acc_num):
                            print("Account deleted successfully.")
                            break
                        else:
                            print("Account deletion failed.")

                    elif acc_choice == '6':
                        break

                    else:
                        print("Invalid choice.")

            else:
                print("Login failed. Invalid account number or password.")

        elif choice == '3':
            print("Exiting...")
            break

        else:
            print("Invalid choice.")

if _name_ == "_main_":
    main()