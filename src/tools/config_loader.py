# JSON LOADER CERBO GX
# ! change the config.json file to your local config.

import json
from pathlib import Path

PATH_ROOT = (Path(__file__).resolve().parents[2])
PATH_ROOT_STR =str(PATH_ROOT)

from logs.log_master import LogMaster
from src.utils.loading import fake_loading_tqdm

LOG_FILE = PATH_ROOT / "logs" / "local" / "mdi.log"

logger = LogMaster(log_file=LOG_FILE)

ROUTE_CONFIG = PATH_ROOT / "config" / "local" / "config.json"
ROUTE_CONFIG_DEMO = PATH_ROOT / "config" / "public" / "example_config.json"

SHORT_ROUTE_CONFIG = "/" + ROUTE_CONFIG.relative_to(PATH_ROOT.parent).as_posix()
SHORT_ROUTE_CONFIG_DEMO = "/" + ROUTE_CONFIG_DEMO.relative_to(PATH_ROOT.parent).as_posix()

def load_config():

    fake_loading_tqdm(environment="local")

    try:
        with ROUTE_CONFIG.open("r", encoding="utf-8") as file:
            config = json.load(file)

            logger.log("info","local","config",f"Configuration file loaded: {SHORT_ROUTE_CONFIG}")
            return config

    except FileNotFoundError:
        logger.log("error","local","config",f"File not found: {SHORT_ROUTE_CONFIG}",)

    except json.JSONDecodeError as error:
        logger.log("error","local","config",f"Invalid JSON syntax at line{error.lineno},column{error.colno}: {error.msg}",)

    except PermissionError:
        logger.log("error","local","config",f"Permission denied: {SHORT_ROUTE_CONFIG}",)

    except UnicodeDecodeError as error:
        logger.log("error","local","config",f"Invalid UTF-8 encoding: {error}",)

    except OSError as error:
        logger.log("crit","local","config",f"Operating system error: {error}")

    return None

def load_demo_config():
    fake_loading_tqdm(environment="demo")

    try:
        with ROUTE_CONFIG_DEMO.open("r", encoding="utf-8") as file:
            config = json.load(file)

            logger.log("info","demo","config",f"Configuration file loaded: {SHORT_ROUTE_CONFIG_DEMO}")
            return config

    except FileNotFoundError:
        logger.log("error","demo","config",f"File not found: {SHORT_ROUTE_CONFIG_DEMO}",)

    except json.JSONDecodeError as error:
        logger.log("error","demo","config",f"Invalid JSON syntax at line{error.lineno},column{error.colno}: {error.msg}",)

    except PermissionError:
        logger.log("error","demo","config",f"Permission denied: {SHORT_ROUTE_CONFIG_DEMO}",)

    except UnicodeDecodeError as error:
        logger.log("error","demo","config",f"Invalid UTF-8 encoding: {error}",)

    except OSError as error:
        logger.log("crit","demo","config",f"Operating system error: {error}")

    return None

if __name__ == "__main__":
    load_config()
    load_demo_config()


