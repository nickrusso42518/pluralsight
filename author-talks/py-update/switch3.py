def balance():
    print("BALANCE CODE")

def deposit():
    print("DEPOSIT CODE")

def withdraw():
    print("WITHDRAW CODE")

choice = input("balance, deposit, withdraw? ")
match choice:
    case "balance":
        balance()
    case "deposit":
        deposit()
    case "withdraw":
        withdraw()
