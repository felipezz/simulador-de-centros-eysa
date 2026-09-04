# Guía de uso — Simulador EYSA

## Objetivo

Esta guía explica cómo **agregar centros simulados** al proyecto sin modificar su arquitectura.

El simulador reemplaza la lectura física y el ThingsBoard Gateway por un proceso Python que publica directamente por MQTT:

```text
Producción:
Sensores -> Modbus -> ThingsBoard Gateway -> MQTT -> ThingsBoard

Simulación:
Python -------------------------------> MQTT -> ThingsBoard
```

ThingsBoard continúa ejecutando las Rule Chains reales, por lo que el procesamiento posterior se mantiene.

---

# 1. Regla principal

Si el nuevo centro utiliza los mismos tipos de dispositivos que A-15:

> **Agregar un centro debe ser una tarea de configuración, no de desarrollo.**

Normalmente solo se modifica:

```text
config.py
```

No modificar para agregar un centro:

```text
main.py
simulators/power_meter.py
simulators/dfm.py
simulators/tank.py
```

---

# 2. Preparar el centro en ThingsBoard

Antes de editar `config.py`:

1. Crear o clonar el sistema en ThingsBoard.
2. Crear un gateway para el centro.
3. Obtener el Access Token de ese gateway.
4. Verificar que existan los Device Profiles que usarán los devices.
5. Configurar assets, relaciones y Rule Chains igual que en un sistema EYSA normal.

No es necesario crear manualmente cada device. Al ejecutar el simulador, la
Gateway MQTT API conecta los devices existentes y crea automáticamente los que no
existan con el `profile` declarado en `config.py`.

Se debe usar:

```text
1 centro simulado = 1 gateway de ThingsBoard
```

Esto permite que las pruebas también aumenten la cantidad de conexiones MQTT al crecer el número de centros.

---

# 3. Convención de nombres de devices

Los nombres son importantes porque EYSA identifica el tipo de dispositivo a partir del comienzo del nombre.

## Power Meters de consumo

```text
pm-general
pm-<zona>
```

Ejemplos:

```text
pm-general
pm-habitabilidad
pm-fotoperiodo
pm-alimentacion
pm-alimentacion2
```

## Power Meters de generadores

```text
pm-gen-general
pm-gen-<nombre>
```

Ejemplos:

```text
pm-gen-general
pm-gen-aux
```

## Estanque

```text
estanque
```

## Flujómetros DFM

```text
dfm-general
dfm-<nombre>
```

Ejemplos:

```text
dfm-general
dfm-aux
```

## Centros simulados

Para diferenciar devices de distintos centros, agregar el identificador del pontón **al final** del nombre.

Ejemplo para `A42`:

```text
pm-general-a42
pm-habitabilidad-a42
pm-fotoperiodo-a42
pm-alimentacion-a42
pm-alimentacion2-a42

pm-gen-general-a42
pm-gen-aux-a42

dfm-general-a42
dfm-aux-a42

estanque-a42
```

Por ahora **no usar el identificador al comienzo**:

```text
a42-pm-general
```

La convención actual requiere conservar `pm-`, `pm-gen-`, `dfm-` o `estanque` al inicio del nombre.

El nombre configurado en `config.py` debe coincidir **exactamente** con el device
esperado en ThingsBoard. Cada device también debe declarar su Device Profile.

---

# 4. Agregar un centro en `config.py`

Cada centro es un objeto dentro de `CENTERS`.

Estructura:

