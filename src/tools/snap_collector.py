import json
import random
import time
from datetime import datetime
from pathlib import Path

from pymodbus.client import ModbusTcpClient

from logs.log_master import LogMaster
from src.tools.modbus_connect import ModbusDemoConnection  # noqa: F401

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEMO_MODE = 1
LOCAL_MODE = 2

SIMULATE_SNAP_DEMO = PROJECT_ROOT / "config" / "public" / "demo_snap.json"
REGISTERS_FILE = PROJECT_ROOT / "config" / "public" / "registers_victron.json" # VICTRON EXCEL INFORMATION ON DATA/PUBLIC/

CONFIG_FILE_LOCAL = PROJECT_ROOT / "config" / "local" / "config.json"
CONFIG_FILE_PUBLIC = PROJECT_ROOT / "config" / "public" / "example_config.json"

class Collector:
    
    def __init__(self, client, logger, mode=LOCAL_MODE):
        self.client = client
        self.logger = logger
        self.mode = mode
        
        self.number_snap = 0
        self.demo_register_values = {}
        
        if self.mode not in(DEMO_MODE, LOCAL_MODE):
            raise ValueError("Use DEMO_MODE or LOCAL_MODE")
        
        if (self.mode == LOCAL_MODE and self.client is None):
            raise ValueError("LOCAL_MODE requires a Modbus Client")
        
    def get_register(self, address, device_id):
        
        if self.mode == DEMO_MODE:
            register_key = (device_id, address)
        
            if (register_key not in self.demo_register_values):
                raise RuntimeError(
                    f"DEMO register not generated:"
                    f"{address} | "
                    f"Unit-ID {device_id}"
                )
            return self.demo_register_values[register_key]
    
        response = self.client.read_holding_registers(
            address=address,
            count=1,
            device_id=device_id,
        )

        if response.isError():
            raise RuntimeError(
                f"Error reading register "
                f"{address} | "
                f"Unit-ID {device_id}"
            )
        return response.registers[0]
        
    def collect_registers(self):

        with open(REGISTERS_FILE, "r", encoding="utf-8") as file:
            registers = json.load(file)

        # SELECT UNIT-IDS CONFIG
        if self.mode == DEMO_MODE:
            config_file = CONFIG_FILE_PUBLIC
        else:
            config_file = CONFIG_FILE_LOCAL

        with open(config_file, "r", encoding="utf-8") as file:
            system_config = json.load(file)

        unit_ids = system_config["unit_ids"]

        # ONLY DEMO GENERATES FAKE RAW VALUES
        if self.mode == DEMO_MODE:
            self.generate_register_values(registers=registers,unit_ids=unit_ids,)

        collected_snap = {}

        for name, config in registers.items():

            address = config["address"]

            service = config["service"]
            device_id = unit_ids[service]

            data_type = config["type"]
            scale = config["scale"]
            unit = config["unit"]

            raw_value = self.get_register(
                address=address,
                device_id=device_id,
            )

            if data_type == "int16" and raw_value >= 32768:
                raw_value -= 65536

            value = raw_value / scale

            collected_snap[name] = {
                "address": address,
                "device_id": device_id,
                "value": value,
                "unit": unit,
            }

            print(
                f"Address:{address:<4} | "
                f"Unit-ID: {device_id:<3} | "
                f"Name: {name:<18} | "
                f"Data: {value:<6} {unit}"
            )

        return collected_snap

    def generate_register_values(self, registers=None, unit_ids=None): # FOR DEMO!!
        if registers is None:
            with open(REGISTERS_FILE,"r", encoding="utf-8") as file:
                registers = json.load(file)
        
        generated_registers = {}
        demo_values = {}
        
        with open (SIMULATE_SNAP_DEMO, "r", encoding="utf-8") as file:
            values = json.load(file)
            
        profiles = values["profiles"]
        
        for name in registers:
            profile = profiles.get(name)
            
            if profile is None:
                demo_values[name] = 0
                continue
            
            demo_values[name] = random.uniform(profile["min"], profile["max"])
            
        # SOLAR_POWER ( VOLTAGE/CURRENT)
        
        if "solar_voltage" in demo_values and "solar_current" in demo_values and "solar_power" in demo_values:
            demo_values["solar_power"] = (demo_values["solar_voltage"] * demo_values["solar_current"])
            
        for name, config in registers.items():
                
                service = config["service"]
                device_id = unit_ids[service]
                
                address = config["address"]
                data_type = config["type"]
                scale = config["scale"]
                
                value = demo_values.get(name,0)
                raw_value = int(round(value * scale))  # noqa: RUF046
                
                # SIMULATE INT16 MODBUS DEMO
                
                if(data_type == "int16" and raw_value < 0):
                    raw_value += 65536
                if not 0 <= raw_value <= 65535:
                    raise ValueError(
                        f"Generated RAW value "
                        f"out of unit16 range: "
                        f"{name} = {raw_value}"
                    )
                register_key = (device_id, address)
                generated_registers[register_key] = raw_value
                
        self.demo_register_values = (generated_registers)
            
    def create_snapshot(self, total_snapshots=None):
        log_mode = "demo" if self.mode == DEMO_MODE else "local"
        
        try:
            registers = self.collect_registers()
            self.number_snap += 1
            snapshot = {"number": self.number_snap,"timestamp":datetime.now().isoformat(),"data": registers,}  # for BD  # noqa: DTZ005
            
            if total_snapshots is None:
                progress = f"({self.number_snap})"
            else:
                progress = f"({self.number_snap}/{total_snapshots})"
                
            self.logger.log("info",log_mode,"collector",f"Gathering the snap...{progress}")
            return snapshot
        
        except Exception as error:
            self.logger.log("error",log_mode,"collector",f"Snapshot failed: {error}")
            raise
        
def demo_bucle(collector, executions=100, interval_s=1):
    
    for _ in range(executions):
        
        try:
            collector.create_snapshot(total_snapshots=executions)
        except Exception:  # noqa: BLE001, S110
            pass
        
        time.sleep(interval_s)

#region MANUAL TESTING
if __name__ == "__main__":

    TEST_MODE = LOCAL_MODE
    SNAP_EXCE = 1

    logger = LogMaster()

    if TEST_MODE == DEMO_MODE:

        collector = Collector(client=None,logger=logger,mode=DEMO_MODE,)

        demo_bucle(collector=collector,executions=SNAP_EXCE,interval_s=1,)

    elif TEST_MODE == LOCAL_MODE:

        with open(CONFIG_FILE_LOCAL,"r",encoding="utf-8",) as file:
            config = json.load(file)

        cerbo_ip = config["modbus"]["ip_cerbo"]
        cerbo_port = config["modbus"]["port_cerbo"]
        interval_s = config["modbus"]["interval_seconds"]

        client = ModbusTcpClient(host=cerbo_ip, port=cerbo_port,)

        try:

            print(
                f"\nConnecting to Cerbo GX: "
                f"{cerbo_ip}:{cerbo_port}"
            )

            if not client.connect():
                raise ConnectionError("Could not connect to Cerbo GX")

            print("Connected to Cerbo GX\n")
            collector = Collector(client=client,logger=logger,mode=LOCAL_MODE,)

            for _ in range(SNAP_EXCE):

                try:
                    snapshot = collector.create_snapshot(total_snapshots=SNAP_EXCE)

                except Exception:  # noqa: BLE001, S110
                    pass

                time.sleep(interval_s)

        finally:
            client.close()
            print("\nConnection closed")
#endregion