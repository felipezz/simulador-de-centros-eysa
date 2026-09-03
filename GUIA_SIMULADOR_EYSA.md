# Guía de uso — Simulador EYSA

## Objetivo

Este proyecto simula la ingesta de telemetría de sistemas EYSA hacia ThingsBoard mediante MQTT.

La idea es poder levantar A-15 y luego agregar centros simulados para pruebas de carga sin instalar gateways físicos ni simular Modbus.

El simulador reemplaza esta parte:

```text
Sensores -> Modbus -> ThingsBoard Gateway -> MQTT -> ThingsBoard
```

por:

```text
Python -> MQTT -> ThingsBoard
```

ThingsBoard y las Rule Chains siguen procesando los datos normalmente.

---

## Arquitectura del proyecto

```text
eysa-simulator/
├── main.py
├── config.py
├── requirements.txt
└── simulators/
    ├── __init__.py
    ├── power_meter.py
    ├── dfm.py
    └── tank.py
```

### Responsabilidad de cada archivo

- `main.py`: conecta los gateways y ejecuta todos los simuladores.
- `config.py`: define qué centros y dispositivos existen.
- `simulators/power_meter.py`: comportamiento de analizadores eléctricos.
- `simulators/dfm.py`: comportamiento de flujómetros.
- `simulators/tank.py`: comportamiento del estanque.

**Para agregar centros o dispositivos no se debe modificar `main.py` ni las clases de `simulators/`.  
Normalmente solo se modifica `config.py`.**

---

## Frecuencias simuladas

### Power Meter

- Variables instantáneas: cada **5 s**
- Acumuladores de energía: cada **15 s**

Variables acumuladas:

```text
realEnergyIntoTheLoad
reactiveEnergyIntoTheLoad
apparentEnergyIntoTheLoad
```

Las variables instantáneas se envían en los bloques HEX esperados por la Rule Chain.

### DFM

- Bloque `gc`: cada **5 s**
- `hoursOp`: cada **60 s**
- Estados del flujómetro: cambian como máximo aproximadamente una vez cada **24 h**

El acumulado de combustible se mantiene internamente como litros y el simulador lo vuelve a convertir al formato bruto esperado por la Rule Chain.

### Estanque

- `nivelEstanque`: cada **15 s**
- El nivel disminuye progresivamente.
- Al quedar cerca de vacío, vuelve a `max_level`, simulando una recarga completa.

---

# Ejecutar el simulador

Desde la raíz del proyecto:

```bash
source .venv/bin/activate
python main.py
```

Para detener:

```text
Ctrl+C
```

Al iniciar se mostrará la cantidad total de dispositivos simulados:

```text
Simuladores activos: 10
```

A-15 actualmente corresponde a:

```text
7 Power Meters
2 DFM
1 Estanque
--------------
10 dispositivos
```

---

# Agregar un nuevo centro

## 1. Preparar el centro en ThingsBoard

Antes de modificar el código:

1. Crear o clonar el sistema en ThingsBoard.
2. Crear su gateway.
3. Obtener el Access Token del gateway.
4. Crear los devices del centro.
5. Configurar sus relaciones/assets/rule chains igual que en un sistema EYSA normal.

### Convención de nombres de devices

Los devices creados en ThingsBoard **deben mantener la convención de nombres actual**, porque EYSA identifica el tipo de dispositivo a partir del comienzo del nombre.

Convenciones base:

```text
Power Meters de consumo:
pm-general
pm-<zona>

Power Meters de generadores:
pm-gen-general
pm-gen-<nombre>

Estanque:
estanque

Flujómetros:
dfm-general
dfm-<nombre>
```

Para un centro simulado, agregar el identificador del pontón **al final** del nombre, sin alterar el prefijo.

Ejemplo para el pontón `A42`:

```text
pm-general-a42
pm-habitabilidad-a42
pm-fotoperiodo-a42
pm-alimentacion-a42

pm-gen-general-a42
pm-gen-aux-a42

estanque-a42

dfm-general-a42
dfm-aux-a42
```

