import flet as ft
from settings import CHART_STROKE_WIDTH, CHART_GRID_COLOR, CHART_LINE_COLOR, CHART_LINE_WIDTH, CHART_MAX_X_INIT, CHART_MAX_Y_INIT, CHART_LABEL_SIZE, CHART_LABEL_AREA_SIZE, CHART_HEIGHT, CHART_WIDTH


'''
Class for data charts
'''


class Chart(ft.UserControl):
    def __init__(self, page, data_points):
        super().__init__()
        self.page = page
        self.data_points = data_points

        self.max_x = CHART_MAX_X_INIT
        self.max_y = CHART_MAX_Y_INIT
        self.stroke_width = CHART_STROKE_WIDTH
        self.grid_color = CHART_GRID_COLOR
        self.line_color = CHART_LINE_COLOR
        self.line_width = CHART_LINE_WIDTH
        self.line_interval_h = self.max_y//4
        self.line_interval_v = self.max_x//4
        self.label_size = CHART_LABEL_SIZE
        self.label_area_size = CHART_LABEL_AREA_SIZE
        self.chart_height = CHART_HEIGHT
        self.chart_width = CHART_WIDTH

    def build(self):
        data = [
            ft.LineChartData(
                data_points=self.data_points,
                stroke_width=self.stroke_width,
                color=self.line_color,
                curved=True,
                stroke_cap_round=True
            )
        ]

        chart = ft.LineChart(
            data_series=data,
            border=ft.border.all(
                width=self.line_width*3,
                color=self.grid_color
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=self.line_interval_h,
                color=self.grid_color,
                width=self.line_width
            ),
            vertical_grid_lines=ft.ChartGridLines(
                interval=self.line_interval_v,
                color=self.grid_color,
                width=self.line_width
            ),
            left_axis=ft.ChartAxis(
                title=ft.Text(
                    'Stück Pro Stunde',
                    size=14,
                    weight=ft.FontWeight.BOLD
                ),
                show_labels=True,
                labels_size=self.label_area_size,
                labels_interval=self.line_interval_h
            ),
            bottom_axis=ft.ChartAxis(
                title=ft.Text(
                    'Zeit (in min)',
                    size=14,
                    weight=ft.FontWeight.BOLD
                ),
                show_labels=True,
                labels_size=self.label_area_size,
                labels_interval=self.line_interval_v
            ),
            tooltip_bgcolor=ft.colors.INVERSE_SURFACE,
            min_y=0,
            max_y=self.max_y,
            min_x=0,
            max_x=self.max_x,
            height=self.chart_height,
            width=self.chart_width,
            expand=True
        )

        return chart

    def update_data(self):
        if self.data_points != []:
            x = self.data_points[-1].x
            y = self.data_points[-1].y

        if x > self.max_x:
            self.max_x = x+60
        if y > self.max_y:
            self.max_y = y+500

    def update_chart(self):
        self.update()
