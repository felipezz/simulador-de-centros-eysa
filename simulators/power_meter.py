import random
import struct
import time

from tb_device_mqtt import TBPublishInfo


class PowerMeterSimulator:
    INSTANT_INTERVAL = 5
    ACCUM_INTERVAL = 15

    def __init__(
        self,
        gateway,
        device_name,
        profile="default",
        real_energy=0.0,
        reactive_energy=0.0,
        apparent_energy=0.0,
    ):
        self.gateway = gateway
        self.device_name = device_name
        self.profile = profile

        self.real_energy = real_energy
        self.reactive_energy = reactive_energy
        self.apparent_energy = apparent_energy

        now = time.monotonic()

        self.next_instant = now
        self.next_accum = now

    def start(self):
        self.gateway.gw_connect_device(
            self.device_name,
            device_type=self.profile,
        )

    def tick(self):
        now = time.monotonic()

        if now >= self.next_instant:
            self._send_instant()
            self.next_instant += self.INSTANT_INTERVAL

        if now >= self.next_accum:
            self._send_accumulated()
            self.next_accum += self.ACCUM_INTERVAL

    def _send_instant(self):
        values = self._generate_instant_values()
        self._send(values, "INSTANT")

    def _send_accumulated(self):
        values = self._generate_accumulated_values()
        self._send(values, "ACCUM")

    def _send(self, values, label):
        telemetry = {
            "ts": int(time.time() * 1000),
            "values": values,
        }

        result = self.gateway.gw_send_telemetry(
            self.device_name,
            telemetry,
            quality_of_service=1,
        )

        success = result.get() == TBPublishInfo.TB_ERR_SUCCESS

        print(
            f"[{time.strftime('%H:%M:%S')}] "
            f"{label:<7} "
            f"{self.device_name:<25} "
            f"ok={success}"
        )

    def _generate_instant_values(self):
        currents = [
            random.uniform(20, 50),
            random.uniform(20, 50),
            random.uniform(20, 50),
            random.uniform(0, 5),
            random.uniform(0, 3),
            random.uniform(20, 50),
        ]

        voltages = [
            random.uniform(380, 410),
            random.uniform(380, 410),
            random.uniform(380, 410),
            random.uniform(380, 410),
            random.uniform(215, 235),
            random.uniform(215, 235),
            random.uniform(215, 235),
            0.0,
            random.uniform(215, 235),
        ]

        powers = [
            random.uniform(20, 50),
            random.uniform(20, 50),
            random.uniform(20, 50),
            random.uniform(60, 150),

            random.uniform(5, 15),
            random.uniform(5, 15),
            random.uniform(5, 15),
            random.uniform(15, 45),

            random.uniform(20, 55),
            random.uniform(20, 55),
            random.uniform(20, 55),
            random.uniform(60, 165),

            random.uniform(0.85, 1.0),
            random.uniform(0.85, 1.0),
            random.uniform(0.85, 1.0),
            random.uniform(0.85, 1.0),

            random.uniform(0.85, 1.0),
            random.uniform(0.85, 1.0),
            random.uniform(0.85, 1.0),
        ]

        thd = [
            random.uniform(1, 5),
            random.uniform(1, 5),
            random.uniform(1, 5),
            0.0,
            0.0,
            random.uniform(1, 5),
            random.uniform(1, 5),
            random.uniform(1, 5),
        ]

        return {
            "currents": self._floats_to_hex(currents),
            "voltages": self._floats_to_hex(voltages),
            "powers": self._floats_to_hex(powers),
            "thd": self._floats_to_hex(thd),
            "harmonicsA": self._floats_to_hex(self._generate_harmonics()),
            "harmonicsB": self._floats_to_hex(self._generate_harmonics()),
            "harmonicsC": self._floats_to_hex(self._generate_harmonics()),
        }

    def _generate_accumulated_values(self):
        self.real_energy += random.uniform(5, 15)
        self.reactive_energy += random.uniform(1, 5)
        self.apparent_energy += random.uniform(5, 18)

        return {
            "realEnergyIntoTheLoad": self.real_energy,
            "reactiveEnergyIntoTheLoad": self.reactive_energy,
            "apparentEnergyIntoTheLoad": self.apparent_energy,
        }

    @staticmethod
    def _generate_harmonics():
        values = [0.0] * 19

        values[0] = random.uniform(0.5, 3.0)
        values[6] = random.uniform(0.5, 3.0)
        values[12] = random.uniform(0.5, 3.0)
        values[18] = random.uniform(0.5, 3.0)

        return values

    @staticmethod
    def _floats_to_hex(values):
        return "".join(
            struct.pack(">f", float(value)).hex()
            for value in values
        )
