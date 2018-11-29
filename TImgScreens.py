"""
This module is for constructing different interface screens
"""

import urwid
import TImgText


class TImgScreen:
    def __init__(self):
        self.texts = TImgText.TImgText()
        self.editField = urwid.Edit
        self.intEditField = urwid.IntEdit
        self.searchField = urwid.Edit
        self.radioButtons = []

    def get_edit_field(self):
        return self.editField

    def get_int_edit_field(self):
        return self.intEditField

    def get_radio_buttons(self):
        return self.radioButtons

    def get_search_field(self):
        return self.searchField

    def show_main(self, banner, version):
        # footer, which locates at the bottom of the screen
        footer = urwid.AttrMap(urwid.Text(self.texts.get_footer_main_text(),
                                          align='center'),
                               'InfoFooter')

        # header, which locates at the top of the screen
        header = urwid.AttrMap(urwid.Text(('InfoHeaderText',
                                           '%s / syx525@bu.edu' % (self.texts.get_header_text(version))),
                                          align='center'),
                               'InfoHeader')

        # Message below the banner
        head_body_foot_frame = urwid.Frame(header=header,
                                           body=self.texts.get_main_page_text(banner),
                                           footer=footer)

        # add background
        bkg = urwid.AttrMap(head_body_foot_frame, 'Bg')

        return bkg
