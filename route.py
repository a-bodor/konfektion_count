from page_home import Home
from page_chart import Data_Chart
from page_settings import Settings
from page_log import Log
from boot import Boot


'''
Class for routing (programm layout)
'''


class Route():
    def __init__(self, page, data):
        self.page = page
        self.data = data
        self.routes = {
            '/': Home(page, data),
            '/data_chart': Data_Chart(page, data),
            '/settings': Settings(page, data),
            '/log': Log(page, data),
            '/boot': Boot(page)
        }
        self.page.add(self.routes['/'])

    def route_change(self, route):
        self.page.controls.pop()
        self.page.add(self.routes[route.route])
        self.page.update()
