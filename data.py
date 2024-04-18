import flet as ft
from buttons import Button
from tile import Tile
from chart import Chart
from table import Table
from settings import PAGE_TILE_FACTOR, TIME_FONT_SIZE, TILE_GFX_WIDTH, GFX_COLOR, INIT_UPDATE_TIME, INIT_UPDATE_TIME_CHART, INIT_DEBOUNCE_TIME, INIT_DECIMALS, PASSWORD, TABLE_COLUMNS


'''
Interface file to store all data for the project
'''


class Data():
    def __init__(self, page):
        self.page = page
        self.page_tile_height = self.page.height*PAGE_TILE_FACTOR
        # Parameters - Variables
        # Main
        self.qty = 0
        self.qty_m = 0
        self.decimals = INIT_DECIMALS
        self.qty_per_m = round(0.0, self.decimals)
        self.qty_per_h = round(0.0, self.decimals)
        self.qty_run = 0
        self.qty_left = 0
        self.time = 0
        self.time_left = '00:00:00'
        # Settings
        self.prev_page = '/'
        self.update_time = INIT_UPDATE_TIME
        self.update_time_chart = INIT_UPDATE_TIME_CHART
        self.debounce_time = INIT_DEBOUNCE_TIME
        self.log_save = True
        # User
        self.password = PASSWORD
        self.users = ['Benutzer', 'Admin']
        self.active_user = self.users[0]
        self.active_user_text = ft.Text(
            self.active_user,
            italic=True
        )
        # Gfx
        self.qty_run_gfx = ft.ProgressRing(
            width=self.page_tile_height,
            height=self.page_tile_height,
            stroke_width=TILE_GFX_WIDTH,
            color=GFX_COLOR,
            value=0
        )
        # Home
        self.tile_empty = Tile(
            '', self.page_tile_height/2, '', border=False
        )
        self.tile_qty = Tile(
            str(self.qty), self.page_tile_height, border=False, padding=10, transparent=True, hide_zero=True)

        self.tile_qty_per_m = Tile(
            str(self.qty_per_m), self.page_tile_height /
            2, 'Stückzahl pro Minute (aktuell)'
        )
        self.tile_qty_per_h = Tile(
            str(self.qty_per_h), self.page_tile_height /
            2, 'Stückzahl pro Stunde (gesamt)'
        )
        self.tile_qty_run = Tile(
            str(self.qty_run), self.page_tile_height/2, 'Produktionsmenge'
        )
        self.tile_qty_left = Tile(
            str(self.qty_left), self.page_tile_height/2, 'Restmenge'
        )
        self.tile_qty_run_gfx = Tile(
            self.qty_run_gfx, self.page_tile_height, border=False, padding=10
        )
        self.tile_time_left = Tile(
            str(self.time_left), self.page_tile_height/2, 'Restzeit'
        )
        # Time Text
        self.time_text = ft.Text(
            value='00:00:00',
            size=TIME_FONT_SIZE,
            weight='bold'
        )
        self.update_time_text = ft.Text(
            value=f'Aktualisierungsrate: ({self.update_time} s)',
            weight='italic'
        )
        self.time_now_text = ft.Text(
            value=''
        )
        # Data Chart
        self.data_points = []
        self.chart = Chart(self.page, self.data_points)
        # Table
        self.table_log_columns = TABLE_COLUMNS
        self.table_log = Table(self.page, self.table_log_columns)
        # Buttons
        # Edit
        self.button_edit = Button(
            ft.icons.EDIT,
            'Produktionsmenge bearbeiten'
        )
        # Reset
        self.button_reset = Button(
            ft.icons.DELETE_FOREVER,
            'Reset'
        )
        # Testbutton
        self.button_test = Button(
            ft.icons.PLUS_ONE,
            'Test',
            self.btn_test_click
        )
        self.button_test.visible = False
        # Switches
        # Testbutton
        self.switch_testbutton = ft.Switch(
            label='Testknopf anzeigen',
            value=False,
            disabled=True,
            on_change=self.switch_testbutton_click
        )
        # Log saving
        self.switch_log = ft.Switch(
            label='Protokoll speichern',
            value=True,
            disabled=True,
            on_change=self.switch_log_click
        )

    # Functions
    def btn_test_click(self, e):
        self.qty += 1
        self.qty_m += 1

    def switch_testbutton_click(self, e):
        if e.control.value == True:
            self.button_test.visible = True
        else:
            self.button_test.visible = False

        self.button_test.update()

    def switch_log_click(self, e):
        if e.control.value == True:
            self.log_save = True
        else:
            self.log_save = False
