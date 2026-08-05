# LOG MASTER
# ! SUB LEVEL 2 LOG (line 54 INFO)
#region IMPORTS

from datetime import datetime
from pathlib import Path

#endregion

#region CLASS LOG
class LogMaster:

    # ANSI COLORS
    RESET = "\033[0m"

    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"

    CRITICAL = "\033[97;41m"

    def __init__(self, log_file="logs/local/mdi.log"):

        # FIRST LEVEL (MASTER)

        self.levels = {
            "info": "INFO",
            "warn": "WARN",
            "debug": "DEBUG",
            "crit": "CRIT",
            "error": "ERROR",
        }
        self.level_colors = {
            "info": self.GREEN,
            "warn": self.YELLOW,
            "debug": self.CYAN,
            "crit": self.CRITICAL,
            "error": self.RED,
        }
        # SUB LEVEL DEMO/LOCAL

        self.sublevels1 = {
            "demo": "DEMO",
            "local": "LOCAL",
            "system": "SYSTEM",

        }
        self.sublevels1_colors = {
            "demo": self.PURPLE,
            "local": self.GREEN,
            "system": self.YELLOW,
        }
        # SUB LEVEL (MDI)
        # !NOTE: CHANGE THE SUBLEVELS ACCORDING TO THE PROJECT NEEDS

        self.sublevels2 = {
            "modbus": "MODBUS",
            "config": "CONFIG",
            "database": "DATABASE",
            "battery": "BATTERY",
            "collector": "COLLECTOR",
            "selector": "SELECTOR"
        }
        # .LOG FILE

        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def log(self,level,sublevel1,sublevel2,message):

        # TIMESTAMP LOG

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # noqa: DTZ005

        # LEVELS AND SUBLEVELS

        level_key = level.lower()
        sublevel1_key = sublevel1.lower()
        sublevel2_key = sublevel2.lower()

        level_name = self.levels.get(level_key,"UNKNOWN",)
        sublevel1_name = self.sublevels1.get(sublevel1_key,"UNKNOWN",)
        sublevel2_name = self.sublevels2.get(sublevel2_key,"UNKNOWN",)
        level_color = self.level_colors.get(level_key,self.RESET,)
        sublevel1_color = self.sublevels1_colors.get(sublevel1_key,self.RESET,)

        # TERMINAL PRINT WITH COLORS

        terminal_message = (
            f"[{timestamp}] "
            f"[{level_color}{level_name:<5}{self.RESET}] "
            f"[{sublevel1_color}{sublevel1_name:<6}{self.RESET}] "
            f"[{sublevel2_name:<9}] "
            f"{message}"
        )

        # FILE CLEAN

        file_message = (
            f"[{timestamp}] "
            f"[{level_name:<5}] "
            f"[{sublevel1_name:<5}] "
            f"[{sublevel2_name:<9}] "
            f"{message}"
        )

        # TERMINAL PRINT

        print(terminal_message)

        # SAVE LOG AND NO ERASE THE FILE ("a"=APPEND MODE)

        with self.log_file.open(mode="a",encoding="utf-8") as file: # UNIVERSAL ENCODING
            file.write(file_message + "\n")

#endregion

#region MANUAL TEST
if __name__ == "__main__":
    logger = LogMaster()

    logger.log("info","local","modbus","This is a test message for the MODBUS category.",)
    logger.log("warn","local","modbus","This is a test message for the MODBUS category.",)
    logger.log("debug","local","modbus","This is a test message for the MODBUS category.",)
    logger.log("crit","local","modbus","This is a test message for the MODBUS category.",)
    logger.log("error","demo","modbus","This is a test message for the MODBUS category.",)

#endregion