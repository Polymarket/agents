import datetime as dt
import time
from polymarket.agents.lib.trade import Trader

from polymarket.agents.lib.history import record_history
from polymarket.agents.lib.refresh import refresh_trades

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
        self.daily(dt.time(hour=12), refresh_trades)
        self.hourly(dt.time(minute=30), record_history)


# TODO: add task objects for generalized schedule management infrastructure
