import flet as ft


'''
File containing all constants (settings)
'''


# Main
VERSION = 'Version 1.0'
MAIN_TITLE = 'Zähler Band 2'
WIDTH_START = 1280
HEIGHT_START = 800
WIDTH_MIN = 800
HEIGHT_MIN = 600

# Colors
COLOR_WHITE = '#F2F2F2'
COLOR_GREY = '#736E6E'
COLOR_RED = '#D93030'
COLOR_RED_DARK = '#A63333'
COLOR_RED_LIGHT = '#F27E7E'
COLOR_GREEN = '#3AC24C'
# #A4A6A5 = hellgrau

# Theme
SCHEME = ft.ColorScheme(
    primary=COLOR_GREY,
    primary_container=COLOR_RED_LIGHT,
    secondary_container=COLOR_RED_LIGHT
)
THEME = ft.Theme(
    color_scheme=SCHEME
)


# Appbar (Header, Footer, Nav)
APPBAR_COLOR = ft.colors.SURFACE_VARIANT
APPBAR_TITLE_SIZE = 35
APPBAR_TITLE_FONT = 'Calibri'
BOTTOM_APPBAR_HEIGHT = 50
BOTTOM_APPBAR_PADDING = 5
TIME_FONT_SIZE = 20

# Snackbar
SNACKBAR_TEXT_COLOR = ft.colors.WHITE
SNACKBAR_DURATION = 3000
SNACKBAR_DURATION_LONG = 600000
SNACKBAR_WIDTH = WIDTH_MIN*0.75


# Tile
TILE_ALIGNMENT = ft.alignment.center
TILE_PADDING = 5
TILE_MARGIN = 15
TILE_SPACING = 40
TILE_COLOR = ft.colors.SURFACE_VARIANT
TILE_REZIZE = {'sm': 12, 'md': 6, 'lg': 5, 'xxl': 4}
TILE_FONT = 'Calibri'
TILE_FONT_SIZE = 30
TILE_TITLE_SIZE = 22
TILE_FONT_WEIGHT = 'bold'
TILE_TITLE_FONT_WEIGHT = 'bold'
TILE_RADIUS = 10
TILE_SHADOW = ft.BoxShadow(
    spread_radius=1,
    blur_radius=5,
    color=ft.colors.ON_SURFACE_VARIANT,
    offset=ft.Offset(0, 0),
    blur_style=ft.ShadowBlurStyle.OUTER
)
TILE_GFX_WIDTH = 20
GFX_COLOR = COLOR_RED_LIGHT

# Button
BUTTON_COLOR_DEFAULT = ft.colors.INVERSE_SURFACE
BUTTON_COLOR_HOVER = ft.colors.PRIMARY_CONTAINER
BUTTON_COLOR_DISABLED = COLOR_GREY
BUTTON_BORDER_SIZE = 0.5
BUTTON_ANIMATION_TIME = 10
BUTTON_ANIMATION_DURATION = 15

# Textfield
TEXTFIELD_TEXT_SIZE = 20
TEXTFIELD_TEXT_ALIGNMENT = 'center'
TEXTFIELD_WIDTH = 100
TEXTFIELD_BORDER_COLOR = ft.colors.ON_SURFACE

# Page: Home
PAGE_TILE_FACTOR = 0.4
PAGE_BG_COLOR = ft.colors.SURFACE_VARIANT
PAGE_BG_RADIUS = 10
PAGE_BG_PADDING = 15
PAGE_BG_MARGIN = 20

# Page: Settings
PAGE_TEXT_SIZE = 16
DEBOUNCE_TIME_MAX = 2000

# Chart
CHART_HEIGHT = 700
CHART_WIDTH = 1800
CHART_STROKE_WIDTH = 5
CHART_LINE_WIDTH = 1
CHART_GRID_COLOR = ft.colors.with_opacity(0.25, ft.colors.ON_SURFACE)
CHART_LINE_COLOR = COLOR_RED_LIGHT
CHART_MAX_X_INIT = 60
CHART_MAX_Y_INIT = 4000
CHART_LABEL_SIZE = 15
CHART_LABEL_AREA_SIZE = 50

# Data
INIT_UPDATE_TIME = 1
INIT_UPDATE_TIME_CHART = 60
INIT_DEBOUNCE_TIME = 0.5
INIT_DECIMALS = None

# Table
TABLE_COLUMNS = ['Startzeit', 'Stoppzeit',
                 'Dauer', 'Produziert', 'Stück/min', 'Status']
TABLE_BORDER_WIDTH = 2
TABLE_BORDER_RADIUS = 5
TABLE_BORDER_COLOR = ft.colors.ON_SURFACE
TABLE_LINE_WIDTH = 1
TABLE_LINE_COLOR_H = ft.colors.with_opacity(0.25, ft.colors.ON_SURFACE)
TABLE_LINE_COLOR_V = ft.colors.ON_SURFACE


# PW
PASSWORD = '100'