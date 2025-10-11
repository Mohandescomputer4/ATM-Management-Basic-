from tkinter import Tk, Label, Button, Entry
from login import login

if __name__ == "__main__":
    root = Tk()
    root.title("Bank Login")

    Label(root, text="Username").grid(row=0, column=0)
    username_entry = Entry(root)
    username_entry.grid(row=0, column=1)

    Label(root, text="Password").grid(row=1, column=0)
    password_entry = Entry(root, show="*")
    password_entry.grid(row=1, column=1)

    Button(root, text="Login", command=lambda: login(username_entry.get(), password_entry.get(), root)).grid(row=2, column=0, columnspan=2, pady=5)

    root.mainloop()
