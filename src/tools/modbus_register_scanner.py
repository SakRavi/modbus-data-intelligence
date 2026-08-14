# SIN USAR ( PENDIENTE DE MODIFICAR)

import json
from pathlib import Path

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

PATH_ROOT = (Path(__file__).resolve().parents[2])
PATH_ROOT_STR =str(PATH_ROOT)
ROUTE_CONFIG = PATH_ROOT / "config" / "local" / "config.json"

with ROUTE_CONFIG.open("r", encoding="utf-8") as file:
    config = json.load(file)
    host = config["ip_cerbo"]

def uint16_to_int16(value):

    if value >= 32768:
        return value - 65536

    return value

def scan_registers(client, device_id, start_register, end_register):

    for register in range(start_register, end_register + 1):

        try:
            response = client.read_holding_registers(
                address=register,
                count=1,
                device_id=device_id
            )
            if response.isError():
                continue
            raw_value = response.registers[0]
            signed_value = uint16_to_int16(raw_value)

            print(
                f"Register {register:4} | "
                f"raw={raw_value:5} | "
                f"int16={signed_value:6}"
            )

        except ModbusException:
            continue

def scan_unit_ids(ip, port=502):

    client = ModbusTcpClient(
        host=ip,
        port=port
    )

    if not client.connect():
        print("Cerbo GX connection failed")
        return

    try:
        for unit_id in range(0, 256):

            response = client.read_holding_registers(
                address=0,
                count=1,
                device_id=unit_id
            )

            print(
                unit_id,
                response
            )

    finally:
        client.close()
        
# SCANNER
client = ModbusTcpClient(host=host,port=502)

if not client.connect():
    print("CONNECTION FAILED")
    raise SystemExit

print("CONNECTED")

try:

    for device_id in range(0, 256):

        response = client.read_holding_registers(
            address=776, # change for scaning
            count=1,
            device_id=device_id
        )

        if not response.isError():

            print(
                f"ID {device_id:3} | "
                f"REGISTER 259 | "
                f"VALUE {response.registers[0]}"
            )

        else:

            print(
                f"ID {device_id:3} | "
                f"ERROR {response.exception_code}"
            )

finally:
    client.close()
    


