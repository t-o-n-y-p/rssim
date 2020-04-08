from sys import exit, exc_info
from os import path, mkdir
from datetime import datetime
from traceback import print_tb
from ctypes import windll

from exceptions import VideoAdapterNotSupportedException, MonitorNotSupportedException, UpdateIncompatibleException, \
    HackingDetectedException
from rssim_core import Launcher
from ui import WINDOW


def main():
    try:
        Launcher().run()
    except (
        VideoAdapterNotSupportedException, MonitorNotSupportedException,
        UpdateIncompatibleException, HackingDetectedException
    ) as e:
        WINDOW.close()
        windll.user32.MessageBoxW(None, e.text, e.caption, 0x1000)
    except Exception:
        if not path.exists('logs'):
            mkdir('logs')

        crash_datetime = datetime.now()
        filename = 'logs/logs_{0}_{1:0>2}-{2:0>2}-{3:0>2}-{4:0>6}.crash'.format(
            str(crash_datetime.date()), crash_datetime.time().hour, crash_datetime.time().minute,
            crash_datetime.time().second, crash_datetime.time().microsecond
        )
        with open(filename, 'w') as crash_dump:
            crash_dump.write('Traceback (most recent call last):\n')
            print_tb(exc_info()[2], file=crash_dump)
            crash_dump.write('{}: {}\n'.format(exc_info()[0].__name__, exc_info()[1]))
    finally:
        exit()


if __name__ == '__main__':
    main()
