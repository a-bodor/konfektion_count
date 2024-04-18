import flet as ft
import threading
import time
import locale
from datetime import datetime, timedelta
from humanfriendly import format_timespan
from snackbars import Snackbar
from gpiozero import Button
from settings import BUTTON_ANIMATION_DURATION, COLOR_RED, COLOR_GREEN, SNACKBAR_DURATION_LONG
# Set date/time to german
locale.setlocale(locale.LC_TIME, 'de_DE')


'''
File containing all the logic
'''


class Logic(ft.UserControl):
    def __init__(self, page, data):
        super().__init__()
        self.page = page
        self.data = data

        self.running = False
        self.gfx_value = 0
        self.snackbar_finished_triggered = False
        self.time_started = 0
        self.qty_started = 0
        # Raspberry Pi
        # self.pi_input = Button(2)
        self.pi_input_debounce = False
        # Threads
        # Time
        self.timer_thread = threading.Thread(
            target=self.update,
            daemon=True
        )
        self.timer_thread.start()
        # PI Input
        '''
        self.pi_input_thread = threading.Thread(
            target=self.listen_pi_input,
            daemon=True
        )
        self.pi_input_thread.start()
        '''
        # Dialog
        # Stop
        self.dialog_running = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                'Wirklich stoppen?',
                text_align='center'
            ),
            content=ft.Text('Messung läuft. Wirklich beenden?'),
            actions=[
                ft.TextButton(text='JA',
                              on_click=self.dialog_running_click,
                              data=True
                              ),
                ft.TextButton(text='NEIN',
                              on_click=self.dialog_running_click,
                              data=False
                              )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        # Reset
        self.dialog_reset = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                'Daten Reset?',
                text_align='center'
            ),
            content=ft.Text('Alle Daten zurücksetzen?'),
            actions=[
                ft.TextButton(text='JA',
                              on_click=self.dialog_reset_click,
                              data=True
                              ),
                ft.TextButton(text='NEIN',
                              on_click=self.dialog_reset_click,
                              data=False
                              )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        # Edit
        self.dialog_edit = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                'Produktionsmenge',
                text_align='center'
            ),
            content=ft.TextField(
                label='Produktionsmenge eingeben',
                autofocus=True,
                input_filter=ft.InputFilter(r'[0-9]'),
                max_length=7,
                on_submit=self.dialog_edit_click,
                data=True
            ),
            actions=[
                ft.TextButton(
                    text='OK',
                    on_click=self.dialog_edit_click,
                    data=True
                ),
                ft.TextButton(
                    text='ABBRECHEN',
                    on_click=self.dialog_edit_click,
                    data=False
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        # Exit
        self.dialog_exit = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                'Programm schließen?',
                text_align='center'
            ),
            content=ft.Text('Soll das Programm wirklich geschlossen werden?'),
            actions=[
                ft.TextButton(text='JA',
                              on_click=self.dialog_exit_click,
                              data=True
                              ),
                ft.TextButton(text='NEIN',
                              on_click=self.dialog_exit_click,
                              data=False
                              )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        # Snackbars
        self.snackbar_qty_run = Snackbar(
            'Keine Produktionsmenge eingegeben!',
            COLOR_RED,
            ft.icons.ERROR_OUTLINE
        ).build()
        self.snackbar_finished = Snackbar(
            '',
            COLOR_GREEN,
            ft.icons.FLAG_OUTLINED,
            True,
            SNACKBAR_DURATION_LONG
        ).build()

    def dialog_running_click(self, e):
        if e.control.data:
            self.page.floating_action_button._set_attr(
                'icon', ft.icons.PLAY_ARROW)
            self.page.floating_action_button._set_attr(
                'tooltip', 'Start')
            self.data.button_edit.disabled = False
            self.data.button_reset.disabled = False
            self.running = False
            # log
            now = self.get_now(short=True)
            last_row = self.data.table_log.rows[-1]
            # enter stop time
            last_row.cells[1].content.value = now
            # calculate and enter duration
            duration = self.data.time-self.time_started
            last_row.cells[2].content.value = format_timespan(duration)
            self.time_started = 0
            # calculate and enter qty
            qty = self.data.qty-self.qty_started
            last_row.cells[3].content.value = qty
            self.qty_started = 0
            # quantity per duration
            last_row.cells[4].content.value = round(qty/duration, 2)
            # enter status
            if self.data.qty >= self.data.qty_run:
                status = 'beendet'
            else:
                status = 'pausiert'
            last_row.cells[5].content.value = status
            # update (if page active)
            if self.page.route == '/log':
                self.data.table_log.update()

        self.dialog_running.open = False
        self.page.update()

    def dialog_reset_click(self, e):
        if e.control.data:
            self.page.go('/')
            # Reset Data
            self.data.qty = 0
            self.data.qty_m = 0
            self.data.qty_per_m = round(0.0, self.data.decimals)
            self.data.qty_per_h = round(0.0, self.data.decimals)
            self.data.qty_run = 0
            self.data.qty_left = 0
            self.data.time_left = '00:00:00'
            self.data.data_points.clear()
            # Snackbar (not clean - maybe fix?)
            self.snackbar_finished.duration = 1
            self.page.show_snack_bar(self.snackbar_finished)
            self.snackbar_finished_triggered = False
            self.snackbar_finished.duration = SNACKBAR_DURATION_LONG
            # Reset Tiles
            self.data.tile_qty.update_value(self.data.qty)
            self.data.tile_qty_per_m.update_value(self.data.qty_per_m)
            self.data.tile_qty_per_h.update_value(self.data.qty_per_h)
            self.data.tile_qty_run.update_value(self.data.qty_run)
            self.data.tile_qty_left.update_value(self.data.qty_left)
            self.data.tile_qty_run_gfx.update_value(self.data.qty_left)
            self.data.tile_time_left.update_value(self.data.time_left)
            # Reset Time
            self.data.time = 0
            self.data.time_text.value = '00:00:00'
            self.data.time_now_text.value = ''

        self.dialog_reset.open = False
        self.page.update()

    def dialog_edit_click(self, e):
        if e.control.data:
            if self.dialog_edit.content.value == '':
                self.dialog_edit.content.value = 0
            self.data.qty_run = int(self.dialog_edit.content.value)
            self.data.tile_qty_run.update_value(
                self.data.qty_run)

        self.dialog_edit.open = False
        self.page.update()

    def dialog_exit_click(self, e):
        if e.control.data:
            # Generate log string and time
            output = ''
            log = self.generate_log_string()
            time = self.get_now(file=True)
            # Write text file if log is not empty
            if len(log) > 2 and self.data.log_save:
                for i in log:
                    output += f'{i}\n'
                f = open(f'KonfApp\logs\{time}.txt', 'x')
                f.write(output)
                f.close()
            # Close window
            self.page.window_destroy()

        self.dialog_exit.open = False
        self.page.update()

    # Start Button
    def floating_action_btn_click(self, e):
        # Check if running
        if self.running:
            self.page.show_dialog(self.dialog_running)
            self.page.update()
        else:
            # Check if QTY has been entered
            if self.data.qty_run == 0:
                self.page.snack_bar = self.snackbar_qty_run
                self.page.snack_bar.open = True
                self.page.update()
                self.button_animation()
                return
            self.page.floating_action_button._set_attr('icon', ft.icons.STOP)
            self.page.floating_action_button._set_attr('tooltip', 'Stop')
            self.data.button_edit.disabled = True
            self.data.button_reset.disabled = True
            self.running = True
            # Set start time
            now = self.get_now()
            if self.data.qty == 0:
                self.data.time_now_text.value = f'Startzeit:\n{now}'
            # Log
            # set start values
            now_short = self.get_now(short=True)
            self.time_started = self.data.time
            self.qty_started = self.data.qty
            # log start time
            self.data.table_log.add_row([now_short, '', '', '', '', ''])
            if self.page.route == '/log':
                self.data.table_log.update()

        self.page.update()

    def button_edit_click(self, e):
        if self.page.route == '/':
            self.page.show_dialog(self.dialog_edit)
            self.page.update()

    def button_reset_click(self, e):
        self.page.show_dialog(self.dialog_reset)
        self.page.update()

    def button_animation(self):
        for i in range(BUTTON_ANIMATION_DURATION):
            if i % 2 == 0:
                self.page.floating_action_button.offset = ft.transform.Offset(
                    -0.1, 0)
            else:
                self.page.floating_action_button.offset = ft.transform.Offset(
                    0.1, 0)
            self.page.floating_action_button.update()

        self.page.floating_action_button.offset = ft.transform.Offset(
            0, 0)
        self.page.floating_action_button.update()

    # Get start time (different formattings)
    def get_now(self, short=False, file=False):
        now = datetime.now()
        if short:
            now = datetime.strftime(now, '%d.%m.%Y, %I:%M%p')
        elif file:
            now = datetime.strftime(now, "%Y-%d-%m_%H%M%S")
        else:
            now = datetime.strftime(now, '%a %d %b %Y, %I:%M%p')

        return now

    # Generate string array of log contents
    def generate_log_string(self):
        row_head = ''
        row_dash = '-'*160
        row_temp = ''
        rows = []

        for i in range(len(self.data.table_log.rows)):
            for j in range(len(self.data.table_log.columns)):
                # Table Header
                if i == 0:
                    row_head += '{:<25}'.format(
                        self.data.table_log.columns[j].label.value
                    )+'| '
                # Table Rows
                row_temp += '{:<25}'.format(
                    self.data.table_log.rows[i].cells[j].content.value
                )+'| '
            rows.append(row_temp)
            row_temp = ''

        rows.insert(0, row_head)
        rows.insert(1, row_dash)

        return rows

    # Window events (atm only close event)
    def window_event(self, e):
        if e.data == 'close':
            self.page.show_dialog(self.dialog_exit)

    # Thread listening for PI input signal
    def listen_pi_input(self):
        while True:
            if self.running:
                if self.pi_input.is_active and not self.pi_input_debounce:
                    self.data.qty += 1
                    self.data.qty_m += 1
                    self.pi_input_debounce = True
                if not self.pi_input.is_active and self.pi_input_debounce:
                    self.pi_input_debounce = False

                time.sleep(self.data.debounce_time)

    # Thread managing all data updates
    def update(self):
        while True:
            if self.running:
                # Time
                self.data.time += 1
                self.data.time_text.value = '{:0>8}'.format(
                    str(timedelta(seconds=self.data.time))
                )
                # Qty
                # Per Min
                one_min = self.data.time % 60
                if one_min == 0:
                    self.data.qty_m = 0
                else:
                    self.data.qty_per_m = self.data.qty_m/(one_min/60)
                    self.data.qty_per_m = round(
                        self.data.qty_per_m, self.data.decimals)
                # Per Hour
                secs_to_hours = (self.data.time/60)/60
                self.data.qty_per_h = self.data.qty/secs_to_hours
                self.data.qty_per_h = round(
                    self.data.qty_per_h, self.data.decimals)
                # Qty left
                if self.data.qty_run > 0:
                    self.data.qty_left = self.data.qty_run - self.data.qty
                    # gfx
                    self.gfx_value = self.data.qty/self.data.qty_run
                # Time left
                # No negative time if finished
                if self.data.qty >= self.data.qty_run:
                    self.data.time_left = '00:00:00'
                    # Trigger Snackbar
                    if not self.snackbar_finished_triggered:
                        now = self.get_now()
                        self.snackbar_finished.content.controls[
                            1].value = f'Auftrag beendet!   ({now})'
                        self.page.show_snack_bar(self.snackbar_finished)
                        self.snackbar_finished_triggered = True
                # Calculate time left
                elif self.data.qty_per_h > 0:
                    time_left_secs = (
                        (self.data.qty_left/self.data.qty_per_h)*60)*60
                    time_left_mins, time_left_secs = divmod(
                        int(time_left_secs), 60)
                    time_left_hours, time_left_mins = divmod(
                        time_left_mins, 60)
                    self.data.time_left = '{:02d}:{:02d}:{:02d}'.format(
                        time_left_hours, time_left_mins, time_left_secs)
                # Data for chart
                if (self.data.time/self.data.update_time_chart) % 1 == 0:
                    self.data.data_points.append(
                        ft.LineChartDataPoint(
                            self.data.time/self.data.update_time_chart, self.data.qty_per_h)
                    )
                    # Update Page: Data Chart
                    self.data.chart.update_data()
                    if self.page.route == '/data_chart':
                        self.data.chart.update_chart()
                # Update Page: Home
                if self.page.route == '/':
                    if (self.data.time/self.data.update_time) % 1 == 0:
                        self.data.tile_qty.update_value(self.data.qty)
                        self.data.tile_qty_per_m.update_value(
                            self.data.qty_per_m)
                        self.data.tile_qty_per_h.update_value(
                            self.data.qty_per_h)
                        self.data.tile_qty_left.update_value(
                            self.data.qty_left)
                        self.data.tile_qty_run_gfx.update_value(self.gfx_value)
                        self.data.tile_time_left.update_value(
                            self.data.time_left)

                self.page.update()
            time.sleep(1)
