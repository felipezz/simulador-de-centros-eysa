import time

from tb_gateway_mqtt import TBGatewayMqttClient
from tb_device_mqtt import TBPublishInfo

from config import HOST, PORT, gateway_token


TOKEN = gateway_token("A-42")

DEVICES = [
    "dfm-general",
    "dfm-aux",
]


def uint16s_to_hex(values):
    """Convierte una lista de uint16 al string HEX esperado por la Rule Chain."""
    return "".join(f"{value:04x}" for value in values)


def total_fuel_to_registers(liters):
    """
    Rule Chain:
        raw = (uints[4] * 65536) + uints[5]
        litros = raw * 0.001
    """
    raw = int(liters * 1000)

    high = (raw >> 16) & 0xFFFF
    low = raw & 0xFFFF

    return high, low


def build_gc():
    # Queremos simular aproximadamente 12.345,678 litros acumulados
    fuel_high, fuel_low = total_fuel_to_registers(12345.678)

    registers = [0] * 16

    # uints[0] * 0.05 → EngineFuelRate
    # 600 * 0.05 = 30 L/h
    registers[0] = 600

    # uints[3] - 40 → fuelTemp
    # 65 - 40 = 25 °C
    registers[3] = 65

    # uints[4:5] → EngineTotalFuelUsed
    registers[4] = fuel_high
    registers[5] = fuel_low

    # Estados
    registers[11] = 1       # engineMode

    # uints[12] * 0.05 → feedRateLh
    registers[12] = 700     # 35 L/h

    # uints[13] * 0.05 → returnRateLh
    registers[13] = 100     # 5 L/h

    # Estados cámaras
    registers[14] = 1       # statusCamaraIn
    registers[15] = 0       # statusCamaraOut

    return uint16s_to_hex(registers)


gateway = TBGatewayMqttClient(
    HOST,
    port=PORT,
    username=TOKEN,
)

print("Conectando...")
gateway.connect()

gc = build_gc()

for device in DEVICES:
    gateway.gw_connect_device(device)

    timestamp = int(time.time() * 1000)

    # Ráfaga gc: en producción será cada 5 segundos
    result = gateway.gw_send_telemetry(
        device,
        {
            "ts": timestamp,
            "values": {
                "gc": gc
            }
        },
        quality_of_service=1,
    )

    success = result.get() == TBPublishInfo.TB_ERR_SUCCESS

    print(f"{device}: gc enviado → {success}")

    # hoursOp: en producción será cada 60 segundos
    result = gateway.gw_send_telemetry(
        device,
        {
            "ts": int(time.time() * 1000),
            "values": {
                "hoursOp": 1234.5
            }
        },
        quality_of_service=1,
    )

    success = result.get() == TBPublishInfo.TB_ERR_SUCCESS

    print(f"{device}: hoursOp enviado → {success}")

gateway.disconnect()

print("Desconectado.")
