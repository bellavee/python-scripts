import pyautogui
import time
import random

import keyboard

def get_img_path(img_name):
    return "img/" + img_name + ".png"

def click(img_name, conf=0.75, timeout=60):
    start_time = time.time()
    while True:
        try:
            img_location = pyautogui.locateCenterOnScreen(get_img_path(img_name), confidence=conf)
            if img_location is not None:
                pyautogui.moveTo(img_location.x, img_location.y, duration=0.1)
                pyautogui.leftClick()
                break
        except pyautogui.ImageNotFoundException:
            pass  # Continue the loop if the image is not found

        if time.time() - start_time > timeout:
            print(f"Timeout reached: Image {img_name} not found.")
            break
        time.sleep(0.25)

def click_pos(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.leftClick()
    time.sleep(0.25)


def random_click(start, end):
    x = random.randint(start[0], end[0])
    y = random.randint(start[1], end[1])

    # Move the mouse to the random position and click
    pyautogui.moveTo(x, y, duration=0)  # Move with a slight delay
    pyautogui.click()

    # Wait for a random time interval
    time.sleep(random.uniform(0.0, 0.05))


def read_story():
    start_time = time.time()
    pyautogui.PAUSE = 0.001
    while True:
        try:
            # Check for step_one, step_two, and step_three
            step_one = pyautogui.locateCenterOnScreen(get_img_path("5"), confidence=0.75)
            if step_one is not None:
                random_click((1942, 751), (1963, 786))

                try:
                    if keyboard.is_pressed('esc'):  # it will stop working by clicking q you can change to to any key
                        print("break")
                        break
                    else:
                        pass
                finally:
                    pass

        except pyautogui.ImageNotFoundException:
            try:
                img_location = pyautogui.locateCenterOnScreen(get_img_path("10"), confidence=0.7)
                if img_location is not None:
                    elapsed_time = time.time() - start_time
                    minutes = int(elapsed_time // 60)
                    seconds = int(elapsed_time % 60)
                    print(f"Elapsed Time: {minutes} minutes, {seconds} seconds")
                    return True
            except pyautogui.ImageNotFoundException:
                pass
            pass  # Continue the loop if the image is not found



def wait_for_image(img_name, timeout=60):
    start_time = time.time()
    while True:
        try:
            img_location = pyautogui.locateCenterOnScreen(get_img_path(img_name), confidence=0.7)
            if img_location is not None:
                return img_location

        except pyautogui.ImageNotFoundException as e:
            pass # Continue the loop if the image is not found
        if time.time() - start_time > timeout:
            print(f"Timeout reached: Image {img_name} not found.")
            return None
        time.sleep(0.25)


def main():
    start_btn = wait_for_image("1")
    if start_btn:
        pyautogui.click(660, 505)
        time.sleep(0.25)
        pyautogui.click(start_btn)
        time.sleep(0.25)

    while True:
        try:
            chapter_screen = pyautogui.locateCenterOnScreen(get_img_path("10"), confidence=0.7)
            if chapter_screen is not None:
                pyautogui.moveTo(1627, 775)
                pyautogui.scroll(-5000)
                pyautogui.scroll(-5000)
                time.sleep(2)
                click_pos(1398, 1140)
                break
        except pyautogui.ImageNotFoundException:
            pass


    click("3")
    time.sleep(0.25)
    click_pos(1280, 1010)

    while not read_story():
        try:
            if keyboard.is_pressed('esc'):  # it will stop working by clicking q you can change to to any key
                print("break")
                break
            else:
                pass
        finally:
            pass
        pass

    while True:
        try:
            img_location = pyautogui.locateCenterOnScreen(get_img_path("10"), confidence=0.7)
            if img_location is not None:
                click_pos(395, 355)
                click_pos(395, 500)
                click_pos(395, 355)
                click_pos(382, 253)
                break
        except pyautogui.ImageNotFoundException:
            pass
    

for i in range(150):
    print("Count: ", i + 1)
    time.sleep(0.25)
    main()
    time.sleep(0.25)