```python
CENTERS = [
    {
        "name": "A-15",
        "gateway_token": gateway_token("A-15"),

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
        "name": "A-42",
        "gateway_token": gateway_token("A-42"),

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

`main.py` crea automáticamente los simuladores definidos en cada centro.

Al conectar cada device, ThingsBoard lo crea automáticamente si todavía no existe
y le asigna el Device Profile indicado. Si ya existe, se conecta sin recrearlo.
Los perfiles deben existir previamente en ThingsBoard. Si falta `profile`, el
simulador usa `default` para conservar compatibilidad con configuraciones antiguas.

No crear un script distinto por centro.

---

# 5. Power Meters

Los Power Meters simulan:

```text
Variables instantáneas -> cada 5 s
Acumuladores de energía -> cada 15 s
```

Agregar cada analizador dentro de:

```python
"power_meters": []
```

Formato:

```python
{
    "name": "pm-general-a42",
    "profile": "pm-5330",
    "real_energy": 100000000.0,
    "reactive_energy": 5000000.0,
    "apparent_energy": 105000000.0,
}
```

## Valores iniciales

Las propiedades corresponden a:

```text
real_energy     <- realEnergyIntoTheLoad
reactive_energy <- reactiveEnergyIntoTheLoad
apparent_energy <- apparentEnergyIntoTheLoad
```

### Si se continúa un centro existente

Usar los últimos valores almacenados en ThingsBoard.

Esto evita que los acumuladores vuelvan hacia atrás.

### Si el centro es completamente simulado

Se pueden usar valores iniciales arbitrarios:

```python
"real_energy": 1000000.0,
"reactive_energy": 100000.0,
"apparent_energy": 1100000.0,
```

No se busca precisión física.

---

# 6. DFM

Los DFM simulan:

```text
Bloque gc -> cada 5 s
hoursOp   -> cada 60 s
```

Además, los estados internos del flujómetro cambian muy poco: como máximo aproximadamente una vez cada 24 horas. La Rule Chain real decide si corresponde persistir esos estados.

Agregar cada DFM dentro de:

```python
"dfms": []
```

Formato:

```python
{
    "name": "dfm-general-a42",
    "profile": "DFM",
    "total_fuel": 32000.0,
    "hours_op": 2400.0,
}
```

## `total_fuel`

Usar directamente el valor procesado visible en ThingsBoard:

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

No es necesario conocer el valor bruto Modbus.

Internamente el simulador realiza la conversión inversa:

```text
litros
-> registros uint16
-> bloque gc HEX
-> MQTT
-> Rule Chain
-> EngineTotalFuelUsed
```

## `hours_op`

Usar directamente el último valor de:

```text
hoursOp
```

Ejemplo:

```python
"hours_op": 2470.2094444444447
```

Para un centro completamente simulado ambos valores pueden ser arbitrarios.

---

# 7. Estanque

El estanque envía:

```text
nivelEstanque -> cada 15 s
```

Agregar dentro de:

```python
"tanks": []
```

Formato:

```python
{
    "name": "estanque-a42",
    "profile": "nivel-estanque",
    "level": 3500.0,
    "max_level": 10000.0,
}
```

Donde:

- `level`: nivel inicial ya procesado, equivalente a `nivelCalculado`.
- `max_level`: capacidad usada para simular una recarga completa.

El nivel disminuye progresivamente. Cuando queda cerca de vacío, el simulador lo lleva nuevamente a `max_level`.

Ejemplo para un estanque de 10.000 L:

```python
{
    "name": "estanque-a42",
    "profile": "nivel-estanque",
    "level": 3521.73,
    "max_level": 10000.0,
}
```

El simulador convierte internamente `level` al valor bruto `nivelEstanque` esperado por la Rule Chain.

---

# 8. Ejemplo de un centro completo

Una réplica de la estructura de A-15 tiene:

```text
7 Power Meters
2 DFM
1 Estanque
--------------
10 dispositivos
```

Ejemplo:

```python
{
    "name": "A-42",
    "gateway_token": gateway_token("A-42"),

    "power_meters": [
        {
            "name": "pm-general-a42",
            "profile": "pm-5330",
            "real_energy": 100000000.0,
            "reactive_energy": 5000000.0,
            "apparent_energy": 105000000.0,
        },
        {
            "name": "pm-habitabilidad-a42",
            "profile": "pm-5330",
            "real_energy": 20000000.0,
            "reactive_energy": 1000000.0,
            "apparent_energy": 22000000.0,
        },
        {
            "name": "pm-fotoperiodo-a42",
            "profile": "pm-5330",
            "real_energy": 30000000.0,
            "reactive_energy": 1000000.0,
            "apparent_energy": 32000000.0,
        },
        {
            "name": "pm-alimentacion-a42",
            "profile": "pm-5330",
            "real_energy": 25000000.0,
            "reactive_energy": 5000000.0,
            "apparent_energy": 30000000.0,
        },
        {
            "name": "pm-alimentacion2-a42",
            "profile": "pm-5330",
            "real_energy": 12000000.0,
            "reactive_energy": 3000000.0,
            "apparent_energy": 15000000.0,
        },
        {
            "name": "pm-gen-general-a42",
            "profile": "pm-5330",
            "real_energy": 90000000.0,
            "reactive_energy": 5000000.0,
            "apparent_energy": 95000000.0,
        },
        {
            "name": "pm-gen-aux-a42",
            "profile": "pm-5330",
            "real_energy": 70000000.0,
            "reactive_energy": 5000000.0,
            "apparent_energy": 75000000.0,
        },
    ],

    "dfms": [
        {
            "name": "dfm-general-a42",
            "profile": "DFM",
            "total_fuel": 32000.0,
            "hours_op": 2400.0,
        },
        {
            "name": "dfm-aux-a42",
            "profile": "DFM",
            "total_fuel": 30000.0,
            "hours_op": 1700.0,
        },
    ],

    "tanks": [
        {
            "name": "estanque-a42",
            "profile": "nivel-estanque",
            "level": 7000.0,
            "max_level": 10000.0,
        },
    ],
}
```

---

# 9. Ejecutar y validar

Desde la raíz del proyecto:

```bash
source .venv/bin/activate
python main.py
```

Al iniciar, revisar:

```text
Simuladores activos: N
```

Para un centro completo como A-15:

```text
Simuladores activos: 10
```

Después validar en ThingsBoard:

1. Abrir algunos devices.
2. Revisar `Latest Telemetry`.
3. Confirmar que las variables cambien con las frecuencias esperadas.
4. Confirmar que los acumuladores aumenten.
5. Confirmar que el estanque disminuya.

---

# 10. Cómo funciona el loop principal

`main.py` mantiene un loop simple:

```python
while True:
    for simulator in simulators:
        simulator.tick()

    time.sleep(0.1)
