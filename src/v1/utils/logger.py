"""Logging script"""
import os
import logging

if not os.path.exists(os.path.join(os.getcwd(), 'logs')):
    os.mkdir(os.path.join(os.getcwd(), 'logs'))
    
# create logger
logger = logging.getLogger('api-v1')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler(os.path.join(os.getcwd(), 'logs/log_file.v1.log'))

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s | %(levelname)s | %(message)s')

# add formatter to ch
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add ch to logger
logger.addHandler(fh)
logger.addHandler(ch)