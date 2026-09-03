# EYSA Simulator

Simulador de telemetría para pruebas de carga de EYSA sobre ThingsBoard.

El proyecto permite simular uno o varios centros sin instalar gateways físicos ni dispositivos Modbus. Python genera la telemetría y la publica por MQTT hacia ThingsBoard, donde las Rule Chains reales continúan procesando los datos normalmente.

```text
Producción:
Sensores -> Modbus -> ThingsBoard Gateway -> MQTT -> ThingsBoard

Simulación:
Python -------------------------------> MQTT -> ThingsBoard
```

## Estado actual

El simulador modela los dispositivos de un sistema EYSA como A-15:

```text
7 Power Meters
2 DFM
1 Estanque
--------------
10 dispositivos
```

Frecuencias actuales:

| Dispositivo | Telemetría | Frecuencia |
|---|---|---:|
| Power Meter | Instantáneas | 5 s |
| Power Meter | Acumuladores de energía | 15 s |
| DFM | Bloque `gc` | 5 s |
| DFM | `hoursOp` | 60 s |
| Estanque | `nivelEstanque` | 15 s |

Los valores simulados no buscan precisión física. El objetivo es reproducir volumen de telemetría, frecuencias, Rule Chains y carga sobre ThingsBoard, Kafka, PostgreSQL/TimescaleDB y EYSA.

## Estructura

```text
eysa-simulator/
├── main.py
├── config.py
├── requirements.txt
├── README.md
├── GUIA_SIMULADOR_EYSA.md
└── simulators/
    ├── __init__.py
    ├── power_meter.py
    ├── dfm.py
    └── tank.py
```

- `main.py`: conecta los gateways y ejecuta todos los simuladores.
- `config.py`: define centros, devices, tokens y valores iniciales.
- `simulators/power_meter.py`: simulación de analizadores eléctricos.
- `simulators/dfm.py`: simulación de flujómetros.
- `simulators/tank.py`: simulación de estanques.

> Para agregar centros que usen los mismos tipos de dispositivos, normalmente solo se modifica `config.py`. No se debe duplicar ni modificar `main.py` o las clases de `simulators/`.

## Instalación

Crear y activar un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Desde la raíz del proyecto:

```bash
source .venv/bin/activate
python main.py
```

Para detener:

```text
Ctrl+C
```

Al iniciar se muestra la cantidad total de dispositivos simulados:

```text
Simuladores activos: 10
```

## Agregar un centro simulado

Cada centro debe tener su propio gateway en ThingsBoard.

Flujo general:

```text
1. Crear centro/gateway/devices en ThingsBoard
2. Obtener el Access Token del gateway
3. Agregar el centro en config.py
4. Configurar Power Meters
5. Configurar DFM
6. Configurar estanque
7. Ejecutar python main.py
8. Validar Latest Telemetry en ThingsBoard
```

Ejemplo:

```python
CENTERS = [
    {
        "name": "SIM-02",
        "gateway_token": "TOKEN_SIM_02",

        "power_meters": [
            {
                "name": "pm-general-a42",
                "real_energy": 100000000.0,
                "reactive_energy": 5000000.0,
                "apparent_energy": 105000000.0,
            },
        ],

        "dfms": [
            {
                "name": "dfm-general-a42",
                "total_fuel": 30000.0,
                "hours_op": 2000.0,
            },
        ],

        "tanks": [
            {
                "name": "estanque-a42",
                "level": 7000.0,
                "max_level": 10000.0,
            },
        ],
    }
]
```

## Convención de nombres

Los devices en ThingsBoard deben conservar la convención actual porque EYSA identifica su tipo a partir del comienzo del nombre.

Convenciones base:

```text
Power Meters:
pm-general
pm-<zona>

Power Meters de generadores:
pm-gen-general
pm-gen-<nombre>

Estanque:
estanque

DFM:
dfm-general
dfm-<nombre>
```

Para centros simulados, agregar el identificador del pontón **al final**.

Ejemplo para `A42`:

```text
pm-general-a42
pm-habitabilidad-a42
pm-gen-general-a42
pm-gen-aux-a42

dfm-general-a42
dfm-aux-a42

estanque-a42
```

No usar por ahora:

```text
a42-pm-general
```

Los nombres definidos en `config.py` deben coincidir exactamente con los devices creados en ThingsBoard.

## Valores iniciales

Para continuar un centro existente, usar los últimos valores almacenados en ThingsBoard.

### Power Meter

```text
realEnergyIntoTheLoad
reactiveEnergyIntoTheLoad
apparentEnergyIntoTheLoad
```

### DFM

```text
EngineTotalFuelUsed -> total_fuel
hoursOp             -> hours_op
```

`total_fuel` se configura en litros ya procesados. El simulador lo convierte internamente nuevamente al formato bruto esperado por la Rule Chain.

### Estanque

```text
nivelCalculado -> level
capacidad      -> max_level
```

Cuando el estanque queda cerca de vacío, el simulador lo vuelve a llenar hasta `max_level`.

Para centros totalmente simulados, los acumuladores iniciales pueden ser valores arbitrarios razonables.

## Arquitectura de ejecución

`main.py` mantiene un loop simple:

```python
while True:
    for simulator in simulators:
        simulator.tick()

    time.sleep(0.1)
```

Cada simulador administra sus propias frecuencias. `main.py` solo pregunta repetidamente si a cada dispositivo le corresponde enviar telemetría.

Esto permite mezclar Power Meters, DFM y estanques sin agregar schedulers, threads o lógica específica por centro.

## Reglas de desarrollo

- Agregar centros y devices en `config.py`.
- Mantener un gateway/token por centro.
- Mantener nombres de devices compatibles con la convención.
- No crear un script por centro.
- No duplicar `power_meter.py`, `dfm.py` o `tank.py` para agregar nuevos devices.
- No agregar lógica específica de un centro en `main.py`.
- No saltarse las Rule Chains enviando directamente variables que normalmente llegan en formato bruto.
- No reutilizar nombres de devices dentro del mismo tenant.

## Documentación

Para instrucciones detalladas de incorporación de nuevos centros y explicación de cada tipo de dispositivo, revisar:

```text
GUIA_SIMULADOR_EYSA.md
```
