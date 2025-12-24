import logging

LOG_LEVEL = 'DEBUG'
LOGGER = logging.getLogger('Broker-Logger')
LOGGER.setLevel(LOG_LEVEL)

logging.basicConfig(
    format='[%(asctime)s] [%(threadName)s][%(filename)s:%(lineno)d][%(name)s-%(levelname)s]: %(message)s',
    level=LOG_LEVEL
)

logging.info(f"Using Debug Level '{LOG_LEVEL}'")