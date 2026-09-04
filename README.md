# EYSA Simulator

Simulador de telemetría para pruebas de carga de EYSA sobre ThingsBoard.

El objetivo es generar tráfico equivalente al de uno o varios centros sin instalar gateways físicos ni simular Modbus. Python publica por MQTT y ThingsBoard procesa los mensajes mediante las Rule Chains reales.

```text
Producción:
Sensores -> Modbus -> ThingsBoard Gateway -> MQTT -> ThingsBoard

Simulación:
Python -------------------------------> MQTT -> ThingsBoard
```

## Estado actual

El simulador soporta los tres tipos de dispositivos utilizados en A-15:

```text
7 Power Meters
2 DFM
1 Estanque
--------------
10 dispositivos
```

Frecuencias simuladas:

| Dispositivo | Telemetría | Frecuencia |
|---|---|---:|
| Power Meter | Variables instantáneas | 5 s |
| Power Meter | Acumuladores de energía | 15 s |
| DFM | Bloque `gc` | 5 s |
| DFM | `hoursOp` | 60 s |
| Estanque | `nivelEstanque` | 15 s |

Los valores no buscan representar con precisión la operación real. Lo importante es reproducir volumen, frecuencia, procesamiento por Rule Chains y carga sobre ThingsBoard, Kafka, PostgreSQL/TimescaleDB y EYSA.

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
- `config.py`: define centros, devices, perfiles y valores iniciales.
- `simulators/`: contiene el comportamiento de cada tipo de dispositivo.

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

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

## Agregar centros

Si el nuevo centro utiliza los mismos tipos de dispositivos que A-15, **no se debe modificar `main.py` ni los archivos de `simulators/`**.

El alta consiste principalmente en:

```text
ThingsBoard:
crear gateway + obtener su token

config.py:
agregar un nuevo bloque dentro de CENTERS y declarar el profile de cada device

main.py:
NO TOCAR

simulators/:
NO TOCAR
```

Al iniciar, el simulador conecta cada device mediante la Gateway MQTT API. Si el
device no existe, ThingsBoard puede crearlo automáticamente con el Device Profile
declarado en `profile`; si ya existe, simplemente lo conecta sin recrearlo. Los
Device Profiles (`pm-5330`, `DFM` y `nivel-estanque`) deben existir previamente en
ThingsBoard.

Si una configuración antigua no declara `profile`, se usa `default` para mantener
el comportamiento anterior.

Los devices deben respetar la convención de nombres actual. Para centros simulados, el identificador del pontón se agrega **al final**:

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

## Documentación

El procedimiento completo para crear un centro, configurar sus devices y definir valores iniciales está en:

```text
GUIA_SIMULADOR_EYSA.md
```
