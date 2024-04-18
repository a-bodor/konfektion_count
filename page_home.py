import flet as ft
from settings import PAGE_BG_COLOR, PAGE_BG_MARGIN, PAGE_BG_RADIUS, PAGE_BG_PADDING, TILE_REZIZE


'''
Main page (home)
'''


# Page: Home
class Home(ft.UserControl):
    def __init__(self, page, data):
        super().__init__()
        self.page = page
        self.page_height = page.height

        self.data = data
        # Tiles
        self.tile_empty = self.data.tile_empty
        self.tile_qty_per_m = self.data.tile_qty_per_m
        self.tile_qty_per_h = self.data.tile_qty_per_h
        self.tile_qty = self.data.tile_qty
        self.tile_qty_run = self.data.tile_qty_run
        self.tile_qty_left = self.data.tile_qty_left
        self.tile_qty_run_gfx = self.data.tile_qty_run_gfx
        self.tile_time_left = self.data.tile_time_left
        # Qty and gfx on top of each other
        self.tile_gfx = ft.Stack(
            controls=[
                ft.Container(
                    content=self.tile_qty_run_gfx,
                    width=self.tile_qty_run_gfx.height
                ),
                ft.Container(
                    content=self.tile_qty,
                    width=self.tile_qty_run_gfx.height,
                    alignment=ft.alignment.center
                )
            ],
            col=TILE_REZIZE
        )

    def build(self):
        row_1 = ft.ResponsiveRow(
            controls=[
                self.tile_qty_run,
                self.tile_qty_left
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            expand=True
        )
        row_2 = ft.ResponsiveRow(
            controls=[
                self.tile_qty_per_h,
                self.tile_time_left
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            expand=True
        )
        row_3 = ft.ResponsiveRow(
            controls=[
                self.tile_qty_per_m,
                self.tile_gfx
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            expand=True
        )

        # Page Layout
        body = ft.Container(
            content=ft.Column(
                controls=[
                    ft.ResponsiveRow(
                        controls=[
                            row_1,
                            row_2,
                            row_3
                        ]
                    )
                ]
            ),
            bgcolor=PAGE_BG_COLOR,
            border_radius=PAGE_BG_RADIUS,
            padding=PAGE_BG_PADDING,
            margin=PAGE_BG_MARGIN,
            expand=True
        )

        return body
