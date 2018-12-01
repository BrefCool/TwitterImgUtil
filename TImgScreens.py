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

    def show_log_in(self, version):
        pass

    def show_sign_up(self):
        """This is a sign up screen"""
        footer = urwid.AttrMap(urwid.Text(self.texts.get_footer_signup_text(), align='center'), 'InfoFooter')

        header = urwid.AttrMap(urwid.Text(('InfoHeaderText', 'Sign Up'), align='center'), 'InfoHeader')

        self.editField = urwid.Edit(('Field', ''),
                                    multiline=True,
                                    edit_text=self.texts.get_signup_record_template(),
                                    edit_pos=len(self.texts.get_signup_record_template().split('\n')[0]),
                                    allow_tab=True)
        # username = urwid.Text(('Field', 'UserName:'))
        # twitter_auth = urwid.Text(('Field', 'Twitter Auth'))
        # google_auth = urwid.Text(('Field', 'Google Auth'))
        editField = urwid.ListBox(urwid.SimpleListWalker([
            urwid.Divider(top=1),
            urwid.AttrWrap(self.editField,
                           'Info', 'OnFocusBg')
        ]))
        explanation = self.texts.get_tips()
        explanation = urwid.ListBox(explanation)

        vline = urwid.AttrWrap(urwid.SolidFill('|'), 'Info')

        bodyWithInfo = urwid.Columns([('fixed', 40, explanation), ('fixed', 1, vline), editField], dividechars=3,
                                     focus_column=2)
        headBodyFootFrame = urwid.Frame(footer=footer, header=header, body=bodyWithInfo)

        # Background
        bkg = urwid.AttrWrap(headBodyFootFrame, 'Bg')

        return bkg
