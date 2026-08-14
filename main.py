import json
import time
from pathlib import Path

from logs.log_master import LogMaster
from src.tools.modbus_connect import select_connection
from src.tools.snap_collector import Collector

# ROUTE PATH
PROJECT_ROOT = Path(__file__).resolve().parent

# CONSTANTS
DEMO_MODE = 1
LOCAL_MODE = 2

BATCH_SIZE = 100

# FILES PATH
CONFIG_FILE_LOCAL = PROJECT_ROOT/ "config"/ "local"/ "config.json"
CONFIG_FILE_PUBLIC = PROJECT_ROOT/ "config"/ "public"/ "example_config.json"

def main():

    logger = LogMaster()
    connection = None
    
# SELECT CONNECTION MODE
    try:
        
        connection_mode = int(input("Select connection mode ""[1 DEMO / 2 LOCAL]: "))
        connection = select_connection(connection_mode=connection_mode,logger=logger,)

        if not connection.open_connection():
            return

        if not connection.check_connection():
            raise ConnectionError("Modbus connection is not available.")

        if connection_mode == DEMO_MODE:
            config_file = CONFIG_FILE_PUBLIC
            collector_client = None
            log_mode = "demo"

        else:
            config_file = CONFIG_FILE_LOCAL
            collector_client = connection.client
            log_mode = "local"

        with open(config_file,"r",encoding="utf-8",) as file:
            config = json.load(file)

        interval_s = config["modbus"]["interval_seconds"]

        collector = Collector(client=collector_client, logger=logger, mode=connection_mode)

        # SQLITE
        batch = []
        batch_number = 0

        logger.log("info",log_mode,"collector","Continuous collector started.",)

        # LOOP
        while True:

            try:
                snapshot = collector.create_snapshot()
                batch.append(snapshot)

                if len(batch) >= BATCH_SIZE:
                    batch_number += 1
                    logger.log("info",log_mode,"collector",(f"Batch {batch_number} ready: {len(batch)} snapshots."))
                    batch.clear()

            except Exception:  # noqa: BLE001, S110
                pass

            time.sleep(interval_s)

    except ValueError:
        pass
        
    except KeyboardInterrupt:

        logger.log("warn","system","collector","Manual stop requested (Ctrl+C).")

    finally:

        if connection is not None:
            connection.close_connection()

if __name__ == "__main__":
    main()