```

Aproximadamente 10 veces por segundo pregunta a cada simulador si le corresponde enviar datos.

Cada clase administra sus propios tiempos:

```text
Power Meter -> 5 s / 15 s
DFM         -> 5 s / 60 s
Estanque    -> 15 s
```

Por eso no se deben agregar `sleep()` particulares en `main.py`.

---

# 11. Reglas para no romper la arquitectura

## Sí hacer

- Agregar centros en `config.py`.
- Agregar devices en la lista correspondiente.
- Crear un gateway/token por centro.
- Declarar el Device Profile de cada device en `config.py`.
- Mantener la convención de nombres.
- Hacer coincidir exactamente los nombres de ThingsBoard y `config.py`.
- Usar los últimos acumuladores reales si se continúa un centro existente.
- Usar valores arbitrarios razonables para centros completamente simulados.

## No hacer

- No crear un script Python por centro.
- No copiar `power_meter.py`, `dfm.py` o `tank.py` para crear otro device.
- No agregar lógica específica de un centro dentro de `main.py`.
- No agregar `sleep()` individuales en `main.py`.
- No enviar directamente variables que actualmente deben pasar por Rule Chain.
- No cambiar las frecuencias globales solo para un centro sin una razón explícita.
- No reutilizar nombres de devices dentro del mismo tenant.
- No poner el identificador del pontón al comienzo del nombre mientras la convención actual dependa del prefijo.

---

# 12. Checklist rápido para un nuevo centro

```text
[ ] Crear gateway en ThingsBoard
[ ] Obtener Access Token
[ ] Verificar que existan los Device Profiles necesarios
[ ] Configurar assets/relaciones/Rule Chains
[ ] Agregar centro en config.py
[ ] Configurar Power Meters con nombre y profile
[ ] Configurar DFM con nombre y profile
[ ] Configurar estanque con nombre y profile
[ ] Ejecutar python main.py
[ ] Confirmar que los devices se crearon/conectaron con el profile correcto
[ ] Confirmar cantidad de simuladores
[ ] Revisar Latest Telemetry
[ ] Dejar el simulador corriendo para la prueba
```

Si el nuevo centro utiliza los mismos tipos de dispositivos que A-15, no debería ser necesario modificar código fuera de `config.py`.
