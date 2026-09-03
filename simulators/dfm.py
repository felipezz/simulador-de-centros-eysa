import random
import time

from tb_device_mqtt import TBPublishInfo


class DfmSimulator:
    GC_INTERVAL = 5
    HOURS_INTERVAL = 60
    STATE_CHANGE_INTERVAL = 24 * 60 * 60  # 24 horas

    def __init__(
        self,
        gateway,
        device_name,
        total_fuel=0.0,
        hours_op=0.0,
    ):
        self.gateway = gateway
        self.device_name = device_name

        # Acumuladores
        self.total_fuel = total_fuel
        self.hours_op = hours_op

        # Estados que cambian muy poco
        self.engine_mode = 1
        self.status_camara_in = 0
        self.status_camara_out = 0

        now = time.monotonic()

        self.next_gc = now
        self.next_hours = now
        self.next_state_change = now + self.STATE_CHANGE_INTERVAL

    def start(self):
        self.gateway.gw_connect_device(self.device_name)

    def tick(self):
        now = time.monotonic()

        if now >= self.next_state_change:
            self._change_state()
            self.next_state_change += self.STATE_CHANGE_INTERVAL

        if now >= self.next_gc:
            self._send_gc()
            self.next_gc += self.GC_INTERVAL

        if now >= self.next_hours:
            self._send_hours()
            self.next_hours += self.HOURS_INTERVAL

    # ------------------------------------------------------------------
    # ENVÍOS
    # ------------------------------------------------------------------

    def _send_gc(self):
        values = self._generate_gc()

        self._send(
            {
                "gc": values
            },
            "GC",
        )

    def _send_hours(self):
        # Una hora de operación acumula 1/60 cada minuto.
        # Para efectos del simulador asumimos que está operando.
        self.hours_op += 1 / 60

        self._send(
            {
                "hoursOp": self.hours_op
            },
            "HOURS",
        )

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

    # ------------------------------------------------------------------
    # GENERACIÓN DFM
    # ------------------------------------------------------------------

    def _generate_gc(self):
        fuel_rate = random.uniform(20, 50)
        fuel_temp = random.uniform(15, 30)

        # No buscamos precisión física.
        # Solo mantener el acumulador creciendo.
        self.total_fuel += random.uniform(0.02, 0.08)

        feed_rate = random.uniform(30, 60)
        return_rate = random.uniform(5, 20)

        registers = [0] * 16

        # uints[0] * 0.05
        registers[0] = int(fuel_rate / 0.05)

        # uints[3] - 40
        registers[3] = int(fuel_temp + 40)

        # uints[4] y uints[5]
        fuel_high, fuel_low = self._fuel_to_registers(self.total_fuel)
        registers[4] = fuel_high
        registers[5] = fuel_low

        # Estados
        registers[11] = self.engine_mode

        # uints[12] * 0.05
        registers[12] = int(feed_rate / 0.05)

        # uints[13] * 0.05
        registers[13] = int(return_rate / 0.05)

        registers[14] = self.status_camara_in
        registers[15] = self.status_camara_out

        return self._uint16s_to_hex(registers)

    def _change_state(self):
        """
        Como máximo cambiamos un estado cada 24 horas.
        La Rule Chain decide si debe persistirlo.
        """

        state = random.choice([
            "engine_mode",
            "status_camara_in",
            "status_camara_out",
        ])

        if state == "engine_mode":
            self.engine_mode = 0 if self.engine_mode == 1 else 1

        elif state == "status_camara_in":
            self.status_camara_in = 1 - self.status_camara_in

        elif state == "status_camara_out":
            self.status_camara_out = 1 - self.status_camara_out

        print(
            f"[STATE] {self.device_name}: "
            f"mode={self.engine_mode}, "
            f"in={self.status_camara_in}, "
            f"out={self.status_camara_out}"
        )

    @staticmethod
    def _fuel_to_registers(liters):
        raw = int(liters * 1000)

        high = (raw >> 16) & 0xFFFF
        low = raw & 0xFFFF

        return high, low

    @staticmethod
    def _uint16s_to_hex(values):
        return "".join(f"{value:04x}" for value in values)
