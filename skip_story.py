import pyautogui
import time

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


def skip_story(timeout=60):
    start_time = time.time()
    while True:
        try:
            # Check for step_one, step_two, and step_three
            step_one = pyautogui.locateCenterOnScreen(get_img_path("5"), confidence=0.75)
            if step_one is not None:
                time.sleep(0.25)
                click("5")

            step_two = pyautogui.locateCenterOnScreen(get_img_path("6"), confidence=0.75)
            if step_two is not None:
                time.sleep(0.25)
                click("6")
            else:
                time.sleep(0.25)
                click("5")
                click("6")

            step_three = pyautogui.locateCenterOnScreen(get_img_path("7"), confidence=0.75)
            if step_three is not None:
                time.sleep(0.25)
                click("7")
                return False  # Step_three found, indicating completion
        

        except pyautogui.ImageNotFoundException:
            try:
                step_four = pyautogui.locateCenterOnScreen(get_img_path("8"), confidence=0.75)
                if step_four is not None:
                    time.sleep(0.5)
                    click("8")
                    return True  # Step_four found, indicating completion
            except pyautogui.ImageNotFoundException:
                pass
            pass  # Continue the loop if the image is not found

        if time.time() - start_time > timeout:
            print("Timeout reached. Moving on.")
            return False  # Timeout reached, indicating failure to complete

        time.sleep(0.25)  # Short delay before the next iteration



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


def wait_and_click():
    start_time = time.time()
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
                click_pos(1405, 540)
                break
        except pyautogui.ImageNotFoundException:
            pass


    click("3")
    time.sleep(0.25)
    click_pos(1280, 1010)

    while not skip_story():
        pass

    while True:
        try:
            img_location = pyautogui.locateCenterOnScreen(get_img_path("10"), confidence=0.7)
            # img_location = pyautogui.locateCenterOnScreen(get_img_path("13"), confidence=0.7)
            if img_location is not None:
                click_pos(395, 355)
                click_pos(395, 500)
                click_pos(395, 355)
                click_pos(382, 253)
                break

        except pyautogui.ImageNotFoundException:
            pass

    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    print(f"Elapsed Time: {minutes} minutes, {seconds} seconds")
    

for i in range(150):
    print("Count: ", i + 1)
    time.sleep(0.25)
    wait_and_click()
    time.sleep(0.25)
