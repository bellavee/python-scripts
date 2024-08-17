import tkinter as tk
from tkinter import scrolledtext
import pyperclip


def parse_accounts(account_string):
    accounts_dict = {}
    lines = account_string.split('\n')
    current_username = None

    username_keys = ['ID：', '卡号：', '引继码：', '引き継ぎID : ']
    password_keys = ['PASS：', '密码：', 'パスワード:', 'パスワード :']

    for line in lines:
        line = line.strip()

        for key in username_keys:
            if key in line:
                current_username = line.split(key)[-1].strip()
                break

        for key in password_keys:
            if key in line:
                line = line.replace('パスワード :', '').replace('PASS：', '')
                if current_username:
                    password = line.split(key)[-1].strip()
                    accounts_dict[current_username] = password
                    current_username = None
                break

    return accounts_dict


def select_account(event):
    widget = event.widget
    index = int(widget.curselection()[0])
    value = widget.get(index)
    username, password = value.split(' - ')

    clipboard_content = f"引き継ぎID : {username}\nパスワード : {password}"
    pyperclip.copy(clipboard_content)
    status_label.config(text="Copied to clipboard!")


def format_accounts():
    account_string = input_text.get("1.0", tk.END)
    accounts = parse_accounts(account_string)

    account_list.delete(0, tk.END)
    for username, password in accounts.items():
        account_list.insert(tk.END, f"{username} - {password}")

    status_label.config(text="Accounts formatted!")


# Create main window
root = tk.Tk()
root.title("Account Formatter")

# Create and pack widgets
input_text = scrolledtext.ScrolledText(root, width=50, height=10)
input_text.pack(padx=10, pady=10)

format_button = tk.Button(root, text="Format Accounts", command=format_accounts)
format_button.pack(pady=5)

account_list = tk.Listbox(root, width=50)
account_list.pack(padx=10, pady=10)
account_list.bind('<<ListboxSelect>>', select_account)

status_label = tk.Label(root, text="")
status_label.pack(pady=5)

# Start the GUI event loop
root.mainloop()