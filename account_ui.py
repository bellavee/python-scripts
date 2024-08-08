import random
import string
import time

import io
import os
import pyautogui
from PIL import Image
import win32clipboard
import pyperclip
import keyboard
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext


def get_img_path(img_name):
    return "img/" + img_name + ".png"


def generate_string_with_first_lowercase(input_string):
    first_letter = input_string[0]
    if not first_letter.isalpha() or not first_letter.islower():
        first_letter = input("Enter first letter: ")
    random_chars = ''.join(random.choices(string.ascii_lowercase, k=7))
    result_string = first_letter + random_chars
    return result_string


def generate_password_to_clipboard():
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(8))
    pyperclip.copy(random_string)
    return random_string


screenshot_counter = 1
def capture_and_copy_to_clipboard():
    global screenshot_counter  # Use the global counter

    # Capture the specified region of the screen
    screenshot = pyautogui.screenshot(region=(324, 198, 1920, 1080))

    # Save the screenshot to the clipboard
    output = io.BytesIO()
    screenshot.save(output, format='BMP')
    data = output.getvalue()[14:]  # The file header off-set for BMP files is 14 bytes
    output.close()

    # Open the clipboard and empty it
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

    # Check if the 'screenshots' folder exists and create it if it doesn't
    folder_path = 'screenshots'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save the screenshot as a JPEG file in the 'screenshots' folder with compression
    file_path = os.path.join(folder_path, f'screenshot_{screenshot_counter}.jpg')
    screenshot.save(file_path, format='JPEG', quality=85)  # Adjust quality for desired file size

    # Increment the counter for the next screenshot
    screenshot_counter += 1

def click(img_name, conf=0.75, timeout=60):
    start_time = time.time()
    while True:
        try:
            img_location = pyautogui.locateCenterOnScreen(get_img_path(img_name), confidence=conf)
            if img_location is not None:
                time.sleep(0.1)
                pyautogui.moveTo(img_location.x, img_location.y, duration=0.1)
                pyautogui.leftClick()
                break
        except pyautogui.ImageNotFoundException:
            pass  # Continue the loop if the image is not found

        if time.time() - start_time > timeout:
            print(f"Timeout reached: Image {img_name} not found.")
            break
        time.sleep(0.2)


