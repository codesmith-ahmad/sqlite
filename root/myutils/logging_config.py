# Setup logger to my own tastes for debugging purposes

import configparser
import logging

config = configparser.ConfigParser()
config.read('config.ini')

if not logging.getLogger().hasHandlers():
    logging.basicConfig(filename=config['Logfile']['filename'],
                        filemode='w',
                        level=logging.INFO,
                        format='%(asctime)s [%(filename)s:%(lineno)d] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S'
                        )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)