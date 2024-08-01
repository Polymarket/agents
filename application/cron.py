import datetime as dt
import time
from application.trade import Trader

from scheduler import Scheduler
from scheduler.trigger import Monday


class Scheduler:
    def __init__(self):
        self.trader = Trader()
        self.schedule = Scheduler()

    def start(self):
        while True:
            self.schedule.exec_jobs()
            time.sleep(1)


class TradingAgent(Scheduler):
    def __init__(self):
        super()
        self.trader = Trader()
        self.weekly(Monday(), self.trader.one_best_trade)


# TODO: add task objects for generalized schedule management infrastructure
