"""
This module is part of front-end. It defines and stores all the texts for TImgClient front-end
"""

import urwid
import random


class TImgText:
    def get_palette(self):
        """Returns a palette used for coloring the text"""
        return [
            ('Bg', 'black', 'black'),                    # screen background
            ('BigText', self.random_color(), 'black'),   # main menu banner text
            ('InfoFooter', 'black', 'dark blue'),        # footer background
            ('InfoFooterText', 'white', 'dark blue'),    # footer text
            ('InfoHeader', 'black', 'dark blue'),        # header background
            ('GeneralInfo', 'brown', 'black'),           # main menu text
        ]

    def random_color(self):
        """Pick a random color for the main menu text"""
        list_of_colors = ['dark red', 'dark green', 'brown', 'dark blue',
                          'dark magenta', 'dark cyan', 'light gray',
                          'dark gray', 'light red', 'light green', 'yellow',
                          'light blue', 'light magenta', 'light cyan', 'default']
        color = list_of_colors[random.randint(0, 14)]
        return color

    def get_version(self):
        return "0.1"

    def get_footer_main_text(self):
        """Returns text for the main screen"""
        return ('InfoFooterText',
                ['Press ', ('InfoFooterHotkey', '"ESC"'), ' to Quit, ', ('InfoFooterHotkey', '"L"'), ' to LogIn ',
                 ('InfoFooterHotkey', '"S"'), ' to SignUp '])

    def get_header_text(self, version):
        """Accept version as an argument, return header text"""
        return "TImgClient version %s" % version

    def get_main_page_text(self, banner):
        """Returns a text for the main page"""
        main_msg = """TImgClient is a client for user to better use the package TwitterImgUtil
                   It includes Twitter+FFMPEG+GOOGLE_VISION to help users download images from
                   twitter accounts and recognize all the images via Google Vision. Finally, It
                   will output several videos about it
                   Author: Yuxuan Su
                   Github: https://github.com/BrefCool/TwitterImgUtil"""
        text = urwid.Text(('GeneralInfo', main_msg), align='center')
        line_box = urwid.LineBox(urwid.Padding(text, align='center', left=3, right=3))
        ret = urwid.LineBox(urwid.AttrMap(urwid.Overlay(line_box, banner, 'center', 150, 'middle', None),
                                          'GeneralInfo'))
        return ret

    def get_main_screen_text_with_banner(self):
        return urwid.AttrWrap(
            urwid.Overlay(urwid.BigText('TImgClient %s' % self.get_version(), urwid.font.HalfBlock7x7Font()),
                          urwid.SolidFill(' '), 'center', None, 'top', None), 'BigText')

    def get_main_screen_text_without_banner(self):
        return urwid.AttrMap(urwid.SolidFill(' '), 'BigText')
