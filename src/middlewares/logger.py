import logging
import colorlog

# Create a custom logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# Create a handler
handler = logging.StreamHandler()

# Create a formatter with colorlog
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s: %(message)s",
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

# Add the formatter to the handler
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)
