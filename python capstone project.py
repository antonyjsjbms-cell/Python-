
import tkinter as tk
from tkinter import messagebox
import base64
import os


# ==========================================
# SETTINGS
# ==========================================

MASTER_PASSWORD = "admin123"
ENCRYPTION_KEY = "MySecretKey123"
FILE_NAME = "passwords.txt"


# ==========================================
# ENCRYPTION
# ==========================================

def encrypt(text):
    result = ""

    for i in range(len(text)):
        result = result + chr(
            ord(text[i]) ^
            ord(ENCRYPTION_KEY[i % len(ENCRYPTION_KEY)])
        )

    return base64.b64encode(result.encode()).decode()


# ==========================================
# DECRYPTION
# ==========================================

def decrypt(text):
    try:
        decoded = base64.b64decode(text).decode()

        result = ""

        for i in range(len(decoded)):
            result = result + chr(
                ord(decoded[i]) ^
                ord(ENCRYPTION_KEY[i % len(ENCRYPTION_KEY)])
            )

        return result

    except:
        return "Error"


# ==========================================
# SAVE PASSWORD
# ==========================================

def save_password():

    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if website == "" or username == "" or password == "":
        messagebox.showwarning(
            "Warning",
            "Please fill all fields."
        )
        return

    encrypted = encrypt(password)

    with open(FILE_NAME, "a") as file:
        file.write(
            website + "|" +
            username + "|" +
            encrypted + "\n"
        )

    messagebox.showinfo(
        "Success",
        "Password saved successfully!"
    )

    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


# ==========================================
# VIEW PASSWORDS
# ==========================================

def view_passwords():

    master = master_entry.get()

    if master != MASTER_PASSWORD:
        messagebox.showerror(
            "Error",
            "Wrong Master Password!"
        )
        return

    if not os.path.exists(FILE_NAME):
        messagebox.showinfo(
            "Information",
            "No passwords stored."
        )
        return

    window = tk.Toplevel(root)
    window.title("Stored Passwords")
    window.geometry("750x400")

    tk.Label(
        window,
        text="STORED PASSWORDS",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    listbox = tk.Listbox(
        window,
        width=110,
        height=15
    )
    listbox.pack(padx=10, pady=10)

    with open(FILE_NAME, "r") as file:

        for line in file:

            data = line.strip().split("|")

            if len(data) == 3:

                website = data[0]
                username = data[1]
                encrypted = data[2]

                password = decrypt(encrypted)

                information = (
                    "Website: " + website +
                    " | Username: " + username +
                    " | Password: " + password
                )

                listbox.insert(
                    tk.END,
                    information
                )


# ==========================================
# DELETE PASSWORD
# ==========================================

def delete_password():

    master = master_entry.get()

    if master != MASTER_PASSWORD:
        messagebox.showerror(
            "Error",
            "Wrong Master Password!"
        )
        return

    if not os.path.exists(FILE_NAME):
        messagebox.showinfo(
            "Information",
            "No passwords stored."
        )
        return

    window = tk.Toplevel(root)
    window.title("Delete Password")
    window.geometry("750x400")

    tk.Label(
        window,
        text="SELECT PASSWORD TO DELETE",
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    listbox = tk.Listbox(
        window,
        width=110,
        height=15
    )
    listbox.pack(padx=10, pady=10)

    records = []

    with open(FILE_NAME, "r") as file:

        for line in file:

            data = line.strip().split("|")

            if len(data) == 3:

                website = data[0]
                username = data[1]
                encrypted = data[2]

                password = decrypt(encrypted)

                display = (
                    "Website: " + website +
                    " | Username: " + username +
                    " | Password: " + password
                )

                listbox.insert(
                    tk.END,
                    display
                )

                records.append(line)

    def delete_selected():

        selected = listbox.curselection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select a password."
            )
            return

        index = selected[0]

        confirm = messagebox.askyesno(
            "Confirm",
            "Delete this password?"
        )

        if confirm:

            del records[index]

            with open(FILE_NAME, "w") as file:
                for record in records:
                    file.write(record)

            listbox.delete(index)

            messagebox.showinfo(
                "Success",
                "Password deleted successfully!"
            )

    tk.Button(
        window,
        text="DELETE SELECTED",
        command=delete_selected,
        width=25,
        height=2
    ).pack(pady=10)


# ==========================================
# CLEAR
# ==========================================

def clear_fields():

    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    master_entry.delete(0, tk.END)


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()

root.title("Password Manager")
root.geometry("500x550")
root.resizable(False, False)


# ==========================================
# TITLE
# ==========================================

tk.Label(
    root,
    text="PASSWORD MANAGER",
    font=("Arial", 22, "bold")
).pack(pady=20)


# ==========================================
# WEBSITE
# ==========================================

tk.Label(
    root,
    text="Website",
    font=("Arial", 12)
).pack()

website_entry = tk.Entry(
    root,
    width=40,
    font=("Arial", 12)
)
website_entry.pack(pady=5)


# ==========================================
# USERNAME
# ==========================================

tk.Label(
    root,
    text="Username",
    font=("Arial", 12)
).pack()

username_entry = tk.Entry(
    root,
    width=40,
    font=("Arial", 12)
)
username_entry.pack(pady=5)


# ==========================================
# PASSWORD
# ==========================================

tk.Label(
    root,
    text="Password",
    font=("Arial", 12)
).pack()

password_entry = tk.Entry(
    root,
    width=40,
    font=("Arial", 12),
    show="*"
)
password_entry.pack(pady=5)


# ==========================================
# MASTER PASSWORD
# ==========================================

tk.Label(
    root,
    text="Master Password",
    font=("Arial", 12)
).pack(pady=(15, 0))

master_entry = tk.Entry(
    root,
    width=40,
    font=("Arial", 12),
    show="*"
)
master_entry.pack(pady=5)


# ==========================================
# BUTTONS
# ==========================================

tk.Button(
    root,
    text="SAVE PASSWORD",
    command=save_password,
    width=25,
    height=2
).pack(pady=7)


tk.Button(
    root,
    text="VIEW PASSWORDS",
    command=view_passwords,
    width=25,
    height=2
).pack(pady=7)


tk.Button(
    root,
    text="DELETE PASSWORD",
    command=delete_password,
    width=25,
    height=2
).pack(pady=7)


tk.Button(
    root,
    text="CLEAR",
    command=clear_fields,
    width=25,
    height=2
).pack(pady=7)


# ==========================================
# START PROGRAM
# ==========================================

root.mainloop()

