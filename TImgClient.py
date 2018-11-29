"""
This module is the front-end of TImgClient to give graphical interface
"""

import urwid
import TImgText
import TImgScreens
import TImgCallbacks


class FrontEnd:
    def __init__(self):
        self.texts = TImgText.TImgText()
        self.palette = self.texts.get_palette()
        self.interfaces = TImgScreens.TImgScreen()

    def begin(self, screen):
        if screen == 'main':
            try:
                self.mainScreen = self.interfaces.show_main(self.texts.get_main_screen_text_with_banner(),
                                                            self.texts.get_version())
                self.loop = urwid.MainLoop(self.mainScreen, self.palette)
                                           # unhandled_input=TImgCallbacks.TImgCallbacks().main_screen_callback)
                self.loop.run()
            except UnicodeEncodeError:
                self.mainScreen = self.interfaces.show_main(self.texts.get_main_screen_text_without_banner(),
                                                            self.texts.get_version())
                self.loop = urwid.MainLoop(self.mainScreen, self.palette)
                                           # unhandled_input=TImgCallbacks.TImgCallbacks().main_screen_callback)
                self.loop.run()


if __name__ == "__main__":
    frontend = FrontEnd()
    frontend.begin("main")
