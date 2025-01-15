import time
import keyboard
import pyautogui


# get the mouse curser position when the 'ctrl' key is pressed.
def get_coordinates(Button = None, Key = 'ctrl', ):

    # Print user instruction
    if Button == None:
        print(f'press "{Key}" key to lock position...')
    else:
        print(f'press "{Key}" key to lock position of the "{Button}" button...')

    # Check if x key is pressed
    timeout_soft_limit = 5 # seconds
    timeout_hard_limit = 60 # seconds
    timeout_start = time.time()
    while True:
        
        time.sleep(0.1)

        # Timeout logic
        if time.time() > timeout_start + timeout_soft_limit:
            print(f'Function time out. Set cursor position within {timeout_soft_limit} seconds')
            return None, None

        # Get the current mouse position
        if keyboard.is_pressed(Key):
            x, y = pyautogui.position()
            print(f'spam at position: {x}, {y}')
            print(f'{Key} key pressed...')
            break
    
    time.sleep(0.5)

    return x, y


def click(coordinates):
    time.sleep(0.5)
    pyautogui.click(coordinates)
    time.sleep(0.5)

