import datetime
import time

import xbmc
import xbmcgui
from default import run_converter
from resources import utils as utils


__license__ = "MIT"

SECONDS_PER_HOUR = 60 * 60


class ConversionScheduler:
    @staticmethod
    def is_enabled():
        if utils.setting("enable_scheduler") == "true":
            if utils.setting("delay_while_playing") == "true":
                return not xbmc.Player().isPlaying()
            else:
                return True
        else:
            return False

    def __init__(self):
        self.next_run = 0
        self.setup()
        self.monitor = SettingsChangedMonitor(callback=self.setup)

    def setup(self):
        if self.is_enabled():
            #scheduler was turned on, find next run time
            utils.log("Scheduler enabled, finding next run time")
            self.next_run = 0
            self.setup_next_run(time.time())
            utils.log("Scheduler will run again on " + datetime.datetime.fromtimestamp(self.next_run).strftime('%m-%d-%Y %H:%M'))

    def setup_next_run(self, now):
        new_run_time = self.next_run
        schedule_type = int(utils.setting("schedule_interval"))

        if self.next_run <= now:
            if schedule_type == 0:
                new_run_time = now + SECONDS_PER_HOUR
            else:
                hour_of_day = int(utils.setting("schedule_time")[0:2])

                delay_map = {
                    1: 24,
                    2: 3 * 24,
                    3: 7 * 24
                }

                dt = datetime.datetime.fromtimestamp(now).replace(hour=hour_of_day)
                dt += datetime.timedelta(hours=delay_map[schedule_type])
                new_run_time = time.mktime(dt.timetuple())

        if new_run_time != self.next_run:
            self.next_run = new_run_time
            next_run = datetime.datetime.fromtimestamp(self.next_run).strftime('%m-%d-%Y %H:%M')
            utils.show_notification(utils.l10n(30050) % next_run)
            utils.log("Scheduler will run again on " + next_run)

    def run(self):
        while not xbmc.abortRequested:
            if self.is_enabled():  # scheduler is still on
                now = time.time()

                if self.next_run <= now:
                    run_converter(True)
                    self.setup_next_run(now)

            xbmc.sleep(5000)

        del self.monitor  # delete monitor to free up memory


class SettingsChangedMonitor(xbmc.Monitor):
    update_method = None

    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)
        self.callback = kwargs['callback']

    def onSettingsChanged(self):
        self.callback()


ConversionScheduler().run()
