import random
import time

from tb_device_mqtt import TBPublishInfo


class TankSimulator:
    INTERVAL = 15
    REFILL_THRESHOLD = 100.0

    def __init__(
        self,
        gateway,
        device_name,
        level,
        max_level,
        profile="default",
    ):
        self.gateway = gateway
        self.device_name = device_name
        self.profile = profile

        self.level = level
        self.max_level = max_level

        self.next_send = time.monotonic()

    def start(self):
        self.gateway.gw_connect_device(
            self.device_name,
            device_type=self.profile,
        )

    def tick(self):
        now = time.monotonic()

        if now >= self.next_send:
            self._send_level()
            self.next_send += self.INTERVAL

    def _send_level(self):
        # Consumo del estanque
        self.level -= random.uniform(0.1, 1.0)

        # Si está casi vacío, simulamos una carga completa
        if self.level <= self.REFILL_THRESHOLD:
            self.level = self.max_level

        # Inversa de la Rule Chain:
        # nivelCalculado = (nivelEstanque - 100) * 11.7391
        raw_level = (self.level / 11.7391) + 100

        telemetry = {
            "ts": int(time.time() * 1000),
            "values": {
                "nivelEstanque": raw_level
            },
        }

        result = self.gateway.gw_send_telemetry(
            self.device_name,
            telemetry,
            quality_of_service=1,
        )

        success = result.get() == TBPublishInfo.TB_ERR_SUCCESS

        print(
            f"[{time.strftime('%H:%M:%S')}] "
            f"TANK    "
            f"{self.device_name:<25} "
            f"level={self.level:.2f} "
            f"ok={success}"
        )