def click_pos(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.leftClick()
    time.sleep(0.3)


def automate_login(user_id, pwd):
    # Click on the window at the specified position
    click("1")
    click("2")
    click("3")

    # Paste the user_id
    click("4")
    time.sleep(0.25)
    pyautogui.write(user_id, interval=0.05)
    time.sleep(0.25)

    click_pos(x=1022, y=832)  # click somewhere

    # Paste the pwd
    click("5")
    pyautogui.write(pwd, interval=0.05)
    time.sleep(0.25)

    click_pos(x=1128, y=822)  # click somewhere

    click_pos(x=1462, y=1012)
    click("7")

    # Click somewhere 4 times
    for _ in range(6):
        click_pos(x=2011, y=720)  # Clicks at the current mouse position


def screenshot():
    try:
        step_one = pyautogui.locateCenterOnScreen(get_img_path("8"), confidence=0.75)
        if step_one is not None:
            time.sleep(0.25)
            click_pos(x=2180, y=682)
            click_pos(x=2180, y=682)
    except pyautogui.ImageNotFoundException:
        click_pos(x=2180, y=782)
        pass

    click("10")
    click("11")

    time.sleep(1.25)
    capture_and_copy_to_clipboard()


def generate_pwd_change_note(string):
    click("12")
    click("13")
    click("14")
    click("15")

    random_string = generate_string_with_first_lowercase(string)
    pyautogui.write(random_string)
    click_pos(1975, 696)

    click("16")
    click("17")
    click("18")

    click_pos(1975, 696)
    click_pos(1975, 696)
    click_pos(1975, 696)

    click("12")
    click("19")

    while True:
        try:
            step_one = pyautogui.locateCenterOnScreen(get_img_path("20"), confidence=0.75)
            if step_one is not None:
                click("20")
                time.sleep(0.5)
                click("21")
                time.sleep(0.5)
                click("22")
                click("23")
                click("24")
                break
        except pyautogui.ImageNotFoundException:
            click("21")
            click("22")
            click("23")
            click("24")
            break

    click("12")
    click("25")


def generate_pwd_logout(string):
    click("12")
    click("13")
    click("14")
    click("15")

    random_string = generate_string_with_first_lowercase(string)
    pyautogui.write(random_string)
    click_pos(1975, 696)

    click("16")
    click("17")
    click("18")

    click_pos(1975, 696)
    click_pos(1975, 696)
    click_pos(1975, 696)

    click("12")
    click("25")


def parse_accounts(account_string):
    accounts_dict = {}
    lines = account_string.split('\n')
    current_username = None

    # Generalize key labels for username and password
    username_keys = ['ID：', '卡号：', '引继码：', '引き継ぎID : ']
    password_keys = ['PASS：', '密码：', 'パスワード:', 'パスワード :']

    for line in lines:
        line = line.strip()

        for key in username_keys:
            if key in line:
                current_username = line.split(key)[-1].strip()
                break  # Once a username is found, break to avoid checking other keys

        for key in password_keys:
            if key in line:
                line = line.replace('パスワード :', '').replace('PASS：', '')
                if current_username:
                    password = line.split(key)[-1].strip()
                    accounts_dict[current_username] = password
                    current_username = None  # Reset current_username to ensure pairing integrity
                break  # Once a password is found, break to avoid checking other keys

    return accounts_dict


def open_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


# --------------------------------------------------

def load_account_details():
    account_string = open_txt("account.txt")
    return parse_accounts(account_string)


def select_account(event):
    widget = event.widget
    index = int(widget.curselection()[0])
    value = widget.get(index)
    username, password = value.split(' - ')

    clipboard_content = f"引き継ぎID : {username}\nパスワード : {password}"
    pyperclip.copy(clipboard_content)


def copy(event):
    widget = event.widget
    index = int(widget.curselection()[0])
    value = widget.get(index)
    pyperclip.copy(value)


def automate_login_gui(account_info):
    if account_info:
        user_id, pwd = account_info.split(' - ')
        if user_id and pwd:
            automate_login(user_id, pwd)


def screenshot_gui():
    capture_and_copy_to_clipboard()


def generate_password_change_note_gui():
    initial_string = simpledialog.askstring("Password Note", "Enter Initial String for Password Note:")
    if initial_string:
        generate_pwd_change_note(initial_string)


def generate_password_to_clipboard_gui():
    generate_password_to_clipboard()


def main_app(accounts, version):
    root = tk.Tk()
    root.title("PJSK Account Management")
    root.geometry("500x640+3200+0")

    if version == 'Manual':
        account_listbox = tk.Listbox(root, height=20, width=50, font=('Arial Unicode MS', 12))
        for username, password in accounts.items():
            account_listbox.insert(tk.END, username)
            account_listbox.insert(tk.END, password)
            account_listbox.insert(tk.END, "\n")
        account_listbox.pack(pady=20)
        account_listbox.bind('<<ListboxSelect>>', copy)

    elif version == 'Auto':
        account_listbox = tk.Listbox(root, height=20, width=50, font=('Arial Unicode MS', 12))
        for username, password in accounts.items():
            account_listbox.insert(tk.END, f"{username} - {password}")
        account_listbox.pack(pady=20)
        account_listbox.bind('<<ListboxSelect>>', select_account)

    def handle_login():
        selection = account_listbox.curselection()
        if selection:
            account_info = account_listbox.get(selection[0])
            automate_login_gui(account_info)

    tk.Button(root, text="Automate Login", command=handle_login).pack(pady=10)
    tk.Button(root, text="Take Screenshot", command=screenshot_gui).pack(pady=10)
    tk.Button(root, text="Generate Password", command=generate_password_to_clipboard_gui).pack(pady=10)
    tk.Button(root, text="Edit Accounts", command=lambda: [root.destroy(), unified_start_window()]).pack(pady=10)

    root.mainloop()


def unified_start_window():
    def save_and_start():
        # Save the text area content to account.txt
        with open("account.txt", "w", encoding="utf-8") as file:
            file.write(text_area.get("1.0", tk.END).strip())

        # Load the accounts and start the main app
        version = var.get()
        accounts = load_account_details()
        unified_root.destroy()
        main_app(accounts, version)

    unified_root = tk.Tk()
    unified_root.title("Account Management Setup")
    unified_root.geometry("600x600+3200+0")

    # Text area for account editing
    text_area = scrolledtext.ScrolledText(unified_root, font=('Arial Unicode MS', 12), height=20)
    text_area.pack(padx=10, pady=10, fill='both', expand=True)

    # Check if account.txt exists, if not create it
    if not os.path.exists("account.txt"):
        with open("account.txt", "w", encoding="utf-8") as file:
            file.write("")  # Create an empty account.txt file

    # Load the existing content from account.txt into the text area
    with open("account.txt", "r", encoding="utf-8") as file:
        text_area.insert(tk.END, file.read())

    # version selection
    var = tk.StringVar(value="Auto")
    tk.Label(unified_root, text="Select version:", font=('Arial Unicode MS', 12)).pack()
    tk.Radiobutton(unified_root, text="Auto", variable=var, value="Auto", font=('Arial Unicode MS', 12)).pack()
    tk.Radiobutton(unified_root, text="Manual", variable=var, value="Manual", font=('Arial Unicode MS', 12)).pack()

    # Control buttons
    tk.Button(unified_root, text="Start", command=save_and_start, font=('Arial Unicode MS', 12)).pack(pady=20)

    unified_root.mainloop()



if __name__ == '__main__':
    unified_start_window()
