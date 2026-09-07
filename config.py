import os

from dotenv import load_dotenv


load_dotenv()


def gateway_token(ponton_name):
    token = os.getenv(ponton_name)
    if not token:
        raise RuntimeError(
            f"Falta el token del gateway {ponton_name!r} en el archivo .env"
        )
    return token


HOST = "158.23.62.92"
PORT = 1883

CENTERS = [
    {
        "name": "A-15",
        "gateway_token": gateway_token("A-15"),

        "power_meters": [
            {
                "name": "pm-general",
                "profile": "pm-5330",
                "real_energy": 194635227.0,
                "reactive_energy": 14511069.0,
                "apparent_energy": 197810189.0,
            },
            {
                "name": "pm-habitabilidad",
                "profile": "pm-5330",
                "real_energy": 21639347.0,
                "reactive_energy": 335969.0,
                "apparent_energy": 22408519.0,
            },
            {
                "name": "pm-fotoperiodo",
                "profile": "pm-5330",
                "real_energy": 112435816.0,
                "reactive_energy": 97.0,
                "apparent_energy": 112497081.0,
            },
            {
                "name": "pm-alimentacion",
                "profile": "pm-5330",
                "real_energy": 25163321.0,
                "reactive_energy": 9651433.0,
                "apparent_energy": 29185387.0,
            },
            {
                "name": "pm-alimentacion2",
                "profile": "pm-5330",
                "real_energy": 11455637.0,
                "reactive_energy": 4352945.0,
                "apparent_energy": 13275347.0,
            },
            {
                "name": "pm-gen-aux",
                "profile": "pm-5330",
                "real_energy": 68917773.0,
                "reactive_energy": 7049105.0,
                "apparent_energy": 70230704.0,
            },
            {
                "name": "pm-gen-general",
                "profile": "pm-5330",
                "real_energy": 98727530.0,
                "reactive_energy": 5652782.0,
                "apparent_energy": 100004573.0,
            },
        ],

        "dfms": [
            {
                "name": "dfm-general",
                "profile": "DFM",
                "total_fuel": 32306.625,
                "hours_op": 2470.2094444444447,
            },
            {
                "name": "dfm-aux",
                "profile": "DFM",
                "total_fuel": 30424.862,
                "hours_op": 1722.661111111111,
            },
        ],
        "tanks": [
            {
                "name": "estanque",
                "profile": "nivel-estanque",
                "level": 3521.73,
                "max_level": 10000.0,
            }
        ]
    },
    {
        "name": "A-42",
        "gateway_token": gateway_token("A-42"),

        "power_meters": [
            {
                "name": "pm-general-a42",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-habitabilidad-a42",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-fotoperiodo-a42",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-alimentacion-a42",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-ensilaje-a42",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-gen-general-1-a42",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-gen-general-2-a42",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-gen-aux-a42",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
        ],

        "dfms": [
            {
                "name": "dfm-general-1-a42",
                "profile": "DFM",
                "total_fuel": 0.0,
                "hours_op": 0.0,
            },
            {
                "name": "dfm-general-2-a42",
                "profile": "DFM",
                "total_fuel": 0.0,
                "hours_op": 0.0,
            },
            {
                "name": "dfm-aux-a42",
                "profile": "DFM",
                "total_fuel": 0.0,
                "hours_op": 0.0,
            },
        ],
        "tanks": [
            {
                "name": "estanque-1-a42",
                "profile": "nivel-estanque",
                "level": 0.0,
                "max_level": 10000.0,
            },
            {
                "name": "estanque-2-a42",
                "profile": "nivel-estanque",
                "level": 0.0,
                "max_level": 10000.0,
            },
        ]
    },
    {
        "name": "A-66",
        "gateway_token": gateway_token("A-66"),

        "power_meters": [
            {
                "name": "pm-general-a66",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-habitabilidad-a66",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-fotoperiodo-a66",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-alimentacion-a66",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-oxigeno-a66",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-gen-general-a66",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-gen-aux-a66",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
        ],

        "dfms": [
            {
                "name": "dfm-general-a66",
                "profile": "DFM",
                "total_fuel": 0.0,
                "hours_op": 0.0,
            },
            {
                "name": "dfm-aux-a66",
                "profile": "DFM",
                "total_fuel": 0.0,
                "hours_op": 0.0,
            },
        ],

        "tanks": [
            {
                "name": "estanque-1-a66",
                "profile": "nivel-estanque",
                "level": 0.0,
                "max_level": 10000.0,
            },
            {
                "name": "estanque-2-a66",
                "profile": "nivel-estanque",
                "level": 0.0,
                "max_level": 10000.0,
            },
        ],
    },
    {
        "name": "A-87",
        "gateway_token": gateway_token("A-87"),

        "power_meters": [
            {
                "name": "pm-general-a87",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-fotoperiodo-a87",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-alimentacion-a87",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-habitabilidad-1-a87",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-habitabilidad-2-a87",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-habitabilidad-3-a87",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-habitabilidad-4-a87",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-bombas-1-a87",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-bombas-2-a87",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-gen-general-a87",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-gen-aux-1-a87",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-gen-aux-2-a87",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
        ],

        "dfms": [
            {
                "name": "dfm-general-a87",
                "profile": "DFM",
                "total_fuel": 0.0,
                "hours_op": 0.0,
            },
            {
                "name": "dfm-aux-1-a87",
                "profile": "DFM",
                "total_fuel": 0.0,
                "hours_op": 0.0,
            },
            {
                "name": "dfm-aux-2-a87",
                "profile": "DFM",
                "total_fuel": 0.0,
                "hours_op": 0.0,
            },
        ],

        "tanks": [
            {
                "name": "estanque-1-a87",
                "profile": "nivel-estanque",
                "level": 0.0,
                "max_level": 10000.0,
            },
            {
                "name": "estanque-2-a87",
                "profile": "nivel-estanque",
                "level": 0.0,
                "max_level": 10000.0,
            },
        ],
    },
    {
        "name": "A-67",
        "gateway_token": gateway_token("A-67"),

        "power_meters": [
            {
                "name": "pm-general-a67",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-habitabilidad-a67",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-fotoperiodo-a67",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-alimentacion-a67",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-gen-general-a67",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-gen-aux-a67",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
        ],

        "dfms": [
            {
                "name": "dfm-general-a67",
                "profile": "DFM",
                "total_fuel": 0.0,
                "hours_op": 0.0,
            },
            {
                "name": "dfm-aux-a67",
                "profile": "DFM",
                "total_fuel": 0.0,
                "hours_op": 0.0,
            },
        ],

        "tanks": [
            {
                "name": "estanque-a67",
                "profile": "nivel-estanque",
                "level": 0.0,
                "max_level": 10000.0,
            },
        ],
    },
    {
        "name": "Palvitad",
        "gateway_token": gateway_token("Palvitad"),

        "power_meters": [
            {
                "name": "pm-general-palvitad",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-habitabilidad-1-palvitad",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-habitabilidad-2-palvitad",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-habitabilidad-3-palvitad",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-habitabilidad-4-palvitad",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-fotoperiodo-1-palvitad",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-fotoperiodo-2-palvitad",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-alimentacion-1-palvitad",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-alimentacion-2-palvitad",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-bombas-1-palvitad",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-bombas-2-palvitad",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-bombas-3-palvitad",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-gen-general-palvitad",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-gen-aux-1-palvitad",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-gen-aux-2-palvitad",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
            {
                "name": "pm-gen-aux-3-palvitad",
                "profile": "pm-5330",
                "real_energy": 0.0,
                "reactive_energy": 0.0,
                "apparent_energy": 0.0,
            },
        ],

        "dfms": [
            {
                "name": "dfm-general-palvitad",
                "profile": "DFM",
                "total_fuel": 0.0,
                "hours_op": 0.0,
            },
            {
                "name": "dfm-aux-1-palvitad",
                "profile": "DFM",
                "total_fuel": 0.0,
                "hours_op": 0.0,
            },
            {
                "name": "dfm-aux-2-palvitad",
                "profile": "DFM",
                "total_fuel": 0.0,
                "hours_op": 0.0,
            },
            {
                "name": "dfm-aux-3-palvitad",
                "profile": "DFM",
                "total_fuel": 0.0,
                "hours_op": 0.0,
            },
        ],

        "tanks": [
            {
                "name": "estanque-1-palvitad",
                "profile": "nivel-estanque",
                "level": 0.0,
                "max_level": 10000.0,
            },
            {
                "name": "estanque-2-palvitad",
                "profile": "nivel-estanque",
                "level": 0.0,
                "max_level": 10000.0,
            },
            {
                "name": "estanque-3-palvitad",
                "profile": "nivel-estanque",
                "level": 0.0,
                "max_level": 10000.0,
            },
        ],
    }
]
