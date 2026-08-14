from pymodbus.client import ModbusTcpClient

from logs.log_master import LogMaster
from src.tools.config_loader import load_config, load_demo_config
from src.utils.loading import fake_loading_tqdm

TIMEOUT = 3
RETRIES = 3
class ModbusLocalConnection:

    def __init__(self,logger):
        self.logger = logger
        self.client = None
        self.host = None
        self.port = None
        self.config_loaded = self.load_connection_config()

    def load_connection_config(self):
        try:
            config = load_config()
            self.host = config["modbus"]["ip_cerbo"]
            self.port = int(config["modbus"]["port_cerbo"])
            self.logger.log("debug","local","config","Modbus connection configuration loaded...")
            return True

        except KeyError as error:
            self.host = None
            self.port = None
            self.logger.log("error","local","config",f"Required configuration key missing: {error}.")
            return False

        except (TypeError, ValueError) as error:
            self.host = None
            self.port = None
            self.logger.log("error","local","config",f"Invalid Modbus connection Config.: {error}.")
            return False

        except Exception as error:  # noqa: BLE001
            self.host = None
            self.port = None
            self.logger.log("crit","local","config",f"Unexpected config. error: {type(error).__name__}: {error}.")
            return False

    def create_client(self):
        if not self.config_loaded:
            self.logger.log("error","local","modbus","Modbus client cannot be created without configuration.",)
            return False

        try:
            self.client = ModbusTcpClient(
                host=self.host,
                port=self.port,
                timeout=TIMEOUT,
                retries=RETRIES,
            )
            self.logger.log("debug","local","modbus","Create Modbus client...")
            return True

        except (TypeError, ValueError) as error:
            self.client = None
            self.logger.log("error","local","modbus",f"Invalid Modbus client configuration: {error}.",)
            return False

        except Exception as error:  # noqa: BLE001
            self.client = None
            self.logger.log("crit","local","modbus",f"Unexpected Modbus client creation error: {type(error).__name__}: {error}.")
            return False

    def open_connection(self):
        if self.client is None and not self.create_client():
            return False

        if self.client.connected:
            self.logger.log("warn","local","modbus","Modbus connection already opened",)
            return True

        try:
            connected = self.client.connect()
            if not connected:
                self.logger.log("error","local","modbus","Modbus connection failed.")
                return False
            fake_loading_tqdm(environment="local")
            self.logger.log("info","local","modbus","Modbus connection opened")
            return True

        except (TimeoutError, OSError) as error:
            self.logger.log("error","local","modbus",f"Modbus network connection error: {type(error).__name__}: {error}.")
            return False

        except Exception as error:  # noqa: BLE001
            self.logger.log("crit","local","modbus",f"Unexpected Modbus connection error: {type(error).__name__}: {error}.")
            return False

    def check_connection(self):
        if self.client is None:
            return False

        try:
            return self.client.connected

        except Exception as error:  # noqa: BLE001
            self.logger.log("error","local","modbus",f"Modbus check error: {type(error).__name__}: {error}.")
            return False

    def close_connection(self):
        if self.client is None:
            self.logger.log("warn","local","modbus","Close requested without a Modbus client.",)
            return False
        try:
            was_connected = self.client.connected
            self.client.close()
            self.client = None
            if was_connected:
                self.logger.log("info","local","modbus","Modbus connection closed...",)

            else:
                self.logger.log("warn","local","modbus","Modbus client removed, but connection was already closed.",)
            return True

        except Exception as error:  # noqa: BLE001
            self.client = None

            self.logger.log("error","local","modbus",f"Modbus connection closing error: {type(error).__name__}: {error}.")
            return False
class DemoModbusClient:

    def __init__(self, host, port, timeout, retries):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.retries = retries
        self.connected = False

    def connect(self):
        self.connected = True
        return True

    def close(self):
        self.connected = False
