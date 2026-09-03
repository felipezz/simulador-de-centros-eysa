# Lista de IPs de Azure

## IPs públicas

| Máquina virtual | IP pública | Servicios |
| --- | --- | --- |
| `vm-pruebas` | `158.23.62.92` | Frontend (`8081`), Backend (`8000`), ThingsBoard / TB (`8085`) y Dokploy (`3000`) |
| `vm-script` | — | Sin IP pública |

### Enlaces de `vm-pruebas`

| Servicio | URL |
| --- | --- |
| Frontend | http://158.23.62.92:8081 |
| Backend | http://158.23.62.92:8000 |
| ThingsBoard (TB) | http://158.23.62.92:8085 |
| Dokploy | http://158.23.62.92:3000 |

## IPs privadas

| IP privada | Recurso |
| --- | --- |
| `172.16.0.4` | Servidor ThingsBoard (TB) |
| `172.16.0.5` | Máquina virtual `vm-script` |
