# CONECTION VICTRON 
# ! change the config.json file to your local config.

import json
import sys
from pathlib import Path

# route path from logs
PATH_ROOT = (Path(__file__).resolve().parent.parent)
PATH_ROOT_STR =str(PATH_ROOT)

if (PATH_ROOT_STR not in sys.path):
    sys.path.append(PATH_ROOT_STR)

from logs.log_master import LogMaster
from src.utils.loading import fake_loading

# LOGGER
LOG_FILE = PATH_ROOT / "logs" / "local" / "mdi.log"
logger = LogMaster(log_file=LOG_FILE)

# CONFIG. FILES
ROUTE_CONFIG = (PATH_ROOT / "config" / "local" / "config.json")
ROUTE_CONFIG_DEMO = (PATH_ROOT / "config" / "public" / "example_config.json")

# CONFIG FILES SHORT
SHORT_ROUTE_CONFIG = ("/" + ROUTE_CONFIG.relative_to(PATH_ROOT.parent).as_posix())
SHORT_ROUTE_CONFIG_DEMO = ("/" + ROUTE_CONFIG_DEMO.relative_to(PATH_ROOT.parent).as_posix())

# LOCAL
def load_config():
    
    fake_loading("local")
    
    # FILE FOUND
    try:
        with ROUTE_CONFIG.open("r", encoding="utf-8") as file:
            CONFIG = json.load(file)
            
            logger.log("info","local","config",f"Configuration file loaded: {SHORT_ROUTE_CONFIG}")
            return CONFIG
            
    except FileNotFoundError:
        logger.log("error","local","config",f"File not found: {SHORT_ROUTE_CONFIG}",)
        
    # INVALID SYNTAX
    except json.JSONDecodeError as error:
        logger.log(
            "error","local","config",
            (
                "Invalid JSON syntax "
                f"at line{error.lineno},column{error.colno}: "
                f"{error.msg} "
                ),
            )
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

# DEMO
def load_demo_config():
    fake_loading("demo")
    
    # FILE FOUND
    try:
        with ROUTE_CONFIG_DEMO.open("r", encoding="utf-8") as file:
            CONFIG = json.load(file)
            
            logger.log("info","demo","config",f"Configuration file loaded: {SHORT_ROUTE_CONFIG_DEMO}")
            return CONFIG
            
    except FileNotFoundError:
        logger.log("error","demo","config",f"File not found: {SHORT_ROUTE_CONFIG_DEMO}",)
        
    # INVALID SYNTAX
    except json.JSONDecodeError as error:
        logger.log(
            "error","demo","config",
            (
                "Invalid JSON syntax "
                f"at line{error.lineno},column{error.colno}: "
                f"{error.msg} "
                ),
            )
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


# TEST
# load_config()
# load_demo_config()

