import logging
import sys
from colorama import init, Fore, Style

init(autoreset=True, strip=False)

CUSTOM_LEVELS = {
    'SECURITY': 60,
    'METRIC': 17,
}

for level_name, level_value in CUSTOM_LEVELS.items():
    logging.addLevelName(level_value, level_name)
    setattr(logging.Logger, level_name.lower(), lambda self, msg, *a, lv=level_value, **kw: self._log(lv, msg, a, **kw) if self.isEnabledFor(lv) else None)

class ColorLogFormatter(logging.Formatter):
    COLOR_MAP = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
        CUSTOM_LEVELS['SECURITY']: Fore.MAGENTA + Style.BRIGHT,
        CUSTOM_LEVELS['METRIC']: Fore.CYAN + Style.BRIGHT,
    }

    def format(self, record):
        color = self.COLOR_MAP.get(record.levelno, "")
        time = self.formatTime(record, "%H:%M:%S")
        level = record.levelname.upper().center(10)
        file = f"{record.filename}:{record.lineno}"
        msg = super().format(record)
        base = f"[{time}] {color}[{level}]{Style.RESET_ALL}"
        return f"{base} {msg}" if record.levelno == CUSTOM_LEVELS['METRIC'] else f"{base} {file} › {msg}"

def get_logger(name="logger"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(ColorLogFormatter('%(message)s'))
        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.propagate = False
    return logger

logger = get_logger()
