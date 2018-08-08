import logging
import datetime
import os

if not os.path.exists('logs'):
    os.mkdir('logs')

log_creation_date = datetime.datetime.now()
fh = logging.FileHandler('logs/log-{}{}{}{}{}.log'.format(log_creation_date.year, log_creation_date.month,
                                                          log_creation_date.day, log_creation_date.hour,
                                                          log_creation_date.minute))
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
