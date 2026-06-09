import json
import os
from datetime import datetime


# ANSI Color codes for beautiful console
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def print_banner():
    print(f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     ██████╗  █████╗ ███╗   ██╗██╗  ██╗                  ║
║     ██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝                  ║
║     ██████╔╝███████║██╔██╗ ██║█████╔╝                   ║
║     ██╔══██╗██╔══██║██║╚██╗██║██╔═██╗                  ║
║     ██████╔╝██║  ██║██║ ╚████║██║  ██╗                  ║
║     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝                  ║
║                                                          ║
║              {Colors.YELLOW}SECURE BANKING SYSTEM{Colors.CYAN}                       ║
╚══════════════════════════════════════════════════════════╝
{Colors.END}
    """)


def print_box(text, color=Colors.GREEN):
    print(f"{color}┌{'─' * (len(text) + 2)}┐{Colors.END}")
    print(f"{color}│ {text} │{Colors.END}")
    print(f"{color}└{'─' * (len(text) + 2)}┘{Colors.END}")


def print_table_row(col1, col2, col3=""):
    print(f"│ {col1:<12} │ {col2:<20} │ {col3:<15} │")


class Account:
    def __init__(self, account_number, name, pin, balance=0):
        self.account_number = account_number
        self.name = name
        self.pin = pin
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.transactions.append({
            'date': timestamp,
            'type': 'DEPOSIT',
            'amount': amount,
            'balance': self.balance
        })
        return True

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.transactions.append({
            'date': timestamp,
            'type': 'WITHDRAW',
            'amount': amount,
            'balance': self.balance
        })
        return True

    def get_transactions(self):
        return self.transactions[-10:]


class Bank:
    def __init__(self):
        self.accounts = {}
        self.load_data()

    def create_account(self, name, pin):
        account_number = str(len(self.accounts) + 1001)
        self.accounts[account_number] = Account(account_number, name, pin)
        self.save_data()
        return account_number

    def login(self, account_number, pin):
        if account_number in self.accounts and self.accounts[account_number].pin == pin:
            return self.accounts[account_number]
        return None

    def save_data(self):
        data = {}
        for acc_num, acc in self.accounts.items():
            data[acc_num] = {
                'name': acc.name,
                'pin': acc.pin,
                'balance': acc.balance,
                'transactions': acc.transactions
            }
        with open('bank_data.json', 'w') as f:
            json.dump(data, f, indent=2)

    def load_data(self):
        if os.path.exists('bank_data.json'):
            with open('bank_data.json', 'r') as f:
                data = json.load(f)
                for acc_num, acc_data in data.items():
                    acc = Account(acc_num, acc_data['name'], acc_data['pin'], acc_data['balance'])
                    acc.transactions = acc_data['transactions']
                    self.accounts[acc_num] = acc

def main():
    bank = Bank()

    while True:
        print_banner()

        print(f"{Colors.BOLD}{Colors.YELLOW}📋 MAIN MENU{Colors.END}")
        print(f"{Colors.CYAN}╔════════════════════════════════╗{Colors.END}")
        print(
            f"{Colors.CYAN}║{Colors.END}  {Colors.GREEN}1.{Colors.END} 🆕 Create New Account     {Colors.CYAN}║{Colors.END}")
        print(
            f"{Colors.CYAN}║{Colors.END}  {Colors.GREEN}2.{Colors.END} 🔐 Login                 {Colors.CYAN}║{Colors.END}")
        print(
            f"{Colors.CYAN}║{Colors.END}  {Colors.GREEN}3.{Colors.END} 🚪 Exit                   {Colors.CYAN}║{Colors.END}")
        print(f"{Colors.CYAN}╚════════════════════════════════╝{Colors.END}")

        choice = input(f"\n{Colors.BOLD}👉 Enter your choice: {Colors.END}")

        if choice == '1':
            print(f"\n{Colors.CYAN}{'═' * 50}{Colors.END}")
            print(f"{Colors.BOLD}📝 NEW ACCOUNT REGISTRATION{Colors.END}")
            print(f"{Colors.CYAN}{'═' * 50}{Colors.END}")

            name = input(f"{Colors.YELLOW}📛 Full Name: {Colors.END}")
            pin = input(f"{Colors.YELLOW}🔑 Set 4-digit PIN: {Colors.END}")

            if len(pin) != 4 or not pin.isdigit():
                print(f"{Colors.RED}❌ PIN must be exactly 4 digits!{Colors.END}")
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                continue

            acc_num = bank.create_account(name, pin)
            print(f"\n{Colors.GREEN}{'═' * 50}{Colors.END}")
            print(f"{Colors.GREEN}✅ ACCOUNT CREATED SUCCESSFULLY!{Colors.END}")
            print(f"{Colors.CYAN}{'═' * 50}{Colors.END}")
            print(f"{Colors.YELLOW}📌 Account Number: {Colors.BOLD}{acc_num}{Colors.END}")
            print(f"{Colors.YELLOW}🔑 Your PIN: **** (keep it secret){Colors.END}")
            print(f"{Colors.GREEN}{'═' * 50}{Colors.END}")
            
            # Ask user what to do next
            print(f"\n{Colors.BOLD}{Colors.CYAN}What would you like to do next?{Colors.END}")
            print(f"{Colors.GREEN}1. Login to your new account{Colors.END}")
            print(f"{Colors.GREEN}2. Return to main menu{Colors.END}")
            
            next_choice = input(f"\n{Colors.BOLD}👉 Choose option: {Colors.END}")
            if next_choice == '1':
                # Direct login attempt
                print(f"\n{Colors.CYAN}{'═' * 50}{Colors.END}")
                print(f"{Colors.BOLD}🔐 LOGIN TO YOUR ACCOUNT{Colors.END}")
                print(f"{Colors.CYAN}{'═' * 50}{Colors.END}")
                
                login_acc = input(f"{Colors.YELLOW}🏦 Account Number: {Colors.END}")
                login_pin = input(f"{Colors.YELLOW}🔑 PIN: {Colors.END}")
                
                account = bank.login(login_acc, login_pin)
                
                if account:
                    print(f"\n{Colors.GREEN}✅ Login successful!{Colors.END}")
                    print(f"{Colors.GREEN}👋 Welcome back, {account.name}!{Colors.END}")
                    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                    user_menu(account, bank)
                else:
                    print(f"\n{Colors.RED}❌ Invalid account number or PIN!{Colors.END}")
                    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
            else:
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

        elif choice == '2':
            print(f"\n{Colors.CYAN}{'═' * 50}{Colors.END}")
            print(f"{Colors.BOLD}🔐 LOGIN TO YOUR ACCOUNT{Colors.END}")
            print(f"{Colors.CYAN}{'═' * 50}{Colors.END}")

            acc_num = input(f"{Colors.YELLOW}🏦 Account Number: {Colors.END}")
            pin = input(f"{Colors.YELLOW}🔑 PIN: {Colors.END}")

            account = bank.login(acc_num, pin)

            if account:
                print(f"\n{Colors.GREEN}✅ Login successful!{Colors.END}")
                print(f"{Colors.GREEN}👋 Welcome back, {account.name}!{Colors.END}")
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                user_menu(account, bank)  # This will enter the banking menu
            else:
                print(f"\n{Colors.RED}❌ Invalid account number or PIN!{Colors.END}")
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

        elif choice == '3':
            print(f"\n{Colors.YELLOW}👋 Thank you for using Simple Bank!{Colors.END}")
            print(f"{Colors.GREEN}Have a great day! 🌟{Colors.END}\n")
            break
        else:
            print(f"{Colors.RED}❌ Invalid choice! Please try again.{Colors.END}")
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")


def user_menu(account, bank):
    while True:
        print(f"\n{Colors.CYAN}{'═' * 50}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}🏦 Welcome {account.name}{Colors.END}")
        print(f"{Colors.CYAN}{'═' * 50}{Colors.END}")

        # Show mini balance card
        print(f"{Colors.GREEN}┌────────────────────────────────────┐{Colors.END}")
        print(f"{Colors.GREEN}│{Colors.END}  💰 CURRENT BALANCE              {Colors.GREEN}│{Colors.END}")
        print(
            f"{Colors.GREEN}│{Colors.END}     ₹{account.balance:>10.2f}                     {Colors.GREEN}│{Colors.END}")
        print(f"{Colors.GREEN}└────────────────────────────────────┘{Colors.END}")

        print(f"\n{Colors.YELLOW}📋 SERVICE MENU{Colors.END}")
        print(f"{Colors.CYAN}┌────────────────────────────────────┐{Colors.END}")
        print(
            f"{Colors.CYAN}│{Colors.END}  {Colors.GREEN}1.{Colors.END} 💰 Check Balance          {Colors.CYAN}│{Colors.END}")
        print(
            f"{Colors.CYAN}│{Colors.END}  {Colors.GREEN}2.{Colors.END} 📥 Deposit Money          {Colors.CYAN}│{Colors.END}")
        print(
            f"{Colors.CYAN}│{Colors.END}  {Colors.GREEN}3.{Colors.END} 📤 Withdraw Money         {Colors.CYAN}│{Colors.END}")
        print(
            f"{Colors.CYAN}│{Colors.END}  {Colors.GREEN}4.{Colors.END} 📜 Transaction History    {Colors.CYAN}│{Colors.END}")
        print(
            f"{Colors.CYAN}│{Colors.END}  {Colors.GREEN}5.{Colors.END} 🚪 Logout                 {Colors.CYAN}│{Colors.END}")
        print(f"{Colors.CYAN}└────────────────────────────────────┘{Colors.END}")

        choice = input(f"\n{Colors.BOLD}👉 Choose option: {Colors.END}")

        if choice == '1':
            print(f"\n{Colors.GREEN}{'═' * 50}{Colors.END}")
            print(f"{Colors.BOLD}💰 CURRENT BALANCE{Colors.END}")
            print(f"{Colors.GREEN}{'═' * 50}{Colors.END}")
            print(f"{Colors.YELLOW}Account Holder: {Colors.CYAN}{account.name}{Colors.END}")
            print(f"{Colors.YELLOW}Account Number: {Colors.CYAN}{account.account_number}{Colors.END}")
            print(f"{Colors.GREEN}{'─' * 50}{Colors.END}")
            print(f"{Colors.BOLD}Available Balance: ₹{account.balance:,.2f}{Colors.END}")
            print(f"{Colors.GREEN}{'═' * 50}{Colors.END}")
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

        elif choice == '2':
            try:
                print(f"\n{Colors.CYAN}{'═' * 50}{Colors.END}")
                print(f"{Colors.BOLD}📥 DEPOSIT MONEY{Colors.END}")
                print(f"{Colors.CYAN}{'═' * 50}{Colors.END}")
                amount = float(input(f"{Colors.YELLOW}💰 Enter amount to deposit: ₹{Colors.END}"))
                if amount <= 0:
                    print(f"{Colors.RED}❌ Amount must be positive!{Colors.END}")
                else:
                    account.deposit(amount)
                    bank.save_data()
                    print(f"\n{Colors.GREEN}✅ Success! Deposited ₹{amount:,.2f}{Colors.END}")
                    print(f"{Colors.GREEN}💰 New Balance: ₹{account.balance:,.2f}{Colors.END}")
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}❌ Invalid amount!{Colors.END}")
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

        elif choice == '3':
            try:
                print(f"\n{Colors.CYAN}{'═' * 50}{Colors.END}")
                print(f"{Colors.BOLD}📤 WITHDRAW MONEY{Colors.END}")
                print(f"{Colors.CYAN}{'═' * 50}{Colors.END}")
                print(f"{Colors.YELLOW}Available Balance: ₹{account.balance:,.2f}{Colors.END}")
                amount = float(input(f"{Colors.YELLOW}💰 Enter amount to withdraw: ₹{Colors.END}"))
                if amount <= 0:
                    print(f"{Colors.RED}❌ Amount must be positive!{Colors.END}")
                elif account.withdraw(amount):
                    bank.save_data()
                    print(f"\n{Colors.GREEN}✅ Success! Withdrawn ₹{amount:,.2f}{Colors.END}")
                    print(f"{Colors.GREEN}💰 Remaining Balance: ₹{account.balance:,.2f}{Colors.END}")
                else:
                    print(f"{Colors.RED}❌ Insufficient balance! Available: ₹{account.balance:,.2f}{Colors.END}")
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}❌ Invalid amount!{Colors.END}")
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

        elif choice == '4':
            print(f"\n{Colors.CYAN}{'═' * 70}{Colors.END}")
            print(f"{Colors.BOLD}📜 TRANSACTION HISTORY (Last 10){Colors.END}")
            print(f"{Colors.CYAN}{'═' * 70}{Colors.END}")
            transactions = account.get_transactions()
            if not transactions:
                print(f"{Colors.YELLOW}│{'No transactions yet':^66}│{Colors.END}")
            else:
                print(f"{Colors.CYAN}│{'Date':<20}│{'Type':<12}│{'Amount':<12}│{'Balance':<12}│{Colors.END}")
                print(f"{Colors.CYAN}├{'─' * 20}┼{'─' * 12}┼{'─' * 12}┼{'─' * 12}┤{Colors.END}")
                for t in transactions:
                    color = Colors.GREEN if t['type'] == 'DEPOSIT' else Colors.RED
                    print(
                        f"{color}│{t['date']:<20}│{t['type']:<12}│₹{t['amount']:<11.2f}│₹{t['balance']:<11.2f}│{Colors.END}")
            print(f"{Colors.CYAN}{'═' * 70}{Colors.END}")
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

        elif choice == '5':
            print(f"\n{Colors.YELLOW}👋 Goodbye {account.name}!{Colors.END}")
            print(f"{Colors.GREEN}Come back soon! 🌟{Colors.END}")
            break
        else:
            print(f"{Colors.RED}❌ Invalid option!{Colors.END}")
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")


if __name__ == "__main__":
    # Clear screen for better visuals
    os.system('cls' if os.name == 'nt' else 'clear')
    main()