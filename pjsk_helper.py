import random
import string
import time

import io
import pyautogui
from PIL import Image
import win32clipboard


def generate_string_with_first_lowercase(input_string):
    # Take the first character of the input string
    first_letter = input_string[0]

    # Check if the first character is a lowercase letter
    if not first_letter.isalpha() or not first_letter.islower():
        first_letter = input("Enter first letter: ")

    # Generate 7 random lowercase letters
    random_chars = ''.join(random.choices(string.ascii_lowercase, k=7))

    # Combine the first letter with the random characters
    result_string = first_letter + random_chars
    return result_string


def capture_and_copy_to_clipboard():
    # Capture the specified region of the screen
    screenshot = pyautogui.screenshot(region=(320, 197, 1920, 1080))

    output = io.BytesIO()
    screenshot.save(output, format='BMP')
    data = output.getvalue()[14:]  # The file header off-set for BMP files is 14 bytes
    output.close()

    # Open the clipboard and empty it
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    
    # Set the clipboard data
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

    print("Screenshot taken and copied to clipboard.")


def print_mouse_position(interval=1):
    try:
        while True:
            # Get the current mouse position
            x, y = pyautogui.position()
            position_str = f"X: {x} Y: {y}"
            
            # Clear the console and print the current position
            print(position_str, end='\r')
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nDone.")


def click(x, y, times=1):
    for _ in range(times):
        pyautogui.click(x, y)
        time.sleep(0.5)


def automate_login(user_id, pwd):
    # Click on the window at the specified position
    pyautogui.click(x=2170, y=250)
    time.sleep(2)

    # Perform a series of clicks and waits
    click(x=1040, y=620)
    click(x=1500, y=650)
    
    # Paste the user_id
    click(x=1247, y=687)
    pyautogui.write(user_id)
    time.sleep(0.5)
    
    click(x=2028, y=822) # click somewhere

    # Paste the pwd 
    click(x=1336, y=775)
    pyautogui.write(pwd)
    time.sleep(0.5)
    
    click(x=1128, y=822) # click somewhere
    click(x=1457, y=993)
    time.sleep(0.5)
    click(x=1457, y=993)
    time.sleep(0.25)

    # Click somewhere four times
    for _ in range(4):
        time.sleep(0.25)
        click(x=2011, y=720)  # Clicks at the current mouse position


def screenshot():
    # click(1280, 1006)
    # click(2040, 265) # close announce

    click(1470, 1174)
    click(1711, 1119)
    time.sleep(1.25)
    capture_and_copy_to_clipboard()
    

def generate_pwd(string):
    click(2177, 257)
    click(1888, 951)
    click(1481, 676)
    time.sleep(1)

    click(1367, 676)

    random_string = generate_string_with_first_lowercase(string)
    pyautogui.write(random_string)
    time.sleep(1)

    click(1452, 1017, times=2) # submit
    click(1457, 830)
    time.sleep(1)
    click(1649, 658) # copy

    time.sleep(1)

    click(1975, 696, times=3)

    time.sleep(1)

    click(2171, 268)
    click(1467, 939)
    time.sleep(2)

    click(1280, 1171)
    time.sleep(1)

    click(1583, 1198)
    click(2040, 1198)
    click(1446, 1009)
    time.sleep(1)

    click(1235, 1004)

    time.sleep(2)
    click(2171, 268)
    time.sleep(0.5)
    click(1881, 1101)


def parse_account_details(account_string):
    accounts_dict = {}
    lines = account_string.split('\n')
    current_username = None

    for line in lines:
        if line.startswith('账号：'):
            current_username = line.split('：')[1]
        elif line.startswith('密码：') and current_username:
            accounts_dict[current_username] = line.split('：')[1]

    return accounts_dict


def parse_account_simple(input_list):
    account_dict = {}
    for item in input_list:
        # Split each string by comma
        parts = item.split(',')
        if len(parts) == 2:
            username, password = parts
            account_dict[username] = password
    return account_dict


def split_username_password(input_string):
    # Split the string by lines
    lines = input_string.split('\n')

    # Initialize variables for username and password
    username = None
    password = None

    for line in lines:
        # Check for username line
        if "引き継ぎID :" in line:
            username = line.split(': ')[1]

        # Check for password line
        elif "パスワード :" in line:
            password = line.split(': ')[1]

    # Return as a dictionary with username as key and password as value
    return {username: password} if username and password else {}


# --------------------------------------------------

account_details = ''''''


def main():

    accounts = parse_account_simple(account_details)

    while True:
        choice = input("Do you want to use account list (1/2): ")
        if (choice == '1'):
            index = input("Enter account index: ")
            index = int(index)
            username, password = list(accounts.items())[index]
        elif (choice == '2'):
            account = split_username_password("")
            username = list(account.keys())[0]
            password = account[username]

        while True:
            print("Username:", username)
            print("Password:", password)

            choice = input("Enter 1 to automate login, 2 to take a screenshot, 3 to generate a password, or 4 to change account/exit: ")
            if choice == '1':
                automate_login(username, password)
            elif choice == '2':
                screenshot()
            elif choice == '3':
                generate_pwd(password)
            elif choice == '4':
                break  # Breaks the inner loop, leading to account change or exit
            else:
                print("Invalid input. Please enter 1, 2, 3, or 4.")
            
            print("Action completed. Choose another action or change account/exit.")

        # Ask if user wants to continue with a new account or exit the program
        continue_choice = input("Do you want to continue with a new account? (1/2): ").strip().lower()
        if continue_choice != '1':
            print("Exiting the program.")
            break  # Breaks the outer loop, exiting the program

main()