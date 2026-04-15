import logging
import time

from scheduler import Scheduler as TimeScheduler
from scheduler.trigger import Monday

from agents.application.trade import Trader

logger = logging.getLogger(__name__)


class TradingScheduler:
    def __init__(self) -> None:
        self.trader = Trader()
        self.schedule = TimeScheduler()

    def start(self) -> None:
        logger.info("Starting trading scheduler loop")
        while True:
            self.schedule.exec_jobs()
            time.sleep(1)


class TradingAgent(TradingScheduler):
    def __init__(self) -> None:
        super().__init__()
        self.schedule.weekly(Monday(), self.trader.one_best_trade)
