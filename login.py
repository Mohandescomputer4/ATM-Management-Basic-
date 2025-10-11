from tkinter.ttk import Treeview
from databasework import *
from tkinter import Label, Button, Entry, Toplevel, messagebox

def login(username, password, parent_window):
    if username == 'admin' and password == '1234':
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        dashboard = Toplevel(parent_window)
        dashboard.title('Bank Dashboard')

        columns = ("id", "full_name", "Balance", "Account number", "Condition", "Opening date", "National number",
                   "Phone number")
        accounts_treeview = Treeview(dashboard, columns=columns, show="headings")
        for col in columns:
            accounts_treeview.heading(col, text=col)
            accounts_treeview.column(col, width=150, anchor="center")

        accounts_treeview.grid(row=1, column=1, columnspan=15, rowspan=15, sticky="nsew", padx=5, pady=5)

        def refresh_treeview(accounts=None):
            for item in accounts_treeview.get_children():
                accounts_treeview.delete(item)

            if accounts is None:
                accounts = get_account_list()

            for account in accounts:
                accounts_treeview.insert('', 'end', values=(
                    account.id,
                    account.full_name,
                    account.balance,
                    account.account_number,
                    account.condition,
                    account.opening_date,
                    account.national_number,
                    account.phone_number
                ))
        refresh_treeview()

        search_entry = Entry(dashboard)
        search_entry.grid(row=0, column=1, columnspan=5, sticky="we", padx=5, pady=5)
        search_button = Button(dashboard, text="Search", command=lambda: refresh_treeview(search_account(search_entry.get())))
        search_button.grid(row=0, column=6, sticky="we", padx=5, pady=5)

        def add_account_window():
            win = Toplevel(dashboard)
            win.title("Add Account")
            labels = ["Full Name","Balance","Account Number","Condition","Opening Date","National Number","Phone Number"]
            entries = []
            for i, text in enumerate(labels):
                Label(win, text=text).grid(row=i, column=0)
                e = Entry(win)
                e.grid(row=i, column=1)
                entries.append(e)
            def save():
                try:
                    create_account(
                        entries[0].get(),
                        float(entries[1].get()),
                        entries[2].get(),
                        entries[3].get(),
                        entries[4].get(),
                        entries[5].get(),
                        entries[6].get()
                    )
                    messagebox.showinfo("Success","Account Created!")
                    win.destroy()
                    refresh_treeview()
                except ValueError:
                    messagebox.showerror("Error","Enter valid numeric values for balance!")
            Button(win, text="Save", command=save).grid(row=len(labels), column=0, columnspan=2)

        def edit_account_window():
            selected = accounts_treeview.focus()
            if not selected:
                messagebox.showerror("Error", "Select an account first!")
                return
            values = accounts_treeview.item(selected, "values")
            account_id = values[0]
            win = Toplevel(dashboard)
            win.title("Edit Account")
            labels = ["Full Name","Balance","Account Number","Condition","Opening Date","National Number","Phone Number"]
            entries = []
            indices = [1, 2, 3, 4, 5, 6, 7]
            for i, text in enumerate(labels):
                Label(win, text=text).grid(row=i, column=0)
                e = Entry(win)
                e.insert(0, values[indices[i]])
                e.grid(row=i, column=1)
                entries.append(e)

            def save():
                try:
                    update_account(
                        account_id,
                        entries[0].get(),
                        float(entries[1].get()),
                        entries[2].get(),
                        entries[3].get(),
                        entries[4].get(),
                        entries[5].get(),
                        entries[6].get()
                    )
                    messagebox.showinfo("Success","Account Updated!")
                    win.destroy()
                    refresh_treeview()
                except ValueError:
                    messagebox.showerror("Error","Enter valid numeric values for balance!")
            Button(win, text="Save", command=save).grid(row=len(labels), column=0, columnspan=2)

        def delete_selected_account():
            selected = accounts_treeview.focus()
            if not selected:
                messagebox.showerror("Error", "Select an account first!")
                return
            account_id = accounts_treeview.item(selected, "values")[0]
            delete_account(account_id)
            messagebox.showinfo("Deleted","Account Deleted!")
            refresh_treeview()

        def deposit_window():
            selected = accounts_treeview.focus()
            if not selected:
                messagebox.showerror("Error", "Select an account first!")
                return
            values = accounts_treeview.item(selected, "values")
            account_id = values[0]
            current_balance = float(values[2])

            win = Toplevel(dashboard)
            win.title("Deposit")
            Label(win, text=f"Current Balance: {current_balance}").grid(row=0, column=0, columnspan=2)
            Label(win, text="Amount to deposit:").grid(row=1, column=0)
            amount_entry = Entry(win)
            amount_entry.grid(row=1, column=1)

            def save():
                try:
                    amount = float(amount_entry.get())
                    new_balance = current_balance + amount
                    update_account(account_id, values[1], new_balance, values[3], values[4], values[5], values[6], values[7])
                    messagebox.showinfo("Success", f"Deposited {amount} successfully!")
                    win.destroy()
                    refresh_treeview()
                except ValueError:
                    messagebox.showerror("Error", "Enter a valid number!")
            Button(win, text="Deposit", command=save).grid(row=2, column=0, columnspan=2)

        def withdraw_window():
            selected = accounts_treeview.focus()
            if not selected:
                messagebox.showerror("Error", "Select an account first!")
                return
            values = accounts_treeview.item(selected, "values")
            account_id = values[0]
            current_balance = float(values[2])

            win = Toplevel(dashboard)
            win.title("Withdraw")
            Label(win, text=f"Current Balance: {current_balance}").grid(row=0, column=0, columnspan=2)
            Label(win, text="Amount to withdraw:").grid(row=1, column=0)
            amount_entry = Entry(win)
            amount_entry.grid(row=1, column=1)

            def save():
                try:
                    amount = float(amount_entry.get())
                    if amount > current_balance:
                        messagebox.showerror("Error", "Insufficient balance!")
                        return
                    new_balance = current_balance - amount
                    update_account(account_id, values[1], new_balance, values[3], values[4], values[5], values[6], values[7])
                    messagebox.showinfo("Success", f"Withdrew {amount} successfully!")
                    win.destroy()
                    refresh_treeview()
                except ValueError:
                    messagebox.showerror("Error", "Enter a valid number!")
            Button(win, text="Withdraw", command=save).grid(row=2, column=0, columnspan=2)

        Button(dashboard, text="Create", command=add_account_window, bg="#B6B6B8").grid(row=0, column=0, sticky="we", padx=5, pady=2)
        Button(dashboard, text="Deposit", command=deposit_window, bg="#B6B6B8").grid(row=1, column=0, sticky="we", padx=5, pady=2)
        Button(dashboard, text="Withdraw", command=withdraw_window, bg="#B6B6B8").grid(row=2, column=0, sticky="we", padx=5, pady=2)
        Button(dashboard, text="Edit", command=edit_account_window, bg="#B6B6B8").grid(row=3, column=0, sticky="we", padx=5, pady=2)
        Button(dashboard, text="Delete", command=delete_selected_account, bg="#B6B6B8").grid(row=4, column=0, sticky="we", padx=5, pady=2)

    else:
        messagebox.showerror("Login Failed", "Login Failed")

