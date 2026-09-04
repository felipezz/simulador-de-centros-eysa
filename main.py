import time

from tb_gateway_mqtt import TBGatewayMqttClient

from config import HOST, PORT, CENTERS
from simulators.power_meter import PowerMeterSimulator
from simulators.dfm import DfmSimulator
from simulators.tank import TankSimulator


def main():
    gateways = []
    simulators = []

    try:
        for center in CENTERS:
            print(f"Conectando gateway de {center['name']}...")

            gateway = TBGatewayMqttClient(
                HOST,
                port=PORT,
                username=center["gateway_token"],
            )

            gateway.connect()
            gateways.append(gateway)

            # Power Meters
            for pm_config in center.get("power_meters", []):
                simulator = PowerMeterSimulator(
                    gateway=gateway,
                    device_name=pm_config["name"],
                    profile=pm_config.get("profile", "default"),
                    real_energy=pm_config["real_energy"],
                    reactive_energy=pm_config["reactive_energy"],
                    apparent_energy=pm_config["apparent_energy"],
                )

                simulator.start()
                simulators.append(simulator)

            # DFM
            for dfm_config in center.get("dfms", []):
                simulator = DfmSimulator(
                    gateway=gateway,
                    device_name=dfm_config["name"],
                    profile=dfm_config.get("profile", "default"),
                    total_fuel=dfm_config["total_fuel"],
                    hours_op=dfm_config["hours_op"],
                )

                simulator.start()
                simulators.append(simulator)

            # Estanques
            for tank_config in center.get("tanks", []):
                simulator = TankSimulator(
                    gateway=gateway,
                    device_name=tank_config["name"],
                    profile=tank_config.get("profile", "default"),
                    level=tank_config["level"],
                    max_level=tank_config["max_level"]
                )

                simulator.start()
                simulators.append(simulator)

        print()
        print(f"Simuladores activos: {len(simulators)}")
        print("Ctrl+C para detener")
        print()

        while True:
            for simulator in simulators:
                simulator.tick()

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nDeteniendo simulador...")

    finally:
        for gateway in gateways:
            gateway.disconnect()

        print("Desconectado.")


if __name__ == "__main__":
    main()
