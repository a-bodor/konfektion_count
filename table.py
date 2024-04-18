import flet as ft
from settings import TABLE_BORDER_WIDTH, TABLE_BORDER_RADIUS, TABLE_BORDER_COLOR, TABLE_LINE_WIDTH, TABLE_LINE_COLOR_H, TABLE_LINE_COLOR_V


'''
Class for data table
'''


class Table(ft.UserControl):
    def __init__(self, page, columns):
        super().__init__()
        self.page = page
        self.columns = []
        self.rows = []
        # Generate Colums
        for i in columns:
            col = ft.DataColumn(ft.Text(i))

            self.columns.append(col)

    def build(self):
        table = ft.DataTable(
            columns=self.columns,
            rows=self.rows,
            border=ft.border.all(
                TABLE_BORDER_WIDTH,
                TABLE_BORDER_COLOR
            ),
            border_radius=TABLE_BORDER_RADIUS,
            horizontal_lines=ft.border.BorderSide(
                TABLE_LINE_WIDTH,
                TABLE_LINE_COLOR_H
            ),
            vertical_lines=ft.border.BorderSide(
                TABLE_LINE_WIDTH,
                TABLE_LINE_COLOR_V
            ),
            heading_text_style=ft.TextStyle(
                weight=ft.FontWeight.BOLD
            )
        )

        return table

    def add_row(self, row_data):
        cell_data = []
        for i in row_data:
            cell_data.append(
                ft.DataCell(
                    ft.Text(i)
                )
            )
        row = ft.DataRow(
            cells=cell_data
        )
        self.rows.append(row)