class ModbusDemoConnection:

    def __init__(self, logger):
        self.logger = logger
        self.client = None
        self.host = None
        self.port = None
        self.config_loaded = self.load_connection_config()

    def load_connection_config(self):
        try:
            config = load_demo_config()
            self.host = config["modbus"]["ip_cerbo"]
            self.port = int(config["modbus"]["port_cerbo"])
            self.logger.log("debug","demo","config","Modbus connection configuration loaded...")
            return True

        except KeyError as error:
            self.host = None
            self.port = None
            self.logger.log("error","demo","config",f"Required configuration key missing: {error}.")
            return False

        except (TypeError, ValueError) as error:
            self.host = None
            self.port = None
            self.logger.log("error","demo","config",f"Invalid Modbus connection Config.: {error}.")
            return False

        except Exception as error:  # noqa: BLE001
            self.host = None
            self.port = None
            self.logger.log("crit","demo","config",f"Unexpected config. error: {type(error).__name__}: {error}.")
            return False

    def create_client(self):
        if not self.config_loaded:
            self.logger.log("error","demo","modbus","Modbus client cannot be created without configuration.")
            return False

        try:
            self.client = DemoModbusClient(
                host=self.host,
                port=self.port,
                timeout=TIMEOUT,
                retries=RETRIES,
            )
            self.logger.log("debug","demo","modbus","Create Modbus client...")
            return True

        except (TypeError, ValueError) as error:
            self.client = None
            self.logger.log("error","demo","modbus",f"Invalid Modbus client configuration: {error}.")
            return False

        except Exception as error:  # noqa: BLE001
            self.client = None
            self.logger.log("crit","demo","modbus",f"Unexpected Modbus client creation error: {type(error).__name__}: {error}.")
            return False

    def open_connection(self):
        if self.client is None and not self.create_client():
            return False

        if self.client.connected:
            self.logger.log("warn","demo","modbus","Modbus connection already opened.")
            return True

        try:
            connected = self.client.connect()

            if not connected:
                self.logger.log("error","demo","modbus","Modbus connection failed.")
                return False

            fake_loading_tqdm(environment="demo")
            self.logger.log("info","demo","modbus","Modbus connection opened.")
            return True

        except (TimeoutError, OSError) as error:
            self.logger.log("error","demo","modbus",f"Modbus network connection error: {type(error).__name__}: {error}.")
            return False

        except Exception as error:  # noqa: BLE001
            self.logger.log("crit","demo","modbus",f"Unexpected Modbus connection error: {type(error).__name__}: {error}.")
            return False

    def check_connection(self):
        if self.client is None:
            return False

        try:
            return self.client.connected

        except Exception as error:  # noqa: BLE001
            self.logger.log("error","demo","modbus",f"Modbus check error: {type(error).__name__}: {error}.")
            return False

    def close_connection(self):
        if self.client is None:
            self.logger.log("warn","demo","modbus","Close requested without a Modbus client.")
            return False

        try:
            was_connected = self.client.connected
            self.client.close()
            self.client = None

            if was_connected:
                self.logger.log("info","demo","modbus","Modbus connection closed...")

            else:
                self.logger.log("warn","demo","modbus","Modbus client removed, but connection was already closed.")

            return True

        except Exception as error:  # noqa: BLE001
            self.client = None
            self.logger.log("error","demo","modbus",f"Modbus connection closing error: {type(error).__name__}: {error}.")
            return False

def select_connection(connection_mode: int, logger):

    try:
        if connection_mode == 1:
            logger.log("info","demo","selector","DEMO connection mode selected")
            return ModbusDemoConnection(logger=logger)

        elif connection_mode == 2:
            logger.log("info","local","selector","LOCAL connection mode selected")
            return ModbusLocalConnection(logger=logger)

        else:
            raise ValueError("Use 1 for DEMO or 2 for LOCAL.")

    except (TypeError, ValueError) as error:
        logger.log("error","system","selector",f"connection mode selection failed: {error}")
        raise

if __name__ == "__main__":

    logger = LogMaster()
    connection = None

    try:
        connection_mode = int(
            input("Select connection mode [1 DEMO / 2 LOCAL]: ")
        )

        connection = select_connection(
            connection_mode=connection_mode,
            logger=logger
        )

        connection.create_client()
        connection.open_connection()
        connection.check_connection()

    except ValueError:
        pass

    except KeyboardInterrupt:
        logger.log("warn","system","selector","Manual connection test cancelled.")
        
    finally:
        if connection is not None:
            connection.close_connection()
