import datetime as dt
import time
from lib.trade import Trader

from lib.history import record_history
from lib.refresh import refresh_trades

from scheduler import Scheduler
from scheduler.trigger import Monday


class MetaScheduler:
    def __init__(self):
        self.trader = Trader()
        self.schedule = Scheduler()

    def start(self):
        while True:
            self.schedule.exec_jobs()
            time.sleep(1)


class TradingAgent(Scheduler):
    def __init__(self):
        self.trader = Trader()
        self.schedule = Scheduler()
        self.schedule.weekly(Monday(), self.trader.one_best_trade)
        self.schedule.daily(dt.time(hour=12), refresh_trades)
        self.schedule.hourly(dt.time(minute=30), record_history)

    def trade(self):
        self.trader.one_best_trade()


# TODO: add task objects for generalized schedule management infrastructure
