FILE = "accounts.txt"


def create_account():
    acc_no = input("Enter Account Number: ")
    name = input("Enter Account Holder Name: ")
    balance = float(input("Enter Initial Balance: "))

    # Check duplicate account
    try:
        with open(FILE, "r") as f:
            for line in f:
                data = line.strip().split(",")

                if data[0] == acc_no:
                    print("Account already exists!")
                    return
    except FileNotFoundError:
        pass

    with open(FILE, "a") as f:
        f.write(acc_no + "," + name + "," + str(balance) + "\n")

    print("Account created successfully!")


def find_account(acc_no):
    try:
        with open(FILE, "r") as f:
            for line in f:
                data = line.strip().split(",")

                if data[0] == acc_no:
                    return data

    except FileNotFoundError:
        return None

    return None


def deposit():
    acc_no = input("Enter Account Number: ")
    amount = float(input("Enter Deposit Amount: "))

    if amount <= 0:
        print("Invalid amount!")
        return

    data = find_account(acc_no)

    if data:
        balance = float(data[2])
        balance = balance + amount
        data[2] = str(balance)

        update_account(acc_no, data)

        print("Amount deposited successfully!")
        print("New Balance:", balance)
    else:
        print("Account not found!")


def withdraw():
    acc_no = input("Enter Account Number: ")
    amount = float(input("Enter Withdrawal Amount: "))

    if amount <= 0:
        print("Invalid amount!")
        return

    data = find_account(acc_no)

    if data:
        balance = float(data[2])

        if amount > balance:
            print("Insufficient balance!")
        else:
            balance = balance - amount
            data[2] = str(balance)

            update_account(acc_no, data)

            print("Amount withdrawn successfully!")
            print("Remaining Balance:", balance)
    else:
        print("Account not found!")


def check_balance():
    acc_no = input("Enter Account Number: ")

    data = find_account(acc_no)

    if data:
        print("\nAccount Number:", data[0])
        print("Account Holder:", data[1])
        print("Balance:", data[2])
    else:
        print("Account not found!")


def display_accounts():
    try:
        with open(FILE, "r") as f:
            print("\n===== ALL ACCOUNTS =====")

            found = False

            for line in f:
                data = line.strip().split(",")

                print("\nAccount Number:", data[0])
                print("Account Holder:", data[1])
                print("Balance:", data[2])

                found = True

            if not found:
                print("No accounts available.")

    except FileNotFoundError:
        print("No accounts available.")


def update_account(acc_no, new_data):
    lines = []

    with open(FILE, "r") as f:
        for line in f:
            data = line.strip().split(",")

            if data[0] == acc_no:
                lines.append(",".join(new_data) + "\n")
            else:
                lines.append(line)

    with open(FILE, "w") as f:
        f.writelines(lines)


# Main Program

while True:

    print("\n==============================")
    print("       MINI BANKING SYSTEM")
    print("==============================")
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Check Balance")
    print("5. Display All Accounts")
    print("6. Exit")
    print("==============================")

    choice = input("Enter your choice: ")

    if choice == "1":
        create_account()

    elif choice == "2":
        deposit()

    elif choice == "3":
        withdraw()

    elif choice == "4":
        check_balance()

    elif choice == "5":
        display_accounts()

    elif choice == "6":
        print("Thank you for using Mini Banking System!")
        break

    else:
        print("Invalid choice!")
