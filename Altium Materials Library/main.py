import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
import time

import Cursor as csr
import WindowManager as wm

import pyautogui


# Get the path of the CSV or TXT file containing the materials to be entered.
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title="Select the CSV or Text file containing the materials.",
    filetypes=[("CSV Files", ".csv .txt")]
    )


# Import the Material CSV.
df = pd.read_csv(file_path)

# Replace empty cells NaN with nothing.
df = df.replace({np.nan: ''})


# Bring the Altium Material Library to the foreground.
AML = wm.get_window('Altium Material Library')
wm.set_foreground(AML)


# Set the coordinates of the 'New' button.
NewButtonPosition = csr.get_coordinates('New')
print(NewButtonPosition)


# Get total number of materials to enter for progress prints.
TotalEntries = len(df.index)
#print(TotalEntries)

# While
i = 0
# Iterate through columns.
while i <  TotalEntries:
    #print(df.at[i, 'Constructions'])

    # Click New
    csr.click(NewButtonPosition)
    # Delay. Especially because the first time clicking New is slow.
    time.sleep(0.5) # UNTESTED if needed. Works but is it needed?
    
    j = 0
    # Iterate through rows.
    while j < len(df.columns):

        Value = str(df.iat[i, j])

        pyautogui.typewrite(Value, interval=0.1)
        pyautogui.press('enter')

        j += 1

    pyautogui.press('enter')
    print(f'Progress {i+1} / {TotalEntries}')

    time.sleep(0.5)

    i += 1


Print('Data entry complete')









