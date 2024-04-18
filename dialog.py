import flet as ft


'''
Class for dialogs
'''


class Dialog(ft.UserControl):
    def __init__(self, page, title, text_main, text_btn_1, text_btn_2, on_click_func):
        super().__init__()
        self.page = page
        self.title = title
        self.text_main = text_main
        self.text_btn_1 = text_btn_1
        self.text_btn_2 = text_btn_2
        self.on_click_func = on_click_func

        self.selected = 0

    def build(self):
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(self.title),
            content=ft.Text(self.text_main),
            actions=[
                ft.TextButton(self.text_btn_1,
                              on_click=self.btn_click,
                              data=True),
                ft.TextButton(self.text_btn_2,
                              on_click=self.btn_click,
                              data=False)
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )

        return dialog

    def btn_click(self, e):
        self.on_click_func
