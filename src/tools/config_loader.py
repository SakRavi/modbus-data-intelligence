# JSON LOADER CERBO GX
# ! change the config.json file to your local config.

#region IMPORTS
import json
import sys
from pathlib import Path

#endregion

#region ROUTE PATH FROM LOGS

PATH_ROOT = (Path(__file__).resolve().parents[2])
PATH_ROOT_STR =str(PATH_ROOT)

if PATH_ROOT_STR not in sys.path:
    sys.path.append(PATH_ROOT_STR)

from logs.log_master import LogMaster
from src.utils.loading import fake_loading_tqdm

#endregion

#region LOGGER

LOG_FILE = PATH_ROOT / "logs" / "local" / "mdi.log"
logger = LogMaster(log_file=LOG_FILE)

#endregion

#region CONFIG. FILES

ROUTE_CONFIG = PATH_ROOT / "config" / "local" / "config.json"
ROUTE_CONFIG_DEMO = PATH_ROOT / "config" / "public" / "example_config.json"

#endregion

#region CONFIG FILES SHORT

SHORT_ROUTE_CONFIG = "/" + ROUTE_CONFIG.relative_to(PATH_ROOT.parent).as_posix()
SHORT_ROUTE_CONFIG_DEMO = "/" + ROUTE_CONFIG_DEMO.relative_to(PATH_ROOT.parent).as_posix()

#endregion

#region LOCAL
def load_config():

    fake_loading_tqdm(environment="local")

    # FILE FOUND
    try:
        with ROUTE_CONFIG.open("r", encoding="utf-8") as file:
            config = json.load(file)

            logger.log("info","local","config",f"Configuration file loaded: {SHORT_ROUTE_CONFIG}")
            return config

    except FileNotFoundError:
        logger.log("error","local","config",f"File not found: {SHORT_ROUTE_CONFIG}",)

    # INVALID SYNTAX
    except json.JSONDecodeError as error:
        logger.log("error","local","config",f"Invalid JSON syntax at line{error.lineno},column{error.colno}: {error.msg}",)

    # INVALID PERMISSION FILE
    except PermissionError:
        logger.log("error","local","config",f"Permission denied: {SHORT_ROUTE_CONFIG}",)

    # UNICODE ERROR
    except UnicodeDecodeError as error:
        logger.log("error","local","config",f"Invalid UTF-8 encoding: {error}",)

    # OS ERROR
    except OSError as error:
        logger.log("crit","local","config",f"Operating system error: {error}")

    return None

#endregion

#region DEMO
def load_demo_config():
    fake_loading_tqdm(environment="demo")

    # FILE FOUND
    try:
        with ROUTE_CONFIG_DEMO.open("r", encoding="utf-8") as file:
            config = json.load(file)

            logger.log("info","demo","config",f"Configuration file loaded: {SHORT_ROUTE_CONFIG_DEMO}")
            return config

    except FileNotFoundError:
        logger.log("error","demo","config",f"File not found: {SHORT_ROUTE_CONFIG_DEMO}",)

    # INVALID SYNTAX
    except json.JSONDecodeError as error:
        logger.log("error","demo","config",f"Invalid JSON syntax at line{error.lineno},column{error.colno}: {error.msg}",)

    # INVALID PERMISSION FILE
    except PermissionError:
        logger.log("error","demo","config",f"Permission denied: {SHORT_ROUTE_CONFIG_DEMO}",)

    # UNICODE ERROR
    except UnicodeDecodeError as error:
        logger.log("error","demo","config",f"Invalid UTF-8 encoding: {error}",)

    # OS ERROR
    except OSError as error:
        logger.log("crit","demo","config",f"Operating system error: {error}")

    return None

#endregion

#region MANUAL TEST
if __name__ == "__main__":
    load_config()
    load_demo_config()

#endregion

