import pyautogui
import pygetwindow as gw

def get_window(Program):
    Handle = gw.getWindowsWithTitle(Program)
    Handle = Handle[0]
    return Handle

def set_foreground(Program_Handle):
    # Some versions of Windows require the 'alt' key to be pressed before activate() will work.
    pyautogui.press('altleft')
    Program_Handle.activate()




#class window_manager:
#    def __init__ (self):
#        """Constructor"""
#        self._handle = None
#    def find_window(self, Program):
#        Handle = gw.getWindowsWithTitle(Program)
#        Handle = Handle[0]
#        return Handle
#    def set_foreground(self):
#        pyautogui.press('altleft')
#        self.activate()




#w = window_manager()
#AML = w.find_window('Altium Material Library')
#AML.set_foreground()


#AML = window_manager('Altium Material Library')
#AML = pygetwindow.getWindowsWithTitle('Altium Material Library')[0]
#pyautogui.press('altleft')
#AML.activate()
#AML.maximize()
#pyautogui.click(AML.center)

#AML.minimize()
#AML.restore()


# pyautogui.write('abc', 0.01)