**No usar el identificador del pontón al comienzo**, por ejemplo:

```text
a42-pm-general
```

La convención actual requiere conservar `pm-`, `pm-gen-`, `dfm-` o `estanque` al inicio. El sufijo del pontón se utiliza solamente para diferenciar e identificar los devices de cada centro simulado.

Los nombres definidos en `config.py` deben coincidir **exactamente** con los devices creados en ThingsBoard.

Se recomienda:

```text
1 centro simulado = 1 gateway de ThingsBoard
```

Esto reproduce mejor la arquitectura real y aumenta también la cantidad de conexiones MQTT durante las pruebas.

---

## 2. Agregar el centro en `config.py`

No crear scripts nuevos por centro.

Agregar otro objeto dentro de `CENTERS`.

Ejemplo:

```python
CENTERS = [
    {
        "name": "A-15",
        "gateway_token": "TOKEN_A15",

        "power_meters": [
            # ...
        ],

        "dfms": [
            # ...
        ],

        "tanks": [
            # ...
        ],
    },

    {
        "name": "SIM-02",
        "gateway_token": "TOKEN_SIM_02",

        "power_meters": [
            # ...
        ],

        "dfms": [
            # ...
        ],

        "tanks": [
            # ...
        ],
    },
]
```

`main.py` detectará automáticamente todos los dispositivos definidos.

---

# Agregar Power Meters

Todos los analizadores usan el mismo `PowerMeterSimulator`.

Agregar cada device dentro de:

```python
"power_meters": []
```

Formato:

```python
{
    "name": "pm-general-a42",
    "real_energy": 100000000.0,
    "reactive_energy": 5000000.0,
    "apparent_energy": 105000000.0,
}
```

Ejemplo con varios:

```python
"power_meters": [
    {
        "name": "pm-general-a42",
        "real_energy": 100000000.0,
        "reactive_energy": 5000000.0,
        "apparent_energy": 105000000.0,
    },
    {
        "name": "pm-habitabilidad-a42",
        "real_energy": 20000000.0,
        "reactive_energy": 1000000.0,
        "apparent_energy": 22000000.0,
    },
]
```

## Valores iniciales de acumuladores

### Centro existente que se quiere continuar

Usar los últimos valores almacenados en ThingsBoard:

```text
realEnergyIntoTheLoad
reactiveEnergyIntoTheLoad
apparentEnergyIntoTheLoad
```

Así el acumulador continúa desde el último dato real.

### Centro completamente simulado

Los valores iniciales pueden ser arbitrarios.

Ejemplo:

```python
"real_energy": 1000000.0,
"reactive_energy": 100000.0,
"apparent_energy": 1100000.0,
```

No es necesario que tengan precisión física. El objetivo principal es generar volumen y frecuencia de telemetría.

---

# Agregar DFM

Agregar los devices dentro de:

```python
"dfms": []
```

Formato:

```python
{
    "name": "dfm-general-a42",
    "total_fuel": 32000.0,
    "hours_op": 2400.0,
}
```

Ejemplo:

```python
"dfms": [
    {
        "name": "dfm-general-a42",
        "total_fuel": 32000.0,
        "hours_op": 2400.0,
    },
    {
        "name": "dfm-aux-a42",
        "total_fuel": 30000.0,
        "hours_op": 1700.0,
    },
]
```

## Importante sobre `total_fuel`

Se ingresa el valor **ya procesado**, es decir, el valor visible en ThingsBoard como:

```text
EngineTotalFuelUsed
```

Ejemplo:

```text
EngineTotalFuelUsed = 32306.625
```

se configura como:

```python
"total_fuel": 32306.625
```

No hace falta conocer el valor bruto enviado por Modbus.

El simulador hace internamente:

```text
litros
-> valor entero
-> registros uint16 high/low
-> bloque gc HEX
-> MQTT
-> Rule Chain
-> EngineTotalFuelUsed
```

`hours_op` corresponde directamente al último valor de:

```text
hoursOp
```

---

# Agregar estanque

Agregar dentro de:

