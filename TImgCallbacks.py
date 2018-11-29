"""
This module defines callbacks/menus for the screen
"""

import urwid
import sys

import TImgScreens
import TImgText


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TImgCallbacks(object, metaclass=Singleton):
    def __init__(self):
        self.interfaces = TImgScreens.TImgScreen()
        self.texts = TImgText.TImgText()
        self.palette = self.texts.get_palette()

        # all self.N vars must be initialized here as well for use in the main screen
        # else it will throw "reference before assignment" type error
        try:
            self.mainScreen = self.interfaces.show_main(
                self.texts.get_main_screen_text_with_banner(), self.texts.get_version())
            self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.main_screen_callback)
        except UnicodeEncodeError:
            self.mainScreen = self.interfaces.show_main(
                self.texts.get_main_screen_text_with_banner(), self.texts.get_version())
            self.loop = urwid.MainLoop(self.mainScreen, self.palette, unhandled_input=self.main_screen_callback)

    def main_screen_callback(self, key):
        """Main Screen Menu"""

        if key == 'esc':
            sys.exit("You have quit TImgClient %s" % self.texts.get_version())
        elif key in ('S', 's'):
            pass
        elif key in ('L', 'l'):
            pass
