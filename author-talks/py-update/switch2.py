def balance():
    print("BALANCE CODE")

def deposit():
    print("DEPOSIT CODE")

def withdraw():
    print("WITHDRAW CODE")

choice = input("balance, deposit, withdraw? ")
choice_map = {
    "balance": balance,
    "deposit": deposit,
    "withdraw": withdraw,
}
choice_map[choice]()