```python
"tanks": []
```

Formato:

```python
{
    "name": "estanque-a42",
    "level": 3500.0,
    "max_level": 10000.0,
}
```

Donde:

- `level`: nivel inicial ya calculado, en litros.
- `max_level`: capacidad a la que vuelve el estanque cuando se simula una recarga.

Ejemplo A-15:

```python
{
    "name": "estanque",
    "level": 3521.73,
    "max_level": 10000.0,
}
```

El simulador convierte internamente el nivel calculado al valor bruto `nivelEstanque` que espera la Rule Chain.

---

# Ejemplo completo de un centro simulado

```python
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
        {
            "name": "pm-habitabilidad-a42",
            "real_energy": 20000000.0,
            "reactive_energy": 1000000.0,
            "apparent_energy": 22000000.0,
        },
    ],

    "dfms": [
        {
            "name": "dfm-general-a42",
            "total_fuel": 30000.0,
            "hours_op": 2000.0,
        },
        {
            "name": "dfm-aux-a42",
            "total_fuel": 25000.0,
            "hours_op": 1500.0,
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
```

Para una réplica completa de A-15 se deben configurar:

```text
7 PM
2 DFM
1 estanque
```

---

# Cómo funciona `main.py`

El loop principal es intencionalmente simple:

```python
while True:
    for simulator in simulators:
        simulator.tick()

    time.sleep(0.1)
```

Aproximadamente 10 veces por segundo pregunta a cada simulador si le corresponde enviar algo.

Cada clase administra sus propios tiempos:

```text
Power Meter -> 5 s / 15 s
DFM         -> 5 s / 60 s
Estanque    -> 15 s
```

`main.py` no necesita conocer estas frecuencias.

Esto permite agregar muchos dispositivos sin duplicar lógica.

---

# Reglas para no romper la arquitectura

## Sí hacer

- Agregar centros en `config.py`.
- Agregar devices en las listas correspondientes.
- Usar un gateway/token por centro.
- Mantener nombres idénticos a ThingsBoard.
- Usar los últimos acumuladores reales si se continúa un centro existente.
- Usar valores arbitrarios razonables para centros completamente simulados.

## No hacer

- No copiar `power_meter.py` para crear un PM nuevo.
- No crear un script Python por centro.
- No agregar lógica específica de un centro dentro de `main.py`.
- No agregar `sleep()` individuales dentro de `main.py`.
- No enviar directamente las variables que actualmente deben pasar por Rule Chain.
- No modificar las frecuencias globales solo para un centro sin una razón explícita.
- No reutilizar nombres de devices que ya pertenezcan a otro sistema dentro del mismo tenant.

---

# Flujo recomendado para agregar centros

```text
1. Crear centro/gateway/devices en ThingsBoard
2. Obtener token del gateway
3. Agregar centro en config.py
4. Agregar sus PM
5. Agregar sus DFM
6. Agregar su estanque
7. Ejecutar python main.py
8. Confirmar cantidad de simuladores
9. Revisar Latest Telemetry en ThingsBoard
10. Dejar correr y monitorear servidor
```

---

# Objetivo de las pruebas

El simulador no busca producir datos físicamente perfectos.

Se busca reproducir principalmente:

- cantidad de centros;
- cantidad de devices;
- frecuencia de envío;
- cantidad de variables;
- procesamiento por Rule Chains;
- tráfico MQTT;
- carga sobre ThingsBoard;
- Kafka;
- PostgreSQL/TimescaleDB;
- consultas del backend EYSA.

Por eso los valores pueden ser simples mientras mantengan el formato esperado y los acumuladores crezcan de forma coherente.

---

## Resumen rápido

Para agregar un centro nuevo:

```text
ThingsBoard:
crear gateway + devices

config.py:
agregar un nuevo bloque dentro de CENTERS

main.py:
NO TOCAR

simulators/:
NO TOCAR
```

Si el nuevo centro usa los mismos tipos de dispositivos que A-15, agregarlo debe ser principalmente una tarea de configuración y no de desarrollo.
