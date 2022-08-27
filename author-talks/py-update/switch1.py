def balance():
    print("BALANCE CODE")

def deposit():
    print("DEPOSIT CODE")

def withdraw():
    print("WITHDRAW CODE")

choice = input("balance, deposit, withdraw? ")
if choice == "balance":
    balance()
elif choice == "deposit":
    deposit()
elif choice == "withdraw":
    withdraw()
