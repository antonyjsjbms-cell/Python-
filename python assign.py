import csv
import os
from datetime import date, datetime, timedelta


# ---------------- CUSTOM EXCEPTIONS ----------------

class LibraryError(Exception):
    pass


class BookNotFoundError(LibraryError):
    pass


class MemberNotFoundError(LibraryError):
    pass


class BookUnavailableError(LibraryError):
    pass


# ---------------- DATA STRUCTURES ----------------

members = {}
books = {}
transactions = []

# Tuple used for book categories
categories = ("Programming", "Science", "Mathematics",
              "Literature", "History", "Other")

# Set used to store lost books
lost_books = set()


# ---------------- FILE NAMES ----------------

MEMBER_FILE = "members.csv"
BOOK_FILE = "books.csv"
TRANSACTION_FILE = "transactions.csv"


# ---------------- FILE HANDLING ----------------

def load_data():

    # Load members
    if os.path.exists(MEMBER_FILE):
        with open(MEMBER_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                members[row["id"]] = {
                    "name": row["name"],
                    "email": row["email"],
                    "borrowed": row["borrowed"].split(";")
                    if row["borrowed"] else []
                }

    # Load books
    if os.path.exists(BOOK_FILE):
        with open(BOOK_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                books[row["id"]] = {
                    "title": row["title"],
                    "author": row["author"],
                    "category": row["category"],
                    "status": row["status"]
                }

                if row["status"] == "Lost":
                    lost_books.add(row["id"])

    # Load transactions
    if os.path.exists(TRANSACTION_FILE):
        with open(TRANSACTION_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                transactions.append(row)


def save_data():

    with open(MEMBER_FILE, "w", newline="") as file:
        fieldnames = ["id", "name", "email", "borrowed"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for member_id, data in members.items():
            writer.writerow({
                "id": member_id,
                "name": data["name"],
                "email": data["email"],
                "borrowed": ";".join(data["borrowed"])
            })

    with open(BOOK_FILE, "w", newline="") as file:
        fieldnames = ["id", "title", "author", "category", "status"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for book_id, data in books.items():
            writer.writerow({
                "id": book_id,
                "title": data["title"],
                "author": data["author"],
                "category": data["category"],
                "status": data["status"]
            })

    with open(TRANSACTION_FILE, "w", newline="") as file:
        fieldnames = [
            "member_id", "book_id", "issue_date",
            "due_date", "return_date", "status"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for transaction in transactions:
            writer.writerow(transaction)


# ---------------- VALIDATION ----------------

def get_non_empty(prompt):

    while True:
        value = input(prompt).strip()

        if value == "":
            print("Input cannot be empty.")
        else:
            return value


def get_member_id():

    member_id = get_non_empty("Enter Member ID: ")

    if member_id not in members:
        raise MemberNotFoundError("Member not found.")

    return member_id


def get_book_id():

    book_id = get_non_empty("Enter Book ID: ")

    if book_id not in books:
        raise BookNotFoundError("Book not found.")

    return book_id


# ---------------- MEMBER MANAGEMENT ----------------

def register_member():

    member_id = get_non_empty("Enter Member ID: ")

    if member_id in members:
        print("Member already exists.")
        return

    name = get_non_empty("Enter Member Name: ")
    email = get_non_empty("Enter Email: ")

    members[member_id] = {
        "name": name,
        "email": email,
        "borrowed": []
    }

    save_data()

    print("Member registered successfully.")


def search_member():

    keyword = get_non_empty("Enter member ID or name: ").lower()

    found = False

    for member_id, data in members.items():

        if (keyword in member_id.lower() or
                keyword in data["name"].lower()):

            print("\nMember ID :", member_id)
            print("Name      :", data["name"])
            print("Email     :", data["email"])
            print("Borrowed  :", data["borrowed"])

            found = True

    if not found:
        print("No member found.")


# ---------------- BOOK MANAGEMENT ----------------

def add_book():

    book_id = get_non_empty("Enter Book ID: ")

    if book_id in books:
        print("Book already exists.")
        return

    title = get_non_empty("Enter Book Title: ")
    author = get_non_empty("Enter Author: ")

    print("\nCategories:")
    for category in categories:
        print("-", category)

    category = get_non_empty("Enter Category: ")

    if category not in categories:
        print("Invalid category.")
        return

    books[book_id] = {
        "title": title,
        "author": author,
        "category": category,
        "status": "Available"
    }

    save_data()

    print("Book added successfully.")


def update_book():

    try:
        book_id = get_book_id()

        print("Current Title:", books[book_id]["title"])

        title = input("Enter new title (press Enter to keep old): ")

        if title.strip():
            books[book_id]["title"] = title

        author = input("Enter new author (press Enter to keep old): ")

        if author.strip():
            books[book_id]["author"] = author

        save_data()

        print("Book details updated.")

    except LibraryError as e:
        print("Error:", e)


def search_book():

    keyword = get_non_empty("Enter title, author or category: ").lower()

    found = False

    for book_id, data in books.items():

        if (keyword in data["title"].lower() or
                keyword in data["author"].lower() or
                keyword in data["category"].lower()):

            print("\nBook ID :", book_id)
            print("Title   :", data["title"])
            print("Author  :", data["author"])
            print("Category:", data["category"])
            print("Status  :", data["status"])

            found = True

    if not found:
        print("No books found.")


# ---------------- ISSUE BOOK ----------------

def issue_book():

    try:
        member_id = get_member_id()
        book_id = get_book_id()

        book = books[book_id]

        if book["status"] != "Available":
            raise BookUnavailableError(
                "Book is not available for lending."
            )

        issue_date = date.today()
        due_date = issue_date + timedelta(days=14)

        book["status"] = "Issued"

        members[member_id]["borrowed"].append(book_id)

        transactions.append({
            "member_id": member_id,
            "book_id": book_id,
            "issue_date": issue_date.isoformat(),
            "due_date": due_date.isoformat(),
            "return_date": "",
            "status": "Issued"
        })

        save_data()

        print("\nBook issued successfully.")
        print("Issue Date:", issue_date)
        print("Due Date  :", due_date)

    except LibraryError as e:
        print("Error:", e)


# ---------------- RETURN BOOK ----------------

def return_book():

    try:
        member_id = get_member_id()
        book_id = get_book_id()

        active_transaction = None

        for transaction in transactions:

            if (transaction["member_id"] == member_id and
                    transaction["book_id"] == book_id and
                    transaction["status"] == "Issued"):

                active_transaction = transaction
                break

        if active_transaction is None:
            raise LibraryError(
                "No active lending transaction found."
            )

        return_date = date.today()

        due_date = datetime.strptime(
            active_transaction["due_date"],
            "%Y-%m-%d"
        ).date()

        overdue_days = (return_date - due_date).days

        if overdue_days < 0:
            overdue_days = 0

        active_transaction["return_date"] = return_date.isoformat()

        if overdue_days > 0:
            active_transaction["status"] = "Overdue"
        else:
            active_transaction["status"] = "Returned"

        books[book_id]["status"] = "Available"

        if book_id in members[member_id]["borrowed"]:
            members[member_id]["borrowed"].remove(book_id)

        save_data()

        print("\nBook returned successfully.")
        print("Return Date :", return_date)
        print("Overdue Days:", overdue_days)

        if overdue_days > 0:
            fine = overdue_days * 5
            print("Fine        : Rs.", fine)

    except LibraryError as e:
        print("Error:", e)


# ---------------- LOST BOOK ----------------

def mark_lost():

    try:
        book_id = get_book_id()

        books[book_id]["status"] = "Lost"
        lost_books.add(book_id)

        save_data()

        print("Book marked as Lost.")

    except LibraryError as e:
        print("Error:", e)


# ---------------- AVAILABILITY ----------------

def check_availability():

    try:
        book_id = get_book_id()

        print("\nBook:", books[book_id]["title"])
        print("Status:", books[book_id]["status"])

    except LibraryError as e:
        print("Error:", e)


# ---------------- OVERDUE BOOKS ----------------

def overdue_books():

    today = date.today()
    found = False

    print("\n========== OVERDUE BOOKS ==========")

    for transaction in transactions:

        if transaction["status"] == "Issued":

            due_date = datetime.strptime(
                transaction["due_date"],
                "%Y-%m-%d"
            ).date()

            overdue = (today - due_date).days

            if overdue > 0:

                book_id = transaction["book_id"]
                member_id = transaction["member_id"]

                print(
                    "Book:", book_id,
                    "| Member:", member_id,
                    "| Overdue Days:", overdue
                )

                found = True

    if not found:
        print("No overdue books.")


# ---------------- FREQUENTLY BORROWED ----------------

def frequent_books():

    count = {}

    for transaction in transactions:

        book_id = transaction["book_id"]

        count[book_id] = count.get(book_id, 0) + 1

    if not count:
        print("No borrowing records available.")
        return

    sorted_books = sorted(
        count.items(),
        key=lambda x: x[1],
        reverse=True
    )

    print("\n====== FREQUENTLY BORROWED BOOKS ======")

    for book_id, number in sorted_books:

        if book_id in books:
            print(
                book_id,
                "-",
                books[book_id]["title"],
                "- Borrowed",
                number,
                "times"
            )


# ---------------- REPORT ----------------

def library_report():

    total_books = len(books)
    total_members = len(members)

    available = 0
    issued = 0
    lost = 0

    for data in books.values():

        if data["status"] == "Available":
            available += 1

        elif data["status"] == "Issued":
            issued += 1

        elif data["status"] == "Lost":
            lost += 1

    returned = 0
    overdue = 0

    for transaction in transactions:

        if transaction["status"] == "Returned":
            returned += 1

        elif transaction["status"] == "Overdue":
            overdue += 1

    print("\n====================================")
    print("       LIBRARY UTILIZATION REPORT")
    print("====================================")

    print("Total Books       :", total_books)
    print("Available Books   :", available)
    print("Issued Books      :", issued)
    print("Lost Books        :", lost)

    print("------------------------------------")

    print("Total Members     :", total_members)
    print("Total Transactions:", len(transactions))
    print("Returned Books    :", returned)
    print("Overdue Returns   :", overdue)

    print("------------------------------------")

    if total_books > 0:
        utilization = (issued / total_books) * 100
        print("Current Utilization:",
              round(utilization, 2), "%")
    else:
        print("Current Utilization: 0%")

    print("====================================")


# ---------------- MAIN MENU ----------------

def menu():

    load_data()

    while True:

        print("\n")
        print("==========================================")
        print("       UNIVERSITY LIBRARY SYSTEM")
        print("==========================================")
        print("1. Register Member")
        print("2. Add Book")
        print("3. Update Book")
        print("4. Search Book")
        print("5. Search Member")
        print("6. Issue Book")
        print("7. Return Book")
        print("8. Check Book Availability")
        print("9. Mark Book as Lost")
        print("10. View Overdue Books")
        print("11. Frequently Borrowed Books")
        print("12. Library Utilization Report")
        print("13. Exit")
        print("==========================================")

        choice = input("Enter your choice: ")

        try:

            if choice == "1":
                register_member()

            elif choice == "2":
                add_book()

            elif choice == "3":
                update_book()

            elif choice == "4":
                search_book()

            elif choice == "5":
                search_member()

            elif choice == "6":
                issue_book()

            elif choice == "7":
                return_book()

            elif choice == "8":
                check_availability()

            elif choice == "9":
                mark_lost()

            elif choice == "10":
                overdue_books()

            elif choice == "11":
                frequent_books()

            elif choice == "12":
                library_report()

            elif choice == "13":
                save_data()
                print("Data saved successfully.")
                print("Thank you for using the Library System.")
                break

            else:
                print("Invalid choice. Please enter 1-13.")

        except Exception as e:
            print("Unexpected error:", e)


# ---------------- PROGRAM START ----------------

menu()
