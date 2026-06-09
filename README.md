
# 🏦 Simple Bank System
A Python-based banking system that runs in the terminal. Create accounts, deposit/withdraw money, and view transaction history.

## Features
- 🔐 Create account with 4-digit PIN
- 💰 Deposit & withdraw money  
- 📊 Check account balance
- 📜 View last 10 transactions
- 💾 Auto-saves data to JSON file
- 🎨 Colored console interface

## Quick Start
# Clone the repo
git clone https://github.com/hifza-irfan/banking-system.git

# Run the program
python banking_system.py

## How to Use
1. **Create Account** - Enter name & 4-digit PIN, get account number
2. **Login** - Use account number & PIN
3. **Banking Menu** - Choose from balance, deposit, withdraw, history, logout

## File Structure
banking-system/
├── banking_system.py   # Main program
├── bank_data.json      # User data (auto-created)
└── README.md          

## Requirements
- Python 3.x only (no external packages needed)

## Notes
- PIN must be exactly 4 digits
- Can't withdraw more than balance
- Your data stays after closing program

## Author
- Hifza Irfan
