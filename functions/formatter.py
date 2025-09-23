import logging
class Formatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(levelname)s:%(lineno)d] %(message)s "

    FORMATS = {
        logging.DEBUG: "\x1b[1;93m[%(levelname)s:%(lineno)d] \x1b[0;96m%(message)s %(filename)s",
        logging.INFO:  "\x1b[1;93m[%(levelname)s:%(lineno)d] \x1b[0;96m%(message)s",
        logging.WARNING: yellow + format + reset,
        logging.ERROR: f"{red} {format}  %(filename)s {reset}",
        logging.CRITICAL:  "\x1b[1;91m[%(levelname)s:%(lineno)d] \x1b[1;31m%(message)s"
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
