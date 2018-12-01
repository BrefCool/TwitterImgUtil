"""
This module is part of front-end. It defines and stores all the texts for TImgClient front-end
"""

import urwid
import random


class TImgText:
    def get_palette(self):
        """Returns a palette used for coloring the text"""
        return [
            ('Field', 'dark green, bold', 'black'),  # information fields, Search: etc.
            ('Info', 'dark green', 'black'),  # information in fields
            ('Bg', 'black', 'black'),  # screen background
            ('InfoFooterText', 'white', 'dark blue'),  # footer text
            ('InfoFooterHotkey', 'dark cyan, bold', 'dark blue'),  # hotkeys in footer text
            ('InfoFooter', 'black', 'dark blue'),  # footer background
            ('InfoHeaderText', 'white, bold', 'dark blue'),  # header text
            ('InfoHeader', 'black', 'dark blue'),  # header background
            ('BigText', self.random_color(), 'black'),  # main menu banner text
            ('GeneralInfo', 'brown', 'black'),  # main menu text
            ('LastModifiedField', 'dark cyan, bold', 'black'),  # Last modified:
            ('LastModifiedDate', 'dark cyan', 'black'),  # info in Last modified:
            ('PopupMessageText', 'black', 'dark cyan'),  # popup message text
            ('PopupMessageBg', 'black', 'dark cyan'),  # popup message background
            ('SearchBoxHeaderText', 'light gray, bold', 'dark cyan'),  # field names in the search box
            ('SearchBoxHeaderBg', 'black', 'dark cyan'),  # field name background in the search box
            ('OnFocusBg', 'white', 'dark magenta')  # background when a widget is focused
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

    def get_footer_signup_text(self):
        """Returns Footer text for record adding screen"""
        return ('InfoFooterText',
                ['Press ', ('InfoFooterHotkey', '"ESC"'), ' to Cancel, ', ('InfoFooterHotkey', '"F2"'), ' to add'])

    def get_header_text(self, version):
        """Accept version as an argument, return header text"""
        return "TImgClient version %s" % version

    def get_main_page_text(self, banner):
        """Returns a text for the main page"""
        main_msg = "TImgClient is a client for user to better use the package TwitterImgUtil\n"\
                   "It includes Twitter+FFMPEG+GOOGLE_VISION to help users download images from\n"\
                   "twitter accounts and recognize all the images via Google Vision. Finally, It\n"\
                   "will output several videos about it\n"\
                   "Author: Yuxuan Su\n"\
                   "Github: https://github.com/BrefCool/TwitterImgUtil"
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

    def get_signup_record_template(self):
        template = "UserName: \n\n" \
                   "Password: \n\n" \
                   "Twitter Auth: \n\n" \
                   "Google Auth: \n\n"
        return template

    def get_tips(self):
        return urwid.SimpleListWalker([
            urwid.Padding(urwid.Text(('GeneralInfo', '\n Tips and tricks filling this form:\n\n' \
                                                     '  1. Use the supplied template to fill in your ' \
                                                     'information. Stick to the defined format to use ' \
                                                     'the program efficiently.\n\n' \
                                                     '  2. The template is given to utilize the search ' \
                                                     'efficiently. Do not alter the format. Not everything ' \
                                                     'must be filled in, input either name, lastname or nickname ' \
                                                     'for the record to appear in the search results.\n\n' \
                                                     '  3. You can add your desired info in free-form, but stick ' \
                                                     'to the format.\n\n' \
                                                     '  4. Use arrow keys to navigate and buttons PAGEUP ' \
                                                     'to get to the first line, use PAGEDOWN to get to the ' \
                                                     'last line. HOME key gets to the start of the line and ' \
                                                     'END key gets to the end of the line.' \
                                                     'TAB key insert multiple spaces.')), left=2)
        ])
