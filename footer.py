import flet as ft
from buttons import Button
from settings import APPBAR_COLOR, BOTTOM_APPBAR_HEIGHT, BOTTOM_APPBAR_PADDING, BUTTON_ANIMATION_TIME


'''
Footer (bottom appbar)
'''


class Footer(ft.UserControl):
    def __init__(self, page, data, logic):
        super().__init__()
        self.page = page
        self.data = data
        self.logic = logic
        # Buttons
        # Floating Action Button
        self.page.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.PLAY_ARROW,
            tooltip='Start',
            animate_offset=ft.animation.Animation(BUTTON_ANIMATION_TIME)
        )
        self.page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED
        # Edit
        self.button_edit = self.data.button_edit
        self.button_edit.function = self.logic.button_edit_click
        # Reset
        self.button_reset = self.data.button_reset
        self.button_reset.function = self.logic.button_reset_click
        # Test Button - remove later?
        self.button_test = self.data.button_test

    def build(self):
        footer = ft.BottomAppBar(
            bgcolor=APPBAR_COLOR,
            shape=ft.NotchShape.AUTO,
            height=BOTTOM_APPBAR_HEIGHT,
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            self.data.update_time_text
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=7
                    ),
                    ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    self.button_edit,
                                    self.button_reset,
                                    self.button_test
                                ],
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        expand=2
                    ),
                    ft.Column(
                        controls=[
                            self.data.time_now_text
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        expand=2
                    ),
                    ft.Column(
                        controls=[
                            self.data.time_text
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        expand=1
                    )
                ]
            )
        )
        footer.padding = BOTTOM_APPBAR_PADDING

        return footer
