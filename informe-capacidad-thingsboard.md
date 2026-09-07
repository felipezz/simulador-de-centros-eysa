# Capacidad de expansión del servidor ThingsBoard

## Conclusión

El servidor actual puede planificarse para un **máximo de 12 pontones**. Se recomienda operar normalmente con hasta **10 pontones** y contratar o habilitar capacidad adicional antes de incorporar el pontón 13.

La VM tiene 4 vCPU y 15,57 GiB de RAM. Con 7 pontones no se observó agotamiento de memoria, reinicios ni saturación sostenida de disco. El componente que más crece es PostgreSQL y el límite aparece en sus picos de CPU.

## Mediciones

Las seis ventanas duran aproximadamente 15 minutos y corresponden a 2–7 pontones.

| Pontones | CPU host promedio | CPU conjunta p95¹ | CPU conjunta máxima¹ | PostgreSQL p95 | RAM usada |
|---:|---:|---:|---:|---:|---:|
| 2 | 5,3% | 66% | 91% | 37% | 8,41 GB |
| 3 | 5,8% | 80% | 87% | 46% | 9,80 GB |
| 4 | 8,2% | 105% | 116% | 72% | 9,80 GB |
| 5 | 8,7% | 127% | 140% | 86% | 9,99 GB |
| 6 | 11,3% | 157% | 186% | 117% | 9,95 GB |
| 7 | 14,3% | 212% | 248% | 172% | 9,96 GB |

¹ Suma de ThingsBoard, PostgreSQL y Kafka. En `docker stats`, 100% equivale a un vCPU y la capacidad total de la VM equivale a 400%.

PostgreSQL explica la mayor parte del aumento desde 5 pontones. La memoria permanece estable cerca de 10 GB y quedan aproximadamente 6 GB disponibles. El `iowait` medio se mantuvo bajo.

## Proyección de capacidad

La proyección se ajustó sobre las mediciones de 2–7 pontones. El p95 conjunto presenta un ajuste lineal consistente (R² 0,95).

| Pontones | CPU conjunta p95 | CPU conjunta máxima | Uso máximo de los 4 vCPU | Evaluación |
|---:|---:|---:|---:|---|
| 10 | 279% | 318% | 79% | Viable con margen |
| **12** | **335%** | **380%** | **95%** | **Máximo de planificación** |
| 13 | 363% | 412% | 103% | Comienza la saturación proyectada |
| 15 | 419% | 475% | 119% | Requiere ampliar capacidad |

El máximo se fija en 12 porque su pico proyectado utiliza aproximadamente 95% de la CPU disponible. En 13 pontones, el pico supera la capacidad física de la VM. El promedio del host no debe usarse solo para dimensionar, ya que oculta picos breves de PostgreSQL.

## Telemetría almacenada

Con 7 pontones se midieron directamente 23,15 lecturas de telemetría/s y 727,60 valores persistidos/s. Cada lectura contiene, en promedio, 31,42 valores.

| Pontones | Lecturas/s | Valores persistidos/s | Valores persistidos/día |
|---:|---:|---:|---:|
| 7 | 23,15 | 728 | 62,86 millones |
| 10 | 33,07 | 1.039 | 89,81 millones |
| **12** | **39,69** | **1.247** | **107,77 millones** |
| 15 | 49,61 | 1.559 | 134,71 millones |

Las proyecciones suponen la misma cantidad de dispositivos y frecuencia de envío por pontón. Las lecturas son un proxy de mensajes persistidos; pueden diferir del número exacto de publicaciones MQTT/HTTP si existen agrupaciones o reintentos.

## Disco y base de datos

| Métrica | Resultado |
|---|---:|
| Disco raíz | 247 GB |
| Uso después de limpiar Docker | 61 GB, 25% |
| Uso después de comprimir el chunk activo | 43 GB, 18% |
| Espacio disponible final | 205 GB |
| PostgreSQL antes de comprimir el chunk activo | 38–38,4 GB |
| Chunk comprimido manualmente | 18 GB antes de la conversión |

TimescaleDB 2.24.0 tiene columnstore habilitado y una política diaria de compresión. El chunk cubría del 3 al 10 de septiembre y había crecido durante las pruebas con 2–7 pontones. Se detuvo el simulador y se convirtió manualmente al columnstore.

La conversión redujo el uso del volumen desde 61 GB hasta 43 GB y aumentó el espacio libre desde 187 GB hasta 205 GB. Esto equivale a aproximadamente **18 GB recuperados por compresión**, sujeto al redondeo de `df`. Sumando la limpieza Docker, el servidor recuperó aproximadamente **25 GB** y bajó de 28% a 18% de ocupación.

El aumento previo de 9,7 GB/día del disco completo no representa el crecimiento estable de PostgreSQL: incluía caché Docker y datos sin comprimir. El chunk activo equivale a un promedio provisional de aproximadamente 3,8 GB/día sin comprimir durante una carga variable. Escalado linealmente, el orden de magnitud sería ~5,4 GB/día con 10 pontones y ~6,5 GB/día con 12, antes de compresión.

La proyección definitiva de almacenamiento requiere conocer el tamaño exacto del chunk después de la conversión y comparar dos mediciones de PostgreSQL separadas por 24 horas con una cantidad fija de pontones.

## Recomendación

- Mantener 10 pontones como objetivo operativo normal.
- Validar 12 pontones con una prueba continua de 4–8 horas.
- Ampliar infraestructura antes de incorporar el pontón 13.
- Medir latencia p95/p99, lag de Kafka, CPU conjunta, tasa persistida y crecimiento diario de PostgreSQL durante la validación.
- Configurar chunks diarios, mantener la compresión automática y definir una política explícita de retención.

El servidor puede considerarse apto para 12 pontones sólo si sostiene aproximadamente 1.247 valores/s sin crecimiento de lag, errores ni degradación de latencia. Hasta completar esa prueba, 12 debe tratarse como límite estimado y 10 como capacidad prudente.

## Alcance

Las pruebas son ventanas cortas y secuenciales. No incluyen latencia ni lag de Kafka, y el throughput se midió directamente sólo con 7 pontones. Por ello, el informe establece un límite de planificación para decidir la expansión, no una garantía de servicio.
