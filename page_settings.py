import flet as ft
from buttons import Button
from textfields import Textfield
from snackbars import Snackbar
from settings import PAGE_TEXT_SIZE, TILE_TITLE_SIZE, TILE_TITLE_FONT_WEIGHT, PAGE_BG_COLOR, PAGE_BG_MARGIN, PAGE_BG_PADDING, PAGE_BG_RADIUS, INIT_UPDATE_TIME, INIT_UPDATE_TIME_CHART, INIT_DEBOUNCE_TIME, INIT_DECIMALS, DEBOUNCE_TIME_MAX, COLOR_GREEN, COLOR_RED


'''
Settings page
'''


class Settings(ft.UserControl):
    def __init__(self, page, data):
        super().__init__()
        self.page = page
        self.data = data

        self.dropdown_width = self.page.width/3
        self.dropdown_padding = 100
        # Buttons
        self.button_back = Button(
            ft.icons.ARROW_BACK,
            'Zurück',
            self.button_back_click
        )
        self.button_save = Button(
            ft.icons.SAVE,
            'Speichern',
            self.button_save_click
        )
        self.button_reset = Button(
            ft.icons.RESTORE,
            'Standardwerte wiederherstellen',
            self.button_reset_click
        )
        # Dropdowns
        self.dropdown_update = ft.Dropdown(
            options=[
                ft.dropdown.Option(1),
                ft.dropdown.Option(5),
                ft.dropdown.Option(10),
                ft.dropdown.Option(30),
                ft.dropdown.Option(60)
            ],
            value=self.data.update_time,
            suffix_text='Sekunden'
        )
        self.dropdown_update_chart = ft.Dropdown(
            options=[
                # ft.dropdown.Option(10),
                ft.dropdown.Option(60),
                # ft.dropdown.Option(600)
            ],
            value=self.data.update_time_chart,
            suffix_text='Sekunden'
        )
        # Keep variable name 'dropdown' for consistency
        self.dropdown_debounce_time = ft.TextField(
            value=round(self.data.debounce_time*1000, None),
            input_filter=ft.InputFilter(r'[0-9]'),
            max_length=4,
            helper_text='max. 2000ms',
            suffix_text='Millisekunden',
            on_submit=self.dialog_debounce_time_click,
            data=True
        )
        self.dropdown_decimals = ft.Dropdown(
            options=[
                ft.dropdown.Option(0),
                ft.dropdown.Option(1),
                ft.dropdown.Option(2),
            ],
            value=self.data.decimals
        )
        # Switches
        self.switch_testbutton = self.data.switch_testbutton
        self.switch_log = self.data.switch_log
        # Dialogs
        self.dialog_update = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                'Aktualisierungsrate',
                text_align='center'
            ),
            content=self.dropdown_update,
            actions=[
                ft.TextButton(text='Okay',
                              on_click=self.dialog_update_click,
                              data=True
                              ),
                ft.TextButton(text='Abbrechen',
                              on_click=self.dialog_update_click,
                              data=False
                              )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        self.dialog_update_chart = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                'Aktualisierungsrate Grafik',
                text_align='center'
            ),
            content=self.dropdown_update_chart,
            actions=[
                ft.TextButton(text='Okay',
                              on_click=self.dialog_update_chart_click,
                              data=True
                              ),
                ft.TextButton(text='Abbrechen',
                              on_click=self.dialog_update_chart_click,
                              data=False
                              )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        self.dialog_debounce_time = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                'Entprellzeit Sensor',
                text_align='center'
            ),
            content=self.dropdown_debounce_time,
            actions=[
                ft.TextButton(text='Okay',
                              on_click=self.dialog_debounce_time_click,
                              data=True
                              ),
                ft.TextButton(text='Abbrechen',
                              on_click=self.dialog_debounce_time_click,
                              data=False
                              )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        self.dialog_decimals = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                'Angezeigte Dezimalstellen',
                text_align='center'
            ),
            content=self.dropdown_decimals,
            actions=[
                ft.TextButton(text='Okay',
                              on_click=self.dialog_decimals_click,
                              data=True
                              ),
                ft.TextButton(text='Abbrechen',
                              on_click=self.dialog_decimals_click,
                              data=False
                              )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        self.dialog_reset = ft.AlertDialog(
            modal=True,
            title=ft.Text('Reset'),
            content=ft.Text('Standardwerte wiederherstellen?'),
            actions=[
                ft.TextButton(text='Okay',
                              on_click=self.dialog_reset_click,
                              data=True
                              ),
                ft.TextButton(text='Abbrechen',
                              on_click=self.dialog_reset_click,
                              data=False
                              )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        # Textfields
        self.textfield_update = Textfield(
            self.data.update_time,
            read_only=True,
            focus_func=lambda _: self.open_dialog(self.dialog_update),
            deselect_func=lambda _: self.button_save.focus(),
            suffix='s'
        )
        self.textfield_update_chart = Textfield(
            self.data.update_time_chart,
            read_only=True,
            focus_func=lambda _: self.open_dialog(self.dialog_update_chart),
            deselect_func=lambda _: self.button_save.focus(),
            suffix='s'
        )
        self.textfield_debounce_time = Textfield(
            round(self.data.debounce_time*1000, None),
            read_only=True,
            focus_func=lambda _: self.open_dialog(self.dialog_debounce_time),
            deselect_func=lambda _: self.button_save.focus(),
            suffix='ms'
        )
        self.textfield_decimals = Textfield(
            self.data.decimals,
            read_only=True,
            focus_func=lambda _: self.open_dialog(self.dialog_decimals),
            deselect_func=lambda _: self.button_save.focus()
        )
        # Snackbars
        self.snackbar_save = Snackbar(
            'Gespeichert',
            COLOR_GREEN,
            ft.icons.SAVE_OUTLINED
        ).build()
        self.snackbar_reset = Snackbar(
            'Standardwerte wiederhergestellt',
            COLOR_GREEN,
            ft.icons.INFO_OUTLINED
        ).build()
        self.snackbar_no_access = Snackbar(
            'Kein Zugriff!',
            COLOR_RED,
            ft.icons.DO_DISTURB_OUTLINED
        ).build()

    def build(self):
        title = ft.Text(
            'Einstellungen',
            size=TILE_TITLE_SIZE,
            weight=TILE_TITLE_FONT_WEIGHT
        )

        # Page Layout
        body = ft.Container(
            content=(
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                title
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text('')
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.textfield_update,
                                ft.Text(
                                    self.dialog_update.title.value,
                                    size=PAGE_TEXT_SIZE,
                                    weight=TILE_TITLE_FONT_WEIGHT
                                )
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.textfield_update_chart,
                                ft.Text(
                                    self.dialog_update_chart.title.value,
                                    size=PAGE_TEXT_SIZE,
                                    weight=TILE_TITLE_FONT_WEIGHT
                                )
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.textfield_decimals,
                                ft.Text(
                                    self.dialog_decimals.title.value,
                                    size=PAGE_TEXT_SIZE,
                                    weight=TILE_TITLE_FONT_WEIGHT
                                )
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.textfield_debounce_time,
                                ft.Text(
                                    self.dialog_debounce_time.title.value,
                                    size=PAGE_TEXT_SIZE,
                                    weight=TILE_TITLE_FONT_WEIGHT
                                )
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Text('')
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.switch_log
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.switch_testbutton
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.button_save,
                                self.button_reset,
                                self.button_back
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ]
                )
            ),
            bgcolor=PAGE_BG_COLOR,
            border_radius=PAGE_BG_RADIUS,
            padding=PAGE_BG_PADDING,
            margin=PAGE_BG_MARGIN,
            expand=True
        )

        return body

    def button_back_click(self, e):
        self.textfield_update.update_value(self.data.update_time)
        self.textfield_update_chart.update_value(self.data.update_time_chart)
        self.textfield_debounce_time.update_value(
            round(self.data.debounce_time*1000, None))
        self.textfield_decimals.update_value(self.data.decimals)
        # Go back
        self.page.go(self.data.prev_page)

    def button_save_click(self, e):
        if self.data.active_user == self.data.users[1]:
            self.data.update_time = int(
                self.textfield_update.controls[0].value)
            self.data.update_time_chart = int(
                self.textfield_update_chart.controls[0].value)
            self.data.debounce_time = float(
                self.textfield_debounce_time.controls[0].value)/1000
            if self.textfield_decimals.controls[0].value == '0':
                self.data.decimals = None
            else:
                self.data.decimals = int(
                    self.textfield_decimals.controls[0].value)
            # Update Footer Text
            self.data.update_time_text.value = f'Aktualisierungsrate: ({self.data.update_time} s)'
            # Display Snackbar
            self.page.snack_bar = self.snackbar_save
            self.page.snack_bar.open = True
            self.page.update()
        else:
            # Display Snackbar
            self.page.snack_bar = self.snackbar_no_access
            self.page.snack_bar.open = True
            self.page.update()

    def button_reset_click(self, e):
        if self.data.active_user == self.data.users[1]:
            self.page.show_dialog(self.dialog_reset)
        else:
            # Display Snackbar
            self.page.snack_bar = self.snackbar_no_access
            self.page.snack_bar.open = True
            self.page.update()

    def open_dialog(self, textfield):
        if self.data.active_user == self.data.users[1]:
            self.page.show_dialog(textfield)

    def dialog_update_click(self, e):
        if e.control.data:
            self.textfield_update.update_value(self.dropdown_update.value)
        self.dialog_update.open = False
        self.page.update()

    def dialog_update_chart_click(self, e):
        if e.control.data:
            self.textfield_update_chart.update_value(
                self.dropdown_update_chart.value)

        self.dialog_update_chart.open = False
        self.page.update()

    def dialog_debounce_time_click(self, e):
        if e.control.data:
            if int(self.dropdown_debounce_time.value) > DEBOUNCE_TIME_MAX:
                self.dropdown_debounce_time.value = DEBOUNCE_TIME_MAX
            self.textfield_debounce_time.update_value(
                self.dropdown_debounce_time.value)

        self.dialog_debounce_time.open = False
        self.page.update()

    def dialog_decimals_click(self, e):
        if e.control.data:
            self.textfield_decimals.update_value(
                self.dropdown_decimals.value)

        self.dialog_decimals.open = False
        self.page.update()

    def dialog_reset_click(self, e):
        if e.control.data:
            # Reset textfields
            self.textfield_update.update_value(INIT_UPDATE_TIME)
            self.textfield_update_chart.update_value(INIT_UPDATE_TIME_CHART)
            self.textfield_debounce_time.update_value(
                round(INIT_DEBOUNCE_TIME*1000, None))
            self.textfield_decimals.update_value('0')
            # Display Snackbar
            self.page.snack_bar = self.snackbar_reset
            self.page.snack_bar.open = True
            self.page.update()

        self.dialog_reset.open = False
        self.page.update()
