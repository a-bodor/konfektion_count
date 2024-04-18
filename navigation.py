import flet as ft


'''
Navigation drawer
'''


class Navigation(ft.UserControl):
    def __init__(self, page, data):
        super().__init__()
        self.page = page
        self.data = data

    def build(self):
        navigation = ft.NavigationDrawer(
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    label='Home',
                    icon=ft.icons.HOME_OUTLINED,
                    selected_icon=ft.icons.HOME
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    label='Übersicht',
                    icon=ft.icons.SHOW_CHART_OUTLINED,
                    selected_icon=ft.icons.SHOW_CHART
                ),
                ft.NavigationDrawerDestination(
                    label='Protokoll',
                    icon=ft.icons.BOOK_OUTLINED,
                    selected_icon=ft.icons.BOOK
                )
            ],
            on_change=self.change_route
        )
        return navigation

    # Page Routing
    def change_route(self, e):
        if self.page.drawer.selected_index == 0:
            self.page.go('/')
        elif self.page.drawer.selected_index == 1:
            self.page.go('/data_chart')
        elif self.page.drawer.selected_index == 2:
            self.page.go('/log')
        else:
            pass

        self.data.prev_page = self.page.route
        self.page.drawer.open = False
        self.page.update()
