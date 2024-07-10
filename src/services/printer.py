class Printer:
    _instance = None

    COLOR_CODES = {
        "purple": "\033[95m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "bold_green": "\033[1m\033[92m",
        "bold_purple": "\033[1m\033[95m",
        "bold_yellow": "\033[1m\033[93m",
        "green": "\033[92m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "bold_red": "\033[1m\033[91m",
        "bold_blue": "\033[1m\033[94m",
        "bold_cyan": "\033[1m\033[96m",
        "bold_white": "\033[1m\033[97m",
        "white": "\033[97m",
        "bold_black": "\033[1m\033[30m",
        "black": "\033[30m",
        "bold_magenta": "\033[1m\033[35m",
        "magenta": "\033[35m"
    }

    RESET_CODE = "\033[00m"

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Printer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        pass

    def print(self, content: str, color: str = "bold_yellow"):
        color_code = self.COLOR_CODES.get(color, "")
        reset_code = self.RESET_CODE if color_code else ""
        print(f"{color_code}{content}{reset_code}")
