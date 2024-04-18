import flet as ft
from settings import APPBAR_TITLE_SIZE, APPBAR_TITLE_FONT, APPBAR_COLOR, TEXTFIELD_WIDTH, COLOR_RED, VERSION
from navigation import Navigation
from snackbars import Snackbar


'''
Header (top appbar)
'''


class Header(ft.UserControl):
    def __init__(self, page, data, title):
        super().__init__()
        self.page = page
        self.data = data
        self.title = title
        self.navigation = Navigation(page, data)

        # Light-/Darkmode Button
        self.toggle_theme = ft.IconButton(
            on_click=self.toggle_mode,
            icon=ft.icons.DARK_MODE_OUTLINED,
            selected_icon=ft.icons.LIGHT_MODE_OUTLINED,
            style=ft.ButtonStyle(
                color={
                    '': ft.colors.BLACK,
                    'selected': ft.colors.WHITE
                }
            )
        )
        # Dialog
        self.dialog_login = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                'Einloggen',
                text_align='center'
            ),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.TextField(
                                value='Admin',
                                width=TEXTFIELD_WIDTH*2
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        controls=[
                            ft.TextField(
                                password=True,
                                autofocus=True,
                                width=TEXTFIELD_WIDTH*2,
                                on_submit=self.dialog_login_click,
                                data=True
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                tight=True
            ),
            actions=[
                ft.TextButton(
                    text='OK',
                    on_click=self.dialog_login_click,
                    data=True
                ),
                ft.TextButton(
                    text='ABBRECHEN',
                    on_click=self.dialog_login_click,
                    data=False
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        self.dialog_about = ft.AlertDialog(
            modal=False,
            title=ft.Text(
                'Über'
            ),
            content=ft.Text(
                VERSION,
                italic=True
            )
        )
        # Snackbars
        self.snackbar_login_error = Snackbar(
            'Falscher Benutzer/Passwort!',
            COLOR_RED,
            ft.icons.ERROR_OUTLINE_OUTLINED
        ).build()

    # Switch Light-/Darkmode
    def toggle_mode(self, e):
        self.page.theme_mode = 'light' if self.page.theme_mode == 'dark' else 'dark'
        self.toggle_theme.selected = not self.toggle_theme.selected

        self.page.update()

    def build(self):
        self.header = ft.AppBar(
            leading=ft.IconButton(
                ft.icons.MENU,
                scale=1.5,
                on_click=self.open_navigation
            ),
            title=ft.Container(
                content=ft.Text(
                    self.title,
                    size=APPBAR_TITLE_SIZE,
                    weight=ft.FontWeight.BOLD,
                    font_family=APPBAR_TITLE_FONT
                ),
                on_click=self.title_click
            ),
            center_title=False,
            bgcolor=APPBAR_COLOR,
            actions=[
                # Active user
                self.data.active_user_text,
                # Space
                ft.Text('     '),
                # Dark/- Lightmode
                self.toggle_theme,
                # Popup menu
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text='Einstellungen',
                            icon=ft.icons.SETTINGS_OUTLINED,
                            on_click=self.menu_click,
                            data=1
                        ),
                        ft.PopupMenuItem(
                            text='Login',
                            icon=ft.icons.LOGIN_OUTLINED,
                            on_click=self.menu_click,
                            data=2
                        ),
                        ft.Divider(),
                        ft.PopupMenuItem(
                            text='Über',
                            icon=ft.icons.HELP_OUTLINE_OUTLINED,
                            on_click=self.menu_click,
                            data=3
                        ),
                        ft.PopupMenuItem(
                            text='Beenden',
                            icon=ft.icons.EXIT_TO_APP_OUTLINED,
                            on_click=self.menu_click,
                            data=4
                        )
                    ]
                )
            ]
        )
        self.page.drawer = self.navigation.build()

        return self.header

    # Click on Title (go Home)
    def title_click(self, e):
        if self.page.route != '/':
            self.page.drawer.selected_index = 0
            self.page.go('/')

    # Toggle Navigation Drawer
    def open_navigation(self, e):
        self.page.drawer.open = True
        self.page.drawer.update()

    # Menu Items
    def menu_click(self, e):
        if e.control.data == 1:
            self.page.go('/settings')
        elif e.control.data == 2:
            if self.header.actions[-1].items[1].text == 'Login':
                self.page.show_dialog(self.dialog_login)
            else:
                self.data.active_user = self.data.users[0]
                self.data.active_user_text.value = self.data.active_user
                self.header.actions[-1].items[1].text = 'Login'
                self.header.actions[-1].items[1].icon = ft.icons.LOGIN_OUTLINED
                # Switches (turn testbutton off on logout)
                self.data.switch_testbutton.value = False
                self.data.switch_testbutton.disabled = True
                self.data.button_test.visible = False
                self.data.switch_log.disabled = True
                if self.page.route == '/settings':
                    self.data.switch_testbutton.update()
                    self.data.switch_log.update()
            self.page.update()
        elif e.control.data == 3:
            self.page.show_dialog(self.dialog_about)
            self.page.update()
        else:
            self.page.window_close()

    def dialog_login_click(self, e):
        if e.control.data:
            user = self.dialog_login.content.controls[0].controls[0].value
            pw = self.dialog_login.content.controls[1].controls[0].value
            if user == 'Admin' and pw == self.data.password:
                self.data.active_user = self.data.users[1]
                self.data.active_user_text.value = self.data.active_user
                self.header.actions[-1].items[1].text = 'Logout'
                self.header.actions[-1].items[1].icon = ft.icons.LOGOUT_OUTLINED
                # Enable Switches
                self.data.switch_testbutton.disabled = False
                self.data.switch_log.disabled = False
                if self.page.route == '/settings':
                    self.data.switch_testbutton.update()
                    self.data.switch_log.update()
            else:
                # Display Snackbar
                self.page.snack_bar = self.snackbar_login_error
                self.page.snack_bar.open = True
                self.page.update()

        self.dialog_login.open = False
        self.dialog_login.content.controls[1].controls[0].value = ''
        self.page.update()
